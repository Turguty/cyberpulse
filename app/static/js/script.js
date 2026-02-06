const aiModal = new bootstrap.Modal(document.getElementById('aiModal'));

async function updateDashboard() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        const tbody = document.getElementById('news-table-body');
        
        tbody.innerHTML = data.news.map(n => {
            const isCritical = n.criticality.includes('🔴');
            const badgeClass = isCritical ? 'badge-critical' : 'badge-low';
            
            return `
            <tr>
                <td data-label="Zaman" class="small text-muted">${n.published_date}</td>
                <td data-label="Risk">
                    <span class="${badgeClass}">${n.criticality}</span>
                </td>
                <td data-label="Başlık" class="fw-bold text-white">${n.title}</td>
                <td data-label="İşlem" class="text-end">
                    <div class="d-flex justify-content-end gap-2">
                        <button class="btn btn-ai-support btn-sm" onclick="getSupport('${n.title}')">AI DESTEK</button>
                        <a href="${n.link}" target="_blank" class="btn btn-sm btn-outline-secondary">GİT</a>
                    </div>
                </td>
            </tr>
            `;
        }).join('');
    } catch (e) {
        console.error("Dashboard güncellenemedi:", e);
    }
}

async function runTool(type) {
    const val = document.getElementById('toolInput').value;
    const resDiv = document.getElementById('toolResult');
    const outDiv = document.getElementById('aiOutput');
    if(!val) return;
    
    resDiv.style.display = "block";
    outDiv.innerHTML = '<div class="spinner-border spinner-border-sm"></div> Analiz ediliyor...';
    
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
    document.getElementById('modalAiBody').innerHTML = '<div class="text-center p-5"><div class="spinner-border text-info"></div><br><br>SOC Analistleri (Mistral & Llama) raporluyor...</div>';
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
