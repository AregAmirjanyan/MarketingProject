from faker import Faker
import pandas as pd
import random
import string
from datetime import datetime

fake=Faker()


def generate_User(user_id):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))

    return {
        "user_id": user_id,
        "password": password,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "db_view": "denied"
        }    

def generate_Product(product_id):
    return {
        "product_id": product_id,
        "product_name": fake.word().capitalize(),
        "brand": fake.random_element(elements=("Smith Inc.", "Johnson Group", "Miller and Sons", "Clark Co.",
                                       "Whitehead Ltd.", "Carter Enterprises", "Adams LLC", "Stewart and Co.",
                                       "Bailey Corp", "Ramirez Ltd.", "Simmons and Sons", "Powell Group",
                                       "Washington Inc.", "Martinez Enterprises", "Lee Co.", "Perry and Sons",
                                       "Gonzalez Corp", "Russell Ltd.", "Butler Group", "Diaz and Sons")),
        "price": round(random.uniform(1.0, 2500.0), 2)
    }


def generate_PaymentMethod(payment_method_id):
    method_names = ["Credit Card", "Debit Card", "PayPal", "Cash"]
    return {
        "payment_method_id": payment_method_id,
        "method_name": method_names[payment_method_id % len(method_names)]
    }

def generate_Rating(rating_id):
    description =  ["terrible", "bad", "normal", "good", "perfect"]
    return {
        "rating_id": rating_id,
        "description": description[rating_id % len(description)]
    }

def generate_TransactionProduct(product_id, transaction_id):
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 4, 30)
    date = fake.date_time_between_dates(start_date, end_date)

    return {
        "transaction_id": transaction_id,
        "product_id": product_id,
        "quantity": round(random.uniform(1.0, 10.0)), 
        "date": date
    }


def generate_Transaction(transaction_id, user_id, payment_method_id, rating_id):
    type_options = ["pre-payment"] * 55 + ["post-payment"] * 45  # Adjust the distribution
    status_options = ["purchased"] * 75 + ["canceled"] * 15 + ["returned"] * 10

    type_choice = fake.random_element(elements=type_options)
    status_choice = random.choice(status_options)

    # Assigning explored_bandit_type based on the transaction type
    if type_choice == "pre-payment":
        # Assign to bandit A with 40% probability
        explored_bandit_type = "bandit B" if random.random() < 0.35 else "bandit A"
    else:
        # Assign to bandit B for post-payment transactions
        explored_bandit_type = "bandit B"

    return {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "payment_method_id": payment_method_id,
        "rating_id": rating_id,
        "status": status_choice,
        "type": type_choice,
        "shipping_address": fake.address(),
        "explored_bandit_type": explored_bandit_type
    }


