const apiUrl = 'http://127.0.0.1:5000/tasks';

document.addEventListener('DOMContentLoaded', () => {
    fetchTasks();

    const createForm = document.getElementById('createForm');
    createForm.addEventListener('submit', event => {
        event.preventDefault();

        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const dueDate = document.getElementById('dueDate').value;
        const status = document.getElementById('status').value;

        const taskData = { title, description, due_date: dueDate, status };
        createTask(taskData);
    });
});

function fetchTasks() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const taskList = document.getElementById('taskList');
            taskList.innerHTML = '';
            data.tasks.forEach(task => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <strong>${task.title}</strong> - ${task.description} - ${task.due_date} - ${task.status}
                    <button onclick="deleteTask(${task.id})">Delete</button>
                `;
                taskList.appendChild(li);
            });
        });
}

function createTask(taskData) {
    fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
    }).then(() => {
        fetchTasks();
        document.getElementById('createForm').reset();
    });
}

function deleteTask(id) {
    fetch(`${apiUrl}/${id}`, { method: 'DELETE' }).then(() => fetchTasks());
}
