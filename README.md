# AI_Agent_Capstone_Project_Personal_Research_Assistant
This project basically can search the web, analyse the content and summarizes it

# Project Setup and Installation

# Create project directory
mkdir research-assistant && cd research-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install google-adk google-generativeai python-dotenv uvloop

# Environment Configuration (create .env file in our project root)

echo "GOOGLE_CLOUD_PROJECT=your-project-id" > .env
echo "GOOGLE_CLOUD_LOCATION=us-central1" >> .env

# Add Gemini API Key
export GEMINI_API_KEY="your-api-key"

# Run Agent by executing in interactive mode
python run_research.py

# Expected Output
🤖 Research Assistant Initialized!
Starting research on 'AI Agents in Healthcare'...

📊 RESEARCH RESULTS:
[Agent will generate research report here...]

📈 CONTENT ANALYSIS:
[Agent will generate analysis here...]





