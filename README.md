# AI Content Strategy Engine

Automated trending content analysis and strategy generation using free data sources.

## Features

- 📊 Real-time trend collection from multiple platforms
- 🤖 AI-powered trend analysis and insights
- 📅 Automated 30-day content calendar generation
- 🎯 Target audience customization
- 📈 Engagement optimization recommendations

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-content-strategy-engine.git
   cd ai-content-strategy-engine
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory with your API keys:
   ```
   GROQ_API_KEY=your_groqapi_key
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Data Sources

- Google Trends
- Reddit
- Twitter (using Twint)
- YouTube (using PyTube)

## Project Structure

- **/app**: The core backend application.
  - **/api**: FastAPI routes and endpoints.
  - **/collectors**: Data collection modules (Google Trends, Reddit, etc.).
  - **/ai**: AI analysis and strategy generation.
- **/frontend**: The React frontend application.
- **/tests**: Unit and integration tests.

## Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Run the frontend development server**
   ```bash
   npm start
   ```

## Deployment

### Frontend (React)

You can deploy the frontend to static hosting services like Netlify, Vercel, or GitHub Pages.

**Deploying to Netlify/Vercel:**

1.  Connect your GitHub repository to Netlify/Vercel.
2.  Set the build command to `npm run build`.
3.  Set the publish directory to `frontend/build`.
4.  Add your environment variables (e.g., `REACT_APP_API_URL`) to the Netlify/Vercel project settings.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

