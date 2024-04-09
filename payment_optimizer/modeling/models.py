import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.stats import ttest_ind
from ..db.sql_interactions import SqlHandler


class DatabaseConnector:
    def __init__(self, db_name):
        self.db_name = db_name
        self.df = None
    
    def data_fetcher(self, table_name):
        handler = SqlHandler(self.db_name, table_name)
        data = handler.get_table_data()
        handler.close_cnxn()
        return data

    def join_tables(self):
        transaction_data = self.data_fetcher('transactions')
        transaction_product_data = self.data_fetcher('transaction_product')
        product_data = self.data_fetcher('product')

        # Join the tables
        data = pd.merge(transaction_data, transaction_product_data, on='transaction_id')
        data = pd.merge(data, product_data, on='product_id')

        # Selecting columns
        self.df = data[[
            'transaction_id', 'user_id', 'payment_method_id', 'rating_id', 'status', 'type', 'shipping_address',
            'product_id', 'quantity', 'date', 'product_name', 'brand', 'price'
        ]]
        #return self.df



class ModelBuilder:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.model = LinearRegression()
    
    def preprocess_data(self):
        data = self.db_connector.df
        data = data.dropna()
        data = pd.get_dummies(data, columns=['status', 'type'])
        return data
    
    def train_model(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def store_results(self, data, table_name):
        #data.to_sql(table_name, self.db_connector.conn, if_exists='replace', index=False)
        pass

class ABTesting():
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def preprocess_data(self):
        data = self.db_connector.df
        self.control_group = data[data['type'] == 'pre-payment']
        self.treatment_group = data[data['type'] == 'post-payment']
    
    def perform_ab_test(self):
        #Choosing Average Order Value (AOV) metrics for control and treatment groups
        control_metric = self.control_group['price'] * self.control_group['quantity']  # AOV for control group
        treatment_metric = self.treatment_group['price'] * self.treatment_group['quantity']  # AOV for treatment group

        self.t_stat, self.p_value = ttest_ind(control_metric, treatment_metric)
        
        if self.p_value < 0.05:
            self.result = "The difference in sales rates is statistically significant."
        else:
            self.result = "The difference in sales rates is not statistically significant."
    
    def results(self):
        ab_test_results = {'Model': "A/B Testing",
                                        't_stat': self.t_stat,
                                        'p_value': self.p_value}
        #ab_test_results.to_sql('ab_test_results', self.conn, if_exists='replace', index=False)
        print(self.result)
        return ab_test_results

