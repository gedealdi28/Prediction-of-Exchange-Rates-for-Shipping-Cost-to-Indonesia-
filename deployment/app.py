import streamlit as st
from streamlit_option_menu import option_menu
import eda
import prediction

# Definisi halaman-halaman
PAGES = {
    "EDA": eda,
    "Tax Calculator": prediction
}

# Navigasi halaman
with st.sidebar:
    ## Menambahkan logo dan nama aplikasi
    st.image("logo.png")
    st.markdown("<h1 style='text-align: center;'><em>Welcome to</em><font color=#38b3e3> CurrenSee IDR</font>!</h1>", unsafe_allow_html=True)
    st.write("___") # Pemisah
    ## Option menu
    selected_page = option_menu("Menu", list(PAGES.keys()), icons=['house', 'calculator'])

# Menjalankan halaman yang dipilih
page = PAGES[selected_page]
page.run()