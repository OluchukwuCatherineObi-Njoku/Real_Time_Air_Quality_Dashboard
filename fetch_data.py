import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = dash.Dash(__name__)

app.layout = html.Div([
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
            return f"Air Quality Index (AQI) for {data['data']['city']['name']}: {data['data']['aqi']}\n\n \
            Particulate Matter 2.5 (PM2.5): {data['data']['iaqi']['pm25']['v']}\n\n \
            Ozone (O3): {data['data']['iaqi']['o3']['v']}\n\n \
            Carbon Monoxide (CO): {data['data']['iaqi']['co']['v']}\n\n \
            Nitrogen Dioxide (NO2): {data['data']['iaqi']['no2']['v']}\n\n \
            Sulfur Dioxide (SO2): {data['data']['iaqi']['so2']['v']}\n\n "
        else:
            return "Error fetching data"

def fetch_data(location):
    token = os.getenv('TOKEN')
    url = f"https://api.waqi.info/feed/{location}/?token={token}"
    response = requests.get(url)
    data = response.json()
    return data

if __name__ == '__main__':
    app.run_server(debug=True)
    