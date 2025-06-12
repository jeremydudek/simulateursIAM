import streamlit as st
from eodhd import APIClient
import pandas as pd
import numpy as np
from datetime import date

# -------------------------------------------------------------------
api = APIClient("68372f83415fe3.24985765")
# -------------------------------------------------------------------

st.logo("https://blog.iam-fp.com/images/logo_iam_horizontal_bleu.png", 
        link="https://www.iam-fp.com/", 
        icon_image="https://blog.iam-fp.com/images/logo_iam_horizontal_bleu.png")

# ---- function pour rebaser à 100 ----
def rebase_df_to_100(df):
    base_values = df.iloc[0]
    return df.divide(base_values) * 100

# ---- function de complétion des données manquantes ---- 
def completion_df(df):
    return df.ffill()

# ---- Mécanique de sélection des dates ----
with st.form("chooseDate"):
    header = st.title("Sélection des dates")
    
    row1 = st.columns([1,1])
    startDate = row1[0].date_input("Date de début", value="2020-12-15")
    endDate = row1[1].date_input("Date de fin")

    st.form_submit_button('Update data')

# récupération des données
# multi_data = yf.download(["TNOW.MI", "LCUJ.DE", "XAD1.DE", "MFEC.PA", "IUSE.L"], start = startDate, end = endDate)

multi_data = api.get_eod_historical_stock_market_data(symbol='VWCE.XETRA', 
                                                      period='d', 
                                                      from_date='2015-01-01', 
                                                      to_date=str(date.today()), 
                                                      order='a')

multi_data = pd.json_normalize(multi_data)

histo      = completion_df(multi_data["close"])
histoPlot  = rebase_df_to_100(histo)

st.dataframe(histo.tail(5))
st.line_chart(histoPlot)