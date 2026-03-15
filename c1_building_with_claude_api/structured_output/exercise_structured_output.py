from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.utils.utils import add_user_message, chat, get_haiku_model, add_assistant_message

if __name__ == "__main__":
    messages = []
    prompt = """
    Generate three different sample AWS CLI commands. Each should be very short. 
    """

    """ Output of this prompt looks like this:
           # Three Sample AWS CLI Commands

           1. **List all S3 buckets:**
           ```bash
           aws s3 ls
           ```

           2. **Describe EC2 instances:**
           ```bash
           aws ec2 describe-instances
           ```

           3. **Get current AWS account ID:**
           ```bash
           aws sts get-caller-identity
           ```
       """
    add_user_message(messages, prompt)
    add_assistant_message(messages, text='Sure! There are three AWS CLI commands in singular block: ```bash')
    text = chat(client=get_client(), model=get_haiku_model(), messages=messages, stop_sequences=["```"])
    print(text.strip())