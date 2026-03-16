import plotly.graph_objects as go
import plotly.colors as pc
import data_extraction_processing as dep

fr_data = dep.fr_final_frames_by_period
no_data = dep.no_final_frames_by_period

periods = ['daily', 'weekly', 'monthly']
default_period = 'weekly'

# Get bidding zone columns from the daily frames (same columns across all periods)
fr_zones = fr_data['daily'].columns.tolist()
no_zones = no_data['daily'].columns.tolist()

# Generate color palettes — avoid near-white by sampling from 0.3 to 0.9
def make_color_map(zones, scale_name):
    n = len(zones)
    if n == 1:
        colors = pc.sample_colorscale(scale_name, [0.6])
    else:
        colors = pc.sample_colorscale(scale_name, [0.3 + 0.6 * i / (n - 1) for i in range(n)])
    return dict(zip(zones, colors))

fr_color_map = make_color_map(fr_zones, 'Reds')
no_color_map = make_color_map(no_zones, 'Blues')

# Build all traces grouped by period
traces = []
traces_per_period = len(fr_zones) + len(no_zones)

for period in periods:
    fr_df = fr_data[period]
    no_df = no_data[period]

    # Align indices
    common_idx = fr_df.index.union(no_df.index)
    fr_df = fr_df.reindex(common_idx)
    no_df = no_df.reindex(common_idx)

    visible = period == default_period

    # France traces
    for i, zone in enumerate(fr_zones):
        traces.append(go.Bar(
            x=fr_df.index,
            y=fr_df[zone],
            name=f"FR → {zone}",
            marker_color=fr_color_map[zone],
            offsetgroup='france',
            legendgroup='france',
            legendgrouptitle_text='France' if i == 0 else None,
            visible=visible,
            hovertemplate="%{x}<br>FR → " + zone + ": %{y:.0f} MW<extra></extra>",
        ))

    # Norway traces
    for i, zone in enumerate(no_zones):
        traces.append(go.Bar(
            x=no_df.index,
            y=no_df[zone],
            name=f"NO → {zone}",
            marker_color=no_color_map[zone],
            offsetgroup='norway',
            legendgroup='norway',
            legendgrouptitle_text='Norway' if i == 0 else None,
            visible=visible,
            hovertemplate="%{x}<br>NO → " + zone + ": %{y:.0f} MW<extra></extra>",
        ))

# Build dropdown buttons
buttons = []
for idx, period in enumerate(periods):
    vis = [False] * (len(periods) * traces_per_period)
    start = idx * traces_per_period
    vis[start:start + traces_per_period] = [True] * traces_per_period
    buttons.append(dict(
        label=period.capitalize(),
        method='update',
        args=[{'visible': vis}],
    ))

fig = go.Figure(data=traces, layout=go.Layout(
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
    updatemenus=[dict(
        type='dropdown',
        direction='down',
        x=1.0,
        y=1.15,
        showactive=True,
        active=periods.index(default_period),
        buttons=buttons,
    )],
))

fig.show()
