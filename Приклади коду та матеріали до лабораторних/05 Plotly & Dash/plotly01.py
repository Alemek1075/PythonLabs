import plotly.graph_objects as go
import numpy as np
# Generate curve data
t = np.linspace(-1, 1, 100)
x = t + t ** 2
y = t - t ** 2
xm = np.min(x) - 1.5
xM = np.max(x) + 1.5
ym = np.min(y) - 1.5
yM = np.max(y) + 1.5
N = 25
s = np.linspace(-1, 1, N)
xx = s + s ** 2
yy = s - s ** 2


# Create figure
fig = go.Figure(
    data=[go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="blue")),
          go.Scatter(x=[xx[0]], y=[yy[0]],
                     mode="markers",
                     marker=dict(color="red", size=10))])
fig.update_layout(width=600, height=450,
        xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
        yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
        title_text="Kinematic Generation of a Planar Curve", title_x=0.5,
        updatemenus = [dict(type = "buttons",
        buttons = [
            dict(
                args = [None, {"frame": {"duration": 200, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 20}}],
                label = "Play",
                method = "animate",

                )])])

fig.update(frames=[go.Frame(
                        data=[go.Scatter(
                                   x=[xx[k]],
                                   y=[yy[k]])],
                        traces=[1])
        for k in range(N)])

fig.show()