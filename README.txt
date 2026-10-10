TELECOMINSIGHT BW - STARTER APPLICATION

Requirements: Python 3.10+, VS Code, internet for installing packages.

WINDOWS SETUP
1. Extract this ZIP file.
2. In VS Code, choose File > Open Folder and open the extracted folder.
3. Choose Terminal > New Terminal.
4. Create a virtual environment:
   py -m venv .venv
5. Activate it in PowerShell:
   .\.venv\Scripts\Activate.ps1
   If PowerShell blocks activation, use Command Prompt terminal and run:
   .venv\Scripts\activate.bat
6. Install packages:
   python -m pip install -r requirements.txt
7. Run the app:
   python -m streamlit run app.py
8. Open the Local URL printed in the terminal if your browser does not open automatically.

MACOS / LINUX
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py

CSV columns required:
date, provider, location, issue_type, download_mbps, upload_mbps,
latency_ms, satisfaction, complaint_reported

IMPORTANT: Sample data is fictional demonstration data. It is not real network
measurement data and should not be used to make claims about actual providers.
