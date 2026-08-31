import re
import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline

CATEGORIES = [
    "Salary & Wages", "Business & Freelance", "Dividends & Interest", "Rental Income", "Refunds & Reimbursements",
    "Housing & Rent", "Groceries & Supermarket", "Utilities & Electricity", "Healthcare & Pharmacy",
    "Fuel & Commute", "Insurance Premiums", "Education & Tuition", "Mobile & Internet",
    "Dining Out & Cafes", "Food Delivery", "Entertainment & Movies", "Shopping & Apparel",
    "Travel & Vacation", "Subscriptions & Streaming", "Personal Care & Grooming", "Gifts & Donations",
    "Mutual Funds & SIP", "Fixed Deposits & RD", "Stocks & Equity", "Home Loan EMI", "Car Loan EMI",
    "Personal Loan EMI", "Credit Card Bill", "Account Transfer", "ATM Cash Withdrawal"
]

SAMPLE_DATA = [
    ("TCS SALARY DIRECT DEPOSIT", "Salary & Wages"),
    ("INFOSYS MONTHLY PAYROLL CREDIT", "Salary & Wages"),
    ("UPWORK FREELANCE CLIENT PAYMENT", "Business & Freelance"),
    ("SWIGGY INSTAMART ORDER GROCERIES", "Groceries & Supermarket"),
    ("BLINKIT QUICK COMMERCE VEGGIES", "Groceries & Supermarket"),
    ("BIGBASKET SUPERMARKET HYD", "Groceries & Supermarket"),
    ("ZEPTO 10 MIN GROCERY STORE", "Groceries & Supermarket"),
    ("STARBUCKS COFFEE INDIRANAGAR", "Dining Out & Cafes"),
    ("ZOMATO RESTAURANT DINING BILL", "Dining Out & Cafes"),
    ("MCDONALDS BURGER DRIVE THRU", "Dining Out & Cafes"),
    ("UBER TRIP BANGALORE RIDE", "Fuel & Commute"),
    ("OLA CABS DAILY COMMUTE", "Fuel & Commute"),
    ("HPCL PETROL BUNK FILLING", "Fuel & Commute"),
    ("BPCL FUEL STATION AUTO CHARGE", "Fuel & Commute"),
    ("AIRTEL POSTPAID BILL PAYMENT", "Mobile & Internet"),
    ("JIO FIBER BROADBAND RECHARGE", "Mobile & Internet"),
    ("BESCOM ELECTRICITY BILL BANGALORE", "Utilities & Electricity"),
    ("TATA POWER BILL MUMBAI", "Utilities & Electricity"),
    ("AMAZON INDIA SHOPPING ELECTRONICS", "Shopping & Apparel"),
    ("FLIPKART CLOTHING AND APPAREL", "Shopping & Apparel"),
    ("MYNTRA FASHION STORE ONLINE", "Shopping & Apparel"),
    ("NETFLIX MONTHLY SUBSCRIPTION PREMIUM", "Subscriptions & Streaming"),
    ("SPOTIFY MUSIC STREAMING FAMILY PLAN", "Subscriptions & Streaming"),
    ("DISNEY HOTSTAR ANNUAL SUBSCRIPTION", "Subscriptions & Streaming"),
    ("APOLLO PHARMACY MEDICINES HYD", "Healthcare & Pharmacy"),
    ("PHARMEASY ONLINE PRESCRIPTION", "Healthcare & Pharmacy"),
    ("HDFC HOME LOAN EMI DEBIT", "Home Loan EMI"),
    ("ICICI CAR LOAN MONTHLY EMI", "Car Loan EMI"),
    ("ZERODHA BROKING MUTUAL FUND SIP", "Mutual Funds & SIP"),
    ("GROWW SIP NIFTY 50 INDEX FUND", "Mutual Funds & SIP"),
    ("SBI CREDIT CARD BILL SETTLEMENT", "Credit Card Bill"),
    ("ATM CASH WITHDRAWAL KORAMANGALA", "ATM Cash Withdrawal")
]

class TransactionCategorizerModel:
    def __init__(self):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
            ("clf", CalibratedClassifierCV(SGDClassifier(loss="log_loss", max_iter=1000, random_state=42)))
        ])
        self.is_fitted = False
        self.classes_ = None

    def fit(self, texts, labels):
        self.pipeline.fit(texts, labels)
        self.is_fitted = True
        self.classes_ = self.pipeline.classes_
        return self

    def predict_with_confidence(self, text: str):
        if not self.is_fitted:
            self.train_default()
        clean = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower()).strip()
        probs = self.pipeline.predict_proba([clean])[0]
        max_idx = np.argmax(probs)
        return {
            "predicted_category": self.classes_[max_idx],
            "confidence_score": float(probs[max_idx])
        }

    def train_default(self):
        texts = [x[0] for x in SAMPLE_DATA] * 10
        labels = [x[1] for x in SAMPLE_DATA] * 10
        self.fit(texts, labels)
        return self

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str):
        if os.path.exists(filepath):
            return joblib.load(filepath)
        model = cls()
        model.train_default()
        return model
