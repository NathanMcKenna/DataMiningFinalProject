import plotly
import plotly.plotly as py
plotly.tools.set_credentials_file(username='NathanMcKenna', api_key='L4z4eGvpGdjQC1q2jasg')
import pandas as pd

df = pd.read_csv('countries.csv')
#print(df.corr())

data = [ dict(
        type = 'choropleth',
        locations = df['Country Code'],
        z = df['GDP per Capita'],
        text = df['Country'],
        colorscale = 'Reds',
        autocolorscale = True,
        reversescale = False,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'Carbon Footprint'),
      ) ]

layout = dict(
    title = 'GDP of Countries',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.plot( fig, validate=False, filename='GDP-world-map' )
