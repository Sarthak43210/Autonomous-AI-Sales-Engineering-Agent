import os
import requests
import time
from bs4 import BeautifulSoup
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def search_company_news(company_name):
    """Uses a free search tool to find info about the company without visiting their site directly."""
    # We use a simple search query that usually bypasses 403s
    search_url = f"https://www.google.com/search?q={company_name}+business+services+2026"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # We just grab the snippets from the search results
        snippets = [s.get_text() for s in soup.find_all('div')[:10]]
        return " ".join(snippets)[:5000]
    except:
        return "Search failed, using general knowledge."

def write_email_logic(company_name, info_text, max_retries=3):
    """The AI Brain with built-in waiting for rate limits."""
    prompt = f"Target Company: {company_name}. Info: {info_text}. Write a short 3-sentence cold email."
    
    for attempt in range(max_retries):
        try:
            # Switch to the more reliable 2.5 Flash-Lite model
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "429" in str(e):
                # We hit the limit. Let's wait 30 seconds as the error suggested.
                print(f"⏳ Quota reached. Waiting 30s to reset... (Attempt {attempt+1}/{max_retries})")
                time.sleep(31) 
            else:
                return f"AI Error: {e}"
    return "Failed to generate email after retries."

if __name__ == "__main__":
    company = "Infosys" # You can change this to any startup name
    print(f"--- 🤖 Searching for info on {company} ---")
    
    # We search Google instead of hitting Infosys.com directly
    research_data = search_company_news(company)
    print("✅ Research gathered. Drafting email...")
    
    email = write_email_logic(company, research_data)
    print("\n--- 📧 YOUR GENERATED EMAIL ---")
    print(email)