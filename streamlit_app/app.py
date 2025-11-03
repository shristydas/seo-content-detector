"""
SEO Content Quality Analyzer - Streamlit App
"""
import streamlit as st
import requests
from pathlib import Path
import sys

# Add utils to path
sys.path.append(str(Path(__file__).parent))

from utils.parser import parse_html_content, clean_text
from utils.features import extract_features
from utils.scorer import load_model, predict_quality, calculate_quality_score

# Page config
st.set_page_config(
    page_title="SEO Content Quality Analyzer",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("🔍 SEO Content Quality Analyzer")
st.markdown("""
Analyze web content for SEO quality. This tool extracts text from any URL and provides:
- **Content metrics**: word count, readability, structure
- **Quality score**: ML-based quality classification
- **Actionable insights**: recommendations for improvement
""")

# Sidebar
st.sidebar.header("About")
st.sidebar.info("""
This application uses machine learning to analyze web content quality based on:
- Word count
- Readability (Flesch Reading Ease)
- Content structure

Built with Python, Streamlit, and scikit-learn.
""")

# Load model
@st.cache_resource
def get_model():
    """Load the trained model (cached)."""
    try:
        model, feature_columns = load_model()  # Uses automatic path resolution
        return model, feature_columns
    except Exception as e:
        st.error(f"⚠️ Could not load model: {str(e)}")
        st.info("Please ensure the notebook has been run to train the model.")
        return None, None

model, feature_columns = get_model()

# Main input
# Check if we have an example URL in session state
default_url = st.session_state.get('selected_url', '')

url_input = st.text_input(
    "Enter a URL to analyze:",
    value=default_url,
    placeholder="https://example.com/article",
    help="Enter any publicly accessible URL"
)

analyze_button = st.button("🚀 Analyze Content", type="primary")

# Auto-trigger analysis if URL was set from example
if 'trigger_analysis' in st.session_state and st.session_state.trigger_analysis:
    analyze_button = True
    st.session_state.trigger_analysis = False

if analyze_button and url_input:
    if not url_input.startswith(('http://', 'https://')):
        st.error("⚠️ Please enter a valid URL starting with http:// or https://")
    else:
        with st.spinner("Fetching and analyzing content..."):
            try:
                # Fetch URL
                response = requests.get(
                    url_input,
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                response.raise_for_status()

                # Parse HTML
                parsed = parse_html_content(response.text)

                if parsed.get('error'):
                    st.error(f"⚠️ Parsing error: {parsed['error']}")
                elif parsed['word_count'] == 0:
                    st.warning("⚠️ No content extracted. The page might be JavaScript-heavy or empty.")
                else:
                    # Extract features
                    clean_txt = clean_text(parsed['body_text'])
                    features = extract_features(parsed['body_text'])

                    # Predict quality
                    if model is not None:
                        quality_label = predict_quality(model, features, feature_columns)
                    else:
                        quality_label = "Unknown"

                    quality_score = calculate_quality_score(features)

                    # Display results
                    st.success("✅ Analysis complete!")

                    # Title
                    st.subheader("📄 Page Information")
                    st.write(f"**Title:** {parsed['title']}")
                    st.write(f"**URL:** {url_input}")

                    # Metrics
                    st.subheader("📊 Content Metrics")
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Word Count", f"{features['word_count']:,}")

                    with col2:
                        st.metric("Sentences", features['sentence_count'])

                    with col3:
                        readability = features['flesch_reading_ease']
                        st.metric("Readability", f"{readability:.1f}")

                    with col4:
                        st.metric("Quality Score", f"{quality_score}/100")

                    # Quality assessment
                    st.subheader("🎯 Quality Assessment")

                    # Color-coded quality label
                    label_colors = {
                        'High': '🟢',
                        'Medium': '🟡',
                        'Low': '🔴'
                    }
                    quality_icon = label_colors.get(quality_label, '⚪')

                    st.markdown(f"### {quality_icon} {quality_label} Quality Content")

                    # Progress bar
                    progress_color = "green" if quality_score >= 70 else "orange" if quality_score >= 50 else "red"
                    st.progress(quality_score / 100)

                    # Recommendations
                    st.subheader("💡 Recommendations")

                    recommendations = []

                    if features['word_count'] < 500:
                        recommendations.append("⚠️ **Thin content**: Consider expanding to at least 500-1500 words for better SEO.")
                    elif features['word_count'] < 1000:
                        recommendations.append("✅ **Good length**: Consider adding more depth to reach 1500+ words for comprehensive coverage.")
                    else:
                        recommendations.append("✅ **Excellent length**: Your content has substantial depth.")

                    if readability < 40:
                        recommendations.append("⚠️ **Difficult to read**: Simplify sentences and use clearer language (target 50-70).")
                    elif readability > 80:
                        recommendations.append("⚠️ **Too simple**: Consider adding more sophisticated content for authority.")
                    else:
                        recommendations.append("✅ **Good readability**: Your content is accessible to most readers.")

                    if features['sentence_count'] > 0:
                        avg_words = features['word_count'] / features['sentence_count']
                        if avg_words > 30:
                            recommendations.append("⚠️ **Long sentences**: Break up complex sentences (target 15-25 words/sentence).")
                        elif avg_words < 10:
                            recommendations.append("⚠️ **Very short sentences**: Vary sentence length for better flow.")
                        else:
                            recommendations.append("✅ **Good sentence structure**: Well-balanced sentence length.")

                    for rec in recommendations:
                        st.markdown(rec)

                    # Content preview
                    with st.expander("📝 Content Preview (first 500 characters)"):
                        preview = parsed['body_text'][:500] + "..." if len(parsed['body_text']) > 500 else parsed['body_text']
                        st.text(preview)

            except requests.RequestException as e:
                st.error(f"⚠️ Failed to fetch URL: {str(e)}")
                st.info("Make sure the URL is accessible and doesn't require authentication.")
            except Exception as e:
                st.error(f"⚠️ Analysis error: {str(e)}")

# Example URLs
st.markdown("---")
st.subheader("🎯 Try These Example URLs")

example_urls = {
    "Wikipedia: Machine Learning": "https://en.wikipedia.org/wiki/Machine_learning",
    "Cisco: Network Security": "https://www.cisco.com/site/us/en/learn/topics/security/what-is-network-security.html",
    "Wikipedia: AI": "https://en.wikipedia.org/wiki/Artificial_intelligence"
}

cols = st.columns(len(example_urls))
for i, (label, url) in enumerate(example_urls.items()):
    with cols[i]:
        if st.button(label, key=f"example_{i}", use_container_width=True):
            st.session_state.selected_url = url
            st.session_state.trigger_analysis = True
            st.rerun()
        # Show URL preview below button
        st.caption(url)

# Footer
st.markdown("---")
st.caption("Built with Streamlit • Machine Learning • NLP")
