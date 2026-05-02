/**
 * Executes the emotion analysis by sending the user input to the backend.
 * This version uses a standard function declaration to ensure global 
 * scope availability for the HTML onclick event.
 */
function runSentimentAnalysis() {
    // Log to confirm the function is being called
    console.log("Function runSentimentAnalysis triggered!");

    // Retrieve DOM elements
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseDiv = document.getElementById("system_response");
    const loader = document.getElementById("loader");

    // Validation: Check if input is empty or just whitespace
    if (!textToAnalyze.trim()) {
        responseDiv.classList.remove("hidden");
        responseDiv.innerHTML = "Please enter some text to analyze.";
        responseDiv.className = "mt-6 p-4 rounded-lg bg-yellow-50 text-yellow-800 border border-yellow-200";
        return;
    }

    // UI Setup: Show loading spinner and hide previous results
    responseDiv.classList.add("hidden");
    loader.classList.remove("hidden");

    // Perform the asynchronous request to the FastAPI backend
    fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`)
        .then(response => {
            // Hide loader as soon as the server responds
            loader.classList.add("hidden");
            
            if (!response.ok) {
                // If the server returns an error, parse the error message
                return response.json().then(err => { 
                    throw new Error(err.detail || 'Server error'); 
                });
            }
            return response.json();
        })
        .then(data => {
            // Make the response container visible
            responseDiv.classList.remove("hidden");
            
            // Log raw data to the console for debugging
            console.log("Server response received:", data);

            // Determine which field contains the result string
            const output = data.result || data.response || JSON.stringify(data);
            
            // Update the UI with the result and success styling
            responseDiv.innerHTML = output;
            responseDiv.className = "mt-6 p-6 rounded-xl bg-white shadow-sm border-t-4 border-blue-500 text-gray-700 leading-relaxed font-medium";
        })
        .catch(error => {
            // Ensure loader is hidden and show the error in the UI
            loader.classList.add("hidden");
            responseDiv.classList.remove("hidden");
            
            console.error('Analysis Error:', error);
            responseDiv.innerHTML = `⚠️ Error: ${error.message}`;
            responseDiv.className = "mt-6 p-4 rounded-lg bg-red-50 text-red-800 border border-red-200";
        });
}

/**
 * Explicitly attach the function to the window object.
 * This acts as a fallback for strict environments (like SES) 
 * that might prevent automatic global function registration.
 */
window.runSentimentAnalysis = runSentimentAnalysis;