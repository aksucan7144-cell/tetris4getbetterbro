import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="Tetris 10-Line Sprint & AI Coach", page_icon="🕹️", layout="wide")

st.title("🕹️ Jstris Style 10-Line Sprint & AI Koçu")
st.markdown("10 satırı en kısa sürede temizle, istatistiklerini al ve yapay zeka e-spor koçundan profesyonel analiz kap!")

# Kenar Çubuğu (API Anahtarı)
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Lütfen devam etmek için kenar çubuğundan Groq API anahtarınızı girin.")
    st.stop()

client = Groq(api_key=api_key)

# HTML dosyasını harici okuyoruz (Sıfır Syntax Hatası)
try:
    with open("tetris.html", "r", encoding="utf-8") as f:
        tetris_html = f.read()
    st.components.v1.html(tetris_html, height=530)
except Exception as e:
    st.error(f"tetris.html okunamadı: {e}")

st.markdown("---")
st.subheader("🧠 Yapay Zeka E-Spor Koçu Analizi")
st.markdown("Maçını bitirdikten sonra süreni ve yaptığın hataları aşağıya yaz, koç seni acımasızca analiz etsin!")

with st.form(key="coach_form"):
    match_stats = st.text_area(
        "Maç İstatistiklerin / Notların:", 
        placeholder="Örn: 10 satırı 22 saniyede bitirdim, A ve D yağ gibi kayıyor..."
    )
    analyze_button = st.form_submit_button("🏆 Koçtan Analiz Al", use_container_width=True)

if analyze_button and match_stats.strip() != "":
    with st.spinner("Koç replikleri hazırlıyor, veriler inceleniyor..."):
        prompt = f"""
        Sen sert, disiplinli, profesyonel bir e-spor Tetris koçusun. Oyuncunun 10 line sprint maçı sonrasında verdiği istatistikler/notlar şunlar:
        "{match_stats}"
        
        Oyuncuya profesyonel bir koç gibi yaklaş; yaptığı hataları yüzüne vur, süre kasması için net taktikler ver, parça yerleşimi hakkında tavsiyelerde bulun. Samimi, enerjik ama otoriter bir e-spor dili kullan.
        """
        
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-20b",
            )
            coach_reply = response.choices[0].message.content
            
            st.success("Koç raporu onayladı!")
            st.markdown(f"### 🎙️ Koçun Değerlendirmesi:\n\n{coach_reply}")
        except Exception as e:
            st.error(f"Analiz sırasında bir hata oluştu: {e}")
