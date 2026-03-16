import json
import re
import ast


class CodeGrader:
    @staticmethod
    def validate_python(text: str) -> int:
        try:
            json.loads(text.strip())
            return 10
        except json.JSONDecodeError:
            return 0

    @staticmethod
    def validate_regex(text: str) -> int:
        try:
            re.compile(text.strip())
            return 10
        except re.error:
            return 0

    @staticmethod
    def validate_json(text: str) -> int:
        try:
            ast.parse(text.strip())
            return 10
        except SyntaxError:
            return 0

    def grade_syntax(self, test_case, response) -> int | None:
        test_format = test_case["format"]
        match test_format:
            case "json":
                return self.validate_json(response)
            case "python":
                return self.validate_python(response)
            case "regex":
                return self.validate_regex(response)
        return None
