# Deployment Guide

This guide will help you host your AI-Driven Stock Market Analysis application for free.

## Prerequisites
1.  **GitHub Account**: To host your code repository.
2.  **Render Account**: For hosting the Backend (Python/FastAPI).
3.  **Vercel Account**: For hosting the Frontend (React/Vite).

---

## Step 1: Push Code to GitHub

1.  Initialize a Git repository in your project folder (if not already done):
    ```bash
    git init
    ```
2.  Add all files:
    ```bash
    git add .
    ```
3.  Commit the changes:
    ```bash
    git commit -m "Initial commit for deployment"
    ```
4.  Create a new repository on GitHub.
5.  Link your local repository to GitHub and push:
    ```bash
    git remote add origin <YOUR_GITHUB_REPO_URL>
    git branch -M main
    git push -u origin main
    ```

---

## Step 2: Deploy Backend (Render)

1.  Log in to [Render](https://render.com/).
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub repository.
4.  Configure the service:
    *   **Name**: `stock-market-backend` (or similar)
    *   **Region**: Choose the one closest to you (e.g., Singapore, Oregon).
    *   **Branch**: `main`
    *   **Root Directory**: `backend` (Important!)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
    *   **Instance Type**: `Free`
5.  **Environment Variables**:
    Scroll down to "Environment Variables" and add the following keys from your `.env` file:
    *   `ALPHA_VANTAGE_KEY`: (Your Key)
    *   `NEWS_API_KEY`: (Your Key)
    *   `GEMINI_API_KEY`: (Your Key)
6.  Click **Create Web Service**.
7.  Wait for the deployment to finish. Copy the **Backend URL** (e.g., `https://stock-backend.onrender.com`).

---

## Step 3: Deploy Frontend (Vercel)

1.  Log in to [Vercel](https://vercel.com/).
2.  Click **Add New...** -> **Project**.
3.  Import your GitHub repository.
4.  Configure the project:
    *   **Framework Preset**: Vite (should be detected automatically).
    *   **Root Directory**: Click "Edit" and select `frontend`.
5.  **Environment Variables**:
    *   Expand the "Environment Variables" section.
    *   Key: `VITE_API_URL`
    *   Value: The **Backend URL** you copied from Render (e.g., `https://stock-backend.onrender.com`). **Note**: Do not add a trailing slash `/`.
6.  Click **Deploy**.

---

## Step 4: Verify

1.  Once Vercel finishes, click the domain link provided (e.g., `https://stock-frontend.vercel.app`).
2.  Test the application:
    *   Search for a stock (e.g., RELIANCE).
    *   Check if the chart loads.
    *   Check if the AI analysis works.

## Troubleshooting

*   **Backend Logs**: Check the "Logs" tab in Render if the API isn't working.
*   **Frontend Errors**: Open the browser console (F12) to see if there are connection errors.
*   **Cold Start**: The free tier on Render spins down after inactivity. The first request might take 50+ seconds. Be patient!
