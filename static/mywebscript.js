/**
 * Executes the emotion analysis by sending the user input to the backend.
 * Updates the UI with the formatted response from the server.
 */
const analyzeEmotion = () => {
    // Retrieve the text input from the DOM element
    const textToAnalyze = document.getElementById("textToAnalyze").value;

    // Check if the input is empty before making the request
    if (!textToAnalyze.trim()) {
        document.getElementById("system_response").innerHTML = "Please enter some text to analyze.";
        return;
    }

    // Initiate an asynchronous GET request to the emotionDetector endpoint
    // encodeURIComponent ensures special characters are handled correctly in the URL
    fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`)
        .then(response => {
            // Check if the HTTP response status is successful (200-299)
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.detail || 'Server error'); });
            }
            return response.json(); // Parse the JSON response body
        })
        .then(data => {
            // Inject the formatted HTML result into the response container
            document.getElementById("system_response").innerHTML = data.result;
        })
        .catch(error => {
            // Log errors for debugging and notify the user
            console.error('Analysis Error:', error);
            document.getElementById("system_response").innerHTML = `Error: ${error.message}`;
        });
};