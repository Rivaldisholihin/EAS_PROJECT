let autoRetryTimer = null;

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("compute-btn").onclick = computeRoute;
    document.getElementById("reset-btn").onclick = resetForm;
});

window.onload = () => {
    window.finalPath = [];
    window.crowdedData = {};
    drawMap();
};

async function computeRoute() {

    const selected = Array.from(
        document.querySelectorAll('input[type="checkbox"]:checked')
    ).map(cb => cb.value);

    if (selected.length === 0) {
        alert("Pilih minimal satu kategori!");
        return;
    }

    const algorithm = document.getElementById("algorithm-select").value;
    if (!algorithm) {
        alert("Pilih algoritma terlebih dahulu!");
        return;
    }

    const resultEl = document.getElementById("result");
    const stepsEl = document.getElementById("steps");
    const distanceEl = document.getElementById("distance");

    resultEl.style.display = "block";
    stepsEl.innerHTML = "<li>Menghitung rute...</li>";
    distanceEl.textContent = "Menghitung...";

    try {
        const res = await fetch("/compute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                categories: selected,
                algorithm: algorithm,
            }),
        });

        const data = await res.json();

        if (data.waiting) {
            stepsEl.innerHTML = `
                <li>
                    Menunggu sampai keramaian di 
                    <b>${data.node}</b> turun...
                    (level: ${data.crowded})
                </li>
                <li>Update otomatis…</li>
            `;
            distanceEl.textContent = "-";

            if (!autoRetryTimer) {
                autoRetryTimer = setInterval(() => {
                    computeRoute();
                }, 3000);
            }

            return;
        }

        if (autoRetryTimer) {
            clearInterval(autoRetryTimer);
            autoRetryTimer = null;
        }

        window.finalPath = data.route || [];
        drawMap();

        distanceEl.textContent = `${data.distance}`;
        stepsEl.innerHTML = "";

        if (!data.steps || data.steps.length === 0) {
            stepsEl.innerHTML = "<li>Tidak ditemukan rute.</li>";
        } else {
            data.steps.forEach(step => {
                const li = document.createElement("li");
                li.textContent = step;
                stepsEl.appendChild(li);
            });
        }

    } catch (err) {
        console.error(err);
        alert("Terjadi kesalahan saat menghitung rute.");
    }
}



function resetForm() {

    if (autoRetryTimer) {
        clearInterval(autoRetryTimer);
        autoRetryTimer = null;
    }

    document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);

    document.getElementById("result").style.display = "none";
    document.getElementById("steps").innerHTML = "";
    document.getElementById("distance").textContent = "0";

    window.finalPath = [];
    drawMap();
}


function handleCrowdedStatusUpdate(event) {
    window.crowdedData = JSON.parse(event.data);
    drawMap();
}

const eventSource = new EventSource("/sse");
eventSource.onmessage = handleCrowdedStatusUpdate;



function drawMap() {
    const canvas = document.getElementById("mapCanvas");
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const scale = 40;
    const offsetX = 50;
    const offsetY = 50;

    const graph = window.graph;
    const coords = window.coords;
    const path = window.finalPath || [];

    for (const [node, neighbors] of Object.entries(graph)) {
        const [x1, y1] = coords[node];

        neighbors.forEach(nbObj => {
            const nb = Array.isArray(nbObj) ? nbObj[0] : nbObj.node;
            const [x2, y2] = coords[nb];

            const pathEdges = new Set();
            for (let i = 0; i < path.length - 1; i++) {
                pathEdges.add(`${path[i]}-${path[i+1]}`);
                pathEdges.add(`${path[i+1]}-${path[i]}`);
            }

            const isOnPath = pathEdges.has(`${node}-${nb}`);

            ctx.beginPath();
            ctx.moveTo(x1 * scale + offsetX, y1 * scale + offsetY);
            ctx.lineTo(x2 * scale + offsetX, y2 * scale + offsetY);

            ctx.strokeStyle = isOnPath ? "limegreen" : "#000";
            ctx.lineWidth = isOnPath ? 4 : 2;
            ctx.stroke();
        });
    }

    for (const [name, [x, y]] of Object.entries(coords)) {

        const px = x * scale + offsetX;
        const py = y * scale + offsetY;

        ctx.beginPath();
        ctx.arc(px, py, 6, 0, Math.PI * 2);
        ctx.fillStyle = "#00eaff";
        ctx.fill();

        if (path.includes(name)) {
            ctx.strokeStyle = "limegreen";
            ctx.lineWidth = 4;
        } else {
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
        }
        ctx.stroke();

        ctx.fillStyle = "red";
        ctx.font = "14px Arial";
        ctx.fillText(name, px - ctx.measureText(name).width / 2, py - 12);

        const crowdedValue = window.crowdedData[name] ?? 0;

        let color = "green";
        if (crowdedValue >= 7) color = "red";
        else if (crowdedValue >= 5) color = "orange";
        else if (crowdedValue >= 3) color = "yellow";

        ctx.fillStyle = color;
        ctx.font = "12px Arial";
        ctx.fillText(`${crowdedValue}`, px - ctx.measureText(`${crowdedValue}`).width / 2, py + 20);
    }
}
