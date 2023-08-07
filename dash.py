import streamlit as st
import pandas as pd
import yfinance as yf



st.title("Inversiones en Acciones")

tickers = ["AAPL","MSFT","TSLA","BTC-USD","ETH-USD"]

dropdown = st.multiselect("Elige tus activos", tickers)

start = st.date_input('Fecha Inicial', value = pd.to_datetime("2023-01-31"))
end = st.date_input("Fecha Final", value = pd.to_datetime("today"))

st.markdown("""---""")

st.markdown("""---""")


def relativeret(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod()-1
    cumret = cumret.fillna(0)
    return cumret



if len(dropdown) > 0:
 
    df = relativeret(yf.download(dropdown, start, end)["Adj Close"])
    
    df2 = yf.download(dropdown, start, end)["Adj Close"]
    
    st.line_chart(df)

    
    st.markdown("""---""")
    
    
    st.bar_chart(df2)
