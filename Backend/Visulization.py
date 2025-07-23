from LLM import LLM
llm = LLM(model_name="gemini-2.0-flash-lite-001")

def choose_visualization(question: str, schema: dict, result) -> str:
    """
    Use LLM to decide which visualization to use.
    Returns: bar, horizontal_bar, scatter, pie, line, or none.
    """
    prompt = f"""
    You are a data visualization expert.
    
    User Question: {question}
    Database Schema: {schema}
    Query Result: {result}

    Decide if a visualization is useful:
    - If the result has a single numeric value or very few rows, return "none".
    - Otherwise, choose one of these: bar, horizontal_bar, pie, line, scatter.

    Rules:
    - 'bar': compare categories.
    - 'horizontal_bar': many categories or long names.
    - 'pie': show percentages of a whole.
    - 'line': time-series or sequential data.
    - 'scatter': relationship between two numeric variables.

    Return ONLY: bar, horizontal_bar, pie, line, scatter, or none.
    """

    response = llm.invoke(prompt).strip().lower()
    print("DEBUG: Suggested Visualization =", response)
    return response
