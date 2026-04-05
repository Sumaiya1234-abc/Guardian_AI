# GuardianAI Fraud Detection - Hugging Face Spaces Deployment Guide

## 🚀 Quick Start

### Option 1: Deploy Directly from GitHub (Recommended for HF Spaces)

1. Visit https://huggingface.co/spaces/new
2. Select **"Python"** as the Space type
3. Paste the GitHub repository URL:
   ```
   https://github.com/guardianai/fraud-detection-env
   ```
4. HF will automatically detect and use `app.py` with `requirements.txt`
5. Space will be live in 2-3 minutes

### Option 2: Manual Docker Deployment on HF Spaces

1. Create a new Space on Hugging Face
2. Create a `Dockerfile` with:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements-deployment.txt .
   RUN pip install -r requirements-deployment.txt
   COPY . .
   CMD ["python", "app.py"]
   ```
3. Push to the Space repository
4. HF will build and deploy automatically

---

## 📦 Local Development Setup

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/guardianai/fraud-detection-env.git
cd guardianai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-deployment.txt

# Verify installation
python -c "import gymnasium; print(f'Gymnasium {gymnasium.__version__}')"
```

### Run Locally

```bash
# Start Gradio web interface
python app.py

# Open browser to: http://localhost:7860
```

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
# Build image
docker build -t guardianai-fraud-detection:latest .

# View image
docker images | grep guardianai
```

### Run Docker Container

```bash
# Run locally
docker run -p 7860:7860 guardianai-fraud-detection:latest

# Run with volume mounting (for persistence)
docker run -p 7860:7860 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  guardianai-fraud-detection:latest

# Run in detached mode
docker run -d -p 7860:7860 \
  --name guardianai-app \
  guardianai-fraud-detection:latest

# View logs
docker logs guardianai-app

# Stop container
docker stop guardianai-app
```

### Push to Docker Hub

```bash
# Tag image
docker tag guardianai-fraud-detection:latest \
  your-username/guardianai-fraud-detection:latest

# Login to Docker Hub
docker login

# Push image
docker push your-username/guardianai-fraud-detection:latest
```

---

## ☁️ Hugging Face Spaces - Complete Setup

### Step 1: Prepare Repository

Ensure your repo has these files:
```
guardianai/
├── app.py                      # Gradio web interface
├── requirements.txt            # Core dependencies
├── requirements-deployment.txt # Deployment dependencies
├── Dockerfile                  # (Optional, for custom setup)
├── openenv.yaml               # Environment specification
├── guardianai/                # Package code
│   ├── __init__.py
│   ├── fraud_detection_env.py
│   └── ...
├── README.md                  # Project documentation
└── LICENSE                    # License file
```

### Step 2: Create on Hugging Face Spaces

#### Method A: Create from Scratch
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. **Name**: `fraud-detection-env`
4. **License**: MIT/Apache 2.0
5. **Space SDK**: Python
6. Click "Create"

#### Method B: Clone Existing Repo
1. Create private repo on GitHub with your code
2. In HF Spaces, select "Linked Repository"
3. Connect your GitHub repo
4. HF will auto-deploy on push

### Step 3: Configure Environment Variables (if needed)

In Space settings, add secrets:
```
DEBUG=false
LOG_LEVEL=INFO
MAX_WORKERS=2
```

### Step 4: Verify Deployment

1. Wait for build to complete (~3-5 minutes)
2. Click on Space URL
3. Test the Interactive Demo tab
4. Verify all tabs work:
   - 🎮 Interactive Demo
   - 📊 Metrics
   - 📋 Transaction History
   - 📚 Documentation

---

## ✅ Testing & Verification

### Local Testing

```bash
# Run unit tests
pytest tests/ -v

# Run specific test
pytest tests/test_environment.py::TestFraudDetectionEnv -v

# Test with coverage
pytest tests/ --cov=guardianai --cov-report=html
```

### Smoke Test

```bash
# Quick test to verify everything works
python tests/smoke_test.py
```

### Integration Test

```bash
# Test environment with app
python tests/integration_test.py
```

### Test the Web Interface Locally

```bash
# Terminal 1: Run app
python app.py

# Terminal 2: Run curl tests
curl http://localhost:7860/health
curl http://localhost:7860/api/status
```

---

## 🔍 Troubleshooting

### Issue: Module not found error

**Solution:**
```bash
# Ensure all dependencies installed
pip install -r requirements.txt -r requirements-deployment.txt

# Add package to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/guardianai"
```

### Issue: Port 7860 already in use

**Solution:**
```bash
# Run on different port
python -c "from app import demo; demo.launch(server_port=7861)"

# Or kill existing process
lsof -ti:7860 | xargs kill -9
```

### Issue: Out of memory on HF Spaces

**Solution:**
```bash
# Reduce dataset size
# Modify in app.py:
DEMO_TRANSACTIONS = 100  # Reduced from default

# Or use lite requirements
cat > requirements-lite.txt << EOF
gymnasium>=0.27.0
numpy>=1.21.0
pandas>=1.3.0
gradio==4.27.0
matplotlib>=3.4.0
EOF
```

### Issue: CORS errors in browser

**Solution:**
```python
# In app.py, enable CORS:
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    show_error=True
)
# This is already set - check HF Space allowed origins
```

### Issue: Slow cold start

**Solution:**
```dockerfile
# In Dockerfile, use prebuilt base image
FROM ghcr.io/python-poetry/python:3.10-slim-bullseye
```

---

## 📊 Monitoring & Logs

### Local Development

```bash
# View logs in real-time
python app.py --log-level DEBUG

# Or with logging file
python -c "
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
from app import demo
demo.launch()
"
```

### On Hugging Face Spaces

1. Go to Space settings
2. View "Build" logs (app startup)
3. View "Runtime" logs (execution)
4. Check "Persistent storage" for data files

---

## 🔐 Security Best Practices

### For Production Deployment

1. **Set environment variables securely:**
   ```bash
   # In HF Spaces settings, add:
   DEBUG=false
   ALLOWED_ORIGINS=https://huggingface.co
   ```

2. **Use authentication (optional):**
   ```python
   # In app.py
   auth = gr.Authentication(username="admin", password="secure_password")
   demo.launch(auth=auth)
   ```

3. **Enable HTTPS (automatic on HF Spaces)**

4. **Rate limiting (for shared Spaces):**
   ```python
   demo.launch(
       max_threads=5,
       queue=True,
       max_size=10
   )
   ```

5. **Input validation:**
   ```python
   def safe_reset(task, scheme):
       valid_tasks = ["EASY", "MEDIUM", "HARD"]
       valid_schemes = ["balanced", "conservative", "aggressive", "learning"]
       
       if task not in valid_tasks or scheme not in valid_schemes:
           raise ValueError("Invalid task or scheme")
       
       return reset_env(task, scheme)
   ```

---

## 📈 Performance Optimization

### Reduce Memory Usage

```python
# In app.py
import gc

def cleanup_after_step():
    gc.collect()
    # Remove large objects

demo.load(cleanup_after_step)
```

### Cache Computations

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def compute_metrics(state_tuple):
    # Expensive computation
    pass
```

### Parallel Processing (for batch evaluation)

```bash
# Use Gradio Queue
demo.queue(concurrency_count=3, max_size=20)
```

---

## 📚 Additional Resources

### Documentation
- [OpenEnv Specification](openenv.yaml)
- [Project README](README.md)
- [API Documentation](docs/api.md)

### Example Notebooks
- [Basic Usage](examples/basic_usage.ipynb)
- [Advanced Agent Training](examples/agent_training.ipynb)

### Related Projects
- [Gymnasium Documentation](https://gymnasium.farama.org/)
- [Gradio Docs](https://www.gradio.app/docs/)
- [Hugging Face Spaces Guide](https://huggingface.co/docs/hub/spaces)

---

## 🤝 Contributing

To contribute improvements:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/improvement`
3. Make changes and test locally
4. Push and create a pull request
5. For HF Spaces, changes auto-deploy from main branch

---

## 📄 License

GuardianAI is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 💬 Support

- **Issues**: https://github.com/guardianai/fraud-detection-env/issues
- **Discussions**: https://github.com/guardianai/fraud-detection-env/discussions
- **Email**: team@guardianai.ai

**Last Updated**: March 26, 2026
**Status**: Production Ready
