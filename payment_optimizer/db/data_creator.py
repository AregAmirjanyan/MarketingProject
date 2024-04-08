import os
import pandas as pd
import random
from payment_optimizer.db.data_generator import (
            generate_User, generate_Product, generate_PaymentMethod, 
            generate_Rating, generate_TransactionProduct, generate_Transaction)

NUMBER_OF_TRANSACTIONS = 5000
NUMBER_OF_USERS = 2000
NUMBER_OF_PRODUCTS = 1000
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
target_directory = os.path.join(parent_directory, 'data')

# Function to write data to CSV file only if it doesn't exist
def write_to_csv(data, csv_file_path):
    if not os.path.exists(csv_file_path):
        pd.DataFrame(data).to_csv(csv_file_path, index=False)

user_data = [generate_User(user_id) for user_id in range(1, NUMBER_OF_USERS + 1)]
product_data = [generate_Product(product_id) for product_id in range(1, NUMBER_OF_PRODUCTS + 1)]
PaymentMethod_data = [generate_PaymentMethod(payment_method_id) for payment_method_id in range(1, 5)]
Rating_data = [generate_Rating(rating_id) for rating_id in range(1, 6)]

# Write data to CSV files only if they don't exist
write_to_csv(user_data, f'{target_directory}/user.csv')
write_to_csv(product_data, f'{target_directory}/product.csv')
write_to_csv(PaymentMethod_data, f'{target_directory}/PaymentMethod.csv')
write_to_csv(Rating_data, f'{target_directory}/Rating.csv')

TransactionProduct_data = []
Transaction_data = []

for transaction_id in range(1, NUMBER_OF_TRANSACTIONS + 1):
    product_id = random.randint(1, len(product_data))
    user_id = random.randint(1, len(user_data))
    payment_method_id = random.randint(1, len(PaymentMethod_data))
    rating_id = random.randint(1, len(Rating_data))

    TransactionProduct = generate_TransactionProduct(product_id, transaction_id)
    Transaction_data.append(generate_Transaction(transaction_id, user_id, payment_method_id, rating_id))

    TransactionProduct_data.append(TransactionProduct)

write_to_csv(TransactionProduct_data, f'{target_directory}/TransactionProduct.csv')
write_to_csv(Transaction_data, f'{target_directory}/Transaction.csv')
