import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc
from dash import Dash, dcc, html, Input, Output

periods = ['daily', 'weekly', 'monthly']
fr_data = {p: pd.read_parquet(f'data/fr_{p}.parquet') for p in periods}
no_data = {p: pd.read_parquet(f'data/no_{p}.parquet') for p in periods}

fr_zones = fr_data['daily'].columns.tolist()
no_zones = no_data['daily'].columns.tolist()


def make_color_map(zones, scale_name):
    n = len(zones)
    if n == 1:
        colors = pc.sample_colorscale(scale_name, [0.6])
    else:
        colors = pc.sample_colorscale(scale_name, [0.3 + 0.6 * i / (n - 1) for i in range(n)])
    return dict(zip(zones, colors))


fr_color_map = make_color_map(fr_zones, 'Reds')
no_color_map = make_color_map(no_zones, 'Blues')


def build_figure(period):
    fr_df = fr_data[period]
    no_df = no_data[period]

    common_idx = fr_df.index.union(no_df.index)
    fr_df = fr_df.reindex(common_idx)
    no_df = no_df.reindex(common_idx)

    traces = []

    for i, zone in enumerate(fr_zones):
        traces.append(go.Bar(
            x=fr_df.index,
            y=fr_df[zone],
            name=f"FR → {zone}",
            marker_color=fr_color_map[zone],
            offsetgroup='france',
            legendgroup='france',
            legendgrouptitle_text='France' if i == 0 else None,
            hovertemplate="%{x}<br>FR → " + zone + ": %{y:.0f} MW<extra></extra>",
        ))

    for i, zone in enumerate(no_zones):
        traces.append(go.Bar(
            x=no_df.index,
            y=no_df[zone],
            name=f"NO → {zone}",
            marker_color=no_color_map[zone],
            offsetgroup='norway',
            legendgroup='norway',
            legendgrouptitle_text='Norway' if i == 0 else None,
            hovertemplate="%{x}<br>NO → " + zone + ": %{y:.0f} MW<extra></extra>",
        ))

    return go.Figure(
        data=traces,
        layout=go.Layout(
            barmode='relative',
            title='Net Electricity Flows: France and Norway',
            yaxis=dict(
                title='Net Flow (MW)',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
            ),
            xaxis=dict(
                title='Date',
                rangeslider=dict(visible=True),
                type='date',
            ),
            legend=dict(groupclick='togglegroup'),
        ),
    )


app = Dash(__name__)
server = app.server  # exposed for gunicorn

app.layout = html.Div([
    html.H2('Net Electricity Flows: France and Norway'),
    dcc.RadioItems(
        id='period-selector',
        options=[{'label': p.capitalize(), 'value': p} for p in periods],
        value='weekly',
        inline=True,
        style={'marginBottom': '12px'},
    ),
    dcc.Graph(id='flow-chart', figure=build_figure('weekly')),
])


@app.callback(
    Output('flow-chart', 'figure'),
    Input('period-selector', 'value'),
)
def update_chart(period):
    return build_figure(period)


if __name__ == '__main__':
    app.run(debug=True)
