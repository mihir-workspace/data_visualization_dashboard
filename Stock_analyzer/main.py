import pandas as pd
import plotly
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from alpha_vantage.timeseries import TimeSeries
# -------------------------------------------------------------------------------

key = 'Enter you API key'  # 

ts = TimeSeries(key, output_format='pandas')


usaStock_list = pd.read_csv(
    '/home/leo/Visulization/Dash-Ploty/stock-analyzer/constituents_csv.csv')


# -------------------------------------------------------------------------------
# Building our Web app and update financial data automatically

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server=app.server


app.layout = html.Div([html.Div([
    dbc.Row(dbc.Col(html.H1("Stock Analyzer"), width={"size": 6, "offset": 4}))]),
    html.Br(),
    html.Div([
        dbc.Row(children=[

            dbc.Col(children=[dcc.Dropdown(id='stock',
                                           options=[
                                               {'label': y, 'value': x, }
                                               for x, y in zip(usaStock_list['Symbol'], usaStock_list['Name'])
                                           ],
                                           value='ACN',
                                           clearable=False,
                                           searchable=True,
                                           placeholder='Accenture plc'
                                           ), ], width={"size": 5, "offset": 2}),
            dbc.Col(html.Big(dcc.RadioItems(
                id='choose',
                options=[
                    {'label': 'Daily', 'value': 'daily'},
                    {'label': 'Weekly', 'value': 'weekly'},
                    {'label': 'Monthly', 'value': 'monthly'}
                ],
                value='daily',
            )), width=4
            ),
        ], align="center", justify="center"),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Button('Apply', id='apply', n_clicks=0, color="primary"),
                width={"size": 3, "offset": 5},
            ),
        ),
        html.Br(),

        dbc.Row(
            dbc.Col(dbc.Spinner(dcc.Graph(id="trading_graph"),
                                color="primary", fullscreen=True)), justify="center",

        ),

    ])
])

# -------------------------------------------------------------------------------


@ app.callback(
    Output('trading_graph', 'figure'),
    Input('apply', 'n_clicks'),
    [State('stock', 'value'),
     State('choose', 'value'), ]
)
def update_graph(apply, stock, ch):
    # if apply > 0:
    if(ch == 'daily'):
        ttm_data, ttm_meta_data = ts.get_intraday(
            symbol=stock, interval='1min', outputsize='compact')
    elif (ch == 'weekly'):
        ttm_data, ttm_meta_data = ts.get_weekly(
            symbol=stock)
    elif(ch == 'monthly'):
        ttm_data, ttm_meta_data = ts.get_monthly(
            symbol=stock)

    df = ttm_data.copy()
    df = df.reset_index().rename(columns={'4. close': 'close'})
    df.transpose()
    df = df[["close", "date"]]

    line_chart = px.line(
        data_frame=df,
        x='date',
        y='close',
        template='plotly_dark',
        title="Stock: {}".format(stock)
    )

    return line_chart
   


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
