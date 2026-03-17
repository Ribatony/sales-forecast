import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_sales(df: pd.DataFrame):
    # Ensure required columns exist
    if "date" not in df.columns or "sales" not in df.columns:
        raise ValueError("CSV must have 'date' and 'sales' columns")

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isnull().any():
        raise ValueError("Invalid date format in 'date' column")

    # Ensure sales column is numeric
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    if df['sales'].isnull().any():
        raise ValueError("Invalid numeric values in 'sales' column")

    # Set date as index
    df = df.set_index('date')

    # Require at least 12 rows for seasonal forecasting
    if len(df) < 12:
        raise ValueError("Need at least 12 rows of data for forecasting")

    # Fit Holt-Winters model
    model = ExponentialSmoothing(df['sales'], trend="add", seasonal="add", seasonal_periods=12)
    fit = model.fit()

    # Forecast next 12 periods
    forecast = fit.forecast(12)
    forecast_df = pd.DataFrame({"date": forecast.index, "forecast": forecast.values})
    return forecast_df

