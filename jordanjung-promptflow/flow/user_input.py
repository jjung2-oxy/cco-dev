from promptflow.core import tool

@tool
def process_user_input(user_input: str) -> str:
    # You can add any preprocessing logic here if needed
    return user_input