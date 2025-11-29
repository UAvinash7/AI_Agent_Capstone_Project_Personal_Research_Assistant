import asyncio
import sys
from research_agent import ResearchAssistant

async def interactive_research():
    assistant = ResearchAssistant()
    
    print("🎓 AI Research Assistant - Capstone Project")
    print("Commands: 'research <topic>', 'analyze <content>', 'quit'")
    
    while True:
        try:
            user_input = input("\n🔍 What would you like to research? ").strip()
            
            if user_input.lower() == 'quit':
                print("Thank you for using Research Assistant!")
                break
            
            elif user_input.startswith('research '):
                topic = user_input[9:].strip()
                if topic:
                    print(f"\n📚 Researching: {topic}")
                    result = await assistant.research_topic(topic)
                    print(f"\n📊 RESULTS:\n{result}")
                else:
                    print("Please provide a research topic")
            
            elif user_input.startswith('analyze '):
                content = user_input[8:].strip()
                if content:
                    print(f"\n🔍 Analyzing content...")
                    result = await assistant.analyze_document(content)
                    print(f"\n📈 ANALYSIS:\n{result}")
                else:
                    print("Please provide content to analyze")
            
            else:
                print("Unknown command. Use 'research <topic>' or 'analyze <content>'")
                
        except KeyboardInterrupt:
            print("\n\nResearch session ended.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(interactive_research())
