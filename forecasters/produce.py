from prophet import Prophet
import pandas as pd
from batches.models import BatchProduce
from django.db.models import F

def produce_use_forecaster(current_produce, periods, freq):
    # Fetching the data from BatchProduce
    data = BatchProduce.objects.filter(produce=current_produce).annotate(
        used=F('initial_stock') - F('left_in_stock')).values('batch__added_to_inventory_on', 'used')

    # Converting data into a pandas DataFrame
    df = pd.DataFrame.from_records(data)
    df.rename(columns={'batch__added_to_inventory_on': 'ds', 'used': 'y'}, inplace=True)

    # Converting 'ds' to datetime
    df['ds'] = pd.to_datetime(df['ds'])

    # Initializing and fitting the Prophet model
    model = Prophet()
    model.fit(df)

    # Making future predictions
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)

    # Extracting the relevant prediction data (date and yhat)
    predictions = forecast[['ds', 'yhat']].tail(periods)

    # Formatting the results as a dictionary for JSON output
    forecast_json = predictions.set_index('ds').to_dict()['yhat']

    return forecast_json
