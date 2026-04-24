# AI Emotion Detector 🤖🧠

![CI Pipeline](https://github.com/AugVe/emotion-detector-python/actions/workflows/ci-testing.yml/badge.svg)

A professional web application that leverages Artificial Intelligence (IBM Watson Natural Language Understanding) to analyze emotional content in text. Built with a modern microservice-oriented architecture, fully containerized, and ready for cloud deployment.

## ✨ Key Features
- **Core Engine:** IBM Watson NLU API integration for high-accuracy emotion detection (Anger, Disgust, Fear, Joy, and Sadness).
- **Backend:** High-performance API built with **FastAPI** (Python 3.11).
- **Frontend:** Responsive and clean UI using HTML5, CSS3, and Vanilla JavaScript.
- **Containerization:** Fully dockerized for consistent environment reproduction.
- **CI/CD Ready:** Configured for seamless deployment on platforms like Render.
- **Testing:** Unit testing suite included to ensure logic reliability.

## 🛠 Tech Stack
* **Language:** Python 3.11
* **Framework:** FastAPI
* **Web Server:** Uvicorn
* **Infrastructure:** Docker
* **External API:** IBM Watson Cloud

## 🚀 Getting Started

### Prerequisites
* Docker installed (Recommended) OR Python 3.11+
* An IBM Cloud account with Natural Language Understanding credentials.

### Option 1: Running with Docker (Recommended)
This is the easiest way to get the app running without worrying about local dependencies.

1. **Build the image:**
   ```bash
   docker build -t emotion-detector .
   ```

2. **Run the container**
Pass your IBM credentials as environment variables to securely connect the application with the Watson API:

   ```bash
   docker run -p 8000:8000 \
   -e WATSON_URL="your_watson_url" \
   -e WATSON_API_KEY="your_api_key" \
   emotion-detector
   ```

3. **Access the application:**
   Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

### Option 2: Manual Installation (Development)

If you prefer to run the application locally without Docker, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AugVe/emotion-detector-python.git
   cd emotion-detector-python
   ```

2. **Setup Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # venv\Scripts\activate   # Windows (Alternative)
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   ```bash
   export WATSON_URL="your_url"
   export WATSON_API_KEY="your_key"
   ```

5. **Run the server:**
   ```bash
   uvicorn server:app --reload
   ```

## 🧪 Testing & Quality Assurance

- **Automated Tests:** GitHub Actions runs the test suite (`test_emotion_detection.py`) automatically on every pull request and push to `main`.
- **Manual Testing:** Run `python3 test_emotion_detection.py` locally.
- **Performance:** Stress-tested using **Apache Benchmark** to verify concurrency handling and response stability.

## ☁️ Deployment & Monitoring

This project is pre-configured for **Render** with a production-ready setup:

- **Runtime:** Docker (Multi-stage build).
- **Health Monitoring:** Service status is monitored in real-time via the `/health` endpoint.
- **Environment Management:** API keys are securely injected via **Render's Environment Variables**, ensuring that sensitive credentials never touch the codebase.

---
*Developed as part of a professional portfolio to demonstrate full-stack AI integration and DevOps practices.*