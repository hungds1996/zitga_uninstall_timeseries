import pickle
import pandas as pd
import numpy as np

def preprocessing_data(lag_range, data):
    p_data = pd.DataFrame(data[data.columns[-1]].copy())
    p_data.columns = ['y']
    
    for i in range(lag_range[0], lag_range[1]):
        p_data['lag_{}'.format(i)] = p_data.y.shift(i)
    
    p_data.index = pd.to_datetime(p_data.index)

    p_data['weekday'] = p_data.index.weekday
    p_data['is_weekend'] = p_data.index.weekday.isin([4, 5])*1

    p_data['weekday_to_predict'] = p_data.index.shift(periods=lag_range[0], freq='D').weekday
    p_data['is_weekend_to_predict'] = p_data.weekday_to_predict.isin([4,5])*1

    X = p_data.dropna().drop(['y'], axis=1)
    
    return X, p_data

def predict_uninstall(data, model_name, lag_range):
    model_dir = './models/' + model_name
    
    with open(model_dir, 'rb') as handle:
        model = pickle.load(handle)

    X, p_data = preprocessing_data(lag_range=lag_range, data=data)

    pred = model.predict(X)
    
    index = pd.DataFrame(p_data.index.shift(lag_range[0], freq='D'))[-lag_range[0]:]
    pred = pd.DataFrame(pred)[-lag_range[0]:]
    
    index.reset_index(drop=True, inplace=True)
    pred.reset_index(drop=True, inplace=True)
        
    index = index.astype('str')
    pred = pred.round(0).astype('int')

    scale = 1.3
    pred_std = pred.std()
    lower = pred - scale * pred_std
    upper = pred + scale * pred_std
    lower = lower.round(0).astype('int')
    upper = upper.round(0).astype('int')
    
    result = pd.concat([index, pred, lower, upper], axis=1)
    
    return result

# def us_predict_5_days(data):
#     with open('us_5.pkl', 'rb') as handle:
#         model = pickle.load(handle)

#     X, p_data = preprocessing_data(lag_range=[5, 15], data=data)

#     pred = model.predict(X)
    
#     index = pd.DataFrame(p_data.index.shift(5, freq='D'))[-5:]
#     pred = pd.DataFrame(pred)[-5:]
    
#     index.reset_index(drop=True, inplace=True)
#     pred.reset_index(drop=True, inplace=True)
        
#     index = index.astype('str')
#     pred = pred.round(0).astype('int')

#     scale = 1.8
#     pred_std = pred.std()
#     lower = pred - scale * pred_std
#     upper = pred + scale * pred_std
#     lower = lower.round(0).astype('int')
#     upper = upper.round(0).astype('int')
    
#     result = pd.concat([index, pred, lower, upper], axis=1)
    
#     return result

# def us_predict_7_days(data):
#     with open('us_7.pkl', 'rb') as handle:
#         model = pickle.load(handle)

#     X, p_data = preprocessing_data(lag_range=[7, 17], data=data)

#     pred = model.predict(X)
    
#     index = pd.DataFrame(p_data.index.shift(7, freq='D'))[-7:]
#     pred = pd.DataFrame(pred)[-7:]
    
#     index.reset_index(drop=True, inplace=True)
#     pred.reset_index(drop=True, inplace=True)
        
#     index = index.astype('str')
#     pred = pred.round(0).astype('int')

#     scale = 1.8
#     pred_std = pred.std()
#     lower = pred - scale * pred_std
#     upper = pred + scale * pred_std
#     lower = lower.round(0).astype('int')
#     upper = upper.round(0).astype('int')
    
#     result = pd.concat([index, pred, lower, upper], axis=1)
    
#     return result


# def gl_predict_7_days(data):
#     recalibrate = 1

#     with open('gl_7.pkl', 'rb') as handle:
#         model = pickle.load(handle)

#     X, p_data = preprocessing_data(lag_range=[7, 17], data=data)

#     pred = model.predict(X) * recalibrate
    
#     index = pd.DataFrame(p_data.index.shift(7, freq='D'))[-7:]
#     pred = pd.DataFrame(pred)[-7:]
    
#     index.reset_index(drop=True, inplace=True)
#     pred.reset_index(drop=True, inplace=True)
        
#     index = index.astype('str')
#     pred = pred.round(0).astype('int')

#     scale = 1.8
#     pred_std = pred.std()
#     lower = pred - scale * pred_std
#     upper = pred + scale * pred_std
#     lower = lower.round(0).astype('int')
#     upper = upper.round(0).astype('int')
    
#     result = pd.concat([index, pred, lower, upper], axis=1)
    
#     return result


# def gl_predict_5_days(data):
#     #recalibrate
#     recalibrate = 1

#     #get model
#     with open('gl_5.pkl', 'rb') as handle:
#         model = pickle.load(handle)

#     #data preprocessing
#     X, p_data = preprocessing_data(lag_range=[5, 15], data=data)

#     # Predict and recalibrate
#     pred = model.predict(X) * recalibrate
    
#     # modifying for visualisation
#     index = pd.DataFrame(p_data.index.shift(5, freq='D'))[-5:]
#     pred = pd.DataFrame(pred)[-5:]
    
#     index.reset_index(drop=True, inplace=True)
#     pred.reset_index(drop=True, inplace=True)
        
#     index = index.astype('str')
#     pred = pred.round(0).astype('int')
    
#     scale = 1.8
#     pred_std = pred.std()
#     lower = pred - scale * pred_std
#     upper = pred + scale * pred_std
#     lower = lower.round(0).astype('int')
#     upper = upper.round(0).astype('int')
    
#     result = pd.concat([index, pred, lower, upper], axis=1)
    
#     return result