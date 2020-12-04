import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
from heatmap import heatmapData, tableData
import pandas as pd
import datetime

# tabledata = pd.DataFrame()
tabledata = tableData('LKS')

def heatmap(lib):
    data = heatmapData(lib)
    fig = px.imshow(data[0],
        labels=dict(x="Date", y="Time of Day", color="Max People Inside"),
        x=data[1],
        y=data[2]
    )
    return fig

app = dash.Dash(__name__, url_base_pathname="/dashboard/")
app.title = 'Live Occupancy'
app.layout = html.Div([
    html.Div([
        html.P("Choose a Library", className="library"),
        dcc.Dropdown("dropdown_tickers", 
            options=[
                {"label":"LKS", "value":"LKS"},
                {"label":"KGC", "value":"KGC"}
            ],value="LKS")], className="Navigation"),

    html.Div([
        html.H1(id="description", className="decription-content"),
        html.Hr(),
        html.P(id="datenow"),
        html.Button("Update Now", id="button_1"),
        html.Div([
            html.Div([], id="heatmap-graphs-content"),
            html.Hr(),
            html.Div([
                dcc.RadioItems("radio_tickers",
                    options=[
                        {'label': ' Hide raw data', 'value': 'off'},
                        {'label': ' Show raw data', 'value': 'on'},
                    ],
                    value='off',
                    labelStyle={'display': 'block'}
                )
            ]),
            html.Div(
                html.Div([
                    dash_table.DataTable(
                        id="table-container",
                        columns = [{"name": col, "id": col} for col in tabledata.columns],
                        data=tabledata.to_dict("records"),
                    )],id="table-content", style= {'display': 'none'})
            )
        ], id="main-content")
    ],className="content")

], className="container")


@app.callback(
    #[Output("description", "children"), Output("heatmap-graphs-content", "children"), Output('datenow', 'children')],
    [Output("description", "children"), Output("heatmap-graphs-content", "children"), Output('table-container', 'data'), Output('datenow', 'children')],
    [Input("dropdown_tickers", "value"), Input("button_1", "n_clicks")]
)
def switchLib(v, n_clicks):
    # if v == None:
    #     raise PreventUpdate
    if v == "LKS":
        description = "Li Ka Shing Library"
    if v == "KGC":
        description = "Kwa Geok Choo Law Library"
    
    data = heatmapData(v)
    fig = px.imshow(data[0],
        labels=dict(x="Date", y="Time of Day", color="Max People Inside"),
        x=data[1],
        y=data[2]
    )

    tabledata = tableData(v)

    #return description, [dcc.Graph(figure=fig)], datetime.datetime.now()
    return description, [dcc.Graph(figure=fig)], tabledata.to_dict('records'), datetime.datetime.now()

@app.callback(
   Output(component_id='table-content', component_property='style'),
   [Input(component_id='radio_tickers', component_property='value')]
   )
def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}


if __name__ == '__main__':
    app.run_server("127.0.0.1",8002, debug=True)