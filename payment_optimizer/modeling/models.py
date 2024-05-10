import pandas as pd
from scipy.stats import ttest_ind
from ..db.sql_interactions import SqlHandler
import math
from datetime import datetime


class DatabaseConnector:
    """
    A class to connect to a database and fetch data.

    Attributes:
        db_name (str): The name of the database.
        df (DataFrame or None): The DataFrame to hold the fetched data.
    """

    def __init__(self, db_name: str):
        """
        Initializes the DatabaseConnector with the given database name.

        Args:
            db_name (str): The name of the database.
        """
        self.db_name = db_name
        self.df = None
    
    def data_fetcher(self, table_name: str) -> pd.DataFrame:
        """
        Fetches data from the specified table in the database.

        Args:
            table_name (str): The name of the table to fetch data from.

        Returns:
            DataFrame: The fetched data.
        """
        handler = SqlHandler(self.db_name, table_name)
        data = handler.get_table_data()
        handler.close_cnxn()
        return data

    def join_tables(self) -> pd.DataFrame:
        """
        Joins multiple tables from the database and filters required columns.

        Returns:
            DataFrame: The joined and filtered DataFrame.
        """
        transaction_data = self.data_fetcher('transactions')
        transaction_product_data = self.data_fetcher('transaction_product')
        product_data = self.data_fetcher('product')

        data = pd.merge(transaction_data, transaction_product_data, on='transaction_id', how="left")
        data = pd.merge(data, product_data, on='product_id', how="left")

        self.df = data[[
            'transaction_id', 'user_id', 'payment_method_id', 'rating_id', 'status', 'type', 'shipping_address',
            'explored_bandit_type',
            'product_id', 'quantity', 'date', 'product_name', 'brand', 'price'
        ]]
        return self.df


class ABTesting():
    """
    A class to perform A/B testing on transaction data.

    Attributes:
        db_connector (DatabaseConnector): The database connector object.
        first_date (datetime or None): The start date for filtering transactions.
        last_date (datetime or None): The end date for filtering transactions.
        A_group (DataFrame or None): Data for group A.
        B_group (DataFrame or None): Data for group B.
        C_group (DataFrame or None): Data for group C.
        A_metric (Series or None): Metric for group A.
        B_metric (Series or None): Metric for group B.
        C_metric (Series or None): Metric for group C.
        t_stat_AB (float or None): T-statistic for A vs. B.
        p_value_AB (float or None): P-value for A vs. B.
        result_AB (str or None): Result message for A vs. B comparison.
        t_stat_BC (float or None): T-statistic for B vs. C.
        p_value_BC (float or None): P-value for B vs. C.
        result_BC (str or None): Result message for B vs. C comparison.
    """
    def __init__(self, db_connector: DatabaseConnector):
        """
        Initializes the ABTesting object with a DatabaseConnector object.

        Args:
            db_connector (DatabaseConnector): The database connector object.
        """
        self.db_connector = db_connector
        self.first_date = None
        self.last_date = None
        self.A_group = None
        self.B_group = None
        self.C_group = None

    def preprocess_data(self)-> None:
        """
        Fetches data from the database and preprocesses it for A/B testing.
        """
        self._fetch_data()
        self._convert_date()
        self._filter_groups()

    def _fetch_data(self)-> None:
        """
        Fetches data from the database using the DatabaseConnector object.
        """
        self.db_connector.join_tables()

    def _convert_date(self)-> None:
        """
        Converts the 'date' column to datetime format.
        """
        self.db_connector.df['date'] = pd.to_datetime(self.db_connector.df['date'])

    def _filter_groups(self)-> None:
        """
        Filters data into groups A, B, and C based on 'explored_bandit_type' and 'status'.
        """
        data = self.db_connector.df
        self.A_group = data[(data['explored_bandit_type'] == 'bandit A') & (data['status'] == 'purchased')]
        self.B_group = data[(data['explored_bandit_type'] == 'bandit B') & (data['status'] == 'purchased')]
        self.C_group = data[(data['explored_bandit_type'] == 'bandit C') & (data['status'] == 'purchased')]

    def perform_ab_test(self, start_date: str = None, end_date: str = None) -> None:
        """
        Performs A/B testing and computes test results.

        Args:
            start_date (str or None): The start date for filtering transactions.
            end_date (str or None): The end date for filtering transactions.
        """
        self._apply_date_filters(start_date, end_date)
        self._calculate_metrics()
        self._perform_tests()

    def _apply_date_filters(self, start_date: str, end_date: str) -> None:
        """
        Applies date filters to the A, B, and C groups.

        Args:
            start_date (str or None): The start date for filtering transactions.
            end_date (str or None): The end date for filtering transactions.
        """
        if start_date:
            self.first_date = self._parse_date(start_date)
            self.A_group = self.A_group[self.A_group['date'] >= self.first_date]
            self.B_group = self.B_group[self.B_group['date'] >= self.first_date]
            self.C_group = self.C_group[self.C_group['date'] >= self.first_date]

        if end_date:
            self.last_date = self._parse_date(end_date)
            self.A_group = self.A_group[self.A_group['date'] <= self.last_date]
            self.B_group = self.B_group[self.B_group['date'] <= self.last_date]
            self.C_group = self.C_group[self.C_group['date'] <= self.last_date]

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parses a date string into a datetime object.

        Args:
            date_str (str): The date string in 'dd/mm/yyyy' format.

        Returns:
            datetime: The parsed datetime object.
        """
        try:
            return datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            print("Invalid date format. Please use 'dd/mm/yyyy'.")
            return None

    def _calculate_metrics(self)-> None:
        """
        Calculates metrics for groups A, B, and C.
        """
        self.A_metric = self.A_group['price'] * self.A_group['quantity'] * math.log(len(self.A_group))
        self.B_metric = self.B_group['price'] * self.B_group['quantity'] * math.log(len(self.B_group))
        self.C_metric = self.C_group['price'] * self.C_group['quantity'] * math.log(len(self.C_group))

    def _perform_tests(self)-> None:
        """
        Performs statistical tests for A vs. B and B vs. C.
        """
        self.t_stat_AB, self.p_value_AB = ttest_ind(self.A_metric, self.B_metric, alternative="less", equal_var=False)
        self.t_stat_BC, self.p_value_BC = ttest_ind(self.C_metric, self.B_metric, alternative="less", equal_var=False)

        if self.p_value_AB < 0.05:
            self.result_AB = "Reject the null hypothesis. There is sufficient evidence to suggest that Revenue Bandit A < Revenue Bandit B."
        else:
            self.result_AB = "Fail to reject the null hypothesis. There is not sufficient evidence to suggest that Revenue Bandit A < Revenue Bandit B."
    

        if self.p_value_BC < 0.05:
            self.result_BC = "Reject the null hypothesis. There is sufficient evidence to suggest that Revenue Bandit C < Revenue Bandit B."
        else:
            self.result_BC = "Fail to reject the null hypothesis. There is not sufficient evidence to suggest that Revenue Bandit C < Revenue Bandit B."

    def get_results(self)-> dict:
        """
        Gets the results of the A/B tests.

        Returns:
            dict: A dictionary containing the test results.
        """
        results = {
            'start_date': self.first_date,
            'end_date': self.last_date,
            't_test_AB': self.t_stat_AB,
            'p_value_AB': self.p_value_AB,
            'message_AB_comparison': self.result_AB,
            't_test_BC': self.t_stat_BC,
            'p_value_BC': self.p_value_BC,
            'message_BC_comparison': self.result_BC,
            'test_date': datetime.now()
        }
        return results
