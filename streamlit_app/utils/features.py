"""Feature extraction utilities."""
import re
import textstat


def count_sentences(text):
    """Count sentences in text."""
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])


def calculate_readability(text):
    """Calculate Flesch Reading Ease score."""
    try:
        if len(text) < 100:
            return 0.0
        return textstat.flesch_reading_ease(text)
    except:
        return 0.0


def extract_features(text):
    """
    Extract all features from text.

    Returns:
        dict with features
    """
    word_count = len(text.split())
    sentence_count = count_sentences(text)
    readability = calculate_readability(text)

    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'flesch_reading_ease': readability
    }
