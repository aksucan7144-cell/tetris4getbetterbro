import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="Tetris 10-Line Sprint & AI Coach", page_icon="🕹️", layout="wide")

st.title("🕹️ Jstris Style 10-Line Sprint & AI Koçu")

# Oyun başlamadan önce cihaz seçimi
device_choice = st.radio(
    "📱 Hangi cihazdan oynuyorsun?",
    ("Masaüstü (PC)", "Mobil (Telefon / Tablet)"),
    horizontal=True
)

is_mobile = "Mobil" in device_choice

client = None
ai_choice = None

if not is_mobile:
    ai_choice = st.radio(
        "🤖 AI yardımı ister misin?",
        ("Hayır (Normal Tetris)", "Evet (AI E-Spor Koçu)"),
        horizontal=True
    )
    st.caption("(Seçersen API isteyecek, seçmezsek normal Tetris oynayacaksın)")
    
    if "Evet" in ai_choice:
        api_key = st.sidebar.text_input("Groq API Key", type="password")
        if api_key:
            client = Groq(api_key=api_key)
        else:
            st.sidebar.warning("AI analizi için kenar çubuğundan Groq API anahtarınızı girin.")
else:
    st.info("📱 Mobil mod aktif: Dokunmatik kontrol butonları etkinleştirildi, AI desteği gizlendi.")

# tetris.html dosyasını okuyup mobil mod bayrağını (flag) Python ile enjekte ediyoruz
try:
    with open("tetris.html", "r", encoding="utf-8") as f:
        tetris_html = f.read()
    
    # Mobil durumu JavaScript tarafına aktarılıyor
    mobile_flag = "true" if is_mobile else "false"
    tetris_html = tetris_html.replace("const IS_MOBILE = false;", f"const IS_MOBILE = {mobile_flag};")
    
    # Mobilde butonlar için iframe yüksekliğini biraz daha fazla veriyoruz
    iframe_height = 720 if is_mobile else 530
    st.components.v1.html(tetris_html, height=iframe_height)
except Exception as e:
    st.error(f"tetris.html okunamadı: {e}")

# Sadece Masaüstü ve AI seçildiyse koç analiz formu görünür
if not is_mobile and ai_choice and "Evet" in ai_choice:
    st.markdown("---")
    st.subheader("🧠 Yapay Zeka E-Spor Koçu Analizi")
    st.markdown("Maçını bitirdikten sonra süreni ve yaptığın hataları aşağıya yaz, koç seni acımasızca analiz etsin!")

    with st.form(key="coach_form"):
        match_stats = st.text_area(
            "Maç İstatistiklerin / Notların:", 
            placeholder="Örn: 10 satırı 22 saniyede bitirdim..."
        )
        analyze_button = st.form_submit_button("🏆 Koçtan Analiz Al", use_container_width=True)

    if analyze_button and match_stats.strip() != "":
        if client:
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
        else:
            st.warning("Lütfen sol kenar çubuğundan Groq API anahtarınızı girin.")
