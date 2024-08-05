from promptflow import tool
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
import json

@tool
def list_blobs_in_container(connection_string: str, container_name: str) -> str:
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        blob_list = container_client.list_blobs()
        blobs = [blob.name for blob in blob_list]
        
        result = {
            "container": container_name,
            "blobs": blobs
        }
        
        return json.dumps(result)
    
    except AzureError as e:
        return json.dumps({"error": str(e)})

# Example usage (not part of the tool, just for testing):
# connection_string = "your_connection_string"
# container_name = "your_container_name"
# result = list_blobs_in_container(connection_string, container_name)
# print(result)
