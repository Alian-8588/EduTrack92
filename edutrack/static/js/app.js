document.addEventListener('DOMContentLoaded', function () {
    loadCourseOptions();
    loadGoals();
    loadStudyGroups();
});

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.slice(name.length + 1));
        }
    }
    return '';
}

async function authorizedFetch(url, options = {}) {
    const csrfToken = getCSRFToken();

    if (!options.headers) {
        options.headers = {};
    }

    // 对非GET请求加CSRF Token和Content-Type
    if (!options.method || options.method.toUpperCase() !== 'GET') {
        options.headers['X-CSRFToken'] = csrfToken;
        if (!options.headers['Content-Type']) {
            options.headers['Content-Type'] = 'application/json';
        }
    }

    // 确保发送 cookie
    options.credentials = 'same-origin';

    const response = await fetch(url, options);

    if (response.status === 403) {
        alert("Forbidden: You might be logged out or CSRF token missing.");
    }

    return response;
}

async function loadStudyGroups() {
    const allList = document.getElementById('all-groups');
    const joinedList = document.getElementById('joined-groups');
    if (!allList || !joinedList) return;

    const res = await authorizedFetch('/api/community/groups/');
    const groups = await res.json();

    allList.innerHTML = '';
    joinedList.innerHTML = '';

    groups.forEach(group => {
        const item = document.createElement('li');
        item.className = 'list-group-item d-flex justify-content-between align-items-center';

        const textSpan = document.createElement('span');
        textSpan.textContent = `📘 ${group.course_title}`;

        const btn = document.createElement('button');
        btn.className = 'btn btn-sm';

        if (group.is_member) {
            btn.textContent = 'Leave';
            btn.classList.add('btn-danger');
            btn.onclick = () => toggleGroupMembership(group.id, 'leave');
            item.appendChild(textSpan);
            item.appendChild(btn);
            joinedList.appendChild(item);
        } else {
            btn.textContent = 'Join';
            btn.classList.add('btn-success');
            btn.onclick = () => toggleGroupMembership(group.id, 'join');
            item.appendChild(textSpan);
            item.appendChild(btn);
            allList.appendChild(item);
        }
    });
}

async function toggleGroupMembership(groupId, action) {
    const res = await authorizedFetch(`/api/community/groups/${groupId}/${action}/`, {
        method: 'POST'
    });
    const data = await res.json();
    if (res.ok) {
        alert(data.detail || 'Operation successful.');
        loadStudyGroups();
    } else {
        alert(data.detail || 'Operation failed.');
    }
}

async function loadCourseOptions() {
    const select = document.getElementById('goal-course');
    if (!select) return;

    const res = await authorizedFetch('/api/courses/courses/');
    const data = await res.json();

    select.innerHTML = '<option value="">Select a course...</option>';
    data.forEach(course => {
        const option = document.createElement('option');
        option.value = course.id;
        option.textContent = `${course.title} (${course.instructor})`;
        option.title = option.textContent;
        select.appendChild(option);
    });
}

async function loadGoals() {
    const list = document.getElementById('goal-list');
    if (!list) return;

    const res = await authorizedFetch('/api/courses/goals/');
    const data = await res.json();

    list.innerHTML = '';
    data.forEach(goal => {
        const item = document.createElement('li');
        item.className = 'list-group-item d-flex justify-content-between align-items-center';

        const textSpan = document.createElement('span');
        textSpan.textContent = `${goal.id} - ${goal.course_title} - Progress: ${goal.progress}%`;

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Stop Learning';
        deleteBtn.className = 'btn btn-sm btn-danger';
        deleteBtn.onclick = () => deleteGoal(goal.id);

        item.appendChild(textSpan);
        item.appendChild(deleteBtn);
        list.appendChild(item);
    });
}

async function deleteGoal(goalId) {
    if (!confirm('Are you sure you want to stop this learning goal?')) return;

    const res = await authorizedFetch(`/api/courses/goals/${goalId}/`, {
        method: 'DELETE'
    });

    if (res.ok) {
        alert('Learning goal stopped successfully.');
        loadGoals();
    } else {
        const result = await res.json();
        alert(result.detail || 'Failed to delete, please try again.');
    }
}

document.getElementById('goal-form')?.addEventListener('submit', async function (e) {
    e.preventDefault();
    const courseId = document.getElementById('goal-course').value;

    const res = await authorizedFetch('/api/courses/goals/create/', {
        method: 'POST',
        body: JSON.stringify({course: courseId, progress: 0.0})
    });

    const result = await res.json();
    document.getElementById('goal-result').innerText = res.ok
        ? 'Goal set successfully!'
        : result.detail || JSON.stringify(result) || 'Failed to set goal.';

    if (res.ok) {
        loadGoals();
    }
});

document.getElementById('progress-form')?.addEventListener('submit', async function (e) {
    e.preventDefault();
    const goalId = document.getElementById('goal-id').value;
    const progress = document.getElementById('progress-value').value;

    const res = await authorizedFetch(`/api/courses/goals/${goalId}/`, {
        method: 'PATCH',
        body: JSON.stringify({progress: progress})
    });

    const result = await res.json();
    document.getElementById('progress-result').innerText = res.ok
        ? 'Progress updated successfully!'
        : result.detail || JSON.stringify(result) || 'Failed to update progress.';

    if (res.ok) {
        loadGoals();
    }
});

document.getElementById('recommend-btn')?.addEventListener('click', async function () {
    const resultDiv = document.getElementById('recommend-result');
    resultDiv.innerText = 'Fetching recommendation, please wait...';

    try {
        const res = await authorizedFetch('/api/recommendations/recommend/');
        const data = await res.json();

        if (res.ok) {
            resultDiv.innerText = `Recommended course:\n${data.recommended_course}`;
        } else {
            resultDiv.innerText = data.detail || 'Recommendation failed, please try again later.';
        }
    } catch (error) {
        resultDiv.innerText = 'Network error, please check your connection or try again.';
        console.error('Recommendation error:', error);
    }
});

function logout() {
    window.location.href = '/accounts/logout/';
}