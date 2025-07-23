from LLM import LLM
from Query import get_db_schema


db_name='D:\DataAnalysisAgent\ecommerce_data.db'

llm = LLM(model_name="gemini-2.0-flash-lite-001")



def validate_query(question):
   
    schema = get_db_schema(db_name)

    if not schema:
        return f"Error in loading Schema"
    
    prompt = f"""
    You are an AI validator. Your job is to check if the given user question can be answered using the database schema.

    User Question:
    {question}

    Database Schema:
    {schema}

    If the user question can be answered using this database schema, return ONLY "True".
    If it cannot, return ONLY "False".
    Do not provide explanations.
    """

    response = llm.invoke(prompt).strip().lower()
    if response == "true":
        return schema
    return {}


def format_result_with_llm(user_question: str, sql_query: str, raw_result) -> str:
    """
    Use Gemini LLM to format the database query result into a user-friendly answer.
    """
    prompt = f"""
        You are a data analysis assistant.
        The user asked: {user_question}
        The SQL query executed was: {sql_query}
        The raw result from the database is: {raw_result}

        Instructions:
        1. If the result is tabular (multiple rows or columns), return the answer in a clean table-like format (e.g., Markdown table or CSV style) so that it can be directly converted to a Pandas DataFrame.
        2. If the result contains only one value or is a summary, give a concise natural language answer (e.g., "The total sales is 12000").
        3. Avoid unnecessary text or explanations beyond the formatted result.
        4. If summarizing the table, add a brief natural summary below the table.
        """

    formatted_response = llm.invoke(prompt)
    return formatted_response


