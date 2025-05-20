import streamlit as st  
import pandas as pd
import numpy as np
import yfinance as yf

meta  = yf.Ticker("AMZN")

st.title("Application performances marchés")
startDate = st.date_input("Date de début")
endDate   = st.date_input("Date de fin")

histo = meta.history(start=startDate, end=endDate)
st.dataframe(histo.head(5))

histoPlot = histo["Close"]
st.line_chart(histoPlot)