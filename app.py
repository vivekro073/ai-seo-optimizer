from flask import Flask, render_template, request
from scraper import scrape_seo_data
from ai_engine import generate_seo_report
from website_scraper import scraper
import asyncio
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def fetch_link_analysis_from_db(website):
    db_url = os.environ.get('DATABASE_URL')

    # Connect to Neon database using RealDictCursor so rows behave like Python dictionaries
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    cursor = conn.cursor()

    # The wildcard helps us filter the database to ONLY the website the user requested
    website_wildcard = f"{website}%"

    # 1. Get 404 Pages
    cursor.execute("""
        SELECT 
            data->>'source_page' AS source_page, 
            data->>'target_link' AS broken_link,
            data->>'anchor_text' AS anchor_text,
            data->>'source_status' AS status
        FROM dataset_records
        WHERE data->>'source_page' LIKE %s 
          AND data->>'source_status' = '404';
    """, (website_wildcard,))
    pages_404 = cursor.fetchall()

    # 2. Get Outbound Links Data
    cursor.execute("""
        SELECT 
            data->>'source_page' AS source_page, 
            COUNT(*) AS total_outbound,
            json_agg(
                json_build_object(
                    'target_link', data->>'target_link', 
                    'anchor_text', data->>'anchor_text'
                )
            ) AS links
        FROM dataset_records
        WHERE data->>'source_page' LIKE %s
        GROUP BY data->>'source_page'
        ORDER BY total_outbound DESC;
    """, (website_wildcard,))
    outbound_links = cursor.fetchall()

    # 3. Get Thin Pages (Less than 5 inbound links)
    cursor.execute("""
        SELECT 
            data->>'target_link' AS target_page,
            COUNT(DISTINCT data->>'source_page') AS inbound_count,
            json_agg(
                json_build_object(
                    'source_page', data->>'source_page',
                    'anchor_text', data->>'anchor_text'
                )
            ) AS referring_pages
        FROM dataset_records
        WHERE data->>'target_link' LIKE %s
        GROUP BY data->>'target_link'
        HAVING COUNT(DISTINCT data->>'source_page') < 5
        ORDER BY inbound_count ASC;
    """, (website_wildcard,))
    thin_pages = cursor.fetchall()


    conn.close()

    # Return everything neatly packaged for your Flask template
    return {
        "404_pages": pages_404,
        "outbound_links": outbound_links,
        "thin_pages": thin_pages
    }


app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")


@app.route('/analyze-page', methods=["POST"])
def analyze_page():
    website = request.form.get("audit_url")

    try:
        ai_payload = scrape_seo_data(website)

        ai_response = generate_seo_report(ai_payload)

        return render_template("seo_repost.html", report=ai_response)

    except Exception as e:
        print(f"API Error: {e}")

        error_msg = "The AI server is experiencing heavy traffic right now. Please wait a moment and try again."
        return render_template("index.html", error=error_msg)


@app.route('/links-analyser', methods=["POST"])
def analyze_links():
    website = request.form.get("link_url")

    try:
        asyncio.run(scraper(website))
        link_data = fetch_link_analysis_from_db(website)
        return render_template("link_report.html", website=website, data=link_data)

    except Exception as e:
        print(f"Scraping Error: {e}")
        error_msg = "We encountered an issue analyzing the links. Please ensure the URL is correct and try again."
        return render_template("index.html", error=error_msg)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
