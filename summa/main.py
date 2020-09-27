import warnings
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output, State
import sd_material_ui
from dash.exceptions import PreventUpdate
import requests
import pandas as pd
from newspaper import Article

from summarizer import summarize
from keywords import keywords

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# instantiating dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # the flask app
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([

    html.Br(),
    html.Br(),
    html.Br(),

    html.Div(html.H1("SimilaritySum"), style={'font-weight':'bold', 'color':'darkblue','text-align':'center'}),

    html.Br(),
    html.Br(),

    dbc.Row([

        dbc.Col(dbc.Input(id='url_1', type='url', size=30, placeholder="Article 1 URL"), width={'size':6, 'order':1, 'offset':3}),
        ]),

    html.Br(),
    dbc.Row([

        dbc.Col(dbc.Input(id='url_2', type='url', size=30, placeholder="Article 2 URL"), width={'size':6, 'order':1, 'offset':3}),
        dbc.Col(dbc.Button("Summarize", id='button', n_clicks=1, color="primary", className="mr-1"), width={'order':2})

        ]),

    html.Br(),
    html.Br(),
    html.Br(),

    dbc.Row([

        dbc.Col(dcc.Loading(), width={'size':6, 'offset':3})

    ]),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H3("Standard Summaries"), width={'size':5, 'offset':1}, style={'text-align':'center'}),
        dbc.Col(html.H3("SimilaritySum Summaries"), width={'size':5, 'offset':0}, style={'text-align':'center'}),
        ]),
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H4(id='title1Left'), width={'size':5, 'offset':1}, style={'text-align':'center'}),
        dbc.Col(html.H4(id='title1Right'), width={'size':5, 'offset':0}, style={'text-align':'center'}),
        ]),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H6(id='individualSummary1'), width={'size':5, 'offset':1}, style={'text-align':'left'}),
        dbc.Col(html.H6(id='mergedSummary1'), width={'size':5, 'offset':0}, style={'text-align':'left'}),
        ]),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H4(id='title2Left'), width={'size':5, 'offset':1}, style={'text-align':'center'}),
        dbc.Col(html.H4(id='title2Right'), width={'size':5, 'offset':0}, style={'text-align':'center'}),
        ]),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H6(id='individualSummary2'), width={'size':5, 'offset':1}, style={'text-align':'left'}),
        dbc.Col(html.H6(id='mergedSummary2'), width={'size':5, 'offset':0}, style={'text-align':'left'}),
        ]),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H6("Similarity Score: ", id='score1'), width={'size':5, 'offset':1}),
        dbc.Col(html.H6("Similarity Score: ", id='score2'), width={'size':5, 'offset':0}),
        ]),

    html.Br(),

])


# Types of summarization
SENTENCE = 0
WORD = 1

DEFAULT_RATIO = 0.25


def textrank(text1, text2, summarize_by=SENTENCE, ratio=DEFAULT_RATIO, words=None, additional_stopwords=None):
    if summarize_by == SENTENCE:
        return summarize(text1, text2, ratio, words, additional_stopwords=additional_stopwords)
    else:
        return keywords(text1, text2, ratio, words, additional_stopwords=additional_stopwords)

def fetch_article_text_and_title(url):
  try:
    article = Article(url)
    article.download()
    article.parse()
    return article.text, article.title
  except:
    return None, None

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("{} not in range [0.0, 1.0]".format(x))
    return x

@app.callback( 
    [Output('title1Left', 'children'),
    Output('title2Left', 'children'),
    Output('title1Right', 'children'),
    Output('title2Right', 'children'),
    Output('individualSummary1', 'children'),
    Output('individualSummary2', 'children'),
    Output('mergedSummary1', 'children'),
    Output('mergedSummary2', 'children'),
    Output('score1', 'children'),
    Output('score2', 'children')],
    [Input('button', 'n_clicks')],
    [State('url_1', 'value'), State('url_2', 'value')])
def similaritySum(n_click:int, url_1, url_2):
    if n_click>1:
        # Fetch the text from each of the URLs
        text1, title1 = fetch_article_text_and_title(url_1)
        text2, title2 = fetch_article_text_and_title(url_2)

        print(text1)
        print(text2)
        individualSummary1, individualSummary2, mergedSummary1, mergedSummary2, score1, score2 = textrank(text1, text2)
        score1 = "Similarity score: " + str(score1)
        score2 = "Similarity score: " + str(score2)
        print("individualSummary1")
        print(individualSummary1)
        print("individualSummary2")
        print(individualSummary2)
        print("mergedSummary1")
        print(mergedSummary1)
        print("mergedSummary2")
        print(mergedSummary2)
        print("score1")
        print(score1)
        print("score2")
        print(score2)

        return title1, title2, title1, title2, individualSummary1, individualSummary2, mergedSummary1, mergedSummary2, score1, score2

    else: 
        return [], [], [], [], [], [], [], [], [], []

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)

