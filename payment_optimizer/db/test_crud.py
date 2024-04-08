from payment_optimizer.db.sql_interactions import SqlHandler
import pandas as pd

# Creating CRUD class

class CRUD_Check():
    def __init__(self, table: str):
        self.table = table
        self.sql_handler = SqlHandler(dbname='e_commerce', table_name=self.table)

    def end_operation(self):
        return self.sql_handler.close_cnxn()

    def create(self, data: dict):
        return self.sql_handler.insert_many(df=pd.DataFrame([data]))

    def read(self, chunksize: int, pk_name: str):
        print(self.sql_handler.from_sql_to_pandas(chunksize=chunksize, id_value=pk_name))
    
    def update(self, condition: str, column_to_be_changed: str, new_value: str):
        set_info = {column_to_be_changed: new_value}
        return self.sql_handler.update_table(condition=condition, new_values=set_info)

    def delete(self, condition: str):
        return self.sql_handler.delete_record(condition=condition)


# Checking functionality on user table

data_new_user = {
    'password': 'gayaneohanjanyan',
    'first_name': 'Gayane',
    'last_name': 'Ohanjanyan',
    'phone_number': '+37493008900',
    'email': 'gayaneohanjanyan@gmail.com'
}

test1 = CRUD_Check('user')
test1.create(data_new_user)
test1.update("user_id = 2001", "password", "gayane__1230")
test1.delete('user_id = 2001')
test1.read(100, 'user_id')
test1.end_operation()


# Checking functionality on product table 
data_new_product = {
    "product_name": "Iphone 14",
    "brand": "Apple",
    "price": 1000
}

test2 = CRUD_Check('product')
test2.create(data_new_product)
test2.update("product_id = 1001", "product_name", "Iphone 14 PRO")
test2.delete("product_id = 1001")
test2.read(100, 'product_id')
test2.end_operation()


