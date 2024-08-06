from promptflow import tool
import logging

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[logging.FileHandler("user_input_debug.log"),
                              logging.StreamHandler()])

@tool
def process_user_input(user_input: str) -> str:
    logging.debug(f"Received user_input: {user_input}")
    logging.debug(f"User input type: {type(user_input)}")
    
    # Ensure user_input is not None and is a string
    if user_input is None:
        logging.warning("Received None user_input")
        return ""
    
    processed_input = str(user_input).strip()
    logging.debug(f"Processed user_input: {processed_input}")
    return processed_input