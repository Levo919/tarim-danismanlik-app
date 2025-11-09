import streamlit as st
from google import genai
import os
from PIL import Image
import io
import time 

# --- 1. Konfigürasyon ve API Anahtarını Çekme (Streamlit Secrets Desteği) ---

try:
    # API Anahtarını Streamlit Secrets veya Ortam değişkeninden alın
    if 'GEMINI_API_KEY' in st.secrets.vars:
        api_key = st.secrets.vars.GEMINI_API_KEY
    else:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("Gemini API Anahtarı bulunamadı. Lütfen Streamlit Secrets'a 'GEMINI_API_KEY' değişkenini ekleyin.")
        st.stop()
        
    client = genai.Client(api_key=api_key)

except Exception as e:
    st.error(f"API istemcisi başlatılamadı: {e}")
    st.stop()

# Tool (Araç) Tanımı: Google Search aracının basit tanımı
weather_tool_config = [{"google_search": {}}]


# --- 2. Oturum Durumu Yönetimi ---
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'input_data' not in st.session_state:
    st.session_state.input_data = {}

st.set_page_config(page_title="YZ Tarım Danışmanlığı", layout="wide")
st.title("🌱 YZ Destekli Tarımsal Danışmanlık (Prototip)")
st.markdown("---")


# --- Navigasyon Butonları (İstenilen Yeni Sıralama) ---
st.sidebar.title("Danışmanlık Aşamaları")

# 1. Planlama (Ekim Öncesi) -> Kod Aşama 1
if st.sidebar.button("1. Planlama (Ekim Öncesi)"):
    st.session_state.current_step = 1
    st.rerun()

# 2. Gelişim Aşaması (Teşhis) -> Kod Aşama 4
if st.sidebar.button("2. Teşhis (Gelişim Aşaması)"):
    st.session_state.current_step = 4
    st.rerun()

# 3. Hasat Dönemi -> Kod Aşama 8
if st.sidebar.button("3. Hasat Tahmini & Satış Stratejisi"):
    st.session_state.current_step = 8
    st.rerun()

# 4. Hava Durumu ve Risk Analizi -> Kod Aşama 7
if st.sidebar.button("4. Hava Durumu ve Kritik İşlem Riski"):
    st.session_state.current_step = 7
    st.rerun()

# 5. Finansal ve Çevresel Analiz -> Kod Aşama 5
if st.sidebar.button("5. Finansal & Çevresel Analiz"):
    st.session_state.current_step = 5
    st.rerun()

# 6. Destek ve Mevzuat Danışmanlığı -> Kod Aşama 6
if st.sidebar.button("6. Destek ve Mevzuat Danışmanlığı"):
    st.session_state.current_step = 6
    st.rerun()
    
st.sidebar.markdown("---")
st.sidebar.info("Projenin bu versiyonu Streamlit Cloud'da çalışacak şekilde optimize edilmiştir.")


# --- AŞAMALARIN TANIMLARI ---

# AŞAMA 1, 2, 3: EKİM ÖNCESİ PLANLAMA (Kullanıcı Sırası: 1)
if st.session_state.current_step == 1:
    st.header("1. Aşama: Temel Tarla Bilgileri")
    il = st.text_input("Tarlanız hangi ilde/ilçede bulunuyor?", key="il_input", value=st.session_state.input_data.get('il', 'Konya'))
    gecmis = st.text_area("Son 3 yılda tarlanızda hangi ürünleri ektiniz?", key="gecmis_input", value=st.session_state.input_data.get('gecmis', '2024: Buğday, 2023: Kanola, 2022: Arpa'))
    if st.button("Planlama Adımı 2"):
        if il and gecmis:
            st.session_state.input_data['il'] = il
            st.session_state.input_data['gecmis'] = gecmis
            st.session_state.current_step = 2
            st.rer
