# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 14:48:42 2020

@author: Madhan Kumar Selvaraj
"""

import flask
from flask import Flask, render_template, request
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import configuration
import main
import os
import re


server = Flask(__name__)
server.debug = True
@server.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        if ('file' in request.files):
            file = request.files['file']  
            filename = request.files['file'].filename 
            choice = request.form["optradio"]
            if choice=="view":
                name, chat_data, no_of_users = main.chat_generator(file.read(), filename)
                first_user, second_user = profile_generator(name, no_of_users)
                return render_template('chat_box.html', name = name, chat = chat_data, first = first_user, second = second_user, color_code = configuration.color_code_dict)
            elif choice == "statistics":
                print(main.chat_generator(file.read(), choice))
                return flask.redirect('/statistics')
    else:
         return render_template('landing_page.html')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app = dash.Dash(
    __name__,
    server=server, external_stylesheets=external_stylesheets,
    routes_pathname_prefix='/statistics/'
)

wa_df = pd.read_csv(configuration.csv_file_path)
wa_df['Time'] =  pd.to_datetime(wa_df['Time'], format='%H:%M')
date_df = pd.DataFrame(wa_df["Date"].value_counts())
date_df = date_df.rename(columns={"Date":"Number of chats"})
date_df['Date']= date_df.index

name_df = pd.DataFrame(wa_df["Name"].value_counts())
name_df = pd.DataFrame(wa_df["Name"].value_counts())
name_df = name_df.rename(columns={"Name":"Number of chats"})
name_df['Name']= name_df.index

fig = px.bar(date_df, x="Date", y="Number of chats", text='Number of chats', title='Number of chats based on date')
fig1 = px.pie(name_df, names='Name', values='Number of chats', title='Number of chats by person')
fig2 = px.line(wa_df, x='Date', y='Time', title='Chat timings')
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Whatsapp chat statistics',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Graph(
        id='Whatsapp',
        figure=fig
    ),
             dcc.Graph(
        id='Whatsapp1',
        figure=fig1
    ),
        dcc.Graph(
        id='Whatsapp2',
        figure=fig2
    )
])

def profile_generator(name, no_of_users):
    first_user = second_user = ""
    if no_of_users == 2:
        path = os.getcwd()   
        directory = os.listdir(path +r"/static/dp")
        for file in directory:
            result = re.findall(name+ ".*", file)
            if result:
                second_user = file
            else:
                first_user = file
    return first_user, second_user
    
if __name__ == '__main__':
    server.run(debug=True)