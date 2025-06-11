# 🛍️ Sales Forecasting AI Web App

A full-stack AI web application that forecasts future product sales using a real-world Walmart dataset. Built using **FastAPI** (backend), **React** (frontend), and deployed with **Render + Netlify**.

Until now, I built ML projects in notebooks or Streamlit — this is my **first end-to-end app** with a proper frontend-backend separation and cloud deployment 🚀

---

## 🌐 Live Demo

**Frontend**: [https://splendid-sable-dbf212.netlify.app/](https://splendid-sable-dbf212.netlify.app/)  
**Backend (FastAPI)**: Hosted on Render and connected via API  
⚠️ *If the app doesn’t respond, it might be because the backend was idling. Refresh after a few seconds to retry.*

---

## 📦 Project Features

- 🔮 **Forecast Future Sales** of a selected product in a chosen store, for any number of days after the last training date.
- 🧠 **ML Pipeline** with preprocessing, feature engineering, and model selection.
- 🔁 **Recursive Forecasting** — uses the model's previous predictions to forecast future values (multi-step prediction).
- ⚙️ **Modular Architecture** — separate folders for training, prediction pipelines, and reusable components.
- 📈 Real-world **Walmart Sales Dataset** used to train and evaluate the model.

---

## 🛠️ Tech Stack

### 👨‍💻 Backend
- **FastAPI** – for API endpoints to serve predictions
- **scikit-learn** – for model training and inference
- **Pandas** – for data manipulation
- **Uvicorn** – ASGI server

### 🖼️ Frontend
- **React.js** – for clean, simple UI
- **Axios** – for API requests

### ☁️ Deployment
- **Render** – to host the FastAPI backend
- **Netlify** – to host the React frontend

---

## 📁 Folder Structure

```
project-root/
│
├── backend/
│   └── app.py  ← FastAPI app + prediction route
│
├── frontend/
│   └── src/    ← React codebase (UI + Axios)
│
├── src/
│   ├── pipelines/
│   │   ├── train_pipeline.py
│   │   └── predict_pipeline.py
│   └── components/
│       └── data_utils, model_utils etc.
│
├── artifact/
│   └── model.pkl ← Trained ML model
```

---

## 📊 Dataset Info

Used the [Walmart Sales Forecasting Dataset](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data), which contains:
- Daily sales data across stores
- Product categories and item details
- Calendar info (holidays, events)
- Prices and promotions

---

## 🙌 Learnings

- Built & deployed a FastAPI ML backend for the first time
- Learned to connect React frontend with an ML API
- Understood hosting differences & deployment pipelines between Netlify and Render
- Gained experience with recursive forecasting (multi-step)

---

## 📌 Future Improvements

- Add option to select multiple products or plot visual trends
- Add error handling and loading states on the frontend
- Integrate model retraining pipeline
- Dockerize the app for smoother deployments

---

