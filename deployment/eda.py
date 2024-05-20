import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

def set_custom_background():
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://www.3csoftware.com/wp-content/uploads/2019/07/iStock-1094465844lg.jpg")
    }

    [data-testid="stAppViewBlockContainer"] {
    background-color: #161721;
    background-image: linear-gradient(-45deg, #161721, #161721 50%, #000000 50%, #000000);
    background-size: 21px 21px;
    }

    [data-testid="stHeader"] {
    background-color: rgba(9, 0, 3, 0.7);
    }

    [data-testid="stSidebar"] {
    background-color: #161721;
    background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #161721 21px ), repeating-linear-gradient( #00000055, #000000 );
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)
    
def run():
    set_custom_background()
    st.markdown("<h1 style='text-align: center;'><font color=#38b3e3> Exploratory Data Analysis</font></h1>", unsafe_allow_html=True)

    # Menampilkan gambar
    response = requests.get('https://statik.tempo.co/data/2017/10/11/id_654342/654342_720.jpg')
    title_pict = Image.open(BytesIO(response.content))
    st.image(title_pict, caption='Ilustrasi Bea dan Cukai . TEMPO/Dhemas Reviyanto',use_column_width='always')

    # Membuat fungsi untuk menarik data
    @st.cache_data
    def fetch_data(data):
        df = pd.read_csv(data, sep = ',')
        df.Date = pd.to_datetime(df.Date)
        df.set_index('Date',inplace=True)
        return df

    # Melakukan loading data
    df_thb = fetch_data('Data/THB-2001.csv')
    df_jpy = fetch_data('Data/JPY-2001.csv')
    df_krw = fetch_data('Data/KRW-2001.csv')
    df_sar = fetch_data('Data/SAR-2001.csv')
    df_sgd = fetch_data('Data/SGD-2001.csv')
    df_usd = fetch_data('Data/USD-2001.csv')

    # Menampilkan grafik tren untuk setiap mata uang
    st.markdown("<h4 style='text-align: center;'>Grafik Tren Kurs Mata Uang Terhadap IDR (Indonesian Rupiah)</h4>", unsafe_allow_html=True)
    currencies = {'USD': df_usd, 'KRW': df_krw, 'JPY': df_jpy, 'SAR': df_sar, 'SGD': df_sgd, 'THB': df_thb}
    for currency, df in currencies.items():
        st.write(f'Grafik Tren Kurs :blue[{currency}] terhadap IDR')
        st.line_chart(df['Close'])