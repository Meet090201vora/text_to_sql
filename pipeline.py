import os
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_community.llms.openai import OpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from config import postgres_user, postgres_database
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_query: str

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
postgres_password = os.getenv("POSTGRES_PASSWORD")

if not openai_api_key:
    raise ValueError("API key for OpenAI not found. Please set it in the .env file.")

# Initialize FastAPI
app = FastAPI()

# Connect to SQL database
db = SQLDatabase.from_uri(f'postgresql://{postgres_user}:{postgres_password}@localhost:5432/{postgres_database}')

llm = ChatOpenAI(model="gpt-4o-mini")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=False,
    agent_executor_kwargs={"return_intermediate_steps": True}
)

def execute_query(query: str):
    """Executes a SQL query and returns the results as JSON."""
    try:
        conn = psycopg2.connect(
            dbname=postgres_database,
            user=postgres_user,
            password=postgres_password,
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-sql")
async def text_to_sql(request: QueryRequest):
    try:
        response = agent_executor.invoke(request.user_query)
        queries = [log.tool_input for (log, output) in response["intermediate_steps"] if log.tool == 'sql_db_query']
        if not queries:
            raise HTTPException(status_code=400, detail="Failed to generate SQL query.")
        sql_query = queries[0]
        result = execute_query(sql_query)
        return {"query": sql_query, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Instructions to start the FastAPI server
# 1. Run the command: `python -m uvicorn pipeline:app --host 0.0.0.0 --port 8000 --reload`
# 2. The API will be available at `http://localhost:8000/docs` for testing.
