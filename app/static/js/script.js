async function loadNews() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        const body = document.getElementById('news-table-body');
        if (!body) return;
        
        body.innerHTML = '';
        data.news.forEach(item => {
            // Başlıktaki tırnak işaretleri JS fonksiyonunu bozmasın diye temizliyoruz
            const safeTitle = item.title.replace(/'/g, "\\'").replace(/"/g, '&quot;');
            
            body.innerHTML += `
                <tr>
                    <td class="time-cell">${item.published_date}</td>
                    <td><a href="${item.link}" target="_blank" class="news-link">${item.title}</a></td>
                    <td><span class="badge bg-secondary">${item.criticality}</span></td>
                    <td>
                        <div class="d-flex gap-2">
                            <a href="${item.link}" target="_blank" class="btn btn-outline-primary btn-sm source-btn">Git</a>
                            <button onclick="analyzeWithAI('${safeTitle}')" class="btn btn-outline-warning btn-sm ai-btn">AI</button>
                        </div>
                    </td>
                </tr>`;
        });
    } catch (e) {
        console.error("Haberler yüklenirken bir hata oluştu:", e);
    }
}

async function analyzeWithAI(title) {
    const resultDiv = document.getElementById('tool-result');
    resultDiv.classList.remove('d-none');
    resultDiv.innerText = "🤖 Mistral AI haberi analiz ediyor, lütfen bekleyin...";
    
    // Kullanıcıyı yukarıdaki analiz kutusuna yönlendir
    window.scrollTo({ top: 0, behavior: 'smooth' });

    try {
        const res = await fetch('/api/ai-analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ title: title })
        });
        const data = await res.json();
        resultDiv.innerText = data.result;
    } catch (e) {
        resultDiv.innerText = "❌ AI Analizi başarısız oldu. API anahtarınızı ve bağlantınızı kontrol edin.";
    }
}

async function runTool(type) {
    const val = document.getElementById('tool-input').value;
    const resultDiv = document.getElementById('tool-result');
    if(!val) return;
    resultDiv.classList.remove('d-none');
    resultDiv.innerText = "🔍 Sorgulanıyor...";
    try {
        const res = await fetch('/api/tool', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type: type, value: val})
        });
        const data = await res.json();
        resultDiv.innerText = data.result;
    } catch (e) {
        resultDiv.innerText = "Hata: Sorgu tamamlanamadı.";
    }
}

document.addEventListener('DOMContentLoaded', loadNews);
