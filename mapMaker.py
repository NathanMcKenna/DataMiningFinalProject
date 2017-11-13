import plotly
import plotly.plotly as py
plotly.tools.set_credentials_file(username='NathanMcKenna', api_key='L4z4eGvpGdjQC1q2jasg')
import pandas as pd

df = pd.read_csv('countries.csv')

data = [ dict(
        type = 'choropleth',
        locations = df['Country Code'],
        z = df['Biocapacity Deficit or Reserve'],
        text = df['Country'],
        colorscale =  [
		['0.0', 'rgb(165,0,38)'],
		['0.115', 'rgb(165,0,38)'],
		['0.115', 'rgb(0,153, 0)'],
		['0.25', 'rgb(0,153, 0)'],
		['0.25', 'rgb(51, 255, 71)'],
		['1.0', 'rgb(51, 255, 71)']
		 	
    
  ],
        autocolorscale = False,
        reversescale = False,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'Footprint Ratio'),
      ) ]

layout = dict(
    title = 'Biocapacity Deficit or Reserve (Ecological Footprint)',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.plot( fig, validate=False, filename='EcoFootprint-world-map' )
