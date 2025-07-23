


def build_prompt1(schema: dict, user_question: str) -> str:
    def format_columns(cols):
        return ', '.join([f"{col['name']} ({col['type']})" for col in cols])

    schema_str = "\n".join(
        [f"Table: {table}\nColumns: {format_columns(cols)}"
         for table, cols in schema.items()]
    )

    examples = """
User Question: What is my total sales?  
SQL Query: SELECT SUM(total_sales) AS total_sales FROM product_sales;

User Question: Which product had the highest CPC (Cost Per Click)?  
SQL Query: SELECT product_name FROM ad_metrics ORDER BY (ad_spend / clicks) DESC LIMIT 1;

User Question: Show the total ad spend and clicks for each product.  
SQL Query: SELECT product_name, SUM(ad_spend) AS total_ad_spend, SUM(clicks) AS total_clicks FROM ad_metrics GROUP BY product_name;

User Question: Find products with total sales greater than 10000 units.  
SQL Query: SELECT product_name, total_sales FROM product_sales WHERE total_sales > 10000;

User Question: What is the Return on Ad Spend (RoAS)?  
SQL Query: SELECT SUM(total_sales) * 1.0 / SUM(ad_spend) AS RoAS FROM product_sales ps JOIN ad_metrics am ON ps.product_id = am.product_id;
    """

    prompt = f"""
You are an expert SQL query generator.

### Database Schema:
{schema_str}

### Task:
Convert the given user question into a correct SQL query using the database schema.  
- Use only columns and tables mentioned in the schema.  
- Use simple, valid SQL syntax for SQLite3.  
- Do NOT include explanations, only return the SQL query.
-Only return the raw SQL query without any explanation or markdown formatting (no ```sql fences).


### Examples:
{examples}

### User Question:
{user_question}

### SQL Query:
"""
    return prompt


def clean_sql_query(sql_text: str) -> str:
    
    sql_text = sql_text.strip()
    # Remove ```sql and ```
    sql_text = sql_text.replace("```sql", "").replace("```", "").strip()
    return sql_text
