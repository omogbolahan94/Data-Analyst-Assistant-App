from langchain.agents import Tool 
from .. import data_store.DATA_STORE as DATA_STORE
from .state import State



def tool_data_summary(state: State) -> str:
    """
    Returns a summary of the dataset including:
    - Shape (rows, columns)
    - Column names and data types
    - Count of missing values per column
    - Basic statistics for numeric columns
    - Top unique values for categorical columns
    """
    file_id = state.get("file_id")
    
    if not file_id or file_id not in DATA_STORE:
        return "❌ No dataset loaded yet. Please upload a CSV or Excel file first."

    df = DATA_STORE[file_id]

    if df is None or df.empty:
        return "❌ Dataset is empty."
    
    summary = ["summary of dataframe:"]
    summary.append(f"\n\nDataset contains {df.shape[0]} rows and {df.shape[1]} columns.\n")

    # Column info
    col_info = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing_values": df.isnull().sum(),
        "non_null_count": df.notnull().sum()
    })
    summary.append("Column Information:\n")
    summary.append(col_info.to_string())
    summary.append("\n")

    # Numeric stats
    numeric_desc = df.describe(include=[float, int]).transpose()
    summary.append("Numeric Column Statistics:\n")
    summary.append(numeric_desc.to_string())
    summary.append("\n")

    # Categorical stats
    cat_desc = df.describe(include=[object, "category"]).transpose()
    if not cat_desc.empty:
        summary.append("Categorical Column Summary:\n")
        summary.append(cat_desc.to_string())
        summary.append("\n")

    return "\n".join(summary)


tool_summary = Tool(name="summarize_data", 
                    func=tool_data_summary, 
                    description=f"Returns the shape and summary of an existing dataframe {shared_data['df']} including numerical and non-numerical fields. Use this tool when the user asks for a data summary."
                )


def tool_data_dashboard(state: State) -> str:
    """
    Creates an interactive dashboard using Plotly from the uploaded dataset.
    Generates scatter, histogram, and bar charts if data types allow.
    Returns the dashboard as HTML.
    """
    figs = []
    nrows = len(df)

    # Separate numeric into continuous and categorical-like
    numeric_cols = df.select_dtypes(include=["number"]).columns
    continuous_cols = []
    categorical_like_numeric = []

    for col in numeric_cols:
        nunique = df[col].nunique()
        unique_ratio = nunique / nrows

        if nunique == nrows: 
            continue
        elif nunique <= 10:  
            categorical_like_numeric.append(col)
        elif unique_ratio > 0.05:  
            continuous_cols.append(col)


    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    cat_cols += categorical_like_numeric  

    if len(continuous_cols) >= 2:
        figs.append(px.scatter(df, x=continuous_cols[0], y=continuous_cols[1],
                               title=f"Scatter Plot: {continuous_cols[0]} vs {continuous_cols[1]}"))

    if len(continuous_cols) >= 1:
        figs.append(px.histogram(df, x=continuous_cols[0],
                                 title=f"Distribution of {continuous_cols[0]}"))

    for col in cat_cols:
        if df[col].nunique() <= 10:
            cat_counts = df[col].value_counts().reset_index()
            cat_counts.columns = [col, "Count"]
            figs.append(px.bar(cat_counts, x=col, y="Count",
                               title=f"Counts of {col}"))

    if not figs:
        return "⚠️ No suitable numeric or categorical columns found for visualization."

    # Combine all charts into HTML
    html_parts = [pio.to_html(fig, full_html=False, include_plotlyjs="cdn") for fig in figs]
    dashboard_html = "\n".join(html_parts)

    return dashboard_html


tool_dashboard = Tool(
    name="create_dashboard",
    func=tool_data_dashboard,
    description="Creates an interactive Plotly dashboard from the uploaded dataset."
)


tools = [tool_summary] # , tool_dashboard]


