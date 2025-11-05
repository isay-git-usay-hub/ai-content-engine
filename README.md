# 🚀 AI Content Strategy Engine (Streamlit Edition)

> **Automated trending content analysis and strategy generation using AI, now powered by Streamlit.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.33+-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 What is AI Content Strategy Engine?

AI Content Strategy Engine is a powerful, open-source platform that automatically discovers trending topics and generates comprehensive content strategies using AI. It combines real-time data collection from Reddit and Google Trends with advanced AI analysis to create actionable content calendars tailored to your target audience, all within an interactive Streamlit interface.

## ✨ Key Features

### 🔍 **Intelligent Trend Discovery**
- **Real-time monitoring** of trending topics across Reddit and Google Trends.
- **Multi-platform analysis** to identify emerging trends before they peak.

### 🤖 **AI-Powered Strategy Generation**
- **Automated content calendars** generated based on trending topics.
- **Audience targeting** with customizable demographics and interests.
- **Content recommendations** including format, hook, and description.

### 📊 **Comprehensive Analytics**
- **Trend analysis dashboard** with visual insights.
- **Competitor analysis** to identify content gaps (using mock data).

### 🎨 **Interactive Streamlit Interface**
- **Fully interactive UI** built entirely in Python with Streamlit.
- **Dynamic dashboards** for data visualization.
- **Simple, single-page application feel** for ease of use.

## 🛠️ Tech Stack

| **Application Logic** | **Frontend** | **AI/ML** | **Infrastructure** |
|-----------------------|--------------|-----------|--------------------|
| **Python 3.9+**       | **Streamlit** - Interactive Python UI | **Groq API** - Fast AI inference | **Railway** - Deployment |
| **Pydantic** - Data validation | **Pandas** - Data manipulation | **AsyncIO** - Concurrency | **Docker** - Containerization |

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.9+** installed on your system.
- **Git** for version control.
- **Groq API key** (free tier available).

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/isay-git-usay-hub/ai-content-engine.git
cd ai-content-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory by copying the example:
```bash
cp .env.example .env  # On Windows: copy .env.example .env
```
Now, edit the `.env` file and add your Groq API key:
```
# AI Configuration
GROQ_API_KEY=your-groq-api-key-here
AI_MODEL=llama3-8b-8192
MAX_TOKENS=1500

# Data Collection
REDDIT_USER_AGENT=AIContentEngine/1.0
```

### 3. Run the Application

```bash
# Run the Streamlit app
streamlit run streamlit_app.py
```
The application will be available at `http://localhost:8501`.

## 📁 Project Structure

```
ai-content-engine/
├── 📁 app/                    # Core application logic
│   ├── 📁 collectors/        # Data collection modules
│   ├── 📁 ai/                # AI analysis and strategy generation
│   ├── 📄 logic.py            # Business logic functions
│   └── 📄 models.py           # Pydantic data models
├── 📁 .streamlit/
│   └── 📄 config.toml         # Streamlit theme configuration
├── 📄 streamlit_app.py        # Main Streamlit application file
├── 📄 requirements.txt       # Python dependencies
├── 📄 README.md
└── ...
```

## 🔧 Development Workflow

1. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```
   The app will automatically reload when you save changes to the source files.

2. **Run tests (for backend logic):**
   ```bash
   pytest tests/ -v
   ```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository** on GitHub.
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests if applicable.
4. **Commit and push** your changes.
5. **Open a Pull Request** with a clear description.

## 📈 Roadmap

- [ ] **Instagram & TikTok Integration:** Add real data collectors for more platforms.
- [ ] **Advanced Analytics:** Introduce more detailed performance and trend prediction charts.
- [ ] **Team Collaboration Features:** Allow multiple users to work on strategies together.

## 🙏 Acknowledgments

- **Groq** for providing lightning-fast AI inference.
- **Streamlit** for the excellent application framework.
- **Contributors** who help make this project better.

---

<div align="center">
  <strong>⭐ Star this repository if you find it helpful!</strong><br>
  <sub>Built with ❤️ by the AI Content Engine team</sub>
</div>
