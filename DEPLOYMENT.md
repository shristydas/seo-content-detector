# Deployment Guide - Streamlit Cloud

This guide walks through deploying the SEO Content Quality Analyzer to Streamlit Cloud.

## Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at https://streamlit.io/cloud)
3. Completed notebook run (trained model in `models/quality_model.pkl`)

## Step 1: Prepare Repository

```bash
# Ensure all files are committed
git add .
git commit -m "Complete SEO analyzer with Streamlit app"
git push origin main
```

## Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io/

2. **Click "New app"**

3. **Configure deployment**:
   - Repository: `yourusername/leadwalnut-shristy`
   - Branch: `main`
   - Main file path: `streamlit_app/app.py`

4. **Advanced settings** (optional):
   - Python version: 3.9+
   - Add secrets if needed

5. **Click "Deploy"**

The app will build and deploy automatically. First deployment takes 2-3 minutes.

## Step 3: Update README

Once deployed, update the README.md with your deployed URL:

```markdown
**🚀 Deployed Streamlit App**: https://your-app-name.streamlit.app
```

## Important Notes

### Model File Size

The trained model (`quality_model.pkl`) must be in the repository. If it's too large (>100MB), consider:

1. Using Git LFS:
   ```bash
   git lfs install
   git lfs track "models/*.pkl"
   git add .gitattributes models/quality_model.pkl
   git commit -m "Add model with LFS"
   ```

2. Or training the model on-demand (add training code to Streamlit app)

### Dependencies

Streamlit Cloud automatically installs from `requirements.txt`. Ensure all versions are pinned for reproducibility.

### Data Files

For the demo app to work with similar content detection, you need the processed data files. Options:

1. **Include in repo** (if < 10MB): Commit `data/features.csv`
2. **Download on-demand**: Modify app to download from external source
3. **Disable feature**: Remove similarity detection from app

## Troubleshooting

**Build fails**:
- Check requirements.txt has correct versions
- Verify Python version compatibility
- Check logs in Streamlit Cloud dashboard

**Model not found**:
- Ensure `models/quality_model.pkl` is in repository
- Check file path in `scorer.py` is correct

**Import errors**:
- Verify all dependencies in requirements.txt
- Check for typos in import statements

## Performance Optimization

For faster loading:

1. Use `@st.cache_resource` for model loading (already implemented)
2. Consider smaller model variants
3. Optimize embedding generation

## Security

- Never commit API keys or secrets
- Use Streamlit secrets management for sensitive data
- Validate and sanitize all user inputs
