import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import emoji
import re
import pandas as pd

# Download required NLTK resources
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def convert_emojis_to_text(text):
    """Convert emojis to text descriptions"""
    if not isinstance(text, str):
        return ""
    return emoji.demojize(text)

def preprocess_text(text):
    """ preprocess text for sentiment analysis"""
    if not isinstance(text, str):
        return ""
    #  keeping emoji descriptions
    text_clean = re.sub(r'[^\w\s:_]', ' ', text)
    return text_clean.lower()

def classify_sentiment_with_rating(score, rating):
    """Classify sentiment based on combined score and original rating"""
    
    if rating == 3.0:
        if score > 0.3:  # Only very positive text can override
            return 'Positive'
        elif score < -0.3:  # Only very negative text can override
            return 'Negative'
        else:
            return 'Neutral'
    
    
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def get_top_words(text_series, n=10):
    """Extract the most common words from a series of text"""
    # Combine all text
    all_text = ' '.join(text_series).lower()
    # Tokenize
    tokens = word_tokenize(all_text)
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words and len(word) > 2]
    # Count and return top n words
    word_counts = Counter(filtered_tokens)
    return word_counts.most_common(n)

def analyze_sentiment(df):
    """Perform sentiment analysis on review data"""
    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Convert emojis to text in the Comment column
    df['Comment'] = df['Comment'].apply(convert_emojis_to_text)
    
    # Create a combined text field that includes both the review title and comment
    df['Combined_Text'] = df['Review Title'].fillna('').apply(convert_emojis_to_text) + ' ' + df['Comment'].fillna('')
    df['Combined_Text'] = df['Combined_Text'].apply(preprocess_text)
    
    # Apply sentiment analysis to combined text (title + comment)
    df['Sentiment_Score_Text'] = df['Combined_Text'].apply(lambda x: sia.polarity_scores(x)['compound'])
    
    # Convert numeric ratings to float
    df['Rating_Numeric'] = df['Rating'].astype(float)
    
    # Normalize ratings to a -1 to 1 scale for compatibility with sentiment scores
    df['Rating_Normalized'] = (df['Rating_Numeric'] - 3) / 2  # Maps 1→-1, 3→0, 5→1
    
    # Combine sentiment from text analysis and ratings
    df['Sentiment_Score'] = 0.7 * df['Sentiment_Score_Text'] + 0.3 * df['Rating_Normalized']
    
    # Classify sentiment using the new function that considers both score and rating
    df['Sentiment'] = df.apply(
        lambda row: classify_sentiment_with_rating(row['Sentiment_Score'], row['Rating_Numeric']), 
        axis=1
    )
    
    # Calculate overall statistics
    overall_stats = {
        'Average_Rating': df['Rating_Numeric'].mean(),
        'Average_Sentiment_Score': df['Sentiment_Score'].mean(),
        'Positive_Reviews': df['Sentiment'].value_counts().get('Positive', 0),
        'Neutral_Reviews': df['Sentiment'].value_counts().get('Neutral', 0),
        'Negative_Reviews': df['Sentiment'].value_counts().get('Negative', 0),
        'Total_Reviews': len(df)
    }
    
    # Calculate percentages
    if overall_stats['Total_Reviews'] > 0:  # Avoid division by zero
        overall_stats['Positive_Percentage'] = (overall_stats['Positive_Reviews'] / overall_stats['Total_Reviews']) * 100
        overall_stats['Neutral_Percentage'] = (overall_stats['Neutral_Reviews'] / overall_stats['Total_Reviews']) * 100
        overall_stats['Negative_Percentage'] = (overall_stats['Negative_Reviews'] / overall_stats['Total_Reviews']) * 100
    else:
        overall_stats['Positive_Percentage'] = 0
        overall_stats['Neutral_Percentage'] = 0
        overall_stats['Negative_Percentage'] = 0
    
    # Get top words for each sentiment category
    positive_df = df[df['Sentiment'] == 'Positive']
    negative_df = df[df['Sentiment'] == 'Negative']
    neutral_df = df[df['Sentiment'] == 'Neutral']
    
    if not positive_df.empty:
        overall_stats['Top_Positive_Words'] = get_top_words(positive_df['Combined_Text'], 10)
    else:
        overall_stats['Top_Positive_Words'] = []
        
    if not negative_df.empty:
        overall_stats['Top_Negative_Words'] = get_top_words(negative_df['Combined_Text'], 10)
    else:
        overall_stats['Top_Negative_Words'] = []
        
    if not neutral_df.empty:
        overall_stats['Top_Neutral_Words'] = get_top_words(neutral_df['Combined_Text'], 10)
    else:
        overall_stats['Top_Neutral_Words'] = []
    
    return df, overall_stats