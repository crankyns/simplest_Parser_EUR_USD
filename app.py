from requests import get
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
from flask import Flask, render_template
import plotly
import plotly.graph_objects as go
import json
app = Flask(__name__)

@app.route('/')
def index():
    bar = get_data()
    return render_template('index.html', plot=bar)


url = 'https://m.myfin.by/currency/minsk/'      
headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

date_now = date.today()
eur_vals = []
usd_vals = []
date_arr = []

def get_data():
    for i in range(15):
        each_day_str = (date_now - timedelta(i)).strftime("%d-%m-%Y")
        each_day_url = url + each_day_str
        date_arr.append(each_day_str)
        resp = get(each_day_url, headers=headers)
        soup = bs(resp.content, 'html.parser')
        usd = soup.find('div', class_='bl_usd_ex').text  
        eur = soup.find('div', class_='bl_eur_ex').text 
        usd_vals.append(float(usd))
        eur_vals.append(float(eur))

    fig = go.Figure()    
    fig.add_trace(go.Scatter(
        x=date_arr[::-1], y=usd_vals[::-1], name='USD'
    ))
    fig.add_trace(go.Scatter(
        x=date_arr[::-1], y=eur_vals[::-1], name='EUR'
    ))
    fig.update_layout(xaxis_tickangle=-45)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON



if __name__ == 'main':
    app.run()