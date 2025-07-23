from fastapi import FastAPI, Query
from pydantic import BaseModel
from Graphs import generate_plot
from Visulization import choose_visualization
from resultformat import format_result_with_llm
from LLM import LLM
from Promt import build_prompt1, clean_sql_query
from Query import get_db_schema, execute_query
from resultformat import validate_query

app = FastAPI()

DB_NAME = 'D:\DataAnalysisAgent\ecommerce_data.db'
llm = LLM(model_name="gemini-2.0-flash-lite-001")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    try:
        schema = validate_query(req.question)
        if not schema:
            return {"error": "Question is not relevant to Data"}

        prompt = build_prompt1(schema, req.question)
        sql_query = llm.invoke(prompt)
        sql_query = clean_sql_query(sql_query)
        result = execute_query(DB_NAME, sql_query)

        user_friendly_answer = format_result_with_llm(req.question, sql_query, result)

        # Visualization
        chart_type = choose_visualization(req.question, schema, result)
        chart_image = generate_plot(result, chart_type, req.question)

        return {
            "question": req.question,
            "sql_query": sql_query,
            "result": result,
            "answer": user_friendly_answer,
            "visualization_type": chart_type,
            "visualization_image": chart_image  # Base64-encoded image
        }

    except Exception as e:
        return {"error": str(e)}