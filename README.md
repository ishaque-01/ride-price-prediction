# 🚗 Ride Price Prediction: Machine Learning App

An end-to-end Data Science project that predicts ride-sharing prices using **Random Forest Regression**. The application features an interactive geospatial interface built with **Streamlit** and **Folium**, allowing users to visualize and select routes in real-time.

<hr>

## 🚀 Features
* **Interactive Map:** Select pickup and drop-off points directly on a map using `streamlit-folium`.
* **Accurate Predictions:** Uses an ensemble learning model (Random Forest) to handle complex pricing variables.
* **Visual Analytics:** Displays pricing trends based on distance, time of day, and demand.
* **User-Friendly UI:** Clean, sidebar-driven interface for adjusting ride parameters.

<hr>

## 🛠️ Tech Stack
* **Language:** Python 3.13.2
* **Model:** Scikit-Learn (Random Forest Regressor)
* **UI/UX:** Streamlit
* **Maps:** Folium & Streamlit-Folium
* **Data Handling:** Pandas, NumPy

<hr>

## 📊 The Model
The core of this project is a **Random Forest Regressor**. This model was chosen because it handles non-linear relationships and high-dimensional data effectively.

<hr>

## 💾 Dataset
The cleaned dataset used for training is approximately **200MB**. Due to GitHub's file size limits, it is hosted on Google Drive.

<hr>

* **Download Dataset and Trained Model File:** [👉 Click here to download cleaned_data.csv](https://drive.google.com/drive/folders/1DCFvSBu9w3DPaSkvfTczHxX1Y4lClXf-?usp=drive_link)
* **Instructions:** Download the CSV, PKL files and place it in the project root directory before running the application.

<hr>

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/ride-price-prediction.git](https://github.com/YourUsername/ride-price-prediction.git)
   cd ride-price-prediction

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Run the Streamlit app:**
   ```bash
    streamlit run app.py

<hr>

## 🗺️ How it Works

1. **Select Locations:**
    Use the interactive Folium map to mark where you want to start and end your ride or use sidebar input fields to add your location by using longitude and latitude coordinates.

2. **Input Details:**
    Adjust the time of day, day of the week.

3. **Predict:**
    The Random Forest model processes the input features and provides a price estimate in seconds.

## 🤝 Contributing
Feel free to fork this project, open issues, or submit pull requests to improve the model accuracy or UI features!