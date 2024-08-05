from promptflow import tool
import json

@tool
def combine_data(blob_data: str, sql_data: str, web_data: str, user_query: str) -> str:
    try:
        # Parse the input JSON strings
        blob_info = json.loads(blob_data)
        sql_info = json.loads(sql_data)
        web_info = json.loads(web_data)

        # Combine the data
        combined = {
            "blob_storage": blob_info,
            "sql_database": sql_info,
            "web_scrape": web_info,
            "user_query": user_query
        }

        # Return the combined data as a JSON string
        return json.dumps(combined, indent=2)

    except json.JSONDecodeError as e:
        return json.dumps({"error": f"JSON parsing error: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"An error occurred: {str(e)}"})

# Example usage (not part of the tool, just for testing):
# blob_data = '{"container": "my-container", "blobs": ["file1.txt", "file2.txt"]}'
# sql_data = '{"query": "SELECT * FROM table", "results": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]}'
# web_data = '{"product": "Example Product", "reviews": [{"title": "Great!", "rating": "5.0", "body": "Excellent product..."}]}'
# user_query = "Tell me about the product and its reviews"
# 
# result = combine_data(blob_data, sql_data, web_data, user_query)
# print(result)
