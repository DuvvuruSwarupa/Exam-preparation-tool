document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    let fileInput = document.getElementById('file');
    let formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayQuestions(data.questions);
    })
    .catch(error => console.error('Error:', error));
});

function displayQuestions(questions) {
    let container = document.getElementById('questions-container');
    container.innerHTML = '';
    questions.forEach(question => {
        let div = document.createElement('div');
        div.classList.add('question');
        div.innerHTML = `
            <p>${question.question}</p>
            <button onclick="modifyQuestion('${question._id}')">Modify</button>
        `;
        container.appendChild(div);
    });
}

function modifyQuestion(questionId) {
    let newQuestion = prompt('Enter the new question text:');
    if (newQuestion) {
        fetch('http://localhost:5000/modify_question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                _id: questionId,
                question: newQuestion
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert('Question modified successfully');
        })
        .catch(error => console.error('Error:', error));
    }
}

// Load questions on page load
fetch('http://localhost:5000/questions')
    .then(response => response.json())
    .then(data => displayQuestions(data))
    .catch(error => console.error('Error:', error));
