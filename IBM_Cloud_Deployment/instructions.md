# IBM Cloud Deployment Guide

This document describes how to deploy the **"Rising Waters: A Machine Learning Approach to Flood Prediction"** Flask application to **IBM Cloud**.

The project is structured with production-ready standards and includes a `Procfile` and `runtime.txt`, making it ready for deployment using either **IBM Cloud Code Engine** (recommended modern container service) or **IBM Cloud Foundry Buildpacks**.

---

## Deployment Option 1: IBM Cloud Code Engine (Recommended)

IBM Cloud Code Engine is a fully managed, serverless platform that runs containerized workloads, including web apps, microservices, and event-driven functions from source code directly.

### Prerequisites
1. Install the [IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cli-install-ibmcloud-cli).
2. Install the Code Engine plugin:
   ```bash
   ibmcloud plugin install code-engine
   ```
3. Ensure you have your `flood.csv` uploaded and models trained locally, or build a pipeline that runs training during container startup. (Since model binaries are small, it is recommended to train models locally first, so `models/flood_model.pkl` and `models/scaler.pkl` are committed in the deployed source).

### Step-by-Step CLI Deployment

1. **Log in to IBM Cloud:**
   ```bash
   ibmcloud login -a cloud.ibm.com
   ```
   *(Add `--sso` at the end if your account uses Single Sign-On federation).*

2. **Target your Resource Group:**
   ```bash
   ibmcloud target -g Default
   ```
   *(Or replace `Default` with your custom resource group name).*

3. **Create a Code Engine Project:**
   ```bash
   ibmcloud ce project create --name FloodPredictionProject
   ```

4. **Select the Project:**
   ```bash
   ibmcloud ce project select --name FloodPredictionProject
   ```

5. **Deploy the application directly from source code:**
   Code Engine will automatically compile the Python environment, scan `requirements.txt`, identify the runtime, and launch the web server:
   ```bash
   ibmcloud ce app create --name rising-waters-app --build-source . --port 5000
   ```
   *(Note: The build process takes a few minutes as Code Engine compiles the code into a container behind the scenes).*

6. **Retrieve your URL:**
   Once completed, the CLI output will print the active HTTPS URL of your application (e.g., `https://rising-waters-app.xxxx.codeengine.appdomain.cloud`).

---

## Deployment Option 2: IBM Cloud Foundry (Legacy Buildpack)

If your organization utilizes Cloud Foundry Enterprise Environment or legacy Cloud Foundry buildpacks:

### Preparation
Make sure you have a `manifest.yml` file in the root of your project. Here is the manifest configuration for this application:

```yaml
---
applications:
  - name: rising-waters-flood-prediction
    memory: 512M
    instances: 1
    buildpacks:
      - python_buildpack
    env:
      PYTHONVERSION: 3.10.12
```

### Steps to Deploy
1. **Target Cloud Foundry Org and Space:**
   ```bash
   ibmcloud target --cf
   ```
2. **Push the application:**
   The Python buildpack automatically reads `runtime.txt` to select the python interpreter, runs `pip install -r requirements.txt` to install Scikit-learn, XGBoost, and Flask, and runs the command declared in `Procfile` (`web: gunicorn app:app`):
   ```bash
   ibmcloud cf push
   ```

---

## Verification
After successful deployment, test the endpoints:
- Homepage: `https://<your-app-domain>/`
- Predictions: Input sample values and check the probability calculations.
- PDF Download: Generate a prediction and verify that the client-side report compiles and downloads without warning tags.
