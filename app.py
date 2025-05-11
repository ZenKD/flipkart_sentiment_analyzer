from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import time
import uuid
import numpy as np
from flask import send_file

from utils.scraper import scrape_flipkart_reviews
from utils.analyzer import analyze_sentiment

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Create a directory for temporary files
if not os.path.exists('static/temp'):
    os.makedirs('static/temp')

def convert_to_serializable(obj):
    """Convert NumPy types to Python native types for JSON serialization"""
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_to_serializable(i) for i in obj)
    else:
        return obj

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_url = request.form.get('product_url')
        
        if not product_url or 'flipkart.com' not in product_url:
            flash('Please enter a valid Flipkart product URL')
            return redirect(url_for('index'))
        
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        try:
            # Scrape reviews
            flash('Scraping reviews... This may take a minute.')
            df = scrape_flipkart_reviews(product_url, pages=2)  # Adjust number of pages as needed
            
            if df.empty or len(df) == 0:
                flash('No reviews found for this product.')
                return redirect(url_for('index'))
                
            # Save raw data
            temp_csv = f'static/temp/{session_id}_raw_data.csv'
            df.to_csv(temp_csv, index=False)
            session['raw_data_path'] = temp_csv
            
            # Analyze sentiment
            df_analyzed, overall_stats = analyze_sentiment(df)
            
            # Save analyzed data
            analyzed_csv = f'static/temp/{session_id}_analyzed_data.csv'
            df_analyzed.to_csv(analyzed_csv, index=False)
            session['analyzed_data_path'] = analyzed_csv
            session['overall_stats'] = convert_to_serializable(overall_stats)  # Convert NumPy types
            
            # Generate visualizations
            viz_paths = generate_visualizations(df_analyzed, session_id)
            session['viz_paths'] = convert_to_serializable(viz_paths)  # Convert if needed
            
            return redirect(url_for('results'))
            
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/results')
def results():
    if 'session_id' not in session:
        flash('Please submit a product URL first')
        return redirect(url_for('index'))
    
    # Get data from session
    overall_stats = session.get('overall_stats', {})
    viz_paths = session.get('viz_paths', {})
    
    # Read a sample of the reviews to display
    df = pd.read_csv(session['analyzed_data_path'])
    sample_reviews = df.sample(min(10, len(df))).to_dict('records')
    
    return render_template(
        'results.html',
        stats=overall_stats,
        visualizations=viz_paths,
        sample_reviews=sample_reviews
    )

def generate_visualizations(df, session_id):
    """Generate and save visualizations for the results page"""
    viz_paths = {}
    
    # 1. Sentiment Distribution Pie Chart 
    plt.figure(figsize=(8, 6))
    sentiment_counts = df['Sentiment'].value_counts()
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', 
            colors=['#66b3ff', '#99ff99', '#ff9999'])
    plt.title('Sentiment Distribution of Reviews')
    plt.tight_layout()
    pie_chart_path = f'static/temp/{session_id}_sentiment_pie.png'
    plt.savefig(pie_chart_path)
    plt.close()
    viz_paths['pie_chart'] = pie_chart_path
    
    # 2. Rating vs Sentiment
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Rating_Numeric', hue='Sentiment', data=df, palette='viridis')
    plt.title('Rating Distribution by Sentiment Category')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.tight_layout()
    rating_chart_path = f'static/temp/{session_id}_rating_sentiment.png'
    plt.savefig(rating_chart_path)
    plt.close()
    viz_paths['rating_chart'] = rating_chart_path
    
    # 3. Text Sentiment vs Rating Correlation
    plt.figure(figsize=(8, 6))
    plt.scatter(df['Sentiment_Score_Text'], df['Rating_Normalized'], alpha=0.5)
    plt.xlabel('Text-based Sentiment Score')
    plt.ylabel('Normalized Rating Score')
    plt.title('Correlation between Text Sentiment and Rating')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.plot([-1, 1], [-1, 1], 'r--', alpha=0.7)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.tight_layout()
    correlation_path = f'static/temp/{session_id}_correlation.png'
    plt.savefig(correlation_path)
    plt.close()
    viz_paths['correlation'] = correlation_path
    
    return viz_paths

@app.route('/download/<file_type>')
def download(file_type):
    if 'session_id' not in session:
        flash('Session expired')
        return redirect(url_for('index'))
        
    if file_type == 'raw':
        file_path = session.get('raw_data_path', '')
        filename = 'flipkart_raw_reviews.csv'
    elif file_type == 'analyzed':
        file_path = session.get('analyzed_data_path', '')
        filename = 'flipkart_sentiment_analysis.csv'
    else:
        flash('Invalid file type')
        return redirect(url_for('results'))
    
    # Make sure the file path is absolute
    if not file_path.startswith('/'):
        file_path = os.path.join(os.getcwd(), file_path)
        
    if not os.path.exists(file_path):
        flash(f'File not found: {file_path}')
        return redirect(url_for('results'))
        
    return send_file(file_path, as_attachment=True, download_name=filename)

# Clean up temporary files periodically (in a production app, you'd use a task scheduler)
@app.route('/cleanup')
def cleanup():
    for file in os.listdir('static/temp'):
        file_path = os.path.join('static/temp', file)
        # Delete files older than 1 hour
        if os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) > 3600:
            os.remove(file_path)
    return 'Cleanup complete'

if __name__ == '__main__':
    app.run(debug=True)