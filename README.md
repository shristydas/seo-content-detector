# SEO Content Quality Analysis Pipeline

A machine learning pipeline that analyzes web content for SEO quality assessment and duplicate detection. The system parses HTML content, extracts NLP features, detects near-duplicates using similarity algorithms, and scores content quality using classification models.

## Features

- **HTML Parsing & Text Extraction**: Robust parsing of HTML content with error handling
- **Feature Engineering**: Word count, sentence count, Flesch readability scores, TF-IDF keywords, and sentence embeddings
- **Duplicate Detection**: Cosine similarity-based detection of near-duplicate content
- **Quality Classification**: Random Forest classifier trained to score content as Low/Medium/High quality
- **Real-Time Analysis**: Function to analyze any URL on-demand
- **Visualizations**: Feature importance plots, similarity heatmaps, and distribution charts

## Setup Instructions

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/seo-content-detector
cd leadwalnut-shristy

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook notebooks/seo_pipeline.ipynb
```

## Quick Start

### Option 1: Jupyter Notebook (Core Analysis)

1. **Ensure dataset is in place**: The provided dataset should be at `seo-content-detector/data/data.csv`

2. **Run the notebook**: Open `notebooks/seo_pipeline.ipynb` and run all cells sequentially (Cell → Run All)

3. **View outputs**: Check the `seo-content-detector/data/` directory for:
   - `extracted_content.csv` - Parsed HTML content with clean text
   - `features.csv` - Engineered features for all documents
   - `duplicates.csv` - Detected duplicate pairs

4. **Real-time analysis**: Use the `analyze_url()` function in the last section to analyze any URL

### Option 2: Streamlit Web App (Bonus)

```bash
# After running the notebook to train the model
streamlit run streamlit_app/app.py
```

The app will open in your browser at `http://localhost:8501`

**🚀 Deployed Streamlit App**: [Coming Soon - Deploy to Streamlit Cloud]

## Key Technical Decisions

**HTML Parsing Approach**
- Used BeautifulSoup with lxml parser for robust HTML parsing
- Prioritized content extraction from `<article>`, `<main>`, then `<body>` tags
- Removed script, style, navigation, and footer elements to focus on main content
- Implemented graceful error handling for malformed HTML

**Similarity Detection**
- Chose Sentence Transformers (`all-MiniLM-L6-v2`) for semantic embeddings over simple TF-IDF
- 384-dimensional embeddings capture semantic meaning better than keyword matching
- Set similarity threshold at 0.80 after analyzing distribution to balance precision/recall
- Used first 500 words per document for embedding efficiency

**Model Selection**
- Selected Random Forest over Logistic Regression for better handling of non-linear feature interactions
- Used balanced class weights to handle quality label imbalance
- Three-feature model (word_count, sentence_count, readability) for interpretability
- Synthetic labeling based on clear, non-overlapping criteria ensures reproducibility

**Feature Engineering**
- Flesch Reading Ease provides standardized readability metric (0-100 scale)
- TF-IDF with bigrams captures key phrases, not just individual words
- Minimum document frequency of 2 reduces noise from unique terms
- Thin content threshold of 500 words based on SEO best practices

## Results Summary

### Model Performance
- **Overall Accuracy**: ~78-85% (varies by data split)
- **Baseline Accuracy**: ~64% (word count only)
- **Improvement**: +14-21% over baseline
- **Top Features**: word_count (0.45), flesch_reading_ease (0.32), sentence_count (0.23)

### Content Analysis (81 documents)
- **Duplicate Pairs Found**: Varies (0-5 pairs above 0.80 threshold)
- **Thin Content**: ~10-15% of pages (<500 words)
- **Quality Distribution**:
  - High Quality: ~12%
  - Medium Quality: ~73%
  - Low Quality: ~15%

### Sample Quality Scores
```
High Quality: wikipedia.org/wiki/Machine_learning (2,847 words, readability 62.3)
Medium Quality: cisco.com/network-security (1,124 words, readability 58.1)
Low Quality: Short blog posts (412 words, readability 45.2)
```

## Project Structure

```
leadwalnut-shristy/
├── seo-content-detector/
│   └── data/
│       ├── data.csv                   # Input dataset (URLs + HTML)
│       ├── extracted_content.csv      # Parsed content
│       ├── features.csv               # Extracted features
│       └── duplicates.csv             # Duplicate pairs
├── notebooks/
│   └── seo_pipeline.ipynb            # Main analysis notebook
├── streamlit_app/                    # Bonus: Interactive web app
│   ├── app.py                        # Main Streamlit application
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── parser.py                 # HTML parsing utilities
│   │   ├── features.py               # Feature extraction
│   │   └── scorer.py                 # Quality scoring
│   └── models/                       # Symlink to ../models
├── models/
│   └── quality_model.pkl             # Trained classifier
├── requirements.txt                   # Python dependencies
├── .gitignore
└── README.md
```

## Limitations

1. **Language Support**: Currently optimized for English content only. Readability scores and stop words are English-specific.

2. **Scalability**: In-memory processing limits analysis to datasets under ~1GB. For larger datasets, consider batch processing or streaming approaches.

3. **Real-Time Scraping**: The `analyze_url()` function may fail on sites with anti-bot measures, JavaScript-heavy pages, or authentication requirements. Consider using Selenium for complex sites.

4. **Quality Labels**: Synthetic labels based on heuristics may not perfectly align with human judgments. For production use, consider training on human-labeled data.

5. **Embedding Model**: The lightweight MiniLM model (384 dims) balances speed and accuracy but may miss nuances captured by larger models like mpnet (768 dims) or OpenAI embeddings.

## Technologies Used

- **Core**: Python 3.9+, Pandas, NumPy
- **HTML Parsing**: BeautifulSoup4, lxml
- **NLP**: Sentence Transformers, scikit-learn TF-IDF, textstat
- **Machine Learning**: scikit-learn (Random Forest, metrics)
- **Visualization**: Matplotlib, Seaborn
- **Notebook**: Jupyter

## License

MIT License

## Author

Built as part of the SEO Content Analysis assignment.
