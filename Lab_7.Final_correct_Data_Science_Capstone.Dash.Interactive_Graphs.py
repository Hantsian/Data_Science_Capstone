# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                # Dropdown for Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        ],
                                                value='ALL',
                                                placeholder="Select a Site",
                                                searchable=True
                                            ),
                                html.Br(),
                                # Pie chart for success/failure
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                # Payload Range Slider
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: str(i) for i in range(0, 11000, 1000)},
                                                value=[min_payload, max_payload]),
                                # Scatter plot for Payload vs. Success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2: Pie Chart Callback
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # For ALL sites, plot the total successful launches by site
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total successful launches by Site')
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Calculate success and failure counts
        success_failure_counts = filtered_df['class'].value_counts().reset_index()
        success_failure_counts.columns = ['class', 'count']
        # Plot pie chart
        fig = px.pie(success_failure_counts, values='count', names='class', 
                     title=f'Success VS Failure for {entered_site}')
    return fig


# TASK 4: Scatter Chart Callback
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    # Filter based on payload range first
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1])]


    if entered_site == 'ALL':
        # For ALL sites, use the entire dataset filtered by payload range
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title='Outcomes based on Payload Mass (kg) for All Sites')
    else:
        # If a specific site is selected, further filter by Launch Site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title=f'Outcomes based on Payload Mass (kg) for {entered_site}')
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8056)
