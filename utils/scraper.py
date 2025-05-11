from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlparse, parse_qs

def get_review_link(product_url):
    """Extract the review page URL from a Flipkart product URL"""
    if "flipkart.com" not in product_url or "pid=" not in product_url:
        return "Invalid Flipkart product URL"

    # Parse URL to extract query parameters
    parsed_url = urlparse(product_url)
    query_params = parse_qs(parsed_url.query)

    # Extract product ID (pid)
    product_id = query_params.get("pid", [None])[0]
    
    # Extract listing ID (lid)
    lid = query_params.get("lid", [None])[0]

    # Ensure both product_id and lid exist
    if not product_id or not lid:
        return "Invalid Flipkart URL: Missing required parameters"

    # To get the product name
    base_url = "https://www.flipkart.com/"
    remaining_url = product_url[len(base_url):]
    product_name = remaining_url.split("/p")[0]

    
    review_url = f"https://www.flipkart.com/{product_name}/product-reviews/{product_id}?pid={product_id}&lid={lid}&marketplace=FLIPKART"
    
    return review_url

def scrape_flipkart_reviews(product_url, pages=2):
    """Scrape reviews from Flipkart product page"""
    #Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    #driver installation
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    
    customer_names = []
    review_title = []
    ratings = []
    comments = []
    
    # Get review page URL
    review_url = get_review_link(product_url)
    if review_url.startswith("Invalid"):
        raise ValueError(review_url)
    
    # Scrape reviews from multiple pages
    for i in range(1, pages + 1):
        url = f"{review_url}&page={i}"
        print(f"Scraping page {i}: {url}")

        
        driver.get(url)
        time.sleep(5)  

        # Click all "READ MORE" buttons
        read_more_buttons = driver.find_elements(By.XPATH, "//span[text()='READ MORE']")
        for button in read_more_buttons:
            try:
                button.click()
                time.sleep(0.5)  
            except Exception as e:
                print("Error clicking READ MORE:", e)

        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        
        names = soup.find_all('p', class_='_2NsDsF AwS1CA')
        for name in names:
            customer_names.append(name.get_text())

        
        title = soup.find_all('p', class_='z9E0IG')
        for t in title:
            review_title.append(t.get_text())

        
        rat = soup.find_all('div', class_='XQDdHH Ga3i8K')
        for r in rat:
            rating = r.get_text()
            if rating:
                ratings.append(rating)
            else:
                ratings.append('0')  # Replace null ratings with 0

        
        cmt = soup.find_all('div', class_='ZmyHeo')
        for c in cmt:
            try:
                comment_text = c.div.div.get_text(strip=True)
                comments.append(comment_text)
            except:
                comments.append("")

        time.sleep(3)

    # Close the Selenium WebDriver
    driver.quit()

    
    min_length = min(len(customer_names), len(review_title), len(ratings), len(comments))
    customer_names = customer_names[:min_length]
    review_title = review_title[:min_length]
    ratings = ratings[:min_length]
    comments = comments[:min_length]

    # Create a DataFrame
    data = {
        'Customer Name': customer_names,
        'Review Title': review_title,
        'Rating': ratings,
        'Comment': comments
    }

    df = pd.DataFrame(data)
    return df


