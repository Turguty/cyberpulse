async function loadNews() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        const body = document.getElementById('news-table-body');
        body.innerHTML = '';

        data.news.forEach(item => {
            // Tarihi mobilde çok yer kaplamaması için biraz kısaltalım
            // Örn: "Sat, 07 Feb 2026 01:21:00 GMT" -> "Sat, 07 Feb 2026"
            const displayDate = item.published_date.split(' ').slice(0, 4).join(' ');

            const row = `
                <tr>
                    <td class="time-cell">${displayDate}</td>
                    <td><a href="${item.link}" target="_blank" class="news-link">${item.title}</a></td>
                    <td><span class="badge bg-secondary" style="font-size: 0.7rem;">${item.criticality}</span></td>
                </tr>`;
            body.innerHTML += row;
        });
    } catch (e) {
        console.error("Haberler yüklenirken hata oluştu:", e);
    }
}

async function runTool(type) {
    const val = document.getElementById('tool-input').value;
    const resultDiv = document.getElementById('tool-result');
    
    if(!val) {
        alert("Lütfen bir CVE kodu veya IP adresi girin!");
        return;
    }
    
    resultDiv.classList.remove('d-none');
    resultDiv.innerText = "Sorgulanıyor...";

    try {
        const res = await fetch('/api/tool', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type: type, value: val})
        });
        const data = await res.json();
        resultDiv.innerText = data.result;
    } catch (e) {
        resultDiv.innerText = "Sorgu sırasında bir bağlantı hatası oluştu.";
    }
}

// Sayfa açıldığında ve her 60 saniyede bir haberleri yenile
document.addEventListener('DOMContentLoaded', () => {
    loadNews();
    setInterval(loadNews, 60000);
});
