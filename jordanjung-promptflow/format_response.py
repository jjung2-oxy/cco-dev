from promptflow.core import tool
import json

@tool
def format_response(llm_output: str, blob_storage_used: bool, referenced_files: list) -> str:
    try:
        # Try to parse the llm_output as JSON
        try:
            parsed_output = json.loads(llm_output)
            content = parsed_output.get('content', llm_output)
        except json.JSONDecodeError:
            # If parsing fails, use the raw llm_output as content
            content = llm_output

        # Filter referenced files to include only CrimeData-20000r4.csv
        relevant_file = next((file for file in referenced_files if 'CrimeData-20000r4.csv' in file), None)

        # Format the response
        if blob_storage_used and relevant_file:
            reference_text = f"Reference from blob storage: {relevant_file}"
        else:
            reference_text = "No specific blob storage reference used"
        
        # Prepare the response dictionary
        response_dict = {
            "content": content,
            "reference": reference_text
        }
        
        # Return the response as a JSON string
        return json.dumps(response_dict)
    except Exception as e:
        # Handle any unexpected errors
        return json.dumps({
            "content": f"Error in formatting response: {str(e)}",
            "reference": "Error in referencing files"
        })