# linear_regression_model

# ✈️ Flight Delay Prediction App – Africa Edition

An end-to-end Machine Learning + Mobile App system that predicts flight departure delays based on airline, airport, and time information using a synthetic African dataset.

---

## 📌 Contents

- [📂 Folder Structure](#-folder-structure)
- [🎯 Project Mission](#-project-mission)
- [🔍 Dataset](#-dataset)
- [🧠 Model Training](#-model-training)
- [⚙️ FastAPI Backend](#️-fastapi-backend)
- [🚀 Deploy on Render](#-deploy-on-render)
- [📱 Flutter App](#-flutter-app)
- [📡 Connecting API & App](#-connecting-api--app)
- [🎥 Video Demo Guide](#-video-demo-guide)
- [✅ Submission Checklist](#-submission-checklist)

---

## 📂 Folder Structure

linear_regression_model/
│
├── summative/
│ ├── linear_regression/
│ │ ├── multivariate.ipynb
│
│ ├── API/
│ │ ├── prediction.py
│ │ ├── model.pkl
│ │ ├── requirements.txt
│ │ ├── render.yaml
│ │ ├── README.md
│
│ ├── FlutterApp/
│ │ ├── lib/
│ │ │ ├── main.dart
│ │ │ ├── screens/
│ │ │ │ ├── input_screen.dart
│ │ │ │ ├── result_screen.dart
│ │ │ ├── services/api_service.dart
│ │ ├── pubspec.yaml
│ │ ├── README.md



---

## 🎯 Project Mission

> Predict potential departure delays in African airline flights using departure schedules, actual times, and flight logistics to enhance travel planning.

---

## 🔍 Dataset

**Synthetic dataset** generated for African flights featuring:

- `ScheduledHour` – e.g., 13:30
- `ActualHour` – e.g., 13:45
- `DepartureDelta` – derived in minutes (actual - scheduled)
- `Airline` – e.g., ET (Ethiopian), KQ (Kenya Airways)
- `Origin`, `Destination` – Airport codes (e.g., ACC, JNB, KGL)
- `DelayMinutes` – Target value

---

## 🧠 Model Training

Located in:  
📁 `summative/linear_regression/multivariate.ipynb`

Includes:

- Data visualization
- Feature engineering
- Time conversion & one-hot encoding
- Linear Regression via scikit-learn
- Comparison: Decision Trees vs Random Forest
- Loss curves (Train/Test)
- Best model exported as `model.pkl`

---

## ⚙️ FastAPI Backend

📁 `summative/API/`

### ▶ Create Virtual Environment

```bash
cd summative/API
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

▶ Install Dependencies
```bash
pip install -r requirements.txt

▶ Run API Locally
```bash
uvicorn prediction:app --reload

▶ Access:
Swagger UI: http://127.0.0.1:8000/docs

Prediction POST: http://127.0.0.1:8000/predict

▶ CORS (enabled for Flutter)
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




🚀 Deploy on Render
1. Create render.yaml (inside API folder)
```yaml
services:
    - type: web
    name: flight-delay-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn prediction:app --host 0.0.0.0 --port 10000
    branch: main
    repo: https://github.com/yourusername/your-repo-name



2. Push to GitHub
```bash
git init
git add .
git commit -m "Initial Commit"
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main



3. Deploy on Render
Go to https://render.com

Link GitHub repo

It will auto-detect render.yaml

Live URL example:
https://flight-delay-api.onrender.com

📱 Flutter App
📁 summative/FlutterApp/

▶ Requirements
Flutter SDK: https://flutter.dev/docs/get-started/install

Dart enabled in your IDE

▶ Run the App
```bash
flutter pub get
flutter run

▶ App Features
-Input: Dropdowns for Airline, Origin, Destination

-TimePickers for Scheduled and Actual Hour (HH:MM)

-Predict Button

-Display predicted delay or error

▶ Clean UI Design
Inspired by modern African airline dashboards:

-Icons

-Light background

-Input validation

-Separation of input and result screens

📡 Connecting API & App
📄 api_service.dart:

```dart
final Uri url = Uri.parse("https://flight-delay-api.onrender.com/predict");
📤 API Request Payload:

```json
{
"ScheduledHour": "12:45",
"ActualHour": "13:20",
"Airline": "ET",
"Origin": "ACC",
"Destination": "KGL"
}
📥 API Response:

```json
{
"prediction": 19.57
}