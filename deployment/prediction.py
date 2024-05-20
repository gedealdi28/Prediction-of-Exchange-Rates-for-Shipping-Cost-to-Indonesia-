import streamlit as st
import pandas as pd
import pickle as pkl
from linreg_predict import forecasting
from arima_predict import forecast_arima
from datetime import date

def set_custom_background():
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://cdn.pixabay.com/photo/2023/11/28/08/53/skyscraper-8416953_1280.jpg")
    }

    [data-testid="stAppViewBlockContainer"] {
    background-color: #000000;
    opacity: 0.95;
    background: radial-gradient(circle, transparent 20%, #000000 20%, #000000 80%, transparent 80%, transparent), radial-gradient(circle, transparent 20%, #000000 20%, #000000 80%, transparent 80%, transparent) 52.5px 52.5px, linear-gradient(#0e101b 4.2px, transparent 4.2px) 0 -2.1px, linear-gradient(90deg, #0e101b 4.2px, #000000 4.2px) -2.1px 0;
    background-size: 105px 105px, 105px 105px, 52.5px 52.5px, 52.5px 52.5px;
    }

    [data-testid="stHeader"] {
    background-color: rgba(9, 0, 3, 0.7);
    }

    [data-testid="stSidebar"] {
    background-color: #161721;
    background: linear-gradient(135deg, #00000055 25%, transparent 25%) -21px 0/ 42px 42px, linear-gradient(225deg, #000000 25%, transparent 25%) -21px 0/ 42px 42px, linear-gradient(315deg, #00000055 25%, transparent 25%) 0px 0/ 42px 42px, linear-gradient(45deg, #000000 25%, #161721 25%) 0px 0/ 42px 42px;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

def run():
    set_custom_background()
    # Melakukan loading pickle files
    models = {}
    with open('Model/bea_cukai_thb_linreg.pkl', 'rb') as file_1:
        models['THB'] = pkl.load(file_1)
    with open('Model/bea_cukai_krw_linreg.pkl', 'rb') as file_2:
        models['KRW'] = pkl.load(file_2)
    with open('Model/bea_cukai_usd_linreg.pkl', 'rb') as file_3:
        models['USD'] = pkl.load(file_3)
    with open('Model/bea_cukai_sar_linreg.pkl', 'rb') as file_4:
        models['SAR'] = pkl.load(file_4)
    with open('Model/bea_cukai_jpy_arima.pkl', 'rb') as file_5:
        models['JPY'] = pkl.load(file_5)
    with open('Model/bea_cukai_sgd_linreg.pkl', 'rb') as file_6:
        models['SGD'] = pkl.load(file_6)
    
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
    
    st.markdown("<h1 style='text-align: center;'><font color=#38b3e3> Kalkulator Pajak Impor Barang</font></h1>", unsafe_allow_html=True)
    st.header('User Input Features')

    with st.form("Input User terkait barang"):
        st.subheader('Mata Uang')
        currency = st.selectbox('Apakah mata uang yang digunakan?',
                                ('Amerika (USD)', 'Jepang (JPY)', 'Thailand (THB)', 'Singapore (SGD)', 'Arab Saudi (SAR)', 'Korea (KRW)'))
        st.subheader('FOB/Cost (Harga Barang)')
        harga_barang = st.number_input("Masukkan FOB/ Cost (Harga Barang) sesuai mata uang negara asal barang.", min_value=0)
        st.subheader('Freight (Biaya Angkut)')
        freight = st.number_input("Masukkan Freight (Biaya Angkut) sesuai mata uang negara asal barang.", min_value=0)
        st.subheader('Asuransi')
        asuransi = st.number_input("Masukkan biaya asuransi sesuai mata uang negara asal barang (isi nilai 0 jika menggunakan asuransi dalam negeri)", min_value=0)
        st.subheader('Tanggal Pengiriman')
        date = st.date_input("Masukkan tanggal barang akan mencapai Indonesia (maksimal 2 minggu ke depan)", format="DD/MM/YYYY")

        # Membuat pilihan currency
        if currency == 'Amerika (USD)':
            currency_rate = 1
            data = df_usd
        elif currency == 'Jepang (JPY)':
            currency_rate = 0.0065
            data = df_jpy
        elif currency == 'Thailand (THB)':
            currency_rate = 0.027
            data = df_thb
        elif currency == 'Singapore (SGD)':
            currency_rate = 0.74
            data = df_sgd
        elif currency == 'Arab Saudi (SAR)':
            currency_rate = 0.27
            data = df_sar
        elif currency == 'Korea (KRW)':
            currency_rate = 0.00074
            data = df_krw

        # currency_rate = 1 # Nanti masukin currency untuk diubah ke USD
        usd_price = harga_barang*currency_rate

        # Membuat tiering untuk pajak sesuai dengan harga barang
        if (usd_price) <= 3:
            ppn = 11
            bea_masuk = 0
            pph = 0
            ppnbm = 0
        elif (usd_price > 3) and (usd_price < 1500):
            ppn = 11
            bea_masuk = 7.5
            pph = 0
            ppnbm = 0
        else :
            st.markdown('<span style="color:orange; font-size:24px;">⚠️Harga barang melebihi dari ketentuan bebas PPN dan PPH. Tolong untuk mengisi form di bawah ini ya 😊</span>', unsafe_allow_html=True)
            st.subheader('Tarif Bea Masuk(%)')
            bea_masuk = st.number_input("Masukkan % tarif Bea Masuk sesuai jenis barang", min_value=0)
            st.subheader('Tarif PPN(%)')
            ppn = st.number_input("Masukkan % tarif PPN sesuai jenis barang", min_value=0)
            st.subheader('Tarif PPh (%)')
            pph_temp = st.selectbox('Pilih % tarif PPh',
                                ('Non NPWP (15%)', 'NPWP/ Non API (7,5%)', 'API (2,5%)'))
            # Pengecekan input pada pph
            if pph_temp == 'Non NPWP (15%)':
                pph = 15
            elif pph_temp == 'NPWP/ Non API (7,5%)':
                pph = 7.5
            else :
                pph = 2.5
            st.subheader('Tarif PPnBM (%)')
            ppnbm = st.number_input("Masukkan % tarif PPnBM sesuai jenis barang", min_value=0)

        sub = st.form_submit_button("Submit data barang")
    

    if sub:
        # Model prediksi nilai kurs per hari yang disebut
        ## Mengambil range_predict (selisih antara input date dengan data)
        date = pd.to_datetime(date)
        range_predict = abs((date - data.index.max()).days)

        # Membuat mapping untuk validasi kode tiap kurs
        currency_mapping = {
            'Jepang (JPY)': 'JPY',
            'Singapore (SGD)': 'SGD',
            'Korea (KRW)': 'KRW',
            'Amerika (USD)': 'USD',
            'Thailand (THB)': 'THB',
            'Arab Saudi (SAR)': 'SAR'
        }
        currency_code = currency_mapping.get(currency)
        if currency_code is None:
            st.error('Mata uang tidak valid')
            return
        
        model = models[currency_code]

        # LINREG Forecast
        if currency_code in ['USD', 'THB', 'KRW', 'SAR', 'SGD']:
            forecast = forecasting(data, model, range_predict)
            kurs = forecast['Close'].iloc[-1]

            st.subheader('Prediksi Kurs', currency)
            st.write(f"Rp {round(kurs,2):,}")
        
        # ARIMA Forecast
        elif currency_code in ['JPY']:
            forecast = forecast_arima(model, data, range_predict)
            kurs = forecast['Close_forecast'].iloc[-1]

            st.subheader('Prediksi Kurs', currency)
            st.write(f"Rp {round(kurs,2):,}")
        
        # Hitung nilai dasar atau cif
        nilai_dasar = (harga_barang + asuransi + freight) * kurs
        st.subheader('Harga Dasar')
        st.write(f"Rp {round(nilai_dasar,2):,}")

        st.divider()
        st.subheader(f'Total Bea Masuk ({bea_masuk}%)')
        total_bea_masuk = nilai_dasar * (bea_masuk/100)
        st.write(f"Rp {round(total_bea_masuk,2):,}")

        # Hitung nilai impor kena bea masuk
        nilai_impor = nilai_dasar + total_bea_masuk

        st.subheader(f'Total PPN ({ppn}%)')
        total_ppn = nilai_impor * (ppn/100)
        st.write(f"Rp {round(total_ppn,2):,}")

        st.subheader(f'Total PPh ({pph}%)')
        total_pph = nilai_impor * (pph/100)
        st.write(f"Rp {round(total_pph,2):,}")

        st.subheader(f'Total PPnBM ({ppnbm}%)')
        total_ppnbm = nilai_impor * (ppnbm/100)
        st.write(f"Rp {round(total_ppnbm,2):,}")

        # Hitung nilai PDRI = (PPN + PPh 22)
        nilai_pdri = total_ppn + total_pph + total_ppnbm

        st.divider()
        st.subheader('TOTAL BIAYA PAJAK')
        total_pajak = nilai_pdri + total_bea_masuk
        st.subheader(f":blue[Rp {round(total_pajak,2):,}]")

        if total_pajak < (nilai_dasar/2):
            st.write(f":green[Total pajak lebih kecil dari harga barang], dengan besar persentase biaya {round(total_pajak/nilai_dasar*100,2)}% dari harga barang.")
        elif total_pajak > (nilai_dasar/2) and total_pajak < nilai_dasar:
            st.write(f":red[Total pajak melebihi 50% dari harga barang], dengan besar persentase biaya {round(total_pajak/nilai_dasar*100,2)}% dari harga barang. Dapat dipertimbangkan kembali dalam pembelian dan pemrosesan barang.")
        else:
            st.write(f":red[Total pajak lebih besar dari harga barang], dengan besar persentase biaya {round(total_pajak/nilai_dasar*100,2)}% dari harga barang. Direkomendasikan untuk tidak membeli barang.")
        
        st.write(":orange[Note : Model memiliki kecenderungan dalam memprediksi hasil yang lebih rendah dari nilai asli. Mohon persiapkan biaya sedikit lebih besar dari hasil prediksi.]")

