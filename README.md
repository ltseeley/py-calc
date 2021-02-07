# Logan Seeley's Web-Based Calculator

This is a simple web-based calculator that allows users to evaluate mathematical
formulas and view the most recently performed calculations. The log of recent
calculations is persistent and shared across clients. When a calculation is
performed by one client, it is pushed to all other clients in real-time.

## Getting Started

### Running Locally with Python

To run this application on your local operating system, you will need to have
[Python installed](https://www.python.org/downloads/).

1. Install required dependencies using the Python package installer (`pip`):

   ```
   $ pip install -r requirements.txt
   ```

1. Run the app:

   ```
   $ FLASK_APP=main.py flask run
   ```

1. Navigate to `http://localhost:5000` in your web browser to access the running
   application

### Running Locally with Docker

This application may be run locally using
[Docker](https://docs.docker.com/get-docker/).

1. Build the Docker image:

   ```
   $ docker build -t py-calc .
   ```

1. Run the docker container:

   ```
   $ docker run --env PORT=5000 -p 5000:5000 py-calc
   ```

1. Navigate to `http://localhost:5000` in your web browser to access the running
   application

### Deploying with Google Cloud Run

This application can be deployed to Google Cloud Run. This requires a Google
account.

1. Select or create a Google Cloud project using the
[Google Cloud Console](https://console.cloud.google.com/projectselector2/home/dashboard)

1. Install and initialize the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

1. Build and deploy the application to Google Cloud Run, following the on-screen
   prompts:

   ```
   $ export PROJECT_ID=$(gcloud config get-value project)
   $ gcloud builds submit --tag gcr.io/$PROJECT_ID/py-calc
   $ gcloud run deploy --image gcr.io/$PROJECT_ID/py-calc --platform managed
   ```

1. When complete, the last command execute in the previous step will display the
   URL of deployed application; navigate to that URL in your web browser to
   access the application.
