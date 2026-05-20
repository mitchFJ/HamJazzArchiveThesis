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

To upload to AWS:
1. run "pip install -r Utilities/requirements.txt"
2. Use "aws configure" and follow the instructions to add AWS login info
3. copy the encodings.npy, exctracted_text.csv, and data_line_number.json from Data into Dockerinfo/Data.
4. Navigate into the Dockerinfo directory
5. Authenticate with aws with the command "aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com"
6. Create the docker image with "docker build --platform linux/amd64 --provenance=false -t <ecr name> ."
7. Tag the docker image with "docker tag <ecr name> <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<ecr name>:latest"
8. Push the docker image to AWS with "docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<ecr name>:latest"

A temporary link to this code can be found here: http://fillius-jazz-archive-014467817391-us-east-2-an.s3-website.us-east-2.amazonaws.com
