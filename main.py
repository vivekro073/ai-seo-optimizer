from flask import Flask, render_template, request
from scraper import scrape_seo_data
from ai_engine import generate_seo_report
import markdown
import os


app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")



@app.route('/analyze', methods=["POST"])
def analyze():
    website = request.form.get("website")
    seo_data = scrape_seo_data(website)
    ai_response = generate_seo_report(seo_data)
    html_report = markdown.markdown(ai_response)
    print(website)
    return render_template("report.html", report=html_report)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
