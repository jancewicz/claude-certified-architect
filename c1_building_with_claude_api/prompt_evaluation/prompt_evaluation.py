import json
import os.path

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.prompt_evaluation.grader import Grader
from c1_building_with_claude_api.prompt_evaluation.graders.code_grader import CodeGrader
from c1_building_with_claude_api.utils.utils import (
    add_user_message,
    chat,
    get_haiku_model,
    add_assistant_message,
)


client = get_client()
model = get_haiku_model()


def run_prompt(test_case: dict[str, str]):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
        Solve the following task:
        
        {test_case["task"]}
        
        * Return only plain python code, regex, or json
        * Do not provide any explanation, commentary or comments
    """

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, text="```code")
    chat_response = chat(client, model, messages, stop_sequences=["```"])
    return chat_response


def run_test_case(test_case: dict[str, str], grader: Grader) -> dict:
    """
    Calls run prompt, then grades the result.
    :param test_case: task to evaluate
    :param grader: task execution grader mechanism
    :return: dictionary with test case output and grading
    """
    chat_response = run_prompt(test_case)

    model_grade = grader.grade_by_model(test_case, chat_response)
    model_score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    syntax_score = CodeGrader().grade_syntax(test_case, chat_response)
    score = (model_score + syntax_score) / 2
    return {
        "output": chat_response,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning,
    }


def run_eval(dataset: dict, grader: Grader) -> list[dict]:
    """
    Run test case for each case from given dataset.
    :param dataset: set of cases to evaluate
    :param grader: task execution grader mechanism
    :return: a list of graded test cases with theirs outputs
    """
    results: list[dict] = []
    for test_case in dataset:
        result = run_test_case(test_case, grader)
        results.append(result)

    return results


def load_dataset(dataset_path: str):
    if os.path.exists(dataset_path):
        with open(path, "r") as f:
            dataset_json = json.load(f)
        return dataset_json
    else:
        raise FileNotFoundError("File does not exist")


if __name__ == "__main__":
    path: str = "test_dataset.json"
    dataset = load_dataset(path)
    grader = Grader(client, model)

    eval_results = run_eval(dataset, grader)
    evaluation_mean_score = grader.calc_mean_scores(eval_results)

    print(eval_results)
    print(evaluation_mean_score)
