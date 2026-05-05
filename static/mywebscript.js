/**
 * Main function to perform emotion analysis.
 * It gathers input, shows a loader, and communicates with the FastAPI backend.
 */
function runSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseDiv = document.getElementById("system_response");
    const loader = document.getElementById("loader");

    // 1. Validation: Prevent empty submissions
    if (!textToAnalyze.trim()) {
        responseDiv.classList.remove("hidden");
        responseDiv.innerHTML = "Please enter some text to analyze.";
        responseDiv.className = "mt-6 p-4 rounded-lg bg-yellow-50 text-yellow-800 border border-yellow-200";
        return;
    }

    // 2. UI Reset: Show loader and hide previous responses
    responseDiv.classList.add("hidden");
    loader.classList.remove("hidden");

    // 3. API Call: Fetch data from the endpoint
    fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`)
        .then(response => {
            loader.classList.add("hidden");
            if (!response.ok) {
                return response.json().then(err => { 
                    throw new Error(err.detail || 'Server error'); 
                });
            }
            return response.json();
        })
        .then(data => {
            responseDiv.classList.remove("hidden");
            console.log("Analysis successful:", data);

            const output = data.result || data.response || JSON.stringify(data);
            responseDiv.innerHTML = output;

            /**
             * DYNAMIC UI STYLING LOGIC
             * We apply specific Tailwind CSS classes based on the dominant emotion detected.
             * This provides immediate visual feedback to the user.
             */
            
            const baseClasses = "mt-6 p-6 rounded-xl shadow-sm border-t-4 leading-relaxed font-medium transition-all duration-500";

            // Conditional styling based on detected emotional context
            if (output.includes("JOY")) {
                responseDiv.className = `${baseClasses} bg-green-50 border-green-500 text-green-900`;
            } else if (output.includes("ANGER") || output.includes("FEAR")) {
                responseDiv.className = `${baseClasses} bg-red-50 border-red-500 text-red-900`;
            } else if (output.includes("SADNESS")) {
                responseDiv.className = `${baseClasses} bg-gray-50 border-gray-500 text-gray-900`;
            } else {
                responseDiv.className = `${baseClasses} bg-blue-50 border-blue-500 text-blue-900`;
            }
        })
        .catch(error => {
            loader.classList.add("hidden");
            responseDiv.classList.remove("hidden");
            console.error('Analysis Error:', error);
            
            responseDiv.innerHTML = `⚠️ Error: ${error.message}`;
            responseDiv.className = "mt-6 p-4 rounded-lg bg-red-50 text-red-800 border border-red-200";
        });
}

/**
 * DEPLOYMENT FIX:
 * Attaches the event listener once the DOM is fully loaded.
 * This approach is mandatory for environments with strict CSP (Content Security Policy)
 * or SES (Secure ECMAScript) like Docker-based Render deployments.
 */
document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeButton');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', runSentimentAnalysis);
        console.log("Success: Button listener attached via addEventListener.");
    } else {
        console.error("Error: analyzeButton not found in the DOM.");
    }
});