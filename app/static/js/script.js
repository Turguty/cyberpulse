async function loadNews() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        const body = document.getElementById('news-table-body');
        if (!body) return;
        
        body.innerHTML = '';
        data.news.forEach(item => {
            body.innerHTML += `
                <tr>
                    <td class="time-cell">${item.published_date}</td>
                    <td><a href="${item.link}" target="_blank" class="news-link">${item.title}</a></td>
                    <td><span class="badge bg-secondary">${item.criticality}</span></td>
                    <td>
                        <a href="${item.link}" target="_blank" class="btn btn-outline-primary btn-sm source-btn">
                            Kaynağa Git
                        </a>
                    </td>
                </tr>`;
        });
    } catch (e) {
        console.error("Haberler yüklenemedi:", e);
    }
}

async function analyzeWithAI(title) {
    const resultDiv = document.getElementById('tool-result');
    resultDiv.classList.remove('d-none');
    resultDiv.innerText = "AI Haberi Analiz Ediyor...";
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Sonucu görmesi için yukarı kaydır

    try {
        const res = await fetch('/api/ai-analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title: title})
        });
        const data = await res.json();
        resultDiv.innerText = data.result;
    } catch (e) { resultDiv.innerText = "AI Analizi başarısız."; }
}

async function runTool(type) {
    const val = document.getElementById('tool-input').value;
    const resultDiv = document.getElementById('tool-result');
    
    if(!val) {
        alert("Lütfen bir CVE kodu veya IP adresi girin!");
        return;
    }
    
    resultDiv.classList.remove('d-none');
    resultDiv.innerText = "Analiz ediliyor...";

    try {
        const res = await fetch('/api/tool', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type: type, value: val})
        });
        const data = await res.json();
        resultDiv.innerText = data.result;
    } catch (e) {
        resultDiv.innerText = "Hata: Sunucu ile iletişim kurulamadı.";
    }
}

document.addEventListener('DOMContentLoaded', loadNews);
// Her 2 dakikada bir otomatik yenile
setInterval(loadNews, 120000);
