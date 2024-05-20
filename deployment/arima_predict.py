# Import library
from datetime import datetime
import pandas as pd

def forecast_arima(model, data, day):
  # Melakukan forecasting pada data
  len_dataset = data.shape[0]
  len_predict = len_dataset + day


  new_pred = model.predict(len_dataset, len_predict)
  new_pred = pd.DataFrame(new_pred)
  new_pred.columns = ['Close_forecast']

  last_date = data.index.max()
  date_range = pd.date_range(start=last_date, periods=day+1)
  new_pred.index = date_range
  return new_pred
