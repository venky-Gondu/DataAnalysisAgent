import json
import pandas as pd
from LLM import LLM

llm = LLM(model_name="gemini-2.0-flash-lite-001")

import json
import pandas as pd
from LLM import LLM

llm = LLM(model_name="gemini-2.0-flash-lite-001")

def choose_visualization(question: str, schema: dict, result) -> dict:
    """
    Decide chart type using LLM but keep x/y labels as column names.
    """
    df = pd.DataFrame(result)
    columns = list(df.columns)

    if len(columns) < 2:
        return {"chart_type": "none"}

    x_col, y_col = columns[0], columns[1]

    prompt = f"""
    You are a data visualization expert.
    
    User Question: {question}
    Database Schema: {schema}
    Query Columns: {columns}

    Choose the best chart type: bar, horizontal_bar, pie, line, scatter, or none.
    """

    response = llm.invoke(prompt).strip().lower()
    if response not in ["bar", "horizontal_bar", "pie", "line", "scatter"]:
        response = "bar"

    return {
        "chart_type": response,
        "x_col": x_col,
        "y_col": y_col,
        "x_label": x_col,
        "y_label": y_col
    }

