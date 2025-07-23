import streamlit as st
import requests
import pandas as pd
import re

# ------------------ API URL ------------------
API_URL = "http://127.0.0.1:8000/ask"

# ------------------ Dark Theme Custom Styling ------------------
st.markdown(
    """
    <style>
    /* Dark background */
    body {
        background-color: #121212 !important;
        color: white !important;
    }
    
    /* Container padding */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    /* Large title */
    h1 {
        font-size: 3rem !important;
        font-weight: bold !important;
        color: #ffffff !important;
        margin-bottom: 1rem !important;
    }

    /* Subtitle */
    h2, h3 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #e0e0e0 !important;
        margin-bottom: 1rem !important;
    }

    /* Input label */
    .stTextInput label {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }

    /* Input box styling */
    .stTextInput input {
        font-size: 1.4rem !important;
        padding: 1rem !important;
        height: 3rem !important;
        width: 100% !important;
        background-color: #2b2b2b !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
    }

    /* Button */
    .stButton button {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        height: 3.5rem !important;
        margin-top: 1.5rem !important;
        background-color: #ff4b33 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0 2rem !important;
    }

    /* Code block - SQL */
    pre {
        font-size: 1.2rem !important;
        line-height: 1.8 !important;
        background-color: #1e1e1e !important;
        color: #dcdcdc !important;
        padding: 1.2rem !important;
        border-radius: 8px !important;
        overflow-x: auto !important;
        border: 1px solid #444 !important;
    }

    /* Dataframe */
    .dataframe {
        font-size: 1.1rem !important;
    }
    div[data-testid="stDataFrame"] table {
        font-size: 1.2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



def format_sql(sql: str) -> str:
    """Formats SQL nicely with each clause on a new line."""
    if not sql.strip():
        return sql

    # Normalize whitespace
    sql = re.sub(r'\s+', ' ', sql).strip()

    # Define search patterns and replacements
    replacements = [
        (r'\bFROM\b', '\nFROM'),
        (r'\b(INNER|LEFT|RIGHT|FULL|OUTER)?\s*JOIN\b', '\nJOIN'),
        (r'\bON\b', '\nON'),
        (r'\bWHERE\b', '\nWHERE'),
        (r'\bGROUP\s+BY\b', '\nGROUP BY'),
        (r'\bHAVING\b', '\nHAVING'),
        (r'\bORDER\s+BY\b', '\nORDER BY'),
        (r'\bLIMIT\b', '\nLIMIT'),
        (r'\bUNION\s+(ALL)?\b', '\nUNION\\1'),
    ]

    # Apply each replacement
    for pattern, replacement in replacements:
        sql = re.sub(pattern, replacement, sql, flags=re.IGNORECASE)

    # Now split into lines and clean up
    lines = []
    for line in sql.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        if lines:  # All lines after SELECT are indented
            lines.append(f"  {stripped}")
        else:
            # First line (should be SELECT)
            if stripped.upper().startswith("SELECT"):
                lines.append(stripped)
            else:
                lines.append(stripped)  # fallback

    return '\n'.join(lines)
# ------------------ App Content ------------------
st.title("🛒 E-commerce Data Analysis Agent")
st.markdown("**Ask questions about your e-commerce data and get instant insights with AI-powered analysis**")

# ------------------ User Input ------------------
user_question = st.text_input(
    "💬 Ask a question about your data:",
    placeholder="What is my total sales? Which product has highest revenue?",
    value="What is my total sales?"
)

# ------------------ Submit Button ------------------
if st.button("🔍 Analyze Data", type="primary"):
    if not user_question.strip():
        st.warning("⚠️ Please enter a question to get started.")
    else:
        with st.spinner("🤖 Analyzing your data..."):
            try:
                response = requests.post(API_URL, json={"question": user_question})
                
                if response.status_code == 200:
                        data = response.json()

                        # Properly check for errors
                        if data.get("error"):
                            st.error(f"❌ API Error: {data['error']}")
                        else:
                            # Extract components
                            raw_sql = data.get("sql_query", "").strip()
                            ai_answer = data.get("answer", "")
                            result_data = data.get("result", [])


                        # Format SQL
                        formatted_sql = format_sql(raw_sql) if raw_sql else "No query generated."

                        # ------------------ Two-column layout: AI Answer | SQL Query ------------------
                        col1, col2 = st.columns([1, 1])

                        with col1:
                            st.subheader("🎯 AI Answer")
                            if ai_answer:
                                st.info(ai_answer, icon="💡")
                            else:
                                st.info("No explanation provided.", icon="ℹ️")

                        with col2:
                            st.subheader("📝 Generated SQL Query")
                            st.code(formatted_sql, language="sql")

                       # ------------------ Query Results ------------------
                st.subheader("📊 Query Results")

                if not result_data:
                    st.info("ℹ️ No results found for your query.")
                else:
                    # Convert to DataFrame
                    df = pd.DataFrame(result_data)

                    # Show full result table
                    st.dataframe(df, use_container_width=True)

                    # Optional: Statistics if numeric
                    num_cols = df.select_dtypes(include='number').columns
                    if len(num_cols) > 0:
                        with st.expander("📈 Quick Statistics"):
                            st.write(df.describe())

                # ------------------ Visualization ------------------
               # ------------------ Visualization ------------------
                chart_image = data.get("visualization_image")  # Get Base64 string from backend
                chart_type = data.get("visualization_type", "none")

                if chart_image and chart_type != "none":
                    st.subheader(f"📈 Visualization ({chart_type.capitalize()})")
                    import base64
                    from io import BytesIO
                    from PIL import Image

                    try:
                        image_bytes = base64.b64decode(chart_image)
                        image = Image.open(BytesIO(image_bytes))
                        st.image(image, use_container_width=True)
                    except Exception as e:
                        st.warning(f"⚠️ Could not load visualization: {e}")


                else:
                    st.error(f"❌ API Error: {response.status_code} – {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("🔌 **Connection Failed**: Could not reach the backend API. Make sure FastAPI server is running at `http://127.0.0.1:8000`")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {str(e)}")

# ------------------ Footer ------------------
st.markdown("---")
st.markdown("*✨ Powered by AI • Built with Streamlit*")