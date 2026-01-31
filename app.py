from flask import Flask, request, jsonify
from flask_cors import CORS

from preprocess import load_data
from model import VehicleRecommender
from users import authenticate, register_user

app = Flask(__name__)
CORS(app)

# Load datasets
car_df, car_encoded = load_data("All_cars_dataset_final.csv")
bike_df, _ = load_data("../dataset/bike_dataset.csv")

car_encoded = car_encoded.fillna(0)

# Train ML model for cars
car_recommender = VehicleRecommender(car_encoded)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if authenticate(data["email"], data["password"]):
        return jsonify({"message": "Login success"})
    return jsonify({"message": "Invalid credentials"}), 401

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if register_user(data["email"], data["password"]):
        return jsonify({"message": "Signup successful"})
    return jsonify({"message": "User already exists"}), 400

# ---------------- CAR RECOMMENDATION ----------------
@app.route("/recommend/car", methods=["POST"])
def recommend_car():
    pref = request.json

    user_input = {
        "Price_numeric": pref.get("budget", 0),
        "Mileage_numeric": pref.get("mileage", 0),
        "Seating_numeric": pref.get("seating", 0),
        f"FUEL TYPE_{pref.get('fuel')}": 1,
        f"TRANSMISSION_{pref.get('transmission')}": 1
    }

    indices = car_recommender.recommend(user_input)

    result = car_df.iloc[indices][
        ["Name", "Price", "Mileage", "FUEL TYPE", "TRANSMISSION"]
    ]

    return jsonify(result.to_dict(orient="records"))

# ---------------- BIKE RECOMMENDATION ----------------
@app.route("/recommend/bike", methods=["POST"])
def recommend_bike():
    pref = request.json

    bikes = bike_df[
        (bike_df["Price_numeric"] <= pref.get("budget", 0)) &
        (bike_df["Mileage_numeric"] >= pref.get("mileage", 0))
    ]

    if pref.get("fuel"):
        bikes = bikes[bikes["FUEL TYPE"] == pref["fuel"]]

    result = bikes.head(5)[
        ["Name", "Price", "Mileage", "FUEL TYPE"]
    ]

    return jsonify(result.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)

