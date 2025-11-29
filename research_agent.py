import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models import VertexAI
from google.adk.tools import Tool
from google.adk.sessions import InMemorySessionManager

# Load environment variables
load_dotenv()

class ResearchAssistant:
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.location = os.getenv('GOOGLE_CLOUD_LOCATION')
        
        # Initialize the session manager
        self.session_manager = InMemorySessionManager()
        
        # Create custom tools for research
        self.research_tools = [
            self._create_web_search_tool(),
            self._create_content_analyzer_tool(),
            self._create_summary_generator_tool()
        ]
        
        # Initialize the AI agent
        self.agent = self._create_agent()
    
    def _create_web_search_tool(self) -> Tool:
        """Create a tool for web search functionality"""
        @Tool
        def web_search(query: str) -> str:
            """
            Search the web for current information about a topic.
            
            Args:
                query: The search query to look up
                
            Returns:
                Search results and relevant information
            """
            # In a real implementation, you'd integrate with Google Search API
            # This is a mock implementation for demonstration
            return f"Search results for '{query}': Latest information shows this is a trending topic with multiple recent developments in the field."
        
        return web_search
    
    def _create_content_analyzer_tool(self) -> Tool:
        """Create a tool for analyzing content"""
        @Tool
        def analyze_content(content: str, analysis_type: str = "comprehensive") -> str:
            """
            Analyze content for key insights, main points, and important details.
            
            Args:
                content: The content to analyze
                analysis_type: Type of analysis (comprehensive, technical, business)
                
            Returns:
                Analysis results with key findings
            """
            analysis_templates = {
                "comprehensive": "Comprehensive analysis reveals key themes: innovation, market impact, and technical feasibility.",
                "technical": "Technical analysis shows advanced implementation requirements and scalability considerations.",
                "business": "Business analysis indicates strong market potential and competitive advantages."
            }
            
            return f"Analysis of {len(content)} characters: {analysis_templates.get(analysis_type, 'Analysis completed')}"
        
        return analyze_content
    
    def _create_summary_generator_tool(self) -> Tool:
        """Create a tool for generating summaries"""
        @Tool
        def generate_summary(content: str, bullet_points: bool = True) -> str:
            """
            Generate a concise summary of content with optional bullet points.
            
            Args:
                content: The content to summarize
                bullet_points: Whether to use bullet points format
                
            Returns:
                Concise summary of the content
            """
            if bullet_points:
                return f"Summary of {len(content)} characters:\n• Key point 1: Main concept\n• Key point 2: Important details\n• Key point 3: Future implications"
            else:
                return f"Summary: The content discusses important developments in the field, highlighting key innovations and their potential impact."
        
        return generate_summary
    
    def _create_agent(self) -> Agent:
        """Create and configure the main research agent"""
        
        agent_instruction = """
        You are a Professional Research Assistant specializing in technical and business analysis.
        
        YOUR CAPABILITIES:
        - Search for current information using web search
        - Analyze content for key insights and technical details
        - Generate comprehensive summaries with actionable insights
        - Provide research recommendations and next steps
        
        RESEARCH METHODOLOGY:
        1. Always start by understanding the research topic thoroughly
        2. Use web search to gather current information when needed
        3. Analyze findings for credibility and relevance
        4. Structure your responses with clear sections
        5. Provide actionable recommendations
        
        RESPONSE FORMAT:
        - Start with an executive summary
        - Break down into logical sections
        - Use bullet points for key findings
        - End with recommendations and next steps
        
        Always be thorough, accurate, and professional in your analysis.
        """
        
        # Create the agent with Gemini 2.0 Flash
        agent = Agent(
            model='gemini-2.0-flash-exp',
            name='research_assistant',
            description='A professional research assistant for technical and business analysis',
            instruction=agent_instruction,
            tools=self.research_tools
        )
        
        return agent
    
    async def research_topic(self, topic: str, research_depth: str = "comprehensive") -> str:
        """
        Conduct research on a specific topic
        
        Args:
            topic: The research topic
            research_depth: Depth of research (quick, comprehensive, deep)
            
        Returns:
            Research report
        """
        
        research_prompt = f"""
        Please conduct {research_depth} research on: {topic}
        
        Please provide:
        1. Executive summary
        2. Key findings and current developments
        3. Technical analysis
        4. Business implications
        5. Recommendations and next steps
        
        Use all available tools to gather and analyze information.
        """
        
        try:
            # Create a session for this research task
            session = self.session_manager.create_session()
            
            # Execute the research query
            response = await self.agent.async_stream_query(
                message=research_prompt,
                session=session
            )
            
            # Collect the response
            full_response = ""
            async for chunk in response:
                full_response += chunk.text
            
            return full_response
            
        except Exception as e:
            return f"Research failed with error: {str(e)}"
    
    async def analyze_document(self, content: str, analysis_type: str = "comprehensive") -> str:
        """
        Analyze provided document content
        
        Args:
            content: Document content to analyze
            analysis_type: Type of analysis to perform
            
        Returns:
            Analysis report
        """
        
        analysis_prompt = f"""
        Please analyze the following document content with {analysis_type} analysis:
        
        {content[:2000]}  # Limit content for demonstration
        
        Provide:
        - Key insights and main arguments
        - Technical/business implications
        - Strengths and weaknesses
        - Recommendations
        """
        
        try:
            session = self.session_manager.create_session()
            response = await self.agent.async_stream_query(
                message=analysis_prompt,
                session=session
            )
            
            full_response = ""
            async for chunk in response:
                full_response += chunk.text
            
            return full_response
            
        except Exception as e:
            return f"Analysis failed with error: {str(e)}"

# Example usage and testing
async def main():
    """Test the research assistant"""
    
    # Initialize the research assistant
    assistant = ResearchAssistant()
    
    print("🤖 Research Assistant Initialized!")
    print("Starting research on 'AI Agents in Healthcare'...\n")
    
    # Example 1: Research a topic
    research_result = await assistant.research_topic(
        "AI Agents in Healthcare",
        "comprehensive"
    )
    
    print("📊 RESEARCH RESULTS:")
    print(research_result)
    print("\n" + "="*50 + "\n")
    
    # Example 2: Analyze content
    sample_content = """
    Artificial Intelligence agents are transforming healthcare delivery through 
    automated diagnosis, personalized treatment plans, and robotic surgery. 
    Recent advancements in large language models have enabled more sophisticated 
    patient interactions and medical record analysis. The market is expected to 
    grow by 35% annually, with significant impacts on patient outcomes and 
    operational efficiency.
    """
    
    analysis_result = await assistant.analyze_document(
        sample_content,
        "business"
    )
    
    print("📈 CONTENT ANALYSIS:")
    print(analysis_result)

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
