function refresh() {
    var div = document.getElementById('myDiv');

    var formData = new FormData();
    
    var fileInput = document.getElementById('challenge-input');
    var file = fileInput.files[0]; // Get the selected file
    if (file) {
        formData.append('file', file); // Append the file to the FormData object
    }

    fetch('/api/v1/scripts/rate_file_by_openai', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        div.innerHTML = data;
    })
    .catch(error => {
        div.innerHTML = 'Error uploading file:' + error;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    refresh()
});

function submitFile() {

    refresh()

};


