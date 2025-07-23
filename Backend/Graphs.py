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

def generate_plot(result, chart_type: str, question: str):
    """
    Generate a plot and return it as a Base64-encoded string (no file saving).
    """
    if chart_type == "none":
        return None

    df = pd.DataFrame(result)
    if df.shape[1] < 2:
        return None

    x_col, y_col = df.columns[0], df.columns[1]

    plt.figure(figsize=(12, 8))
    plt.title(question, fontsize=14, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    if chart_type == "bar":
        plt.bar(df[x_col], df[y_col], color="skyblue")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
    elif chart_type == "horizontal_bar":
        plt.barh(df[x_col], df[y_col], color="lightgreen")
        plt.xlabel(y_col)
        plt.ylabel(x_col)
    elif chart_type == "line":
        plt.plot(df[x_col], df[y_col], marker="o", color="orange")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
    elif chart_type == "pie":
        plt.pie(df[y_col], labels=df[x_col], autopct='%1.1f%%')
        plt.axis('equal')
    elif chart_type == "scatter":
        plt.scatter(df[x_col], df[y_col], color="purple")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
    else:
        return None

    plt.tight_layout()

    # Save to memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Encode to Base64
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return image_base64
