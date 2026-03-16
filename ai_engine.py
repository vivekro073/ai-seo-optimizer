from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_seo_report(website_data):
    prompt = (f"Act as an Expert SEO Consultant. I am going to give you a website's Title, Meta Description, and H1 tags. You need to grade the SEO out of 100, "
              f"explain what is wrong, provide three optimized alternatives for the Title, the Meta Description, and the primary H1 Heading. Here is the website data "
              f"Title = {website_data['title']}, Description = {website_data['description']} and H1 = {website_data['h1']}."
              f"Format your output cleanly using markdown bullet points. Do NOT include raw HTML tags like <h1> or <title> in your suggested alternatives; just provide the plain text.")

    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    return response.text