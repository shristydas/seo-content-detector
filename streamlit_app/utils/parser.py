"""HTML parsing utilities."""
from bs4 import BeautifulSoup
import re


def parse_html_content(html_content):
    """
    Parse HTML and extract title and clean body text.

    Args:
        html_content: Raw HTML string

    Returns:
        dict with 'title', 'body_text', 'word_count'
    """
    try:
        soup = BeautifulSoup(html_content, 'lxml')

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ''

        # Remove script and style elements
        for script in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            script.decompose()

        # Extract text from main content areas
        main_content = soup.find('article') or soup.find('main') or soup.find('body') or soup

        # Get text and clean it
        text = main_content.get_text(separator=' ', strip=True)

        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Calculate word count
        word_count = len(text.split())

        return {
            'title': title,
            'body_text': text,
            'word_count': word_count
        }

    except Exception as e:
        return {
            'title': '',
            'body_text': '',
            'word_count': 0,
            'error': str(e)
        }


def clean_text(text):
    """Clean text for feature extraction."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text
