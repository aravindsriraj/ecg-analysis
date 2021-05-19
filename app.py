import io
import json
import os

import plotly.utils
from flask import Flask , render_template , request
import os
from scipy.io import loadmat
import pandas as pd
import plotly.express as px
import numpy as np

app = Flask(__name__)
global data
global new_data
global start
global end


@app.route("/" , methods=["GET" , "POST"])
def index ():
    return render_template("index.html")


@app.route('/data' , methods=['GET' , 'POST'])
def data ():
    if request.method == "POST":
        file = request.files["mat"]
        if not os.path.isdir('static'):
            os.mkdir('static')
        filepath = os.path.join('static' , file.filename)
        file.save(filepath)
        mat = loadmat(filepath)
        mat = {k: v for k , v in mat.items() if k[0] != '_'}

        mat = mat["ECG_1"]
        # data = pd.DataFrame(
        #     {k: pd.Series(v[0]) for k, v in mat.items()})

        global data
        data = pd.DataFrame(mat)

        return render_template("data.html" , df=data.to_html(classes="table-primary" , header=False))
    else:

        return render_template("data.html" , df=data.to_html(classes="table-primary" , header=False))


@app.route("/graph")
def graph ():
    fig = px.line(data)
    div = fig.to_html(full_html=False)
    return render_template("graph.html" , div=div)


@app.route("/graph2" , methods=["POST"])
def graph2 ():
    global start
    global end
    start = int(request.form["start"])
    end = int(request.form["end"])
    global new_data
    new_data = data[start:end]
    fig2 = px.line(new_data)
    div2 = fig2.to_html(full_html=False)
    return render_template("graph2.html" , div=div2 , start=start , end=end)


@app.route("/stats" , methods=["POST"])
def stat ():
    values = new_data.values.tolist()
    d = {
        'mean':0,
        'median':0,
        'std':0,
        'q1':0,
        'q2':0,
        'q3':0,
        'iqr':0
    }


    d["mean"] = np.mean(values)

    d["median"] = np.median(values)

    d["std"]=np.std(values)

    d["q1"]= np.quantile(values , 0.25)

    d["q2"]= np.quantile(values , 0.5)

    d["q3"]= np.quantile(values , 0.75)

    d["iqr"]= np.quantile(values , 0.75) - np.quantile(values , 0.25)
    fig2 = px.box(new_data)
    div2 = fig2.to_html(full_html=False)


    return render_template("stats.html",d = d,start=start,end=end,div=div2)




if __name__ == '__main__':
    app.run(debug=True)
