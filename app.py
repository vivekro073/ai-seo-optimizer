from flask import Flask, render_template, request
from scraper import scrape_seo_data
from ai_engine import generate_seo_report
import os


app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")


@app.route('/analyze', methods=["POST"])
def analyze():
    website = request.form.get("website")

    try:
        ai_payload = scrape_seo_data(website)

        ai_response = generate_seo_report(ai_payload)

        return render_template("report.html", report=ai_response)

    except Exception as e:
        print(f"API Error: {e}")

        error_msg = "The AI server is experiencing heavy traffic right now. Please wait a moment and try again."
        return render_template("index.html", error=error_msg)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
