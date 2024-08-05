from promptflow import tool
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
import json

@tool
def query_database(query: str, db_config: dict) -> str:
    try:
        db_url = URL.create(**db_config)
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = [dict(row) for row in result]
        
        return json.dumps({"query": query, "results": rows})
    
    except Exception as e:
        return json.dumps({"error": str(e)})

# Example usage (not part of the tool, just for testing):
# db_config = {
#     'drivername': 'mssql+pyodbc',
#     'username': "username@server",
#     'password': "password",
#     'host': "server.database.windows.net",
#     'port': 1433,
#     'database': "database_name",
#     'query': {'driver': "ODBC Driver 18 for SQL Server"}
# }
# query = "SELECT TOP 5 * FROM your_table"
# result = query_database(query, db_config)
# print(result)
