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



csv_path_user = os.path.join(parent_dir, 'data', 'user.csv')

user_handler=SqlHandler('C:\\Users\\USER\\Desktop\\MarketingProject\\e_commerce', 'user')
user_data = pd.read_csv(csv_path_user)

# Inst.truncate_table()
user_handler.insert_many(user_data)
user_handler.close_cnxn()

#--
csv_path_rating = os.path.join(parent_dir, 'data', 'Rating.csv')

rating_handler=SqlHandler('C:\\Users\\USER\\Desktop\\MarketingProject\\e_commerce', 'rating')
rating_data = pd.read_csv(csv_path_rating)

# Inst.truncate_table()
rating_handler.insert_many(rating_data)
rating_handler.close_cnxn()


#--
csv_path_paymentmethod = os.path.join(parent_dir, 'data', 'PaymentMethod.csv')

pm_handler=SqlHandler('C:\\Users\\USER\\Desktop\\MarketingProject\\e_commerce', 'payment_method')
pm_data = pd.read_csv(csv_path_paymentmethod)

# Inst.truncate_table()
pm_handler.insert_many(pm_data)
pm_handler.close_cnxn()


#--
csv_path_transaction = os.path.join(parent_dir, 'data', 'Transaction.csv')

transaction_handler = SqlHandler('C:\\Users\\USER\\Desktop\\MarketingProject\\e_commerce', 'transactions')
transaction_data = pd.read_csv(csv_path_transaction)

# Inst.truncate_table()
transaction_handler.insert_many(transaction_data)
transaction_handler.close_cnxn()



#--
csv_path_product = os.path.join(parent_dir, 'data', 'product.csv')

product_handler = SqlHandler('C:\\Users\\USER\\Desktop\\MarketingProject\\e_commerce', 'product')
product_data = pd.read_csv(csv_path_product)

# Inst.truncate_table()
product_handler.insert_many(product_data)
product_handler.close_cnxn()


#--
csv_path_tp = os.path.join(parent_dir, 'data', 'TransactionProduct.csv')

tp_handler = SqlHandler('C:\\Users\\USER\\Desktop\\MarketingProject\\e_commerce', 'transaction_product')
tp_data = pd.read_csv(csv_path_tp)

# Inst.truncate_table()
tp_handler.insert_many(tp_data)
tp_handler.close_cnxn()


