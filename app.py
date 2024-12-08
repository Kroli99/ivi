import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load your dataset
df = pd.read_csv('data/cleaned.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Used Car Interactive Dashboard"), className="mb-2 text-center")),
    dbc.Row(dbc.Col(html.Img(src=app.get_asset_url('car_exchange.jpg'), style={'width': '100%', 'height': 'auto'}))),
    dbc.Row(dbc.Col(html.P([
        "Welcome to the Used Car Interactive Dashboard. Dive deep into a comprehensive dataset of over 9,582 used car listings collected from the Indian market up to November 2024. This tool allows you to explore diverse vehicle attributes including brand, model, year of manufacture, mileage, and pricing. Adjust the filters to analyze trends, compare different segments, and make informed decisions based on detailed market insights. Whether you're a potential buyer, a car enthusiast, or a market analyst, this dashboard provides valuable perspectives on the dynamics of India's used car market.",
        html.Br(),
        html.Br(),
        "For more details, visit the dataset on ",
        html.A("Kaggle", href="https://www.kaggle.com/datasets/mohitkumar282/used-car-dataset", target="_blank"),
        "."
    ], className="intro-text text-center mb-4"))),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='brand-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Brand'].unique()],
                value='All',
                multi=True,
                placeholder="Select Brands",
                className="mb-2"
            ),
            dcc.Dropdown(
                id='currency-dropdown',
                options=[
                    {'label': 'EUR', 'value': 'AskPriceEUR'},
                    {'label': 'USD', 'value': 'AskPriceUSD'},
                    {'label': 'CHF', 'value': 'AskPriceCHF'},
                    {'label': 'GBP', 'value': 'AskPriceGBP'}
                ],
                value='AskPriceEUR',
                clearable=False,
                className="mb-2"
            )
        ], width=12)
    ]),
    dbc.Row(dbc.Col(dcc.Graph(id='price-km-plot'), width=12)),
    dbc.Row(dbc.Col(dcc.Graph(id='price-age-plot'), width=12)),
    dbc.Row(dbc.Col(dcc.Graph(id='fuel-type-pie-chart'), width=12)),
    dbc.Row(dbc.Col(dcc.Graph(id='model-year-distribution'), width=12))
], fluid=True)

@app.callback(
    [Output('price-km-plot', 'figure'),
     Output('price-age-plot', 'figure'),
     Output('fuel-type-pie-chart', 'figure'),
     Output('model-year-distribution', 'figure')],
    [Input('brand-dropdown', 'value'),
     Input('currency-dropdown', 'value')]
)
def update_graphs(selected_brands, selected_currency):
    filtered_df = df
    if 'All' not in selected_brands and selected_brands:
        filtered_df = filtered_df[filtered_df['Brand'].isin(selected_brands)]
    
    # Scatter plot for Price vs. Kilometers Driven
    fig_km = px.scatter(filtered_df, x='kmDriven', y=selected_currency, color='FuelType',
                        title='Price vs. Kilometers Driven', labels={'kmDriven': 'Kilometers Driven', selected_currency: 'Asking Price'})

    # Bar plot for Average Price by Age
    avg_price_by_age = filtered_df.groupby('Age')[selected_currency].mean().reset_index()
    fig_age = px.bar(avg_price_by_age, x='Age', y=selected_currency, title='Average Price by Age of Car',
                     labels={selected_currency: 'Average Asking Price', 'Age': 'Age of Car'})

    # Pie chart for Fuel Type Distribution
    fig_fuel_type = px.pie(filtered_df, names='FuelType', title='Distribution of Fuel Types',
                           color_discrete_sequence=px.colors.sequential.RdBu)

    # Histogram for Model Year Distribution
    fig_model_year = px.histogram(filtered_df, x='Year', nbins=30, title='Distribution of Model Years',
                                  labels={'Year': 'Model Year'})

    return fig_km, fig_age, fig_fuel_type, fig_model_year

if __name__ == '__main__':
    app.run_server(debug=True)