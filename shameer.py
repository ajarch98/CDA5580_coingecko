import streamlit as st
import pandas as pd
import requests
import json

from datetime import datetime

# _data = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=cad&days=90&interval=daily").json()
# with open('_data.json', 'w+') as f:
#     json.dump(_data, f)


def extract_data(currency, num_days):
    if currency is None:
        raise APIException("Currency parameter is undefined")
    if num_days is None:
        raise APIException("`num_days` parameter is undefined")
    
    # TODO: Use params instead of f-strings
    _data = requests.get(
        f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency={currency}&days={num_days}&interval=daily",
        params={
            "vs_currency": currency,
            "days": num_days,
            "interval": "daily"
        }
    )
    return _data.json()


def transform_load_data(_data):
    df = pd.DataFrame(
        data=(price_elem[1] for price_elem in _data['prices'])
    )
    return df


# setup

def main():
    st.title('Streamliting CoinGecko')
    num_days = st.slider(
        label="Number of days",
        min_value=1,
        max_value=750,
        format=None
    )
    currency = st.radio(
        label="Currency",
        options=["CAD", "USD", "INR"],
        index=0
    ).lower()

    # Extraction
    _data = extract_data(
        currency=currency,
        num_days=num_days
    )
    df = transform_load_data(_data)
    avg = (df[df.index < num_days].sum()/num_days)[0]

    num_prices = len([price_elem[1] for price_elem in _data['prices']]) # TODO: debugging, remove

    # Post-extraction
    st.line_chart(
        data=df,
        use_container_width=True
    )
    st.write(f"Average price during this time was {avg}")


if __name__ == "__main__":
    main()

