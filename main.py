import json
import os
import yfinance as yf
from dotenv import load_dotenv
from fredapi import Fred
from alpha_vantage.timeseries import TimeSeries


load_dotenv()

results = {}


# Yahoo Finance Test
try:
    stock = yf.Ticker("AAPL")

    price = stock.fast_info["last_price"]

    results["Yahoo Finance"] = {
        "status": "success",
        "price": float(price)
    }

except Exception as e:
    results["Yahoo Finance"] = {
        "status": "failed",
        "error": str(e)
    }

# FRED API Test
try:
    fred_key = os.getenv("FRED_API_KEY")

    fred = Fred(api_key=fred_key)

    gdp = fred.get_series("GDP")

    results["FRED"] = {
        "status": "success",
        "latest_value": float(gdp.dropna().iloc[-1])
    }

except Exception as e:
    results["FRED"] = {
        "status": "failed",
        "error": str(e)
    }


# Alpha Vantage Test
try:
    alpha_key = os.getenv("ALPHA_VANTAGE_KEY")

    ts = TimeSeries(
        key=alpha_key,
        output_format="json"
    )

    data, meta = ts.get_quote_endpoint(
        symbol="IBM"
    )

    results["Alpha Vantage"] = {
        "status": "success",
        "data": data
    }

except Exception as e:
    results["Alpha Vantage"] = {
        "status": "failed",
        "error": str(e)
    }


print(json.dumps(results, indent=4))