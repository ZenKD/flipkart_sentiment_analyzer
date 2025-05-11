# Flipkart Review Sentiment Analyzer

**Automated Analysis System for E-commerce Customer Feedback**

A Software Engineering project by:
**Name:** Kamal Das
Date: 22/04/2025

---

## 📖 Abstract

This project presents a web-based sentiment analysis tool designed to extract, analyze, and visualize customer opinions from Flipkart product reviews. The system combines web scraping techniques with natural language processing to provide actionable insights into customer sentiment. By automating the review analysis process, the tool helps users make informed purchasing decisions and assists businesses in understanding customer feedback at scale.

The application utilizes Selenium and BeautifulSoup for data extraction, NLTK's VADER for sentiment analysis, and Flask for the web interface. The system processes both textual content and numerical ratings to generate a comprehensive sentiment score, identifying positive, neutral, and negative opinions. Visualizations and statistical summaries provide an intuitive understanding of overall product reception and highlight key themes in customer feedback.

---

## ✨ Key Features

*   **Efficient Web Scraping:** Extracts product reviews from Flipkart, handling dynamic content (like "READ MORE" buttons) and pagination.
*   **Robust Sentiment Analysis:**
    *   Utilizes NLTK's VADER for text-based sentiment scoring.
    *   Integrates numerical star ratings with text sentiment for a holistic score.
    *   Classifies reviews as Positive, Neutral, or Negative.
*   **Intuitive Web Interface:** Built with Flask, providing a user-friendly way to input product URLs and view results.
*   **Actionable Insights:**
    *   Generates visualizations (e.g., sentiment distribution pie charts, text-rating correlation scatter plots).
    *   Performs keyword extraction to identify common themes in positive and negative reviews.
    *   Displays overall statistics and sample reviews.
*   **Data Export:** Allows users to download both raw and analyzed review data in CSV format.

---

## 🚀 Technologies Used

*   **Backend:** Python
*   **Web Framework:** Flask
*   **Web Scraping:**
    *   Selenium (for browser automation and dynamic content)
    *   BeautifulSoup4 (for HTML parsing)
*   **Natural Language Processing:**
    *   NLTK (Natural Language Toolkit)
    *   VADER (Valence Aware Dictionary and sEntiment Reasoner) for sentiment analysis
*   **Data Handling & Analysis:**
    *   Pandas (for data manipulation)
*   **Data Visualization:**
    *   Matplotlib
    *   Seaborn
*   **Frontend (Styling):**
    *   HTML, CSS
    *   Bootstrap (for responsive design)

---

## 🖼️ Screenshots

*(Consider adding screenshots of your application here. For example:)*

**Figure 1: Homepage with URL input form**
![Homepage](https://github.com/user-attachments/assets/abddf4f0-8010-45d3-a7d7-b287ee3a44f7)

**Figure 2: Results page with sentiment analysis visualizations**
![image](https://github.com/user-attachments/assets/c7e3e552-f908-405e-bdc0-9663fb154e35)


---

## ⚙️ System Architecture Overview

The system follows a modular architecture:

1.  **Scraper Module:** Handles URL processing, web navigation (using Selenium), and data extraction (using BeautifulSoup) from Flipkart product pages.
2.  **Analyzer Module:** Processes extracted review text and ratings. This includes text preprocessing (emoji conversion, special character removal), sentiment scoring with VADER, rating normalization, and combining scores. It also handles keyword extraction.
3.  **Web Application (Flask):** Manages user interaction (URL input), orchestrates the scraping and analysis process, generates visualizations using Matplotlib/Seaborn, and presents the results on a web interface. It also handles data export.

**Data Flow:**
1.  User submits a Flipkart product URL via the web interface.
2.  The Scraper Module extracts reviews.
3.  The Analyzer Module processes these reviews to generate sentiment scores and insights.
4.  The Web Application displays these insights through statistics, visualizations, and sample reviews.
5.  User can download the analyzed data.

---

## 🛠️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/flipkart-review-sentiment-analyzer.git
    cd flipkart-review-sentiment-analyzer
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    Ensure you have a `requirements.txt` file. If not, create one using `pip freeze > requirements.txt` after installing packages manually.
    ```bash
    pip install -r requirements.txt
    ```
    dependencies include: `flask`, `selenium`, `beautifulsoup4`, `nltk`, `pandas`, `matplotlib`, `seaborn`, `requests` (often used with BeautifulSoup).

4.  **Download NLTK resources (VADER lexicon):**
    Run Python and execute:
    ```python
    import nltk
    nltk.download('vader_lexicon')
    # You might also need 'stopwords' if you are using it for keyword extraction
    nltk.download('stopwords')
    ```

5.  **Setup WebDriver:**
    Selenium requires a WebDriver to interface with the chosen browser.
    *   Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Google Chrome, GeckoDriver for Firefox).
    *   Ensure the WebDriver executable is in your system's PATH or specify its path in your Selenium configuration within the code.
    *   Example: If using Chrome, download ChromeDriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

---

## ▶️ How to Run

1.  Ensure all dependencies and NLTK resources are installed and WebDriver is set up.
2.  Navigate to the project directory.
3.  Run the Flask application:
    ```bash
    python app.py
    ```
    (Or whatever your main Flask script is named).
4.  Open your web browser and go to `http://127.0.0.1:5000/` (or the address shown in your terminal).
5.  Enter a Flipkart product URL into the input form and submit to see the sentiment analysis.

---

## ⚖️ Methodology Highlights

*   **Web Scraping:**
    *   **Dynamic Content Handling:** Selenium WebDriver clicks "READ MORE" buttons to fetch full review text.
    *   **Robust Parsing:** BeautifulSoup extracts customer names, review titles, star ratings, and comments.
    *   **Pagination:** Scraper iterates through multiple review pages.
*   **Sentiment Analysis:**
    *   **Preprocessing:** Emoji conversion, special character removal, lowercasing.
    *   **VADER Scoring:** Generates compound sentiment scores (-1 to +1).
    *   **Rating Integration:** `Sentiment_Score = 0.7 * Text_Score + 0.3 * Rating_Normalized`
    *   **Classification:** Positive, neutral, or negative, with special handling for 3-star reviews.
    *   **Keyword Extraction:** Identifies frequent terms in positive/negative reviews after stop word removal.

---

## 🚧 Limitations and Challenges

1.  **Web Scraping Reliability:** The scraper is dependent on Flipkart's HTML structure and may break if the website's design changes.
2.  **Language Limitations:** Currently optimized for English reviews.
3.  **Contextual Understanding:** VADER may not capture complex nuances like sarcasm or deep context.
4.  **Processing Time:** Scraping and analyzing a large number of reviews can be time-consuming.
5.  **Anti-Scraping Measures:** Flipkart might implement more robust anti-scraping techniques that could block the scraper.

---

## 💡 Future Enhancements

*   Implement more robust error handling and logging for the scraper.
*   Add support for multiple languages.
*   Explore more advanced NLP models (e.g., transformer-based models like BERT) for better contextual understanding.
*   Optimize scraping speed (e.g., using asynchronous requests or distributed scraping).
*   Develop strategies to handle CAPTCHAs or other anti-scraping measures.
*   Add user accounts and history of analyzed products.

---

## 📜 References

1.  Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text.
2.  Mitchell, R. (2018). Web Scraping with Python: Collecting More Data from the Modern Web.
3.  Selenium Documentation.
4.  Beautiful Soup Documentation.
5.  Flask Documentation.
6.  NLTK Documentation.
7.  Pandas Documentation.
8.  Matplotlib Documentation.

---

