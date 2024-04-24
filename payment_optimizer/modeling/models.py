import pandas as pd
from scipy.stats import ttest_ind
from ..db.sql_interactions import SqlHandler
import math


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
        data = pd.merge(transaction_data, transaction_product_data, on='transaction_id', how = "left")
        data = pd.merge(data, product_data, on='product_id', how = "left")

        # Selecting columns
        self.df = data[[
            'transaction_id', 'user_id', 'payment_method_id', 'rating_id', 'status', 'type', 'shipping_address',
            'explored_bandit_type',
            'product_id', 'quantity', 'date', 'product_name', 'brand', 'price'
        ]]
        return self.df



class ABTesting():
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def preprocess_data(self):
        
        data = self.db_connector.df
        '''
        file_path = "data.csv"
        self.db_connector.df.to_csv(file_path, index=False)
        '''

        self.control_group = data[data['explored_bandit_type'] == 'bandit A']
        self.treatment_group = data[data['explored_bandit_type'] == 'bandit B']
    
    def perform_ab_test(self):
        #Choosing Average Order Value (AOV) metrics for control and treatment groups
        control_metric = self.control_group['price'] * self.control_group['quantity'] * math.log(len(self.control_group))  # AOV for control group
        treatment_metric = self.treatment_group['price'] * self.treatment_group['quantity'] * math.log(len(self.treatment_group))  # AOV for treatment group

        # H0: Revenue Bandit A = Revenue Bandit B
        # H1: Revenue Bandit A < Revenue Bandit B

        self.t_stat, self.p_value = ttest_ind(control_metric, treatment_metric, alternative = "less", equal_var = False)
        
        if self.p_value < 0.05:
            self.result = "Reject the null hypothesis. There is sufficient evidence to suggest that Revenue Bandit A < Revenue Bandit B."
        else:
            self.result = "Fail to reject the null hypothesis. There is not sufficient evidence to suggest that Revenue Bandit A < Revenue Bandit B."
    

    def results(self):
        ab_test_results = {'Model': "A/B Testing",
                                        't_stat': self.t_stat,
                                        'p_value': self.p_value}
        #ab_test_results.to_sql('ab_test_results', self.conn, if_exists='replace', index=False)
        print(self.result)
        return ab_test_results

