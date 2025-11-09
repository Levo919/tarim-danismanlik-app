import streamlit as st
from google import genai
import os
from PIL import Image
import io
import time 

# --- 1. Konfigürasyon ve API Anahtarını Çekme ---

# --- CSS İYİLEŞTİRMELERİ ---
st.markdown("""
<style>
/* Streamlit'in ana menü butonunu (sağ üst) ve footer'ını gizle */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Navigasyon butonlarını (sidebar) yuvarlak ve config.toml renginde yap */
.stButton>button {
    border-radius: 20px;
    border: 1px solid #3CB371; /* config.toml primaryColor (varsayılan yeşil) */
    color: #333333;
    background-color: #F7F9FB; /* config.toml backgroundColor (varsayılan açık gri) */
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
    # Lütfen "pankobirlik_logo.png" dosya adını, GitHub'a yüklediğiniz dosya adıyla DEĞİŞTİRİN.
    st.image("pankobirlik_logo.png", width=70) 

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
        
        prompt = f"""
        Sen Türkiye'deki çiftçilere bilimsel ve lokal verilere dayalı danışmanlık veren bir YZ Ziraat Mühendisisin. 
        Aşağıdaki verilere göre en uygun ekim öncesi tavsiyeni (ürün, münavebe ve temel gübreleme) 3 ana başlıkta özetle. 
        Cevabını Markdown formatında, net ve madde madde sun. (Veriler: Konum: {st.session_state.input_data.get('il', 'Bilinmiyor')}, Geçmiş: {st.session_state.input_data.get('gecmis', '')}, Toprak: {st.session_state.input_data.get('toprak', '')}, Amaç: {st.session_state.input_data.get('amac', '')})
        """
        
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
            
            if st.button("Görüntüyü Analiz Et ve Müdahale Önerisi Al", key="btn_analiz_teshis_4"):
                if ek_bilgi.strip() == "":
                    st.warning("Lütfen teşhisin doğruluğu için ek bilgi (ürün, yayılım) girin.")
                else:
                    teshis_prompt = f"""
                    Sen uzman bir ziraat mühendisisin. Ekteki görselde gördüğünüz bitki hastalığı/zararlısı nedir? 
                    Teşhisi koyduktan sonra, lütfen Türkiye tarımına uygun, uygulanabilir bir mücadele ve dozaj önerisi sun. Türkiye'deki kimyasal mücadele ruhsatlarını göz önünde bulundur.
                    
                    --- EK BİLGİLER ---
                    Hastalık hakkında çiftçinin verdiği ek bilgi: {ek_bilgi}
                    """
                    
                    contents = [teshis_prompt, image]
                    
                    with st.spinner("Gemini hem görseli hem de metni analiz ediyor..."): 
                        response = client.models.generate_content(
                            model='gemini-2.5-flash', 
                            contents=contents
                        )
                        st.success("✅ Teşhis Tamamlandı!")
                        st.subheader("🔬 YZ'den Teşhis ve Müdahale Önerisi")
                        st.markdown(response.text)
                        
        except Exception as e:
            st.error(f"Görüntü işlenirken bir hata oluştu: {e}")
            
    st.markdown("---")
    if st.button("Yeni Teşhis Başlat", key="btn_yeni_teshis_4"):
        st.session_state.current_step = 4
        st.rerun()

# AŞAMA 5: FİNANSAL VE ÇEVRESEL ANALİZ (Kullanıcı Sırası: 5)
elif st.session_state.current_step == 5:
    st.header("5. Aşama: Finansal ve Çevresel Etki Analizi")
    st.info("Bu modül, girdi planlarınızın ekonomik yükünü ve çevresel ayak izini değerlendirir.")
    
    gubre_plan = st.text_area(
        "Kullanmayı planladığınız gübre türlerini (Örn: Üre, DAP, Amonyum Sülfat) ve miktarlarını (kg/dekar) girin:", 
        key="gubre_plan_input_5", 
        value="Üre: 25 kg/dekar, DAP: 15 kg/dekar, Potasyum Sülfat: 5 kg/dekar"
    )
    
    col_fiyat, col_alan = st.columns(2)
    with col_fiyat:
        gubre_fiyat = st.text_input("Bölgenizdeki ortalama gübre fiyatı (Örn: Üre'nin 50 kg çuvalı 800 TL):", key="gubre_fiyat_input_5", value="800 TL / 50 kg çuval")
    with col_alan:
        islem_alani = st.number_input("İşlem yapılacak toplam tarım alanı (Dekar):", min_value=1, value=100, key="islem_alani_input_5")
        
    
    if st.button("Maliyet ve Etkiyi Analiz Et", key="btn_maliyet_analiz_5"):
        if gubre_plan and gubre_fiyat and islem_alani:
            analiz_prompt = f"""
            Sen uzman bir tarım ekonomistisin. Aşağıdaki verileri kullanarak çiftçiye 3 ana başlıkta kapsamlı bir analiz sun:
            
            1. **Toplam Girdi Maliyeti Tahmini (Gübreleme):** Verilen plan ve fiyatlara göre toplam gübre maliyetini hesapla (TL ve TL/dekar cinsinden).
            2. **Çevresel Etki Özeti (Karbon ve Su):** Verilen gübre türlerinin tahmini karbon ayak izini (CO2 eşdeğeri olarak) ve tahmini su kirliliği potansiyelini özetle.
            3. **Maliyet Optimizasyonu Önerisi:** Maliyeti düşürmek veya çevresel etkiyi azaltmak için (Örn: Yaprak gübresi kullanımı, yavaş salınımlı gübreye geçiş, dozaj optimizasyonu) somut 2 adet öneri sun.

            --- GİRDİ VERİLERİ ---
            Gübreleme Planı: {gubre_plan}
            Bölge Ortalama Fiyatı: {gubre_fiyat}
            Toplam Alan: {islem_alani} Dekar
            """
            
            with st.spinner("Gemini maliyet ve çevresel etki analizi yapıyor..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        contents=analiz_prompt
                    )
                    st.success("✅ Finansal ve Çevresel Analiz Tamamlandı!")
                    st.subheader("📊 YZ'den Maliyet ve Etki Analizi")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Gemini API çağrısında bir hata oluştu: {e}")
        else:
            st.warning("Lütfen tüm analiz alanlarını doldurun.")
            
# AŞAMA 6: DESTEK VE MEVZUAT DANIŞMANLIĞI (Kullanıcı Sırası: 6)
elif st.session_state.current_step == 6:
    st.header("6. Aşama: Destek ve Mevzuat Danışmanlığı")
    st.info("Bu modül, Türkiye'deki güncel tarım destekleri ve mevzuat değişiklikleri hakkında bilgi sağlar.")
    
    konu = st.text_input("Öğrenmek istediğiniz destek/mevzuat konusunu veya ürün adını girin (Örn: Mazot ve Gübre Desteği, Sertifikalı Tohum Desteği, Zeytinlik Yasası):", key="mevzuat_konu_input_6")
    il_bilgisi = st.text_input("Hangi il/bölge için bilgi istiyorsunuz? (Bölgesel destekler değişebilir):", key="mevzuat_il_input_6")

    if st.button("Mevzuat Bilgisi Al", key="btn_mevzuat_analiz_6"):
        if konu and il_bilgisi:
            mevzuat_prompt = f"""
            Sen Türkiye Cumhuriyeti Tarım ve Orman Bakanlığı'nın mevzuatlarını ve güncel desteklerini bilen bir YZ Danışmanısın.
            Lütfen Google arama aracını kullanarak en güncel ve resmi verilere dayalı bir bilgi notu hazırla.
            Aşağıdaki bilgilere göre çiftçiye, istediği konuda bir bilgi notu hazırla. 
            Cevabın; 1) Desteğin/Mevzuatın Amacı, 2) Başvuru Şartları ve 3) Güncel Miktarı/Önemli Maddeleri başlıklarını içermelidir.
            
            --- GİRDİ VERİLERİ ---
            Konu: {konu}
            İl/Bölge: {il_bilgisi}
            """
            
            with st.spinner("Gemini, güncel destek ve mevzuatları araştırıyor..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        contents=mevzuat_prompt,
                        config={"tools": tools_config}
                    )
                    st.success("✅ Mevzuat Bilgisi Hazır!")
                    st.subheader(f"⚖️ '{konu}' Konusunda YZ Analizi")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Gemini API çağrısında bir hata oluştu: {e}")
        else:
            st.warning("Lütfen hem konu hem de il bilgisini girin.")

# AŞAMA 7: KRİTİK HAVA VE İŞLEM RİSK ANALİZİ (Kullanıcı Sırası: 4)
elif st.session_state.current_step == 7:
    st.header("4. Aşama: Hava Durumu & Kritik İşlem Riski Analizi")
    st.info("Bu modül, anlık hava durumu tahminlerini analiz ederek kritik tarımsal işlemler (Hasat, İlaçlama vb.) için risk değerlendirmesi yapar.")
    
    konum = st.text_input("Hava durumunu öğrenmek istediğiniz yer (İl/İlçe):", key="hava_konum_input_7", value="Konya Cihanbeyli")
    islem = st.radio("Yapılacak Planlı Tarımsal İşlem:", 
                     ('Hasat/Kurulama', 'İlaçlama (Fungisit/Pestisit)', 'Yoğun Sulama', 'Ekim/Hasat'), 
                     key="tarimsal_islem_radio_7")
    ek_not = st.text_input("Hasat edilecek ürün adı (Sadece Hasat seçili ise doldurun):", key="hasat_urun_kritik_7", value="Buğday")

    if st.button("Hava Durumu ve Risk Analizi Yap", key="btn_risk_analiz_7"):
        if konum:
            # İşlem Hasat ise, prompt'u daha spesifik hale getiriyoruz.
            if islem == 'Hasat/Kurulama' or islem == 'Ekim/Hasat':
                risk_prompt = f"""
                Sen Türkiye'deki tarımsal hasat riskleri konusunda uzman bir YZ'sin.
                Lütfen Google arama aracını kullanarak '{konum}' konumunun önümüzdeki 7-10 günlük hava durumu tahminini bul.
                Bulduğun verilere dayanarak, '{ek_not}' ürünü için:
                1. **Kritik Koşullar Özeti:** Hasat öncesi ve sırası için en kritik riskleri (Yağış, Aşırı Sıcaklık, Rüzgar vb.) ve günlerini belirt. Ayrıca, bu ürün için hasat sırasındaki optimum nem ve sıcaklık aralığını araştır ve belirt.
                2. **Tavsiye:** Hasatın yapılacağı en uygun 3 günlük zaman dilimini ve kesinlikle kaçınılması gereken günleri net bir şekilde tavsiye et.
                """
            else:
                # Diğer işlemler (İlaçlama, Sulama) için mevcut prompt'u kullanıyoruz.
                 risk_prompt = f"""
                Sen Türkiye'deki tarımsal hava durumu riskleri konusunda uzman bir YZ'sin.
                Lütfen Google arama aracını kullanarak '{konum}' konumunun önümüzdeki 7 günlük hava durumu tahminini bul.
                Bulduğun verilere dayanarak, '{islem}' işlemi için:
                1. **Risk Özeti:** Önümüzdeki günlerdeki en kritik riskleri (Don, Aşırı Yağış, Kuvvetli Rüzgar, Kuraklık vb.) ve günlerini belirt.
                2. **Tavsiye:** İşlemin (Ekim/İlaçlama/Sulama) yapılacağı en uygun 3 günü ve kaçınılması gereken günleri net bir şekilde tavsiye et.
                """
            
            with st.spinner("Gemini hava durumu verilerini topluyor ve risk analizi yapıyor..."):
                try:
                    # Google Search aracını doğru config ile kullanıyoruz.
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        contents=risk_prompt,
                        config={"tools": tools_config}
                    )
                    
                    st.success("✅ Hava Durumu ve Risk Analizi Tamamlandı!")
                    st.subheader("⛈️ YZ'den Hava Durumu Risk Analizi")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Gemini API çağrısında bir hata oluştu veya hava durumu verisi alınamadı: {e}")
        else:
            st.warning("Lütfen konum bilgisini girin.")

# AŞAMA 8: HASAT TAHMİNİ VE FİNANSAL STRATEJİ (Kullanıcı Sırası: 3)
elif st.session_state.current_step == 8:
    st.header("3. Aşama: Hasat Tahmini ve Finansal Strateji")
    st.info("Bu modül, verim tahmini, kâr analizi ve satış/depolama stratejileri hakkında bilgi sağlar.")
    
    urun_adi = st.text_input("Hasat edilecek ürün adı:", key="hasat_urun_input_8", value="Buğday (Makarnalık)")
    tahmini_verim = st.text_input("Tahmini verim (Örn: 500 kg/dekar):", key="hasat_verim_input_8", value="500 kg/dekar")
    
    col_tar, col_fiy = st.columns(2)
    with col_tar:
        tarla_alani = st.number_input("Toplam Tarla Alanı (Dekar):", min_value=1, value=100, key="hasat_alan_input_8")
    with col_fiy:
        girdi_maliyeti = st.number_input("Toplam Girdi Maliyeti (TL/Dekar):", min_value=0, value=2500, key="hasat_maliyet_input_8")
    
    if st.button("Kâr ve Strateji Analizi Yap", key="btn_kar_analiz_8"):
        if urun_adi and tahmini_verim and tarla_alani > 0 and girdi_maliyeti >= 0:
            hasat_prompt = f"""
            Sen Türkiye'deki tarım piyasası ve ürün depolama koşulları konusunda uzman bir Ziraat Mühendisi/Ekonomistsin.
            Aşağıdaki verilere göre çiftçiye 3 ana başlıkta kapsamlı bir analiz sun:
            
            1. **Kâr Tahmini ve Başabaş Noktası:** Google arama aracını kullanarak '{urun_adi}' ürünü için güncel piyasa fiyatlarını bul. Toplam {tarla_alani} dekar alan ve {tahmini_verim} tahmini verim ile beklenen toplam geliri ve {girdi_maliyeti} TL/dekar maliyetle beklenen tahmini net kârı (TL) hesapla. Başabaş noktası (kg/dekar) nedir?
            2. **Depolama ve Kalite Koruma:** '{urun_adi}' için uzun süreli depolama gerekiyorsa, ürünün nem oranı, sıcaklık ve havalandırma açısından optimum depolama koşulları ne olmalıdır?
            3. **Satış Stratejisi Tavsiyesi:** Güncel piyasa ve trendlere göre, ürünü hasat sonrası hemen satmak mı, yoksa 3-6 ay depolayıp daha sonra satmak mı daha mantıklı olabilir? Somut bir öneri sun.

            Cevabını Markdown formatında, net hesaplamalar ve maddelemeler ile sun.
            """
            
            with st.spinner("Gemini piyasa verilerini topluyor ve hasat stratejisi analizi yapıyor..."):
                try:
                    # Google Search aracını doğru config ile kullanıyoruz.
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        contents=hasat_prompt,
                        config={"tools": tools_config}
                    )
                    
                    st.success("✅ Kâr ve Strateji Analizi Tamamlandı!")
                    st.subheader("💰 YZ'den Finansal Analiz ve Strateji")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Gemini API çağrısında bir hata oluştu: {e}")
        else:
            st.warning("Lütfen tüm alanları doğru ve eksiksiz doldurun.")
