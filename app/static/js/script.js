const aiModal = new bootstrap.Modal(document.getElementById('aiModal'));

async function updateDashboard() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        const tbody = document.getElementById('news-table-body');
        
        tbody.innerHTML = data.news.map(n => `
            <tr>
                <td class="small" style="color: #999;">${n.published_date}</td>
                <td>
                    <span class="critical-badge ${n.criticality.includes('🔴') ? 'badge-red' : 'badge-green'}">
                        ${n.criticality}
                    </span>
                </td>
                <td class="fw-bold text-white">${n.title}</td>
                <td class="text-end">
                    <button class="btn btn-ai btn-sm me-2" onclick="getSupport('${n.title}')">AI DESTEK</button>
                    <a href="${n.link}" target="_blank" class="btn btn-sm btn-outline-secondary">GİT</a>
                </td>
            </tr>
        `).join('');
    } catch (e) { console.error("Veri hatası:", e); }
}

async function runTool(type) {
    const val = document.getElementById('toolInput').value;
    const resDiv = document.getElementById('toolResult');
    const outDiv = document.getElementById('aiOutput');
    if(!val) return;
    
    resDiv.style.display = "block";
    outDiv.innerHTML = 'İşleniyor...';
    
    const response = await fetch('/api/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: type, value: val })
    });
    const data = await response.json();
    outDiv.innerText = data.result;
}

async function getSupport(title) {
    document.getElementById('aiModalTitle').innerText = title;
    document.getElementById('modalAiBody').innerHTML = '<div class="text-center p-4"><div class="spinner-border text-info"></div><br>Analiz ediliyor...</div>';
    aiModal.show();

    const response = await fetch('/api/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'CVE', value: title })
    });
    const data = await response.json();
    document.getElementById('modalAiBody').innerText = data.result;
}

document.addEventListener('DOMContentLoaded', () => {
    updateDashboard();
    setInterval(updateDashboard, 60000);
});
