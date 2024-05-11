from payment_optimizer.db.sql_interactions import SqlHandler
import pandas as pd
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(parent_dir, 'e_commerce')


# Creating CRUD class

class CRUD_Check():
    """
    Class to perform CRUD operations on a specified table in the database.

    Attributes:
        table (str): The name of the table in the database.
        sql_handler (SqlHandler): An instance of SqlHandler for interacting with the database.
    """
    def __init__(self, table: str):
        """
        Initializes the CRUD_Check object with the specified table name.

        Args:
            table (str): The name of the table.
        """
        self.table = table
        self.sql_handler = SqlHandler(dbname=db_path, table_name=self.table)

    def end_operation(self)-> None:
        """
        Closes the connection to the database.
        """
        return self.sql_handler.close_cnxn()

    def create(self, data: dict) -> None:
        """
        Creates a new record in the table with the provided data.

        Args:
            data (dict): A dictionary containing the data for the new record.
        """
        return self.sql_handler.insert_many(df=pd.DataFrame([data]))

    def read(self, chunksize: int, pk_name: str)-> None:
        """
        Reads records from the table.

        Args:
            chunksize (int): The number of rows to read at a time.
            pk_name (str): The primary key name used for filtering.

        Returns:
            None
        """
        return(self.sql_handler.from_sql_to_pandas(chunksize=chunksize, id_value=pk_name))
    
    def update(self, condition: str, column_to_be_changed: str, new_value: str)-> None:
        """
        Updates records in the table based on the provided condition.

        Args:
            condition (str): The condition to filter records.
            column_to_be_changed (str): The name of the column to be updated.
            new_value (str): The new value to be set.

        Returns:
            None
        """
        set_info = {column_to_be_changed: new_value}
        return self.sql_handler.update_table(condition=condition, new_values=set_info)

    def delete(self, condition: str)-> None:
        """
        Deletes records from the table based on the provided condition.

        Args:
            condition (str): The condition to filter records for deletion.

        Returns:
            None
        """
        return self.sql_handler.delete_record(condition=condition)


# Adding group members, instructor, teaching associate as granted users

Gayane = {
    'password': 'gayaneohanjanyan',
    'first_name': 'Gayane',
    'last_name': 'Ohanjanyan',
    'phone_number': '+37493008900',
    'email': 'gayane_ohanjanyan@edu.aua.am',
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
    'email': 'nane_mambreyan@edu.aua.am',
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
    'email': 'hasmik_sahakyan@edu.aua.am',
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
    'email': 'areg_amirjanyan@edu.aua.am',
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
    'email': 'khovhannisyan@aua.am',
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
    'email': 'garo_bozadjian18@alumni.aua.am',
    'db_view': "granted"
}

test1 = CRUD_Check('user')
test1.create(Garo)
test1.end_operation()
