# This file is required to make Python treat the directory as a package
# You can leave it empty or add package-level imports for convenience

from utils.scraper import scrape_flipkart_reviews, get_review_link
from utils.analyzer import analyze_sentiment

# This allows users to import directly from utils
# For example: from utils import scrape_flipkart_reviews