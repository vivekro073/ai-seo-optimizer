from bs4 import BeautifulSoup
import requests
import re


def scrape_seo_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        page = requests.get(url, headers=headers, timeout=10)
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch URL: {str(e)}"}
    data = page.text

    soup = BeautifulSoup(data, 'html.parser')

    title = soup.find("title")
    description = soup.find('meta', attrs={'name': re.compile("description", re.IGNORECASE)})

    h1 = soup.find_all("h1")
    h1_text = [h1_heading.text for h1_heading in h1]
    h2 = soup.find_all("h2")
    h2_text = [h2_heading.text for h2_heading in h2]
    h3 = soup.find_all("h3")
    h3_text = [h3_heading.text for h3_heading in h3]
    h4 = soup.find_all("h4")
    h4_text = [h4_heading.text for h4_heading in h4]
    h5 = soup.find_all("h5")
    h5_text = [h5_heading.text for h5_heading in h5]
    h6 = soup.find_all("h6")
    h6_text = [h6_heading.text for h6_heading in h6]

    images = soup.find_all("img")
    image_tags = [{'src': img.get("src"), 'alt': img.get("alt")} for img in images]

    website_data = {"title": title.text if title else "No Title",
                    "description": description["content"] if description else "No description found",
                    "h1": h1_text if h1_text else "No h1",
                    "h2": h2_text if h2_text else "No h2",
                    "h3": h3_text if h3_text else "No h3",
                    "h4": h4_text if h4_text else "No h4",
                    "h5": h5_text if h5_text else "No h5",
                    "h6": h6_text if h6_text else "No h6",
                    "alt_tag": image_tags,
                    }

    return website_data