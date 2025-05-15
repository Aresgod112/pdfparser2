# Vercel Deployment Notes

## Important: Streamlit Limitations on Vercel

Streamlit applications are designed to run as long-running processes, which is not compatible with Vercel's serverless architecture. Vercel functions have execution time limits and are stateless, which conflicts with Streamlit's stateful, interactive nature.

## Current Deployment

The current Vercel deployment provides a simple landing page that:
1. Explains what the PDF Parser application does
2. Directs users to the GitHub repository
3. Provides instructions for running the application locally

## Why Streamlit Doesn't Work on Vercel

Streamlit applications:
- Run as continuous processes
- Maintain state between interactions
- Use websockets for real-time updates
- Often exceed Vercel's function execution time limits

## Alternative Deployment Options

If you want to deploy the full Streamlit application, consider these platforms:
1. **Streamlit Cloud** - Specifically designed for Streamlit apps: https://streamlit.io/cloud
2. **Heroku** - Can run long-running processes
3. **AWS, GCP, or Azure** - Using container services like ECS, GKE, or AKS
4. **DigitalOcean** - Using App Platform or Droplets

## Local Development

The application works perfectly when run locally. To run it:

```bash
# Clone the repository
git clone https://github.com/Aresgod112/PDF-Parser.git
cd PDF-Parser

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

This will start the Streamlit server and open the application in your browser.
