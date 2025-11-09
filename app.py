import streamlit as st
from google import genai
import os
from PIL import Image
import io
import time 

# --- 1. Konfigürasyon ve API Anahtarını Çekme ---

# --- CSS İYİLEŞTİRMELERİ (Line 20 Civarı) ---
st.markdown("""
<style>
/* Streamlit'in ana menü butonunu (sağ üst) ve footer'ını gizle */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Navigasyon butonlarını (sidebar) yuvarlak ve config.toml renginde yap */
.stButton>button {
    border-radius: 20px;
    border: 1px solid #3CB371; /* config.toml primaryColor */
    color: #333333;
    background-color: #F7F9FB; /* config.toml backgroundColor */
}
.stButton>button:hover {
    color: white;
    background-color: #3CB371;
    border: 1px solid #3CB371;
}
</style>
""", unsafe_allow_html=True)
# --- CSS İYİLEŞTİRMELERİ SONU ---

try:
    # API Anahtarını Streamlit Secrets'tan (vars/GEMINI_API_KEY) çekin
    if 'vars' in st.secrets and 'GEMINI_API_KEY' in st.secrets.vars:
        api_key = st.secrets.vars.GEMINI_API_KEY
    else:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("Gemini API Anahtarı bulunamadı. Lütfen Streamlit Secrets'a '[vars] GEMINI_API_KEY' değişkenini ekleyin.")
        st.stop()
        
    client = genai.Client(api_key=api_key)

except Exception as e:
    st.error(f"API istemcisi başlatılamadı: {e}")
    st.stop()

# GOOGLE SEARCH ARACI KONFİGÜRASYONU: Doğru format
tools_config = [{"google_search": {}}]


# --- 2. Oturum Durumu Yönetimi ve Navigasyon Fonksiyonu ---
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'input_data' not in st.session_state:
    st.session_state.input_data = {}

def set_step(step_number):
    """Navigasyon durumunu ayarlar."""
    st.session_state.current_step = step_number

# Uygulama ayarları (Wide mode seçildi).
st.set_page_config(page_title="🌱 YZ Tarım Danışmanlığı", layout="wide")

# Yeni Başlık ve Logo Yapısı (Pancar Kooperatifi teması için)
col_logo, col_title = st.columns([1, 6]) 

with col_logo:
    # Geçici logo yer tutucu
    st.markdown("## 🚜") 

with col_title:
    st.markdown("# YZ Destekli Tarımsal Danışmanlık (Prototip)") 

st.markdown("---")


# --- Navigasyon Butonları ---
st.sidebar.title("Danışmanlık Aşamaları")

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
        
        # Hata düzeltmesi Line 72/83: Parantez ve tırnak hatası (SyntaxError: '(' was never closed) giderildi.
        gecmis = st.text_area("Son 3 yılda tarlanızda hangi ürünleri ektiniz?", key="gecmis_input_1", value=st.session_state.input_data.get('gecmis', '2024: Buğday, 2023: Kanola, 2022: Arpa'))
        
        if st.button("Planlama Adımı 2", key="btn_planlama_ileri"):
            if il and gecmis:
                st.session_state.input_data['il'] = il
                st.session_state.input_data['gecmis'] = gecmis
                st.session_state.current_step = 2
                st.rerun()
            else:
                st.warning("Lütfen tüm alanları doldurun.")

    elif st.session_state.current_step == 2:
        # Hata düzeltmesi Line 91: Tırnak ve sözdizimi hataları (SyntaxError: unterminated string literal) giderildi.
        st.header("1. Aşama Devamı: Toprak Durumu ve Amaç")
        toprak = st.text_area("Toprak analiz sonuçlarınızın özetini girin veya önemli değerleri (pH, NPK) belirtin:", key="toprak_input_2", value=st.session_state.input_data.get('toprak', 'pH: 7.5, Organik Madde: %1.5 (Düşük), Azot (N) düzeyi orta.'))
        
        amac = st.radio("Bu sezon ana hedefiniz nedir?", 
                        ('Maksimum Kâr', 'Toprak Sağlığını Geliştirme (Münavebe)', 'Maksimum Verim'), 
                        index=['Maksimum Kâr', 'Toprak Sağlığını Geliştirme (Münavebe)', 'Maksimum Verim'].index(st.session_state.input_data.get('amac', 'Maksimum Kâr')), key="amac_radio_2")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Geri", key="back2_step2"):
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.button("Analiz Et", key="analyze2_step2"):
                if toprak and amac:
                    st.session_state.input_data['toprak'] = toprak
                    st.session_state.input_data['amac'] = amac
                    st.session_state.current_step = 3
                    st.rerun()
                else:
                    st.warning("Lütfen tüm alanları doldurun.")

    elif st.session_state.current_step == 3:
        st.header("1. Aşama Devamı: Ekim Öncesi YZ Analizi")
        
        # Hata düzeltmesi Line 118: Parantez hatası (SyntaxError: '{' was never closed) giderildi.
        prompt = f"""
        Sen Türkiye'deki çiftçilere bilimsel ve lokal verilere dayalı danışmanlık veren bir YZ Ziraat Mühendisisin. 
        Aşağıdaki verilere göre en uygun ekim öncesi tavsiyeni (ürün, münavebe ve temel gübreleme) 3 ana başlıkta özetle. 
        Cevabını Markdown formatında, net ve madde madde sun. (Veriler: Konum: {st.session_state.input_data.get('il', 'Bilinmiyor')}, Geçmiş: {st.session_state.input_data.get('gecmis', '')}, Toprak: {st.session_state.input_data.get('toprak', '')}, Amaç: {st.session_state.input_data.get('amac', '')})
        """
        
        # Hata düzeltmesi Line 103: Geçersiz sözdizimi (SyntaxError: invalid syntax) giderildi.
        with st.spinner("Gemini derinlemesine tarımsal analiz yapıyor..."): 
            try:
                response = client.models.generate_content( 
                    model='gemini-2.5-flash', 
                    contents=prompt
                )
                st.success("✅ Analiz Tamamlandı!")
                st.subheader("💡 Gemini'den Ekim Öncesi Tavsiye")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Gemini API çağrısında bir hata oluştu: {e}")
                
        st.markdown("---")
        if st.button("Yeniden Planlama Yap", key="btn_planlama_yeniden"):
            st.session_state.current_step = 1
            st.session_state.input_data = {}
            st.rerun()

# AŞAMA 4: GÖRÜNTÜ İLE TEŞHİS (Kullanıcı Sırası: 2)
elif st.session_state.current_step == 4:
    st.header("2. Aşama: Görüntü ile Hastalık/Zararlı Teşhisi")
    st.warning("Bu özellik, görsel veri gerektirir. Lütfen net, sadece sorunlu bölgeyi gösteren bir fotoğraf yükleyin.")
    
    uploaded_file = st.file_uploader("Bitki Hastalığı veya Zararlısının Fotoğrafını Yükleyin", type=["jpg", "jpeg", "png"], key="file_teshis_4")
    ek_bilgi = st.text_area("Hastalığın yayılımı, ürün adı, ne zaman başladığı gibi ek bilgileriniz varsa girin:", key="ek_bilgi_teshis_4")
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Yüklenen Görüntü', width=300)
            
            if st.button("Görüntüyü Analiz Et ve Mü
