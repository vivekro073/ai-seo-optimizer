from google import genai
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_seo_report(website_data):
    prompt = f"""
    Act as a Senior Technical SEO Auditor. I am providing you with a JSON payload containing a webpage's extracted SEO data: Title, Meta Description, Header Hierarchy (H1-H6), and an Image Audit list.

    Your task is to analyze this data and return a strictly formatted JSON response.

    Here are your analysis rules:
    1. Overall Score: Assign a strict SEO score out of 100 based on technical best practices.
    2. Meta Data: Evaluate the Title and Description length and quality. Provide 3 optimized, high-converting alternatives for both.
    3. Header Hierarchy: Analyze the H1-H6 arrays. Flag structural errors. Provide 3 alternatives for the H1. Identify up to 3 weak subheadings (H2-H6) and provide optimized, keyword-rich alternatives for them.
    4. Image Accessibility: Review the `alt_tag` list. Identify any images where the `alt` value is null, None, or "". Provide a short, actionable recommendation for what the alt text should be based on the image URL file name.

    You MUST return your analysis using this exact JSON schema:
    {{
      "seo_score": 0,
      "executive_summary": "A 2-sentence harsh but fair summary of the page's SEO health.",
      "meta_optimizations": {{
        "title_issues": "Explanation of what is wrong with the current title.",
        "title_alternatives": ["Alt 1", "Alt 2", "Alt 3"],
        "description_issues": "Explanation of description issues.",
        "description_alternatives": ["Alt 1", "Alt 2", "Alt 3"]
      }},
      "header_audit": {{
        "hierarchy_errors": ["List of structural errors, e.g., 'Skipped from H2 to H4'"],
        "h1_alternatives": ["Alt 1", "Alt 2", "Alt 3"],
        "subheading_improvements": [
          {{"original": "Current weak H2/H3 text", "suggested": "Optimized alternative", "reason": "Why it's better"}}
        ]
      }},
      "image_audit": {{
        "missing_alt_count": 0,
        "fix_recommendations": [
          {{"src": "https://example.com/logo.png", "suggested_alt": "Clear description of the image"}}
        ]
      }}
    }}

    Here is the website data to analyze:
    {website_data}
    """

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)

        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)
                print(f"Google is busy (503). Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e