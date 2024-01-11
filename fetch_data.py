import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Air Quality Index'), html.Br(),html.Br(),
] + [
    html.Div([
        html.Span(chunk), 
        html.Br() 
    ]) for chunk in 'Good: 0 - 50; Moderate: 51 - 100; Unhealthy for sensitive groups : 101 - 150; Unhealthy: 151 - 200; Very Unhealthy: 201 - 300; Harzardous: 301+'.split('; ')
] + [
    html.Br(), html.Br(),
    dcc.Input(id='location-input', type='text', placeholder='Enter a location'),
    html.Button('Submit', id='submit-button', n_clicks=0), 
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('location-input', 'value')]
)


def update_output(n_clicks, value):
    if n_clicks > 0:
        data = fetch_data(value)
        if data['status'] == 'ok':
             return [
                html.Br(),
                f"Air Quality Index (AQI) for {data['data']['city']['name']}: {data['data']['aqi']}", html.Br(), html.Br(),
                f"Particulate Matter 2.5 (PM2.5): {data['data']['iaqi']['pm25']['v']}", html.Br(),
                f"Ozone (O3): {data['data']['iaqi']['o3']['v']}", html.Br(),
                f"Carbon Monoxide (CO): {data['data']['iaqi']['co']['v']}", html.Br(),
                f"Nitrogen Dioxide (NO2): {data['data']['iaqi']['no2']['v']}", html.Br(),
                f"Sulfur Dioxide (SO2): {data['data']['iaqi']['so2']['v']}", html.Br(), html.Br(),
                f"DateTime: {data['data']['time']['s']}"
            ]
        else:
            return "Error fetching data: " + json.dumps(data['data'])

def fetch_data(location):
    token = os.getenv('TOKEN')
    url = f"https://api.waqi.info/feed/{location}/?token={token}"
    response = requests.get(url)
    data = response.json()
    return data

if __name__ == '__main__':
    app.run_server(debug=True)
    