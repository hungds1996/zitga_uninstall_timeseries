import json
import os
import time
import csv
import pandas as pd

from flask import Flask, jsonify, request, render_template, flash, current_app
from werkzeug.utils import secure_filename


def get_uploaded_file():
    """
    Get uploaded file, save as a new file in upload folder with unique timestamp
    """

    timestampe = time.time()
    file = request.files['fileupload']

    old_name = secure_filename(file.filename).split('.')
    filename = old_name[0] + str(timestampe) + '.' + old_name[1]
    file.save(os.path.join('C:/Users/Asus/Documents/Python/Uninstall predicition/product/upload', filename))

    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    # APP_UPLOAD = os.path.join(APP_ROOT, 'upload')

    with current_app.open_resource('upload/' + filename) as f:
        if old_name[1] == 'csv':
            df = pd.read_csv(f, index_col=0, parse_dates=True)
        elif old_name[1] == 'xlsx':
            df = pd.read_excel(f, index_col=0, parse_dates=True)
    
    return df

def get_chart_data(prediction, data, history_length=50):
    """
    Prepare data for visualizing predition

    predition: prediction data, preferable with low and high threshold. 2 required columns: "date", "pred"
    data: past data of the predicted variable, required column: "date"
    history_length: default = 50, how many time step to be visulized for past data
    """

    chart_d = {}

    for i in prediction.columns:
        if i == 'date':
            continue
        chart_data = prediction[['date', i]].to_dict(orient='records')
        chart_data = json.dumps(chart_data)
        chart_d[i] = chart_data

    df_new = data.copy()
    df_new['date'] = df_new.index.astype(str)
    df_new.columns = ['uninstall', 'date']

    history = df_new[-history_length:].to_dict(orient='records')
    history = json.dumps(history)

    return chart_d, history
