# 🚀 AI-Powered Technical SEO Auditor

A full-stack, serverless web application that extracts live DOM data from target URLs and utilizes an LLM to generate structured, actionable Technical SEO feedback. 

**[View Live Demo]** *https://ai-seo-optimizer-fawn.vercel.app/*
**[Watch 60-Second Video Breakdown]** *https://youtu.be/5auSnPZffgc*

## 🧠 The Engineering Problem & Solution
Large Language Models (LLMs) are notoriously difficult to integrate into strict data pipelines because they naturally want to output conversational text. 

This application solves the "unstructured output" problem by leveraging the Google Gemini API's `response_mime_type` configuration. 
By physically locking the LLM into a JSON-only generation mode, the Python backend can flawlessly map the AI's analysis directly into a 
frontend Tailwind CSS dashboard without relying on fragile Regex parsing.

## ⚙️ Tech Stack
* **Backend:** Python, Flask (Configured for Vercel Serverless Functions)
* **Data Ingestion:** `requests`, `BeautifulSoup4` (BS4)
* **AI Integration:** Google GenAI SDK (gemini-2.5-flash)
* **Frontend:** HTML5, Tailwind CSS
* **Deployment:** Vercel CI/CD

## 🔥 Key Technical Features
* **Live DOM Extraction:** Sanitizes and parses target URLs for Meta tags, H1-H6 hierarchy, and Image Alt data.
* **Fault Tolerance:** Implements an exponential backoff algorithm to gracefully handle API rate limits and 503 server overloads from the free-tier LLM.
* **Serverless Architecture:** Refactored standard Flask WSGI deployment into a lightweight serverless configuration via `vercel.json`.

## 💻 Local Installation
If you want to run this application locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vivekro073/ai-seo-optimizer.git
   cd ai-seo-optimizer