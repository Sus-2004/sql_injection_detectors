# SQL Injection Detector (Flask)

## Setup (VS Code)
1. Clone/copy the project folder `sql_injection_detector/`.
2. Create a virtual environment:
   - `python -m venv venv`
   - Activate:
     - Windows: `venv\Scripts\activate`
     - macOS/Linux: `source venv/bin/activate`
3. Install requirements:
   - `pip install -r requirements.txt`
4. Run the app:
   - `python app.py`
   - Visit `http://127.0.0.1:5000`

NB: The SQLite DB will be created at `instance/app.db`.

## Deployment
You can deploy this Flask app to free platforms such as Render, Railway, or PythonAnywhere.
(You asked earlier to avoid GitHub for deployment — Render and PythonAnywhere allow direct uploads / linking with CLI.)