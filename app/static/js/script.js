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
                    <td><a href="${item.link}" target="_blank" class="btn btn-outline-primary btn-sm source-btn">Kaynağa Git</a></td>
                </tr>`;
        });
    } catch (e) { console.error("Hata:", e); }
}

async function runTool(type) {
    const val = document.getElementById('tool-input').value;
    const resultDiv = document.getElementById('tool-result');
    if(!val) return;
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
    } catch (e) { resultDiv.innerText = "Hata oluştu."; }
}
document.addEventListener('DOMContentLoaded', loadNews);
