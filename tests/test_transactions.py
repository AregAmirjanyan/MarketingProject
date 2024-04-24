from payment_optimizer.db.sql_interactions import SqlHandler
import pandas as pd
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(parent_dir, 'e_commerce')


# Creating CRUD class

class CRUD_Check():
    def __init__(self, table: str):
        self.table = table
        self.sql_handler = SqlHandler(dbname=db_path, table_name=self.table)

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



# Checking functionality on product table 
data_new_product = {
    "product_name": "Iphone 14",
    "brand": "Apple",
    "price": 1000
}

test2 = CRUD_Check('product')
test2.create(data_new_product)
#test2.update("product_id = 1001", "product_name", "Iphone 15 PRO MAX")
#test2.delete("product_id = 1002")
#test2.read(100, 'product_id')
test2.end_operation()


# Adding group members, instructor, teaching associate as granted users

Gayane = {
    'password': 'gayaneohanjanyan',
    'first_name': 'Gayane',
    'last_name': 'Ohanjanyan',
    'phone_number': '+37493008900',
    'email': 'gayaneohanjanyan@gmail.com',
    'db_view': "granted"
}

test1 = CRUD_Check('user')
test1.create(Gayane)
test1.end_operation()

Nane = {
    'password': 'nanemambreyan',
    'first_name': 'Nane',
    'last_name': 'Mambreyan',
    'phone_number': '+37494233204',
    'email': 'nanemambreyan@gmail.com',
    'db_view': "granted"
}

test1 = CRUD_Check('user')
test1.create(Nane)
test1.end_operation()

Hasmik = {
    'password': 'hasmiksahakyan',
    'first_name': 'Hasmik',
    'last_name': 'Sahakyan',
    'phone_number': '+37491053492',
    'email': 'hasmiksahakyan@gmail.com',
    'db_view': "granted"
}

test1 = CRUD_Check('user')
test1.create(Hasmik)
test1.end_operation()


Areg = {
    'password': 'aregamirjanyan',
    'first_name': 'Areg',
    'last_name': 'Amirjanyan',
    'phone_number': '+37498120376',
    'email': 'aregamirjanyan@gmail.com',
    'db_view': "granted"
}

test1 = CRUD_Check('user')
test1.create(Areg)
test1.end_operation()


Hovhannisyan = {
    'password': 'karenhovhannisyan',
    'first_name': 'Karen',
    'last_name': 'Hovhannisyan',
    'phone_number': '+37494596123',
    'email': 'karenhovhannisyan@gmail.com',
    'db_view': "granted"
}

test1 = CRUD_Check('user')
test1.create(Hovhannisyan)
test1.end_operation()


Garo = {
    'password': 'garobozadijan',
    'first_name': 'Garo',
    'last_name': 'Bozadijan',
    'phone_number': '+37493123456',
    'email': 'garobozadijan@gmail.com',
    'db_view': "granted"
}

test1 = CRUD_Check('user')
test1.create(Hovhannisyan)
test1.end_operation()
