/**
 * Executes the emotion analysis by sending the user input to the backend.
 * Updates the UI with the formatted response from the server and manages
 * loading states and visibility.
 */
const runSentimentAnalysis = () => {
    // Retrieve DOM elements for input, response, and loader
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseDiv = document.getElementById("system_response");
    const loader = document.getElementById("loader");

    // Check if the input is empty or just whitespace before making the request
    if (!textToAnalyze.trim()) {
        responseDiv.classList.remove("hidden");
        responseDiv.innerHTML = "Please enter some text to analyze.";
        responseDiv.className = "mt-6 p-4 rounded-lg bg-yellow-50 text-yellow-800 border border-yellow-200";
        return;
    }

    // Prepare the UI: Show loader and hide any previous response
    responseDiv.classList.add("hidden");
    loader.classList.remove("hidden");

    // Initiate an asynchronous GET request to the emotionDetector endpoint
    // encodeURIComponent ensures special characters are handled correctly in the URL
    fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`)
        .then(response => {
            // Hide the loader as the server has responded
            loader.classList.add("hidden");
            
            // Check if the HTTP response status is successful (200-299)
            if (!response.ok) {
                return response.json().then(err => { 
                    throw new Error(err.detail || 'Server error'); 
                });
            }
            return response.json(); // Parse the JSON response body
        })
        .then(data => {
            // Make the response container visible and inject the result
            responseDiv.classList.remove("hidden");
            responseDiv.innerHTML = data.result;
            
            // Apply a professional success style using Tailwind classes
            responseDiv.className = "mt-6 p-6 rounded-xl bg-white shadow-sm border-t-4 border-blue-500 text-gray-700 leading-relaxed";
        })
        .catch(error => {
            // Ensure loader is hidden and show error message to the user
            loader.classList.add("hidden");
            responseDiv.classList.remove("hidden");
            
            console.error('Analysis Error:', error);
            responseDiv.innerHTML = `⚠️ Error: ${error.message}`;
            responseDiv.className = "mt-6 p-4 rounded-lg bg-red-50 text-red-800 border border-red-200";
        });
};