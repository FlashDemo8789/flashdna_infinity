import pandas as pd
from prophet import Prophet

def scenario_runway(burn_rate, current_cash, monthly_revenue=50000.0, rev_growth=0.1):
    meltdown=-1
    cash= current_cash
    for m in range(1,13):
        net= monthly_revenue - burn_rate
        cash+= net
        monthly_revenue*= (1+rev_growth)
        if cash<0 and meltdown<0:
            meltdown= m
    return meltdown, round(cash,2)

def prophet_forecast(df: pd.DataFrame, periods=12):
    m= Prophet(daily_seasonality=False, weekly_seasonality=False)
    m.fit(df)
    future= m.make_future_dataframe(periods=periods, freq="M")
    fc= m.predict(future)
    return fc