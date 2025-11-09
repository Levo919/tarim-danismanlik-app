import streamlit as st
from google import genai
import os
from PIL import Image
import io

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
st.sidebar.markdown("---")
st.sidebar.info("Projenin bu versiyonu Streamlit Cloud'da çalışacak şekilde optimize edilmiştir.")


# --- AŞAMALARIN TANIMLARI ---

# AŞAMA 1, 2, 3: EKİM ÖNCESİ PLANLAMA
if st.session_state.current_step == 1:
    st.header("1. Aşama: Temel Tarla Bilgileri")
    il = st.text_input("Tarlanız hangi ilde/ilçede bulunuyor?", key="il_input", value=st.session_state.input_data.get('il', 'Konya'))
    gecmis = st.text_area("Son 3 yılda tarlanızda hangi ürünleri ektiniz?", key="gecmis_input", value=st.session_state.input_data.get('gecmis', '2024: Buğday, 2023: Kanola, 2022: Arpa'))
    if st.button("Planlama Adımı 2"):
        if il and gecmis:
            st.session_state.input_data['il'] = il
            st.session_state.input_data['gecmis'] = gecmis
            st.session_state.current_step = 2
            st.rerun()
        else:
            st.warning("Lütfen tüm alanları doldurun.")

elif st.session_state.current_step == 2:
    st.header("2. Aşama: Toprak Durumu ve Amaç")
    toprak = st.text_area("Toprak analiz sonuçlarınızın özetini girin veya önemli değerleri (pH, NPK) belirtin:", key="toprak_input", value=st.session_state.input_data.get('toprak', 'pH: 7.5, Organik Madde: %1.5 (Düşük), Azot (N) düzeyi orta.'))
    amac = st.radio("Bu sezon ana hedefiniz nedir?", 
                    ('Maksimum Kâr', 'Toprak Sağlığını Geliştirme (Münavebe)', 'Maksimum Verim'), 
                    index=['Maksimum Kâr', 'Toprak Sağlığını Geliştirme (Münavebe)', 'Maksimum Verim'].index(st.session_state.input_data.get('amac', 'Maksimum Kâr')), key="amac_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Geri", key="back2"):
            st.session_state.current_step = 1
            st.rerun()
    with col2:
        if st.button("Analiz Et", key="analyze2"):
            if toprak and amac:
                st.session_state.input_data['toprak'] = toprak
                st.session_state.input_data['amac'] = amac
                st.session_state.current_step = 3
                st.rerun()
            else:
                st.warning("Lütfen tüm alanları doldurun.")

elif st.session_state.current_step == 3:
    st.header("3. Aşama: Ekim Öncesi YZ Analizi")
    prompt = f"""
    Sen Türkiye'deki çiftçilere bilimsel ve lokal verilere dayalı danışmanlık veren bir YZ Ziraat Mühendisisin. 
    Aşağıdaki verilere göre en uygun ekim öncesi tavsiyeni (ürün, münavebe ve temel gübreleme) 3 ana başlıkta özetle. 
    Cevabını Markdown formatında, net ve madde madde sun. (Veriler: Konum: {st.session_state.input_data.get('il', 'Bilinmiyor')}, Geçmiş: {st.session_state.input_data.get('gecmis', '')}, Toprak: {st.session_state.input_data.get('toprak', '')}, Amaç: {st.session_state.input_data.get('amac', '')})
    """
    
    with st.spinner("Gemini derinlemesine tarımsal analiz yapıyor..."):
        try:
            response =
