# 1. The Imports: Import the requests library, and import BeautifulSoup from bs4.
#
# 2. The Function Definition: Define a function called scrape_seo_data(url) that takes a single target URL as its parameter.
#
# 3. The Network Request: Inside the function, use requests.get() to fetch the webpage.
# (Pro-tip: Websites routinely block automated scripts. Create a dictionary with a standard User-Agent header and pass it into your request so the target server thinks you are a normal Chrome browser).
#
# 4. The Parser: Pass the text of the webpage response into BeautifulSoup using the "html.parser".
#
# 5. The Extraction: Use BeautifulSoup to extract three specific pieces of data:
#
# The text of the <title> tag.
#
# The content attribute of the <meta name="description"> tag.
#
# A list of all <h1> tags on the page (extract just the text from them).
#
# 6. The Payload: Package everything into a clean Python dictionary and return it. It should look something like this structurally: {"title": ..., "description": ..., "h1_tags": [...]}


from bs4 import BeautifulSoup
import requests
import re


def scrape_seo_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page =  requests.get(url, headers=headers)
    data = page.text

    soup = BeautifulSoup(data, 'html.parser')

    title = soup.find("title")
    description = soup.find('meta', attrs={'name': re.compile("description", re.IGNORECASE)})
    h1 = soup.find_all("h1")
    h1_text = [heading.text for heading in h1]

    website_data = {"title": title.text if title else "No Title",
                    "description": description["content"] if description else "No description found",
                    "h1": h1_text if h1_text else "No h1"}

    return website_data

#print(scrape_seo_data("https://www.apple.com"))