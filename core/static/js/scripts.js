function updateCounts() {
    fetch('get_counts/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('student-count').textContent = data.total_students;
            document.getElementById('teacher-count').textContent = data.total_teachers;
        })
}

setInterval(updateCounts, 5000);  // update every 5 seconds