from flask import Flask, jsonify, request, render_template, flash, current_app, send_file
from flask_cors import CORS

import pandas as pd

from predictor import predict_uninstall
from utils import get_chart_data, get_uploaded_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zLvTkr>G}85rbU|S/-jS|X5M9g+~H:'
CORS(app)

@app.route('/', methods=['GET'])
def default():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    try: 
        return send_file('sample.xlsx', as_attachment=True, attachment_filename='uninstall _data.xlsx')
    except Exception as e:
        return str(e)
        
@app.route('/us_pred.html', methods=['POST'])
def us_pred_route():
    if request.method == 'POST':
        df = get_uploaded_file()

        result_7 = predict_uninstall(data=df, model_name='us_7.pkl', lag_range=[7, 17])
        result_5 = predict_uninstall(data=df, model_name='us_5.pkl', lag_range=[5, 15])

        r7 = result_7.set_axis(['date', 'pred', 'lower', 'upper'], axis=1, inplace=False)
        
        chart_d, history = get_chart_data(r7, df)

        return render_template('result.html', 
                                result_7=result_7.values.tolist(),
                                result_5=result_5.values.tolist(),
                                chart_data=chart_d,
                                history=history,
                                region='United States')



@app.route('/gl_pred.html', methods=['POST'])
def gl_pred_route():
    if request.method == 'POST':
        df = get_uploaded_file()
        
        result_7 = predict_uninstall(data=df, model_name='gl_7.pkl', lag_range=[7, 17])
        result_5 = predict_uninstall(data=df, model_name='gl_5.pkl', lag_range=[5, 15])

        r7 = result_7.set_axis(['date', 'pred', 'lower', 'upper'], axis=1, inplace=False)
        
        chart_d, history =  get_chart_data(r7, df)

        return render_template('result.html', 
                                result_7=result_7.values.tolist(),
                                result_5=result_5.values.tolist(),
                                chart_data=chart_d,
                                history=history,
                                region='GLOBAL')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0') 
