

import os
from browser_use import Agent, ChatGoogle
from dotenv import load_dotenv
import warnings
import sys

warnings.filterwarnings("ignore", category=ResourceWarning)

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load credentials
load_dotenv()
username = os.getenv("VEEVA_USERNAME")
password = os.getenv("VEEVA_PASSWORD")

# Read test scenarios from file
with open('test_scenarios.txt', 'r', encoding='utf-8') as f:
    data = f.read()

# Replace placeholders with actual values from .env
data = data.replace('{username}', username).replace('{password}', password)
print("--------------", data)

# Function to check for upload keyword in scenario
def check_upload_keyword(scenario_text):
    """Check if scenario contains upload keyword and return status"""
    if 'upload' in scenario_text:
        return True, "upload"
    elif 'UPLOAD' in scenario_text:
        return True, "UPLOAD"
    else:
        return False, ""

# Debug: Check for upload keyword first
print("\n=== KEYWORD CHECK DEBUG ===")
print(f"Scenario text length: {len(data)}")
print(f"Looking for 'upload' in text: {'upload' in data}")
print(f"Looking for 'UPLOAD' in text: {'UPLOAD' in data}")
print("=== END DEBUG ===")

upload_found, found_keyword = check_upload_keyword(data)
print(f"\nKeyword check result: upload_found={upload_found}, found_keyword='{found_keyword}'")

if upload_found:
    print(f"\nUpload keyword '{found_keyword}': PRESENT")
    
    # Ask for file path input
    file_path = input("Enter the file path for upload: ").strip()
    
    # Convert to absolute path
    file_path = os.path.abspath(file_path)
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        exit(1)
    
    print(f"Using file: {file_path}")
    
    # Initialize LLM with API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY or GEMINI_API_KEY not found in .env file")
        exit(1)
    
    llm = ChatGoogle(model="gemini-2.5-flash", api_key=api_key)
    
    # Build and run the agent
    agent = Agent(
        task=data,
        llm=llm,
        available_file_paths=[file_path],
        record_video=False,
        save_screenshots=True,
    )
    
    try:
        result = agent.run_sync()
        with open("agent_result.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
        print("Agent completed successfully")
        print("Result saved to agent_result.txt")
    except Exception as e:
        print(f"Error during agent run: {e}")
else:
    print("\nUpload keyword: NOT PRESENT")
    print("Running browser task without file upload...")
    
    # Initialize LLM with API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY or GEMINI_API_KEY not found in .env file")
        exit(1)
    
    llm = ChatGoogle(model="gemini-2.5-flash", api_key=api_key)
    
    # Build and run the agent without file upload
    agent = Agent(
        task=data,
        llm=llm,
        record_video=False,
        save_screenshots=True,
    )
    
    try:
        result = agent.run_sync()
        with open("agent_result.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
        print("Agent completed successfully")
        print("Result saved to agent_result.txt")
    except Exception as e:
        print(f"Error during agent run: {e}")
