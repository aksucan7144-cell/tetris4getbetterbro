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

# Tetris Oyununu HTML/JS Olarak Gömüyoruz
tetris_html = """
<!DOCTYPE html>
<html>
<head>
<style>
body { background-color: #0e1117; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 10px; }
canvas { border: 3px solid #ff4b4b; background-color: #111; box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.3); display: block; margin: 0 auto; }
#stats { font-size: 18px; margin-top: 10px; font-weight: bold; }
.btn { background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; font-size: 16px; cursor: pointer; margin-top: 10px; border-radius: 5px; font-weight: bold; }
.btn:hover { background-color: #ff2222; }
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

function arenaSweep() {
    let rowCount = 1;
    outer: for (let y = arena.length - 1; y > 0; --y) {
        for (let x = 0; x < arena[y].length; ++x) {
            if (arena[y][x] === 0) { continue outer; }
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
            if (m[y][x] !== 0 && (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) { return true; }
        }
    }
    return false;
}

function createMatrix(w, h) {
    const matrix = [];
    while (h--) { matrix.push(new Array(w).fill(0)); }
    return matrix;
}

function createPiece(type) {
    if (type === 'T') return [[0, 1, 0], [1, 1, 1], [0, 0, 0]];
    if (type === 'O') return [[2, 2], [2, 2]];
    if (type === 'L') return [[0, 0, 3], [3, 3, 3], [0, 0, 0]];
    if (type === 'J') return [[4, 0, 0], [4, 4, 4], [0, 0, 0]];
    if (type === 'I') return [[0, 5, 0, 0], [0, 5, 0, 0], [0, 5, 0, 0], [0, 5, 0, 0]];
    if (type === 'S') return [[0, 6, 6], [6, 6, 0], [0, 0, 0]];
    if (type === 'Z') return [[7, 7, 0], [0, 7, 7], [0, 0, 0]];
}

function drawMatrix(matrix, offset) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                context.fillStyle = colors[value];
                context.fillRect(x + offset.x, y + offset.y, 1, 1);
            }
        });
    });
}

function draw() {
    context.fillStyle = '#000';
    context.fillRect(0, 0, canvas.width, canvas.height);
    drawMatrix(arena, {x: 0, y: 0});
    drawMatrix(player.matrix, player.pos);
}

function merge(arena, player) {
    player.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) { arena[y + player.pos.y][x + player.pos.x] = value; }
        });
    });
}

function playerDrop() {
    player.pos.y++;
    if (collide(arena, player)) {
        player.pos.y--;
        merge(arena, player);
        playerReset();
        arenaSweep();
        dropInterval = linesCleared >= 10 ? 0 : 500;
    }
    dropCounter = 0;
}

function playerMove(dir) {
    player.pos.x += dir;
    if (collide(arena, player)) { player.pos.x -= dir; }
}

function playerReset() {
    const pieces = 'TJLOSZI';
    player.matrix = createPiece(pieces[Math.floor(pieces.length * Math.random())]);
    player.pos.y = 0;
    player.pos.x = (arena[0].length / 2 | 0) - (player.matrix[0].length / 2 | 0);
    if (collide(arena, player)) {
        arena.forEach(row => row.fill(0));
        gameOver = true;
    }
}

function playerRotate(dir) {
    const posX = player.pos.x;
    let offset = 1;
    rotate(player.matrix, dir);
    while (collide(arena, player)) {
        player.pos.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > player.matrix[0].length) {
            rotate(player.matrix, -dir);
            player.pos.x = posX;
            return;
        }
    }
}

function rotate(matrix, dir) {
    for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
            let t = matrix[y][x];
            matrix[y][x] = matrix[x][y];
            matrix[x][y] = t;
        }
    }
    if (dir > 0) { matrix.forEach(row => row.reverse()); } else { matrix.reverse(); }
}

let dropCounter = 0;
let dropInterval = 500;
let lastTime = 0;
let startTime = 0;
let gameOver = true;
let linesCleared = 0;

const colors = [null, '#FF0d72', '#0dc2ff', '#0dff72', '#f538ff', '#ff8e0d', '#ffe138', '#3877ff'];
const arena = createMatrix(10, 20);
const player = {pos: {x: 0, y: 0}, matrix: null};

function update(time = 0) {
    if (gameOver) return;
    const deltaTime = time - lastTime;
    lastTime = time;
    dropCounter += deltaTime;
    if (dropCounter > dropInterval) { playerDrop(); }
    document.getElementById('time').innerText = ((Date.now() - startTime) / 1000).toFixed(1);
    draw();
    animationId = requestAnimationFrame(update);
}

function resetGame() {
    arena.forEach(row => row.fill(0));
    playerReset();
    linesCleared = 0;
    document.getElementById('lines').innerText = 0;
    startTime = Date.now();
    gameOver = false;
    lastTime = performance.now();
    cancelAnimationFrame(animationId);
    update();
}

let animationId;
document.addEventListener('keydown', event => {
    if
