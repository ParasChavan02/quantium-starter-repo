import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("output/formatted_output.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Sort values
df = df.sort_values("date")

# Initialize app
app = Dash(__name__)

# App layout
app.layout = html.Div([

    html.H1(
        "Soul Foods Sales Visualizer",
        className="title"
    ),

    html.Div([

        html.Label(
            "Select Region:",
            className="radio-label"
        ),

        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True,
            className="radio-items"
        )

    ], className="filter-container"),

    dcc.Graph(id="sales-chart")

], className="main-container")


# Callback for updating graph
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):

    # Filter data
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"].str.lower() == selected_region]

    # Group by date
    daily_sales = filtered_df.groupby(
        "date",
        as_index=False
    )["sales"].sum()

    # Create figure
    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales - {selected_region.title()} Region",
        labels={
            "date": "Date",
            "sales": "Total Sales"
        }
    )

    # Add vertical reference line
    fig.add_vline(
        x="2021-01-15",
        line_width=3,
        line_dash="dash",
        line_color="red"
    )

    # Add annotation
    fig.add_annotation(
        x="2021-01-15",
        y=daily_sales["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=2
    )

    # Improve styling
    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    return fig


# Run app
if __name__ == "__main__":
    app.run(debug=True)