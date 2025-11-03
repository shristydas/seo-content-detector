# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies (2 min)

```bash
# Navigate to project directory
cd leadwalnut-shristy

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

**Note**: First-time installation downloads ML models (~100MB). This is normal.

## Step 2: Run the Notebook (2 min)

```bash
# Launch Jupyter
jupyter notebook

# In browser: Open notebooks/seo_pipeline.ipynb
# Click: Cell → Run All
```

**Expected output**:
- Parsing progress messages
- Feature extraction logs
- Model training results
- Visualizations

**Time to complete**: ~2-3 minutes

## Step 3: Check Results (30 sec)

Navigate to `seo-content-detector/data/`:
- ✅ `extracted_content.csv` - Parsed text
- ✅ `features.csv` - ML features
- ✅ `duplicates.csv` - Similar pairs

## Step 4: Try Real-Time Analysis (30 sec)

In the notebook, scroll to the last section and run:

```python
result = analyze_url("https://en.wikipedia.org/wiki/Machine_learning")
print(json.dumps(result, indent=2))
```

## (Optional) Launch Streamlit App

```bash
# After running notebook to train model
streamlit run streamlit_app/app.py
```

Opens in browser at http://localhost:8501

## Troubleshooting

**Import errors**:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Jupyter kernel not found**:
```bash
python -m ipykernel install --user --name=venv
```

**Model not found**:
Run the notebook first to train and save the model.

**Out of memory**:
Close other applications. The pipeline needs ~2GB RAM.

## Test URLs

Try these in the real-time analyzer:
- https://en.wikipedia.org/wiki/Artificial_intelligence (High quality)
- https://www.cisco.com/site/us/en/learn/topics/security/what-is-network-security.html (Medium)

## What to Expect

### Dataset Analysis Output
```
Dataset loaded: 81 rows
Successfully parsed: 81 rows
Word count statistics:
  Mean: ~1200 words
  Min: ~100 words
  Max: ~4500 words
```

### Model Performance
```
Overall Accuracy: 0.78-0.85
Baseline Accuracy: 0.64
Improvement: +14-21%
```

### Duplicate Detection
```
Total pages analyzed: 81
Duplicate pairs: 0-5 (varies)
Thin content pages: ~10-15%
```

## Next Steps

1. ✅ Review visualizations in notebook
2. ✅ Examine CSV outputs
3. ✅ Test analyze_url() with your URLs
4. ✅ Launch Streamlit app for interactive demo
5. ✅ Read README.md for detailed documentation

## Need Help?

- **Setup issues**: Check README.md
- **Deployment**: See DEPLOYMENT.md
- **Technical details**: Review PROJECT_SUMMARY.md
- **Code understanding**: Read notebook comments

---

**Estimated total time**: 5 minutes + 2-3 min processing
