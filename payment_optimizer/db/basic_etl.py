from payment_optimizer.db.sql_interactions import SqlHandler
from payment_optimizer.db.logger import CustomFormatter
import pandas as pd
import os
from pathlib import Path



# Get the current directory
current_dir = Path.cwd()

# Navigate up the directory tree until reaching "MarketingProject"
while current_dir.name != "MarketingProject" and current_dir.parent != current_dir:
    current_dir = current_dir.parent

# Check if "MarketingProject" is found
if current_dir.name == "MarketingProject":
    print("Found 'MarketingProject' directory at:", current_dir)
    parent_dir = current_dir
else:
    print("Directory 'MarketingProject' not found in the directory tree.")


db_file_path = os.path.join(parent_dir, "e_commerce")

files_dictionary = {
    "user": "user.csv",
    "rating": "Rating.csv",
    "payment_method": "PaymentMethod.csv",
    "transactions": "Transaction.csv",
    "product": "product.csv",
    "transaction_product": "TransactionProduct.csv"
}


for table_name, file_name in files_dictionary.items():
    """  Loads data from CSV files into SQLite database tables.
    """    
    csv_path = os.path.join(parent_dir, 'data', file_name)
    handler = SqlHandler(db_file_path, table_name)
    data = pd.read_csv(csv_path)
    handler.insert_many(data)
    handler.close_cnxn()