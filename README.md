# About Project
This project is a website that searches for quotes within transcripts conducted with Jazz Musicians through a query and label filters.

Use:
run "pip install -r Utilities/requirements.txt" to get correct packages
unzip API key and enter correct password
run "python3 Utilities/download_data.py" to get all data (this will take a few minutes, but only needs to be done once)

IF RUNNING LOCALLY:
Open two terminals/command lines, both within the Website directory.
In Terminal 1: run "python -m http.server 8000". It should print "Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ..." or similar, and remain open. Leave running.
In Terminal 2: run "python jazzDataModule.py" (or python file running equivalent). It may take a moment, but it should print " * Running on http://127.0.0.1:5000" or similar, and remain open with some additional information. Leave running.
Open your browser and navigate to "http://localhost:8000/results_v1.html". This will only load if Terminal 1 is active, and will only produce results if Terminal 2 is also active.
