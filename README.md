# 🚀 AI Content Strategy Engine

> **Automated trending content analysis and strategy generation using AI and free data sources**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 What is AI Content Strategy Engine?

AI Content Strategy Engine is a powerful, open-source platform that automatically discovers trending topics across multiple platforms and generates comprehensive 30-day content strategies using AI. It combines real-time data collection from Reddit, Google Trends, and other sources with advanced AI analysis to create actionable content calendars tailored to your target audience.

## ✨ Key Features

### 🔍 **Intelligent Trend Discovery**
- **Real-time monitoring** of trending topics across Reddit, Google Trends, and social platforms
- **Multi-platform analysis** to identify emerging trends before they peak
- **Sentiment analysis** to understand audience reception and engagement potential

### 🤖 **AI-Powered Strategy Generation**
- **30-day content calendars** automatically generated based on trending topics
- **Audience targeting** with customizable demographics and interests
- **Engagement optimization** with AI-driven posting schedules and formats
- **Content type recommendations** (videos, blogs, infographics, etc.)

### 📊 **Comprehensive Analytics**
- **Trend analysis dashboard** with visual insights
- **Competitor analysis** to identify content gaps
- **Performance predictions** using historical data patterns
- **ROI projections** for content campaigns

### 🎨 **Modern Web Interface**
- **Responsive React frontend** with intuitive design
- **Interactive dashboards** for data visualization
- **Real-time updates** without page refresh
- **Mobile-friendly** responsive design

## 🛠️ Tech Stack

| **Backend** | **Frontend** | **AI/ML** | **Infrastructure** |
|-------------|--------------|-----------|-------------------|
| **FastAPI** - High-performance Python web framework | **React 18** - Modern UI library | **Groq API** - Lightning-fast AI inference | **Railway** - Zero-config deployment |
| **Pydantic** - Data validation | **Tailwind CSS** - Utility-first styling | **LangChain** - AI orchestration | **Docker** - Containerization |
| **AsyncIO** - Concurrent data collection | **React Query** - Server state management | **Transformers** - NLP processing | **GitHub Actions** - CI/CD |
| **PostgreSQL** - Primary database | **Chart.js** - Data visualization | **Sentiment Analysis** - Audience insights | **Nginx** - Reverse proxy |

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.9+** installed on your system
- **Node.js 16+** and **npm** for frontend
- **Git** for version control
- **Groq API key** (free tier available)

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/isay-git-usay-hub/ai-content-engine.git
cd ai-content-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
# AI Configuration
GROQ_API_KEY=your-groq-api-key-here
AI_MODEL=llama3-8b-8192
MAX_TOKENS=1500

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Data Collection
REDDIT_USER_AGENT=AIContentEngine/1.0
TRENDS_LIMIT=10
COLLECTION_INTERVAL=3600  # seconds

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///./content_engine.db
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 4. Run the Application

```bash
# Start backend server
cd ..  # Back to root directory
python -m app.main

# Frontend will be available at: http://localhost:3000
# Backend API will be available at: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

## 📁 Project Structure

```
ai-content-engine/
├── 📁 app/                    # Backend application
│   ├── 📁 api/               # FastAPI routes and endpoints
│   ├── 📁 collectors/        # Data collection modules
│   ├── 📁 ai/                # AI analysis and strategy generation
│   ├── 📁 models/              # Pydantic models and schemas
│   ├── 📁 utils/              # Utility functions and helpers
│   └── 📄 main.py             # FastAPI application entry point
├── 📁 frontend/               # React frontend application
│   ├── 📁 src/
│   │   ├── 📁 components/     # Reusable React components
│   │   ├── 📁 pages/          # Application pages/screens
│   │   ├── 📁 services/       # API service layer
│   │   └── 📁 hooks/          # Custom React hooks
│   └── 📄 package.json        # Frontend dependencies
├── 📁 tests/                  # Comprehensive test suite
├── 📁 scripts/               # Development and deployment scripts
├── 📄 railway.json           # Railway deployment configuration
├── 📄 build.sh              # Build automation script
└── 📄 requirements.txt       # Python dependencies
```

## 🔧 Development Workflow

### Local Development

1. **Start backend in development mode:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start frontend with hot reload:**
   ```bash
   cd frontend && npm start
   ```

3. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

### Code Quality

```bash
# Format code
black app/ tests/

# Linting
flake8 app/

# Type checking
mypy app/
```

## 🚀 Deployment Options

### 🚂 Railway (Recommended)

Railway provides zero-config deployment with automatic scaling:

1. **Connect GitHub repository** to Railway
2. **Environment variables** are automatically detected from `railway.json`
3. **Deploy on every push** to main branch
4. **Custom domains** supported

### 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t ai-content-engine .

# Run container
docker run -p 8000:8000 -e GROQ_API_KEY=your-key ai-content-engine
```

### ☁️ Alternative Platforms

- **Heroku**: Use the included `Procfile`
- **Render**: Connect GitHub repository
- **DigitalOcean**: Use Docker deployment
- **AWS**: EC2, ECS, or Lambda deployment

## 📊 API Documentation

### Core Endpoints

| **Endpoint** | **Method** | **Description** |
|--------------|------------|-----------------|
| `/api/trends` | GET | Get trending topics from all sources |
| `/api/strategy` | POST | Generate content strategy for topics |
| `/api/calendar` | GET | Get 30-day content calendar |
| `/api/analytics` | GET | Get trend analytics and insights |
| `/health` | GET | Health check endpoint |

### Example API Usage

```bash
# Get trending topics
curl -X GET "http://localhost:8000/api/trends?limit=10"

# Generate content strategy
curl -X POST "http://localhost:8000/api/strategy" \
  -H "Content-Type: application/json" \
  -d '{
    "topics": ["AI", "Machine Learning"],
    "audience": "tech_enthusiasts",
    "platforms": ["twitter", "linkedin", "youtube"]
  }'
```

## 🎯 Usage Examples

### Content Creator
Generate a 30-day content calendar for your tech YouTube channel:

1. **Set target audience**: "Tech enthusiasts aged 18-35"
2. **Select platforms**: YouTube, Twitter, LinkedIn
3. **Choose topics**: AI, Programming, Tech Reviews
4. **Generate calendar**: Get daily content ideas with optimal posting times

### Marketing Team
Create data-driven content strategies:

1. **Analyze competitors**: Identify trending topics in your industry
2. **Generate campaigns**: Create month-long content campaigns
3. **Optimize timing**: Use AI to determine best posting schedules
4. **Track performance**: Monitor engagement predictions vs. actual results

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. **Fork the repository** on GitHub
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** and add tests
4. **Run the test suite**:
   ```bash
   pytest tests/ -v
   ```
5. **Commit and push** your changes
6. **Open a Pull Request** with a clear description

### Contribution Guidelines

- **Code style**: Follow PEP 8 for Python, ESLint for JavaScript
- **Tests**: Add tests for new features
- **Documentation**: Update README for API changes
- **Issues**: Check existing issues before creating new ones

## 📈 Roadmap

### Q1 2025
- [ ] **Instagram integration** for visual content analysis
- [ ] **TikTok trend detection** for viral content insights
- [ ] **A/B testing framework** for content optimization

### Q2 2025
- [ ] **Multi-language support** for global markets
- [ ] **Advanced analytics dashboard** with predictive modeling
- [ ] **Team collaboration features** for content teams

## 🆘 Support & Troubleshooting

### Common Issues

**Q: Getting "Module not found" errors?**
```bash
pip install -r requirements.txt --upgrade
```

**Q: Frontend not connecting to backend?**
- Check if backend is running on `http://localhost:8000`
- Verify CORS settings in `app/main.py`

**Q: API rate limits?**
- Check your Groq API key usage
- Consider upgrading to a paid plan for higher limits

### Getting Help

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Discord**: Join our community server
- **Email**: support@ai-content-engine.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for providing lightning-fast AI inference
- **FastAPI** for the excellent web framework
- **React** for the powerful frontend library
- **Contributors** who help make this project better

---

<div align="center">
  <strong>⭐ Star this repository if you find it helpful!</strong><br>
  <sub>Built with ❤️ by the AI Content Engine team</sub>
</div>

