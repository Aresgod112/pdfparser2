from flask import Flask, redirect, url_for, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PDF Parser</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                color: #1E88E5;
            }
            .container {
                border: 1px solid #ddd;
                padding: 20px;
                border-radius: 5px;
                margin-top: 20px;
            }
            .note {
                background-color: #f8f9fa;
                padding: 15px;
                border-left: 4px solid #1E88E5;
                margin-bottom: 20px;
            }
            .button {
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <h1>📄 Contract PDF Parser</h1>
        
        <div class="note">
            <strong>Note:</strong> This application is designed to run locally with Streamlit, which is not fully compatible with Vercel's serverless environment.
        </div>
        
        <div class="container">
            <h2>About This Application</h2>
            <p>The PDF Parser application extracts key information from contract PDFs:</p>
            <ul>
                <li>Effective Date</li>
                <li>Start Date</li>
                <li>Initial Term</li>
                <li>Further Term</li>
            </ul>
            <p>It supports both text-based PDFs and scanned documents (using OCR).</p>
            
            <h2>How to Run This Application</h2>
            <p>To use this application, you need to run it locally:</p>
            <ol>
                <li>Clone the repository from GitHub</li>
                <li>Install the required dependencies with <code>pip install -r requirements.txt</code></li>
                <li>Run the application with <code>streamlit run app.py</code></li>
            </ol>
            
            <a href="https://github.com/Aresgod112/PDF-Parser" class="button">View on GitHub</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
