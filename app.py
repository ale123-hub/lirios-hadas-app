import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Lirios Amarillos y Hadas de Luz", layout="centered")

st.markdown("<h1 style='text-align: center;'>✨ Lirios Amarillos y Hadas de Luz</h1>", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        background-color: #0a0f23;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }
    canvas {
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
</style>
</head>
<body>
<canvas id="canvas" width="800" height="600"></canvas>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const WIDTH = 800;
const HEIGHT = 600;

// Estrellas
const stars = [];
for(let i = 0; i < 80; i++) {
    stars.push({
        x: Math.random() * WIDTH,
        y: Math.random() * 350,
        size: Math.random() * 1.5 + 0.5
    });
}

// Césped
const grassBlades = [];
for(let x = 0; x < WIDTH; x += 4) {
    grassBlades.push({
        x: x,
        height: Math.random() * 30 + 15,
        bend: (Math.random() - 0.5) * 0.6,
        phase: Math.random() * Math.PI * 2
    });
}

// Lirios
const lilyPositions = [
    [120, 580, 160, 0.75],
    [220, 585, 210, 0.95],
    [340, 595, 240, 1.1],
    [450, 580, 180, 0.85],
    [560, 600, 260, 1.2],
    [670, 585, 200, 0.9],
    [740, 575, 150, 0.7]
];

// Hadas
class Fairy {
    constructor(x, y) {
        this.baseX = x;
        this.baseY = y;
        this.x = x;
        this.y = y;
        this.size = Math.random() * 3 + 2;
        this.speed = Math.random() * 0.03 + 0.02;
        this.angle = Math.random() * Math.PI * 2;
        this.radius = Math.random() * 25 + 15;
        this.alpha = Math.random();
    }

    update() {
        this.angle += this.speed;
        this.x = this.baseX + Math.cos(this.angle) * this.radius + Math.sin(this.angle * 2) * 10;
        this.y = this.baseY + Math.sin(this.angle) * this.radius + Math.cos(this.angle * 1.5) * 10;
        this.alpha = 0.5 + 0.5 * Math.sin(this.angle * 3);
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        
        let grad = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 3);
        grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        grad.addColorStop(0.4, 'rgba(255, 235, 150, 0.8)');
        grad.addColorStop(1, 'rgba(255, 235, 150, 0)');
        
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

const fairies = [];
lilyPositions.forEach(pos => {
    let flowerTopY = pos[1] - pos[2];
    for(let i = 0; i < 10; i++) {
        fairies.push(new Fairy(pos[0] + (Math.random() - 0.5) * 50, flowerTopY + (Math.random() - 0.5) * 50));
    }
});

function drawMoon() {
    let glow = ctx.createRadialGradient(650, 120, 30, 650, 120, 90);
    glow.addColorStop(0, 'rgba(245, 245, 230, 0.8)');
    glow.addColorStop(1, 'rgba(245, 245, 230, 0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(650, 120, 90, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#f5f5e6';
    ctx.beginPath();
    ctx.arc(650, 120, 45, 0, Math.PI * 2);
    ctx.fill();
}

function drawGrass(time) {
    ctx.fillStyle = '#00230a';
    ctx.beginPath();
    ctx.ellipse(400, 600, 500, 100, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#004614';
    ctx.beginPath();
    ctx.ellipse(400, 610, 450, 80, 0, 0, Math.PI * 2);
    ctx.fill();

    grassBlades.forEach((blade, i) => {
        let wind = Math.sin(time * 0.002 + blade.phase) * 6;
        let topX = blade.x + blade.bend * 10 + wind;
        let topY = HEIGHT - blade.height;

        ctx.strokeStyle = (i % 2 === 0) ? '#228b22' : '#004614';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(blade.x, HEIGHT);
        ctx.lineTo(topX, topY);
        ctx.stroke();
    });
}

function drawLily(x, baseY, height, scale, time) {
    let flowerTopY = baseY - height;
    let controlX = x + Math.sin(time * 0.001) * 10;

    // Tallo curvo meciéndose
    ctx.strokeStyle = '#228b22';
    ctx.lineWidth = Math.max(2, 6 * scale);
    ctx.beginPath();
    ctx.moveTo(x, baseY);
    ctx.quadraticCurveTo(controlX, baseY - height / 2, x, flowerTopY);
    ctx.stroke();

    // Hojas del tallo
    ctx.strokeStyle = '#004614';
    ctx.lineWidth = Math.max(1, 4 * scale);
    
    ctx.beginPath();
    ctx.arc(x - 40 * scale, baseY - 80 * scale, 50 * scale, 0, Math.PI / 2);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.arc(x - 10 * scale, baseY - 110 * scale, 50 * scale, Math.PI / 2, Math.PI);
    ctx.stroke();

    // Pétalos estilo Pygame (Polygon cuadrático)
    let petalAngleStep = Math.PI / 3;
    ctx.fillStyle = '#ffd700'; // Amarillo
    ctx.strokeStyle = '#daa520'; // Borde dorado
    ctx.lineWidth = 1;

    for (let i = 0; i < 6; i++) {
        let angle = i * petalAngleStep - Math.PI / 2;
        let px = x + Math.cos(angle) * (45 * scale);
        let py = flowerTopY + Math.sin(angle) * (55 * scale);

        let ctrl1X = x + Math.cos(angle - 0.4) * (25 * scale);
        let ctrl1Y = flowerTopY + Math.sin(angle - 0.4) * (25 * scale);
        let ctrl2X = x + Math.cos(angle + 0.4) * (25 * scale);
        let ctrl2Y = flowerTopY + Math.sin(angle + 0.4) * (25 * scale);

        ctx.beginPath();
        ctx.moveTo(x, flowerTopY);
        ctx.lineTo(ctrl1X, ctrl1Y);
        ctx.lineTo(px, py);
        ctx.lineTo(ctrl2X, ctrl2Y);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    }

    // Centro del lirio
    ctx.fillStyle = '#ffa500';
    ctx.beginPath();
    ctx.arc(x, flowerTopY, Math.max(3, 8 * scale), 0, Math.PI * 2);
    ctx.fill();

    // Pistilos y anteras
    for (let i = 0; i < 5; i++) {
        let stamenAngle = i * (Math.PI / 2.5) - Math.PI / 1.2;
        let stX = x + Math.cos(stamenAngle) * (18 * scale);
        let stY = flowerTopY + Math.sin(stamenAngle) * (18 * scale);

        ctx.strokeStyle = '#ffa500';
        ctx.lineWidth = Math.max(1, 2 * scale);
        ctx.beginPath();
        ctx.moveTo(x, flowerTopY);
        ctx.lineTo(stX, stY);
        ctx.stroke();

        ctx.fillStyle = '#8b4513';
        ctx.beginPath();
        ctx.arc(stX, stY, Math.max(2, 3 * scale), 0, Math.PI * 2);
        ctx.fill();
    }
}

let startTime = Date.now();

function animate() {
    let time = Date.now() - startTime;

    ctx.fillStyle = '#0a0f23';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    ctx.fillStyle = '#ffffff';
    stars.forEach(s => {
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
        ctx.fill();
    });

    drawMoon();
    drawGrass(time);

    lilyPositions.forEach(pos => {
        drawLily(pos[0], pos[1], pos[2], pos[3], time);
    });

    fairies.forEach(f => {
        f.update();
        f.draw();
    });

    requestAnimationFrame(animate);
}

animate();
</script>
</body>
</html>
"""

components.html(html_code, height=620)