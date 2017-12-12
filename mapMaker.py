import plotly
import plotly.plotly as py
plotly.tools.set_credentials_file(username='NathanMcKenna', api_key='L4z4eGvpGdjQC1q2jasg')
import pandas as pd

df = pd.read_csv('finalmerge.csv')
print(df.corr())

data = [ dict(
        type = 'choropleth',
        locations = df['Country Code'],
        z = df['Happiness Score'],
        text = df['Country'],
        colorscale = 'Earth',
        autocolorscale = False,
        reversescale = False,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'Score'),
      ) ]

layout = dict(
    title = 'Happiness Score of Countries',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.plot( fig, validate=False, filename='HDI-world-map' )
