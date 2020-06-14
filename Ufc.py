import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots


# DATA SET PROCESSING

# read data
df = pd.read_excel('data/fights.xlsx')
a=df['Colour_Winner'].value_counts()
b=df['Colour_Winner'].unique()
c=df['title_bout'].value_counts()
d=df['title_bout'].unique()
wc=df['win_by'].value_counts()
cnn=df['Weight Class'].value_counts()
sinn=["Lightweight","Welterweight","Middleweight","Heavyweight","Light Heavyweight","Featherweight","Bantamweight","Flyweight","Women's Strawweight","Women's Bantamweight","Open Weight","Women's Flyweight","Catch Weight","Women's Featherweight"]
a1=np.flip(cnn)
b1=np.flip(sinn)
w=['Decision - Unanimous','KO/TKO','Submission','Decision - Split','TKO - Doctors Stoppage','Decision - Majority', 'Overturned',
       'DQ', 'Could Not Continue', 'Other']
v=[' ','Decision - Unanimous','KO/TKO','Submission','Decision - Split','TKO - Doctors Stoppage','Decision - Majority', 'Overturned',
       'DQ', 'Could Not Continue', 'Other']

labels1 = d
values = np.flip(c)

dfg = pd.read_excel('data/fighter.xlsx')
cn=dfg['Stance'].value_counts()
sin=dfg['Stance'].unique()
nc=np.flip(cn)
nis=np.flip(sin)

df3 = pd.read_excel('data/map.xlsx')
df3.dropna()
df_countries = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder_with_codes.csv")
df_countries = df_countries.loc[:, ["country", "continent","iso_alpha"]]
df_countries = df_countries.groupby(["country"]).first()
df3= df3.merge(df_countries, left_on="Country", right_index=True, how="left")

#================================================================================================================
fig = make_subplots(rows=2, cols=1)


#Fights by winner
colors1= ['red', 'blue', 'white']
fig.add_trace(go.Bar(
   # title_text='Total Fights by Winner',
    x=b,
    y=a,
    marker_color=colors1
),row=1,col=1)


#fig.update_layout(title_text='Total Fights by Winner',font=dict(color='rgb(255,255,255)'),plot_bgcolor='rgb(64, 64, 64)', paper_bgcolor='#1a1a1a')

#Titles Bout

fig2 = go.Figure(data=[go.Pie(labels=labels1, values=values,hole=.7)])
fig2.update_layout(title_text='Title Fights', plot_bgcolor='rgb(64, 64, 64)',font=dict(color='rgb(255,255,255)'),paper_bgcolor='#1a1a1a')

#Stance by figter

colors = ['red'] * 5
colors[1] = 'blue'
colors[2] = 'white'
colors[3] = 'blue'
fig.add_trace(go.Bar(
           # title_text='Stance by Fighter',
            x=nc,
            y=nis,
            marker_color=colors,
            orientation='h',), row=2, col=1)
fig.update_layout(title_text='Total Fights By Winner  /Total Fighters by Stance',plot_bgcolor='rgb(64, 64, 64)',font=dict(color='rgb(255,255,255)'),paper_bgcolor='#1a1a1a',showlegend=False,)
fig.update_yaxes(showgrid=False,tickfont=dict(color='white'))
fig.update_xaxes(showgrid=False,tickfont=dict(color='white'))

#treemap
values = wc
labels = w
parents = v

fig4 = go.Figure(go.Treemap(
    labels = labels,
    values = values,
    parents =parents ,
    marker_colors = ["darkblue", "royalblue", "lightblue", "red", "lightred", "lightgray", "lightblue"]))
fig4.update_layout(paper_bgcolor='#1a1a1a',title_text='Total Fights by Win By',font=dict(color='rgb(255,255,255)')


   )
#class weight
colors2 = ['blue','blue','red','red'] *14

fig5 = go.Figure(go.Bar(
            x=a1,
            y=b1,
            marker_color=colors2,
            orientation='h',))
fig5.update_xaxes(showgrid=True,tickfont=dict(color='white'))


fig5.update_layout(title_text='Total Fights by Class Weight ',font=dict(color='rgb(255,255,255)'),plot_bgcolor='rgb(64, 64, 64)',paper_bgcolor='#1a1a1a')

#MAP
colors3 = ['Blue','Red','Blue'] * 207
figmap= px.scatter_geo(df3, locations="iso_alpha",color=colors3,
                     hover_name="Country", size="Total",
                     #text="continent",
                    animation_frame="Year"
                    )
figmap.update_layout(showlegend=False,title_text='Total Fights by Country ',font=dict(color='rgb(255,255,255)'),geo = dict(
            landcolor = 'rgb(3, 0,0)',  bgcolor = 'rgb(64, 64, 64)',
        ),paper_bgcolor='#1a1a1a')


# The App itself

app = dash.Dash(__name__)

server = app.server
app.title = "UFC FIGHTS"
app.layout = html.Div([
    html.Div([html.A([
        html.Img(
            src=app.get_asset_url("fin.png"),
            alt="UFC's logo",
            id="logo",
        )
    ]),



                    html.Div([html.Label("26          Total Years")], className='mini pretty'),
                    html.Div([html.Label("476          Total Events")], className='mini pretty'),
                    html.Div([html.Label("5144         Total Fights")], className='mini pretty'),
                    html.Div([html.Label("3313         Total Fighters")], className='mini pretty'),


                ], className='4 containers row'),
    html.Div([
    html.Div([dcc.Graph(id='figweight',figure=fig5)], className='column1 pretty1'),
    html.Div([dcc.Graph(id='figmap',figure=figmap)], className='column2 pretty1')
], className='row'),
html.Div([

    html.Div([dcc.Graph(id='f1', figure=fig)], className='column1 pretty1'),
    html.Div([dcc.Graph(id='titlebout', figure=fig2)], className='column3 pretty1'),
     html.Div([dcc.Graph(id='treemap', figure=fig4)], className='column3 pretty2'),
], className='row')

])




if __name__ == '__main__':
    app.run_server(debug=True)
