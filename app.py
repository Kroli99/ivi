import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load your dataset
df = pd.read_csv('data/jobs_in_data.csv')

# Initialize the Dash app (using a Bootstrap theme for nice styling)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Counting the number of employees per country for the geoplot
country_counts = df['employee_residence'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Jobs Salary Dashboard", className="bg-primary text-white p-2 text-center")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("About the Dataset:", className="text-primary mt-3"),
                html.Ul([
                    html.Li("work_year: The year in which the data was recorded."),
                    html.Li("job_title: The specific title of the job role."),
                    html.Li("job_category: A classification of the job role into broader categories."),
                    html.Li("salary_currency: The currency in which the salary is paid."),
                    html.Li("salary: The annual gross salary of the role in the local currency."),
                    html.Li("salary_in_usd: The annual gross salary converted to USD."),
                    html.Li("employee_residence: The country of residence of the employee."),
                    html.Li("experience_level: Classifies the professional experience level of the employee."),
                    html.Li("employment_type: Specifies the type of employment."),
                    html.Li("work_setting: The work setting or environment."),
                    html.Li("company_location: The country where the company is located."),
                    html.Li("company_size: The size of the employer company.")
                ]),
                html.H3("Visualizations:", className="text-primary mt-3"),
                html.P("Each filter dropdown controls a histogram plot below it, showing the distribution of salaries based on the selected attribute.")
            ], className="p-3")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='job_category_filter',
                options=[{'label': i, 'value': i} for i in df['job_category'].unique()],
                value=df['job_category'].unique()[0],
                clearable=False
            ),
            dcc.Graph(id='job_category_plot')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='experience_level_filter',
                options=[{'label': i, 'value': i} for i in df['experience_level'].unique()],
                value=df['experience_level'].unique()[0],
                clearable=False
            ),
            dcc.Graph(id='experience_level_plot')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='employment_type_filter',
                options=[{'label': i, 'value': i} for i in df['employment_type'].unique()],
                value=df['employment_type'].unique()[0],
                clearable=False
            ),
            dcc.Graph(id='employment_type_plot')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='work_setting_filter',
                options=[{'label': i, 'value': i} for i in df['work_setting'].unique()],
                value=df['work_setting'].unique()[0],
                clearable=False
            ),
            dcc.Graph(id='work_setting_plot')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='company_size_filter',
                options=[{'label': i, 'value': i} for i in df['company_size'].unique()],
                value=df['company_size'].unique()[0],
                clearable=False
            ),
            dcc.Graph(id='company_size_plot')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='geoplot', style={'height': '100vh'})
        ], width=12)
    ])
], fluid=True)

# Callbacks to update each graph based on its corresponding filter
@app.callback(
    Output('job_category_plot', 'figure'),
    Input('job_category_filter', 'value')
)
def update_job_category_plot(selected_category):
    filtered_data = df[df['job_category'] == selected_category]
    fig = px.histogram(filtered_data, x='salary_in_usd', nbins=30)
    fig.update_layout(title='Salary Distribution by Job Category', title_x=0.5)
    return fig

@app.callback(
    Output('experience_level_plot', 'figure'),
    Input('experience_level_filter', 'value')
)
def update_experience_level_plot(selected_experience):
    filtered_data = df[df['experience_level'] == selected_experience]
    fig = px.histogram(filtered_data, x='salary_in_usd', nbins=30)
    fig.update_layout(title='Salary Distribution by Experience Level', title_x=0.5)
    return fig

@app.callback(
    Output('employment_type_plot', 'figure'),
    Input('employment_type_filter', 'value')
)
def update_employment_type_plot(selected_employment):
    filtered_data = df[df['employment_type'] == selected_employment]
    fig = px.histogram(filtered_data, x='salary_in_usd', nbins=30)
    fig.update_layout(title='Salary Distribution by Employment Type', title_x=0.5)
    return fig

@app.callback(
    Output('work_setting_plot', 'figure'),
    Input('work_setting_filter', 'value')
)
def update_work_setting_plot(selected_setting):
    filtered_data = df[df['work_setting'] == selected_setting]
    fig = px.histogram(filtered_data, x='salary_in_usd', nbins=30)
    fig.update_layout(title='Salary Distribution by Work Setting', title_x=0.5)
    return fig

@app.callback(
    Output('company_size_plot', 'figure'),
    Input('company_size_filter', 'value')
)
def update_company_size_plot(selected_size):
    filtered_data = df[df['company_size'] == selected_size]
    fig = px.histogram(filtered_data, x='salary_in_usd', nbins=30)
    fig.update_layout(title='Salary Distribution by Company Size', title_x=0.5)
    return fig

@app.callback(
    Output('geoplot', 'figure'),
    Input('job_category_filter', 'value')  # You can modify the input if you want the map to respond to specific filters
)
def update_geoplot(selected_category):
    filtered_data = country_counts  # Modify this line if your geoplot should respond to the selected category
    fig = px.choropleth(
        filtered_data,
        locations='country',
        locationmode='country names',
        color='count',
        hover_name='country',
        color_continuous_scale=px.colors.sequential.Plasma  # Using Plasma color scale for vibrant visuals
    )
    fig.update_layout(
        title='Global Distribution of Employees',
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        margin=dict(l=0, r=0, t=50, b=0)  # Adjust margins to minimize white space
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)