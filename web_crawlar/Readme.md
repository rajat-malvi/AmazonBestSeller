# Web Crawler Documentation

## Overview
This Python script is a simple web crawler that fetches and processes content from a list of seed URLs. The script extracts, cleans, and saves textual content while following hyperlinks up to a specified depth.

## Features
- Uses a list of at least 10 popular seed URLs as a starting point.
- Fetches web page content using `requests`.
- Crawls URLs up to a minimum depth of 2.
- Maintains a queue for managing URLs, implementing a breadth-first search (BFS) or depth-first search (DFS) approach.
- Extracts hyperlinks from the HTML content for further crawling.
- Cleans HTML content by removing scripts, styles, and unwanted characters while keeping the main text.
- Saves processed text into structured text files.
- Implements a delay to prevent overwhelming web servers.

## Dependencies
Ensure the following Python modules are installed:
```bash
pip install requests
```
The script also uses built-in modules: `re`, `os`, `time`, and `collections`.

## Function Descriptions

### `get_page_content(url)`
Fetches the HTML content of a given URL.
- Uses a custom User-Agent header to mimic a real browser.
- Returns the HTML text if the request is successful, otherwise returns `None`.

### `extract_links(html, base_url, limit=2)`
Extracts up to `limit` hyperlinks from the given HTML content.
- Uses regular expressions to find absolute URLs.
- Filters and returns a subset of unique links to ensure diversity.

### `clean_html(html)`
Processes raw HTML content to extract meaningful text.
- Removes scripts, styles, comments, and redundant HTML tags.
- Normalizes spaces and line breaks.
- Filters out unnecessary characters and alphanumeric patterns.
- Does not remove stop words to retain the original context of the content.

### `save_text(content, filename)`
Saves the cleaned text into a file under the `data/` directory.
- Creates the `data/` directory if it does not exist.
- Writes the cleaned content into a UTF-8 encoded text file.

### `web_crawler(seed_urls, max_depth)`
Manages the web crawling process.
- Uses a queue-based approach (BFS or DFS) to explore links iteratively.
- Ensures a minimum crawling depth of 2.
- Avoids revisiting pages.
- Saves crawled and cleaned content.
- Respects a delay to prevent excessive requests to servers.

## Execution
The script can be run directly using:
```bash
python script.py
```
### Configuration
- Modify the `seed_urls` list to specify at least 10 initial websites to crawl.
- Adjust `max_depth` to control the extent of link-following.

## Example Workflow
1. The crawler starts with predefined seed URLs.
2. It fetches and cleans content, saving it as text files.
3. Extracted links are added to the queue for further exploration up to `max_depth`.
4. The process repeats until all pages in the queue are visited or the depth limit is reached.

## Notes
- This script is designed for educational purposes. Ensure compliance with website terms of service before scraping.
- Avoid excessive crawling to prevent IP bans.
- Can be extended with additional features such as database storage, content filtering, or keyword-based crawling.

## Enhancements
Potential improvements include:
- Multi-threading for faster crawling.
- Adding logging mechanisms for better debugging.
- Implementing a more advanced parser like `BeautifulSoup` instead of regex-based extraction.
