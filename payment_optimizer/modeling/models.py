import pandas as pd
import sqlite3
from sklearn.linear_model import LinearRegression
from scipy.stats import ttest_ind


class DatabaseConnector:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
    
    def close(self):
        if self.conn:
            self.conn.close()



class ModelBuilder:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.model = LinearRegression()
    
    def retrieve_data(self):
        query = """
        SELECT
            t.transaction_id,
            t.user_id,
            t.payment_method_id,
            t.rating_id,
            t.status,
            t.type,
            t.shipping_address,
            tp.product_id,
            tp.quantity,
            tp.date,
            p.product_name,
            p.brand,
            p.price
        FROM
            Transaction t
        JOIN
            TransactionProduct tp ON t.transaction_id = tp.transaction_id
        JOIN
            Product p ON tp.product_id = p.product_id
        """
        return pd.read_sql_query(query, self.db_connector.conn)
    
    def preprocess_data(self, data):
        data = data.dropna()
        data = pd.get_dummies(data, columns=['status', 'type'])
        return data
    
    def train_model(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def store_results(self, data, table_name):
        data.to_sql(table_name, self.db_connector.conn, if_exists='replace', index=False)




class ABTesting:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
    
    def retrieve_data(self):
        query = """
        SELECT
            t.transaction_id,
            t.user_id,
            t.payment_method_id,
            t.rating_id,
            t.status,
            t.type,
            t.shipping_address,
            tp.product_id,
            tp.quantity,
            tp.date,
            p.product_name,
            p.brand,
            p.price
        FROM
            Transaction t
        JOIN
            TransactionProduct tp ON t.transaction_id = tp.transaction_id
        JOIN
            Product p ON tp.product_id = p.product_id
        """
        self.data = pd.read_sql_query(query, self.conn)
    
    def preprocess_data(self):
        self.control_group = self.data[self.data['type'] == 'pre-payment']
        self.treatment_group = self.data[self.data['type'] == 'post-payment']
    
    def perform_ab_test(self):
        control_metric = self.control_group['sales_rate']
        treatment_metric = self.treatment_group['sales_rate']
        
        self.t_stat, self.p_value = ttest_ind(control_metric, treatment_metric)
        
        if self.p_value < 0.05:
            self.result = "The difference in sales rates is statistically significant."
        else:
            self.result = "The difference in sales rates is not statistically significant."
    
    def store_results(self):
        ab_test_results = pd.DataFrame({'group': ['control', 'treatment'],
                                        't_stat': [self.t_stat_control, self.t_stat_treatment],
                                        'p_value': [self.p_value_control, self.p_value_treatment]})
        ab_test_results.to_sql('ab_test_results', self.conn, if_exists='replace', index=False)
    
    def close_connection(self):
        self.conn.close()

