AI-Driven Indian Stock Market Analysis and Recommendation

Projects
- frontend/ (Vite + React)
- backend/ (FastAPI)

Run Backend
1) cd backend
2) pip install -r requirements.txt
3) uvicorn main:app --reload

Run Frontend
1) cd frontend
2) npm install
3) npm run dev

Endpoints
- http://localhost:8000/api/stock/{symbol}
- http://localhost:8000/api/predict/{symbol}
- http://localhost:8000/api/news/{symbol}

Example Symbols: RELIANCE.BSE, TCS.BSE, INFY.NSE

