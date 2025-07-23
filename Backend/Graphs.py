import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from Query import get_db_schema
from plotrules import PLOT_RULES



import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def generate_plot(result, chart_info: dict, question: str):
    """
    Generate a plot using chart_info (from LLM).
    chart_info: {"chart_type": str, "x_col": str, "y_col": str, "x_label": str, "y_label": str}
    """
    chart_type = chart_info.get("chart_type", "none")
    x_col = chart_info.get("x_col")
    y_col = chart_info.get("y_col")
    x_label = chart_info.get("x_label", x_col)
    y_label = chart_info.get("y_label", y_col)

    if chart_type == "none":
        return None

    df = pd.DataFrame(result)
    if x_col not in df.columns or y_col not in df.columns:
        # fallback to first two columns if LLM fails
        if df.shape[1] >= 2:
            x_col, y_col = df.columns[0], df.columns[1]
        else:
            return None

    plt.figure(figsize=(12, 8))
    plt.title(question, fontsize=14, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    if chart_type == "bar":
        plt.bar(df[x_col], df[y_col], color="skyblue")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    elif chart_type == "horizontal_bar":
        plt.barh(df[x_col], df[y_col], color="lightgreen")
        plt.xlabel(y_label)
        plt.ylabel(x_label)
    elif chart_type == "line":
        plt.plot(df[x_col], df[y_col], marker="o", color="orange")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    elif chart_type == "pie":
        plt.pie(df[y_col], labels=df[x_col], autopct='%1.1f%%')
        plt.axis('equal')
    elif chart_type == "scatter":
        plt.scatter(df[x_col], df[y_col], color="purple")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    else:
        return None

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")
