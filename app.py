import streamlit as st
from google import genai
import os
from PIL import Image
import io
import time 

# --- 1. Konfigürasyon ve API Anahtarını Çekme ---

try:
    # API Anahtarını Streamlit Secrets veya Ortam değişkeninden alın
    # Streamlit Cloud'daki "Secrets" ayarınızdaki [vars] bölümünü kullanır
    if 'GEMINI_API_KEY' in st.secrets.vars:
        api_key = st.secrets.vars.GEMINI_API_KEY
    else:
        # Lokal veya diğer ortamlar için
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


# --- 2. Oturum Durumu Yönetimi ve Navigasyon Fonksiyonu ---
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'input_data' not in st.session_state:
    st.session_state.input_data = {}

def set_step(step_number):
    """Navigasyon durumunu ayarlar ve sayfanın yeniden yüklenmesini zorlar."""
    st.session_state.current_step = step_number
    # Streamlit, on_click kullanıldığında durumu değiştirdikten sonra otomatik rerun yapar.

st.set_page_config(page_title="YZ Tarım Danışmanlığı", layout="wide")
st.title("🌱 YZ Destekli Tarımsal Danışmanlık (Prototip)")
st.markdown("---")


# --- Navigasyon Butonları (İstenilen Yeni Sıralama) ---
st.sidebar.title("Danışmanlık Aşamaları")

# Her butonda `on_click` argümanı ve `args` kullanılarak durum değişikliği fonksiyona devredildi.
if st.sidebar.button("1. Planlama (Ekim Öncesi)", key="nav_planlama", on_click=set_step, args=(1,)):
    pass

if st.sidebar.button("2. Teşhis (Gelişim Aşaması)", key="nav_teshis", on_click=set_step, args=(4,)):
    pass

if st.sidebar.button("3. Hasat Tahmini & Satış Stratejisi", key="nav_hasat", on_click=set_step, args=(8,)):
    pass

if st.sidebar.button("4. Hava Durumu ve Kritik İşlem Riski", key="nav_hava", on_click=set_step, args=(7,)):
    pass

if st.sidebar.button("5. Finansal & Çevresel Analiz", key="nav_finansal", on_click=set_step, args=(5,)):
    pass

if st.sidebar.button("6. Destek ve Mevzuat Danışmanlığı", key="nav_mevzuat", on_click=set_step, args=(6,)):
    pass
    
st.sidebar.markdown("---")
st.sidebar.info("Projenin bu versiyonu Streamlit Cloud'da çalışacak şekilde optimize edilmiştir.")


# --- AŞAMALARIN TANIMLARI ---

# AŞAMA 1, 2, 3: EKİM ÖNCESİ PLANLAMA (Kullanıcı Sırası: 1)
if st.session_state.current_step in [1, 2, 3]:
    if st.session_state.current_step == 1:
        st.header("1. Aşama: Temel Tarla Bilgileri")
        il = st.text_input("Tarlanız hangi ilde/ilçede bulunuyor?", key="il_input_1", value=st.session_state.input_data.get('il', 'Konya'))
        # HATA DÜZELTİLDİ: Çift tırnaklar doğru kapatıldı.
        gecmis = st.text_area("Son 3 yılda tarlanızda hangi ürünleri ektiniz?", key="gecmis_input_1", value=st.session_state.input_data.get('gecmis', '2024: Buğday, 2023: Kanola, 2022: Arpa'))
        if st.button("Planlama Adımı 2", key="btn_planlama_ileri"):
            if il and gecmis:
                st.session_state.input_data['il'] = il
                st.session_state.input_data['gecmis'] = gecmis
                st.session_state.current_step = 2
                st.rerun()
            else:
                st.warning("Lütfen tüm alanları doldurun.")

    elif st.session_state.current_step
