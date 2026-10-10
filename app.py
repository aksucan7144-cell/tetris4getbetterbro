import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="Tetris 10-Line Sprint & AI Coach", page_icon="🕹️", layout="wide")

st.title("🕹️ Tetris 10-Line Sprint & AI Koçu")
st.markdown("10 satırı en kısa sürede temizle, istatistiklerini al ve yapay zeka e-spor koçundan profesyonel analiz kap!")

# Kenar Çubuğu (API Anahtarı)
st.sidebar.header("⚙️ Konfigürasyon")
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Lütfen devam etmek için kenar çubuğundan Groq API anahtarınızı girin.")
    st.stop()

client = Groq(api_key=api_key)

# Tetris Oyununu HTML/JS olarak arayüze gömüyoruz
tetris_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #0e1117;
            color: white;
            font-family: sans-serif;
            text-align: center;
            margin: 0;
            padding: 10px;
        }
        canvas {
            border: 3px solid #ff4b4b;
            background-color: #111;
            box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.3);
            display: block;
            margin: 0 auto;
        }
        #stats {
            font-size: 18px;
            margin-top: 10px;
            font-weight: bold;
        }
        .btn {
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .btn:hover {
            background-color: #ff2222;
        }
    </style>
</head>
<body>
    <h3>Tetris 10-Line Sprint (Yön Tuşları ile Oyna)</h3>
    <canvas id="tetris" width="200" height="400"></canvas>
    <div id="stats">Temizlenen Satır: <span id="lines">0</span>/10 | Süre: <span id="time">0.0</span>s</div>
    <button class="btn" onclick="resetGame()">Oyunu Başlat / Sıfırla</button>

    <script>
        const canvas = document.getElementById('tetris');
        const context = canvas.getContext('2d');
        context.scale(20, 20);

        const matrix = [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0],
        ];

        function arenaSweep() {
            let rowCount = 1;
            outer: for (let y = arena.length - 1; y > 0; --y) {
                for (let x = 0; x < arena[y].length; ++x) {
                    if (arena[y][x] === 0) {
                        continue outer;
                    }
                }
                const row = arena.splice(y, 1)[0].fill(0);
                arena.unshift(row);
                ++y;
                linesCleared++;
                document.getElementById('lines').innerText = linesCleared;
                
                if (linesCleared >= 10 && !gameOver) {
                    gameOver = true;
                    cancelAnimationFrame(animationId);
                    alert("Tebrikler! 10 satırı tamamladın. Süre: " + ((Date.now() - startTime)/1000).toFixed(1) + " saniye.");
                }
            }
        }

        function collide(arena, player) {
            const m = player.matrix;
            const o = player.pos;
            for (let y = 0; y < m.length; ++y) {
                for (let x = 0; x < m[y].length; ++x) {
                    if (m[y][x] !== 0 &&
                       (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) {
                        return true;
                    }
                }
            }
            return false;
        }

        function createMatrix(w, h) {
            const matrix = [];
            while (h--) {
                matrix.push(new Array(w).
