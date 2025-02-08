import requests
import re
import os
import time
from urllib.parse import urljoin
from collections import deque

def get_page_content(url):
    """Fetch page content using requests."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None
    return None

def extract_links(html, base_url, limit=2):
    """Extract and return a limited number of hyperlinks from a webpage."""
    links = re.findall(r'href=["\'](https?://[^"\']+)', html)
    unique_links = list(set(urljoin(base_url, link) for link in links))
    
    length = len(unique_links) // 2
    return unique_links[length:(length + limit)]

def clean_html(html):
    """Remove unnecessary content and keep main text."""
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)  # Remove scripts
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)  # Remove styles
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)  # Remove comments
    html = re.sub(r'<br\s*/?>', '\n', html)  # Convert <br> tags to newlines
    html = re.sub(r'</p>', '\n', html)  # Convert </p> tags to newlines
    html = re.sub(r'<[^>]+>', ' ', html)  # Remove remaining HTML tags
    html = re.sub(r'\.\w*\d+\w*', '', html)  # Remove alphanumeric patterns like ".leftflex0"
    html = re.sub(r'[^\w\s,.!?]', '', html)  # Remove unwanted characters
    html = re.sub(r'\s+', ' ', html).strip()  # Normalize spaces
    return html

def save_text(content, filename):
    """Save cleaned text to a file."""
    os.makedirs("data", exist_ok=True)
    with open(os.path.join("data", filename), "w", encoding="utf-8") as f:
        f.write(content)

def web_crawler(seed_urls, max_depth):
    """Crawl web pages and store structured text files."""
    queue = deque([(url, f"url{idx+1}", 0) for idx, url in enumerate(seed_urls)])  # (URL, identifier, depth)
    visited = set()

    while queue:
        url, identifier, depth = queue.popleft()

        if url in visited or depth > max_depth:
            continue  # Skip if already visited or depth exceeded

        print(f"Crawling: {url} -> Saving as {identifier}.txt")
        page_content = get_page_content(url)
        if not page_content:
            print(f"No more content for {url}")
            continue

        cleaned_text = clean_html(page_content)
        save_text(cleaned_text, f"{identifier}.txt")
        visited.add(url)

        if depth < max_depth:  # Continue crawling within depth limit
            links = extract_links(page_content, url, limit=2)
            for i, link in enumerate(links, start=1):
                queue.append((link, f"{identifier}{i}", depth + 1))

        time.sleep(5)  # Avoid hitting servers too quickly

if __name__=="__main__":
    # Seed URLs
    seed_urls = [
        "https://www.totalhealthandfitness.com/blog/",
        "https://www.healthline.com/health/",
        "https://simplifaster.com/articles/",
        "https://www.glofox.com/blog/fitness-blogs/",
        "https://www.purplepatchfitness.com/nutritionconsult",
        "https://overtimeathletes.com/blog/",
        "https://www.athletico.com/blog/",
        "https://elitetrack.com/",
        "https://theathleteblog.com/blog/",
        "https://www.bornfitness.com/blog/"
    ]


    web_crawler(seed_urls, max_depth=2)