import pandas as pd
from scipy.stats import ttest_ind
from ..db.sql_interactions import SqlHandler
import math
from datetime import datetime, timedelta



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
        self.first_date = None
        self.last_date = None
        self.t_stat = None
        self.p_value = None
        self.result = None

    def preprocess_data(self):
        
        data = self.db_connector.df
        '''
        file_path = "data.csv"
        self.db_connector.df.to_csv(file_path, index=False)
        '''
        # Convert 'date' column to datetime type
        data['date'] = pd.to_datetime(data['date'])

        self.first_date = data['date'].min()
        self.last_date = data['date'].max()
        self.control_group = data[(data['explored_bandit_type'] == 'bandit A') & (data['status'] == 'purchased')]
        self.treatment_group = data[(data['explored_bandit_type'] == 'bandit B') & (data['status'] == 'purchased')]
        
    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            print("Invalid date format. Please use 'dd/mm/yyyy'.")
            return None
    
    def perform_ab_test(self, start_date = None, end_date = None):
        #start_date and end_date should be in format dd/mm/yyyy

        # Filter data by start_date and end_date if provided
        if start_date:
            self.first_date = self.parse_date(start_date)
            if self.first_date is None:
                return
            self.control_group = self.control_group[self.control_group['date'] >= self.first_date]
            self.treatment_group = self.treatment_group[self.treatment_group['date'] >= self.first_date]
        
        if end_date:
            self.last_date = self.parse_date(end_date)
            if self.last_date is None:
                return
            # Increment the end_date by one day to include the end_date itself
            #self.last_date += timedelta(days=1)
            self.control_group = self.control_group[self.control_group['date'] <= self.last_date]
            self.treatment_group = self.treatment_group[self.treatment_group['date'] <= self.last_date]

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
        ab_test_results = {
            'start_date': self.first_date,
            'end_date': self.last_date,
            't_test': self.t_stat,
            'p_value': self.p_value,
            'message': self.result,
            'test_date': datetime.now()
        }
        #print(self.result)
        return ab_test_results

