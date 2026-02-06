async function loadNews() {
    const res = await fetch('/api/data');
    const data = await res.json();
    const body = document.getElementById('news-table-body');
    body.innerHTML = '';
    
    data.news.forEach(item => {
        body.innerHTML += `
            <tr>
                <td class="time-cell">${item.published_date}</td>
                <td><a href="${item.link}" target="_blank" class="news-link">${item.title}</a></td>
                <td><span class="badge bg-secondary">${item.criticality}</span></td>
            </tr>`;
    });
}

async function runTool(type) {
    const val = document.getElementById('tool-input').value;
    if(!val) return;
    const res = await fetch('/api/tool', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type: type, value: val})
    });
    const data = await res.json();
    document.getElementById('tool-result').innerText = data.result;
    document.getElementById('tool-result').classList.remove('d-none');
}

document.addEventListener('DOMContentLoaded', loadNews);
