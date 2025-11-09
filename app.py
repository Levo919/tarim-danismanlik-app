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

# Tool (Araç) Tanımı: Hava durumu verisi almak için Google Search aracını tanımlıyoruz
weather_tool = {
    "name": "google:search",
    "description": "Google Search motorunu kullanarak gerçek zamanlı hava durumu bilgisi ve tahmini alınır.",
    "parameters": {
        "queries": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Hava durumu bilgisini almak için kullanılacak arama sorguları."
        }
    }
}
# --- 2. Oturum Durumu Yönetimi ---
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'input_data' not in st.session_state:
    st.session_state.input_data = {}

st.set_page_config(page_title="YZ Tarım Danışmanlığı", layout="wide")
st.title("🌱 YZ Destekli Tarımsal Danışmanlık (Prototip)")
st.markdown("---")


# --- Navigasyon Butonları ---
st.sidebar.title("Danışmanlık Aşamaları")
if st.sidebar.button("1. Planlama (Ekim Öncesi)"):
    st.session_state.current_step = 1
    st.rerun()
if st.sidebar.button("2. Teşhis (Gelişim Aşaması)"):
    st.session_state.current_step = 4
    st.rerun()
if st.sidebar.button("3. Finansal & Çevresel Analiz"):
    st.session_state.current_step = 5
    st.rerun()
if st.sidebar.button("4. Destek ve Mevzuat Danışmanlığı"):
    st.session_state.current_step = 6
    st.rerun()
if st.sidebar.button("5. Hava Durumu & Risk Analizi"):
    st.session_state.current_step = 7
    st.rerun()
st.sidebar.markdown("---")
st.sidebar.info("Projenin bu versiyonu Stream
                
