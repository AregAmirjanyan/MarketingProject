import sqlite3
import logging 
import pandas as pd
import numpy as np
import os
from payment_optimizer.db.logger import CustomFormatter




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from payment_optimizer.db.schema import Base 



logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class SqlHandler:

    def __init__(self, dbname:str,table_name:str) -> None:
        self.cnxn=sqlite3.connect(f'{dbname}.db')
        self.cursor=self.cnxn.cursor()
        self.dbname=dbname
        self.table_name=table_name

    def close_cnxn(self)->None:

        logger.info('commiting the changes')
        self.cursor.close()
        self.cnxn.close()
        logger.info('the connection has been closed')

    def insert_one(self, record: dict) -> None:
        if not record:
            raise ValueError("Record dictionary cannot be empty")

        # Construct the SQL query
        columns = ', '.join(record.keys())
        placeholders = ', '.join(['?' for _ in record])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        
        # Log the SQL query for debugging
        logger.info(f"Executing SQL query: {query}")

        # Execute the query
        try:
            self.cursor.execute(query, list(record.values()))
            self.cnxn.commit()
            logger.info("Record inserted successfully.")
        except Exception as e:
            logger.error(f"Error inserting record: {e}")
            self.cnxn.rollback()
            raise


    def get_table_columns(self)->list:
        self.cursor.execute(f"PRAGMA table_info({self.table_name});")
        columns = self.cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        logger.info(f'the list of columns: {column_names}')
        # self.cursor.close()

        return column_names
    
    def truncate_table(self)->None:
        
        query=f"DROP TABLE IF EXISTS {self.table_name};"
        self.cursor.execute(query)
        logging.info(f'the {self.table_name} is truncated')
        # self.cursor.close()

    def drop_table(self):
        
        query = f"DROP TABLE IF EXISTS {self.table_name};"
        logging.info(query)

        self.cursor.execute(query)

        self.cnxn.commit()

        logging.info(f"table '{self.table_name}' deleted.")
        logger.debug('using drop table function')
    
    def insert_many(self, df: pd.DataFrame) -> None:
        df = df.replace(np.nan, None)  # Replace NaN values with None
        df.rename(columns=lambda x: x.lower(), inplace=True)  # Convert column names to lowercase
        columns = list(df.columns)  # Get column names

        # Filter out columns that exist in both DataFrame and SQL table
        sql_column_names = [i.lower() for i in self.get_table_columns()]
        print("colsL", columns)
        print(sql_column_names)
        columns = list(set(columns) & set(sql_column_names))

        # Prepare data for insertion
        data_to_insert = df.loc[:, columns]
        values = [tuple(row) for row in data_to_insert.values]

        # Construct SQL query to filter out existing records
        existing_query = f"""
            SELECT DISTINCT {', '.join(columns)}
            FROM {self.table_name}
        """
        existing_records = set(self.cursor.execute(existing_query).fetchall())

        # Filter out rows that already exist in the database
        values_to_insert = [row for row in values if tuple(row) not in existing_records]

        if not values_to_insert:
            logger.warning('All rows already exist in the database. No new records inserted.')
            return

        '''
        # Hash password column if it exists
        if 'password' in columns:
            password_index = columns.index('password')
            for index, row in enumerate(values_to_insert):
                hashed_password = pwd_context.hash(row[password_index])
                row = list(row)
                row[password_index] = hashed_password
                values_to_insert[index] = tuple(row)
        '''

        # Construct SQL query for insertion
        cols = ', '.join(columns)  # Comma-separated column names
        params = ', '.join(['?' for _ in columns])  # Comma-separated placeholders for values

        query = f"""
            INSERT INTO {self.table_name} ({cols})
            VALUES ({params});
        """

        # Execute the query and commit changes
        self.cursor.executemany(query, values_to_insert)
        self.cnxn.commit()

        logger.warning('New records inserted into the database.')


    def is_table_empty(self) -> bool:
        # Check if the table is empty
        query = f"SELECT COUNT(*) FROM {self.table_name};"
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        return count == 0



    def from_sql_to_pandas(self, chunksize:int, id_value:str )-> pd.DataFrame:
        offset=0
        dfs=[]
       
        
        while True:
            query=f"""
            SELECT * FROM {self.table_name}
                ORDER BY {id_value}
                LIMIT {chunksize} OFFSET {offset}
            """
            data = pd.read_sql_query(query,self.cnxn) 
            logger.info(f'the shape of the chunk: {data.shape}')
            dfs.append(data)
            offset += chunksize
            if len(dfs[-1]) < chunksize:
                logger.warning('loading the data from SQL is finished')
                logger.debug('connection is closed')
                break
        df = pd.concat(dfs)

        return df



    def update_table(self, condition: str, new_values: dict) -> None:
   
        set_clause = ', '.join([f"{key} = ?" for key in new_values.keys()])

    # Constructing the UPDATE query
        query = f"""
            UPDATE {self.table_name}
            SET {set_clause}
            WHERE {condition}
         """

        values = list(new_values.values())
        self.cursor.execute(query, values)
        self.cnxn.commit()

        logger.info(f"Table '{self.table_name}' updated successfully.")


    def count_rows(self) -> int:
        query = f"SELECT COUNT(*) FROM {self.table_name};"
        self.cursor.execute(query)
        row_count = self.cursor.fetchone()[0]
        return row_count


    def select_by_user_id(self, user_id: int) -> pd.DataFrame:

        query = f"SELECT * FROM {self.table_name} WHERE user_id = ?;"
        self.cursor.execute(query, (user_id,))
        filtered_records = self.cursor.fetchall()
        if filtered_records:
            columns = [col[0] for col in self.cursor.description]
            df = pd.DataFrame(filtered_records, columns=columns)
            return df
        else:
            logger.info(f"No records found in table: {self.table_name} for user_id: {user_id}.")
            return pd.DataFrame()

    def select_row(self, column_name, value):
        query = f"SELECT * FROM {self.table_name} WHERE {column_name} = ?;"

        self.cursor.execute(query, (value,))
        rows = self.cursor.fetchall()
        if not rows:
            return "No matching data found."
        else:
            return rows
        
    def get_entries(self, n: int) -> pd.DataFrame:
        query = f"""
            SELECT * FROM {self.table_name}
            LIMIT {n};
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        data = pd.DataFrame(rows, columns=columns)
        logger.info(f'Selected {n} entries from table {self.table_name}.')
        return data
        
    def delete_record(self, condition: str) -> None:
        # Constructing the DELETE query
        query = f"""
            DELETE FROM {self.table_name}
            WHERE {condition}
        """

        # Execute the DELETE query
        self.cursor.execute(query)
        self.cnxn.commit()
        
        logger.info(f"Records deleted successfully from '{self.table_name}'.")

    def get_table_data(self, columns: list = None, condition: str = None) -> pd.DataFrame:
        if columns is None:
            columns = self.get_table_columns()

        if not columns:
            return pd.DataFrame()

        column_names = ', '.join(columns)

        query = f"SELECT {column_names} FROM {self.table_name}"
        if condition:
            query += f" WHERE {condition}"

        data = pd.read_sql_query(query, self.cnxn)
        return data

    def _execute_query(self, query: str) -> pd.DataFrame:
        logger.info(f"Executing SQL query: {query}")
        data = pd.read_sql_query(query, self.cnxn)
        return data

    def inner_join(self, table2: str, key1: str, key2: str) -> pd.DataFrame:
        query = f"""
            SELECT *
            FROM {self.table_name} t1
            INNER JOIN {table2} t2 
            ON t1.{key1} = t2.{key2}
        """
        return self._execute_query(query)

    def left_join(self, table2: str, key1: str, key2: str) -> pd.DataFrame:
        query = f"""
            SELECT *
            FROM {self.table_name} t1
            LEFT JOIN {table2} t2 
            ON t1.{key1} = t2.{key2}
        """
        return self._execute_query(query)

    def right_join(self, table2: str, key1: str, key2: str) -> pd.DataFrame:
        query = f"""
            SELECT *
            FROM {self.table_name} t1
            RIGHT JOIN {table2} t2
            ON t1.{key1} = t2.{key2}
        """
        return self._execute_query(query)

    def full_outer_join(self, table2: str, key1: str, key2: str) -> pd.DataFrame:
        query = f"""
            SELECT *
            FROM {self.table_name} t1
            FULL OUTER JOIN {table2} t2 
            ON t1.{key1} = t2.{key2}
        """
        return self._execute_query(query)
    


    def get_transactions_by_user_id(self, user_id: int) -> pd.DataFrame:
        query = f"""
            SELECT *
            FROM transactions
            WHERE user_id = {user_id}
        """
        return pd.read_sql_query(query, self.cnxn)
    

    def search_products(self, **kwargs):
        query = "SELECT * FROM product WHERE "
        conditions = []
        values = []

        for key, value in kwargs.items():
            if value is not None:
                conditions.append(f"{key} LIKE ?")
                values.append(f"%{value}%")  # Using LIKE operator for partial matches

        if conditions:
            query += " OR ".join(conditions)
            self.cursor.execute(query, tuple(values))
            rows = self.cursor.fetchall()
            if not rows:
                return []
            else:
                # Convert each row tuple to a dictionary
                columns = [col[0] for col in self.cursor.description]
                results = []
                for row in rows:
                    result_dict = dict(zip(columns, row))
                    results.append(result_dict)
                return results
        else:
            return []



        

