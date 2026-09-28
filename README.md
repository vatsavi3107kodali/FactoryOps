# FactoryOps – Smart Factory Monitoring & Predictive Maintenance

FactoryOps is a smart factory monitoring application designed to monitor
industrial machines, analyze sensor data, detect anomalies, predict machine
health, and support predictive maintenance.

The application provides an interactive dashboard for viewing machine
conditions, sensor readings, maintenance information, incidents, and
prediction results.

## Features

- 🔐 User and Admin login
- 🏭 Factory machine monitoring
- 📊 Interactive dashboard
- 📡 Sensor data monitoring
- 🚨 Anomaly detection
- 🔮 Machine health prediction
- 🛠️ Predictive maintenance support
- 📋 Maintenance tracking
- ⚠️ Incident management
- 📈 Machine and sensor analytics
- 🗄️ SQLite database
- 🔌 REST APIs using FastAPI
- 🖥️ Interactive interface using Streamlit
- 🌱 Demo database generation using Faker

## Tech Stack

### Frontend
- Streamlit
- Python
- Pandas

### Backend
- FastAPI
- Uvicorn
- Pydantic

### Database
- SQLite
- SQLAlchemy

### Other Tools
- Python
- REST API
- Faker
- Requests
- python-dotenv

## Project Structure

```text
FactoryOps/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   ├── isometric_factory.jpg
│   ├── login_bg_engineer.png
│   ├── login_bg_framed.png
│   ├── login_bg.jpg
│   └── login_bg.png
│
├── backend/
│   ├── api/
│   │   ├── dashboard_api.py
│   │   ├── incident_api.py
│   │   ├── machine_api.py
│   │   ├── main.py
│   │   ├── maintenance_api.py
│   │   ├── prediction_api.py
│   │   └── sensor_api.py
│   │
│   ├── crud/
│   ├── database/
│   │   └── seed_database.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   ├── db_config.py
│   └── main.py
│
├── app.py
├── factoryops.db
├── requirements.txt
├── .gitignore
└── README.md