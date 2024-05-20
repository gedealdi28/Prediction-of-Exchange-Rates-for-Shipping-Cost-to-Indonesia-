# Import library
from datetime import datetime
import pandas as pd

def forecasting(data, model, day):
  kurs_forecast = data.copy()
  window=5
  for i in range(day):
    temp_X = pd.DataFrame(kurs_forecast[-window:].values.reshape(1,-1))
    new_idx = datetime(kurs_forecast.index.year[-1],kurs_forecast.index.month[-1],kurs_forecast.index.day[-1]+1)
    # Forecast
    kurs_forecast.loc[new_idx] = model.predict(temp_X)
  return kurs_forecast
