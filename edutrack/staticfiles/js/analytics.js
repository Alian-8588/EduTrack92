document.addEventListener('DOMContentLoaded', async () => {
    const res = await authorizedFetch('/api/analytics/data/');
    const data = await res.json();

    // 渲染总结
    const summary = document.getElementById('summary');
    summary.innerText = `学习总时长：${data.total_hours} 小时，推荐课程数：${data.recommended}`;

    const labels = data.courses.map(c => c.course);
    const progresses = data.courses.map(c => c.progress);

    renderBarChart(labels, progresses);
    renderPieChart(labels, progresses);
});

function renderBarChart(labels, data) {
    const ctx = document.getElementById('progressChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '各课程进度 (%)',
                data: data,
                borderWidth: 1,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function renderPieChart(labels, data) {
    const ctx = document.getElementById('pieChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: '课程占比',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)'
                ],
            }]
        }
    });
}

// 授权封装
async function authorizedFetch(url, options = {}) {
    let token = localStorage.getItem('access');
    if (!options.headers) options.headers = {};
    options.headers['Authorization'] = `Bearer ${token}`;

    let response = await fetch(url, options);
    if (response.status === 401) {
        const refreshed = await refreshToken();
        if (refreshed) {
            token = localStorage.getItem('access');
            options.headers['Authorization'] = `Bearer ${token}`;
            response = await fetch(url, options);
        } else {
            alert("登录过期，请重新登录。");
            window.location.href = '/login';
        }
    }
    return response;
}

async function refreshToken() {
    const refresh = localStorage.getItem('refresh');
    if (!refresh) return false;

    const res = await fetch('/api/token/refresh/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({refresh})
    });

    if (res.ok) {
        const data = await res.json();
        localStorage.setItem('access', data.access);
        return true;
    } else {
        return false;
    }
}
