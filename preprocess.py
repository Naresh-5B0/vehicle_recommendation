import pandas as pd

# -------------------------------------------------
# PRICE CLEANING
# -------------------------------------------------
def convert_price(price):
    """
    Converts:
    '8.5 Lakh', '1.2 Crore', '₹10 Lakh', '-', NaN
    → numeric INR value
    """
    if price is None:
        return 0

    price = str(price).lower().strip()

    if price in ["-", " - ", "", "nan"]:
        return 0

    price = price.replace("₹", "")

    try:
        if "lakh" in price:
            return float(price.replace("lakh", "").strip()) * 100000
        if "crore" in price:
            return float(price.replace("crore", "").strip()) * 10000000
        return float(price)
    except:
        return 0


# -------------------------------------------------
# MILEAGE CLEANING
# -------------------------------------------------
def clean_mileage(m):
    """
    Handles:
    '17 kmpl'
    '9 - 40 kmpl'
    '470 km' (EV range)
    '-', NaN
    """
    if m is None:
        return 0

    m = str(m).lower().strip()

    if m in ["-", " - ", "", "nan"]:
        return 0

    # EV range like "470 km"
    if "km" in m and "kmpl" not in m:
        try:
            return float(m.replace("km", "").strip())
        except:
            return 0

    # Normal mileage like "17 kmpl"
    if "kmpl" in m:
        m = m.replace("kmpl", "").strip()

    # Range like "9 - 40"
    if "-" in m:
        try:
            return float(m.split("-")[-1].strip())
        except:
            return 0

    try:
        return float(m)
    except:
        return 0


# -------------------------------------------------
# SEATING CAPACITY CLEANING
# -------------------------------------------------
def clean_seating(s):
    """
    Converts:
    '5', '7', '-', NaN
    → integer seating capacity
    """
    if s is None:
        return 0

    s = str(s).strip()

    if s in ["-", " - ", "", "nan"]:
        return 0

    try:
        return int(s)
    except:
        return 0


# -------------------------------------------------
# LOAD & PREPARE DATA
# -------------------------------------------------
def load_data(csv_path):
    """
    Loads dataset, cleans data,
    and returns:
    1. Original dataframe (for display)
    2. ML-ready encoded dataframe
    """
    df = pd.read_csv(csv_path)

    # Clean numeric fields
    df["Price_numeric"] = df["Price"].apply(convert_price)
    df["Mileage_numeric"] = df["Mileage"].apply(clean_mileage)
    df["Seating_numeric"] = df["Seating Capacity"].apply(clean_seating)

    # Select ONLY ML features (NO text columns)
    features = df[
        [
            "Price_numeric",
            "Mileage_numeric",
            "Seating_numeric",
            "FUEL TYPE",
            "TRANSMISSION",
        ]
    ]

    # One-hot encode categorical features
    encoded = pd.get_dummies(
        features,
        columns=["FUEL TYPE", "TRANSMISSION"]
    )

    # Final safety cleanup
    encoded = encoded.fillna(0)

    return df, encoded
