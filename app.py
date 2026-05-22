import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv("output/formatted_output.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort values by date
df = df.sort_values("date")

# Group sales by date
daily_sales = df.groupby("date", as_index=False)["sales"].sum()

# Create line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={
        "date": "Date",
        "sales": "Total Sales"
    }
)

# Add vertical line for price increase date
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

# Improve layout styling
fig.update_layout(
    template="plotly_white",
    title_x=0.5
)

# Create Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([

    html.H1(
        "Soul Foods Sales Visualizer",
        style={
            "textAlign": "center",
            "marginBottom": "40px"
        }
    ),

    dcc.Graph(
        figure=fig
    )

], style={
    "width": "90%",
    "margin": "auto"
})

# Run app
if __name__ == "__main__":
    app.run(debug=True)