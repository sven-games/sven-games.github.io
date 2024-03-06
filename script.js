document.getElementById('inputForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form submission
    var userInput = document.getElementById('userInput').value;

    // AJAX request to Python script
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'your_python_script.py', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var output = JSON.parse(xhr.responseText).output;
            document.getElementById('output').innerText = output;
        }
    };
    xhr.send(JSON.stringify({input: userInput}));
});
