# Import the lib
import streamlit as st
import pandas as pd
from alpha_vantage.cryptocurrencies import CryptoCurrencies

# Put the API KEY of ref:
API_KEY = '<YOUR_API_KEY'

# Set the Layout
st.set_page_config(layout="wide")
# Define function to take the data and do cache


@st.cache(allow_output_mutation=True)
def get_data(curr, exchange):

    cc = CryptoCurrencies(key=API_KEY, output_format='pandas')

    data, meta = cc.get_digital_currency_daily(
        symbol=curr, market=exchange)
    data.drop(columns=['1b. open (USD)', '2b. high (USD)',
                       '3b. low (USD)', '4b. close (USD)'], inplace=True)

    df = data.rename(columns={'5. volume': 'Volume',
                              '6. market cap (USD)': 'Market Cap'}, inplace=True)

    close = '4a. close ({})'.format(exchange)
    open = '1a. open ({})'.format(exchange)
    high = '2a. high ({})'.format(exchange)
    low = '3a. low ({})'.format(exchange)
    data.rename(columns={close: 'Close', open: 'Open',
                         high: 'High', low: 'Low'}, inplace=True)
    return data, meta

# Chart function for plotting


def graph_plot(data):
    val = st.selectbox(options=['Open', 'Close', 'High',
                                'Low', 'Volume', 'Market Cap'], label='Select Attributes of currency {}'.format(curr))

    if val == 'Volume' or val == 'Market Cap':
        st.bar_chart(data[val])
    else:
        st.line_chart(data[val])

# -------------- Define the Layout --------------


# Define layout for Title
left, right = st.beta_columns(2)
with left:
    st.markdown("# CryptoCurrency Analyzer")

with right:
    st.image('data/crypto.png')

# Info on the cryptocurrency
st.markdown("A cryptocurrency (or “crypto”) is a digital currency that can be used to buy goods and services, but uses an online ledger with strong cryptography to secure online transactions. Much of the interest in these unregulated currencies is to trade for profit, with speculators at times driving prices skyward.")

# Info regrading cryptocurrency
st.markdown(
    "To know more about it :point_right: [Article](https://www.nerdwallet.com/article/investing/cryptocurrency-7-things-to-know)")

# Import the CSV Currenecy files
crypto_list = pd.read_csv('data/digital_currency_list.csv')
market = pd.read_csv('data/physical_currency_list.csv')

# Define layout for Dropdown
left, right = st.beta_columns(2)
with left:
    curr = st.selectbox(label='Choose CryptoCurrency',
                        options=crypto_list['currency code'])

with right:
    exchange = st.selectbox(label='Exchnage Rate CryptoCurrency',
                            options=market['currency code'])
# Take the data
data, meta = get_data(curr, exchange)

# Pront the Info
st.markdown("Market Name is **{}**".format(meta['5. Market Name']))

# Show the table
st.dataframe(data)

# Show the Graph
graph_plot(data)
