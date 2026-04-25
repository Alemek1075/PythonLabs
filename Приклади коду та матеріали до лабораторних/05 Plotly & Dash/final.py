import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

years = list(range(2005, 2021))

ad = pd.read_csv('airline_data.csv',
                 encoding="ISO-8859-1",
                 dtype={'Div1Airport': str, 'Div1TailNum': str,
                        'Div2Airport': str, 'Div2TailNum': str})
ad = ad[(2005 <= ad.Year) & (ad.Year <= 2020)]


def data1(cur):
    cancelled = cur[cur['Cancelled'] == 1.0].groupby(['Month', 'CancellationCode'])['Flights'].sum().reset_index()
    cancelled.Flights = cancelled.Flights.astype(int)

    airtime = cur.groupby(['Month','Reporting_Airline'])['AirTime'].mean().reset_index()

    diverted = cur[cur.DivAirportLandings != 0.0]

    by_states = cur.groupby(['OriginState'])['Flights'].sum().reset_index()
    by_states.Flights = by_states.Flights.astype(int)

    to_states = cur.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    to_states.Flights = to_states.Flights.astype(int)

    return cancelled, airtime, diverted, by_states, to_states


def avgdata(cur):
    carrier = cur.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    weather = cur.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    NAS = cur.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    security = cur.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    late = cur.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return carrier, weather, NAS, security, late


cur_year = 2012
cur = ad[ad['Year'] == int(cur_year)]
cancelled, airtime, diverted, by_states, to_states = data1(cur)
carrier, weather, NAS, security, late = avgdata(cur)

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

title = html.H1('US Domestic Airline Flights Performance',
                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24})

menu = dcc.Dropdown(id='input-type',
                    options=[
                        {'label': 'Yearly Airline Performance Report', 'value': 'OPT1'},
                        {'label': 'Yearly Airline Delay Report', 'value': 'OPT2'}
                    ],
                    placeholder='Select a report type',
                    style={'width': '80%', 'padding': '3px', 'text-align-last': 'center', 'font-size': '20px'})
yearmenu = dcc.Dropdown(id='input-year',
                        # Update dropdown values using list comphrehension
                        options=[{'label': i, 'value': i} for i in years],
                        placeholder="Select a year",
                        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'})

# Application layout
app.layout = html.Div(children=[
    title,

    html.Div([
        html.Div([
            html.Div(
                [
                    html.H2('Report Type:', style={'margin-right': '2em'}),
                ]
            ),
            menu,
        ], style={'display': 'flex'}),

        html.Div([
            html.Div(
                [
                    html.H2('Choose Year:', style={'margin-right': '2em'})
                ]
            ),
            yearmenu,
        ], style={'display': 'flex'}),
    ]),


    html.Div([], id='plot1'),

    html.Div([
        html.Div([], id='plot2', style={'width': '50%'}),
        html.Div([], id='plot3', style={'width': '50%'})
    ], style={'display': 'flex'}),

    html.Div([
        html.Div([], id='plot4', style={'width': '50%'}),
        html.Div([], id='plot5', style={'width': '50%'})
    ], style={'display': 'flex'}),
])


@app.callback([Output(component_id='plot1', component_property='children'),
                Output(component_id='plot2', component_property='children'),
                Output(component_id='plot3', component_property='children'),
                Output(component_id='plot4', component_property='children'),
                Output(component_id='plot5', component_property='children'),
                ],
              [Input(component_id='input-type', component_property='value'),
               Input(component_id='input-year', component_property='value')],
              [State("plot1", 'children'), State("plot2", "children"),
               State("plot3", "children"), State("plot4", "children"),
               State("plot5", "children")
               ]
              )

def get_graph(chart, year, c1, c2, c3, c4, c5):
    if year is None:
        raise dash.exceptions.PreventUpdate
    print(chart, year)
    cur = ad[ad['Year'] == int(year)]


    if chart == 'OPT1':
        cancelled, airtime, diverted, by_states, to_states = data1(cur)

        bar_fig = px.bar(cancelled, x='Month', y='Flights', color='CancellationCode',
                         title='Monthly Flight Cancellation')

        line_fig=px.line(airtime, x='Month', y='AirTime', color='Reporting_Airline',
                            title='Average monthly flight time (minutes) by airline')

        pie_fig = px.pie(diverted, values='Flights', names='Reporting_Airline',
                         title='% of flights by reporting airline')

        map_fig = px.choropleth(by_states,  # Input data
                                locations='OriginState',
                                color='Flights',
                                hover_data=['OriginState', 'Flights'],
                                locationmode='USA-states',  # Set to plot as US States
                                color_continuous_scale='GnBu',
                                range_color=[0, by_states['Flights'].max()])
        map_fig.update_layout(
            title_text='Number of flights from origin state',
            geo_scope='usa')  # Plot only the USA instead of globe

        tree_fig = px.treemap(to_states, path=['DestState', 'Reporting_Airline'],
                              values='Flights',
                              color='Flights',
                              color_continuous_scale='RdBu',
                              title='Flight count by airline to destination state'
                              )

        return [dcc.Graph(figure=tree_fig),
                dcc.Graph(figure=pie_fig),
                dcc.Graph(figure=map_fig),
                dcc.Graph(figure=bar_fig),
                dcc.Graph(figure=line_fig)
                ]
    else:
        avg_car, avg_weather, avg_NAS, avg_sec, avg_late = avgdata(cur)

        carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
                              title='Average carrrier delay time (minutes) by airline')
        weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                              title='Average weather delay time (minutes) by airline')
        nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
                          title='Average NAS delay time (minutes) by airline')
        sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
                          title='Average security delay time (minutes) by airline')
        late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                           title='Average late aircraft delay time (minutes) by airline')

        return [dcc.Graph(figure=carrier_fig),
                dcc.Graph(figure=weather_fig),
                dcc.Graph(figure=nas_fig),
                dcc.Graph(figure=sec_fig),
                dcc.Graph(figure=late_fig)]



if __name__ == '__main__':
    app.run()
