import os
from payment_optimizer.modeling.models import *
import pandas as pd
from tests.test_transactions import CRUD_Check

def run_ab_tests(data_connect: DatabaseConnector, start_date: str = None, end_date: str = None) -> dict:
    """
    Runs A/B tests on the provided data.

    Args:
        data_connect (DatabaseConnector): The database connector object.
        start_date (str, optional): The start date for the test. Defaults to None.
        end_date (str, optional): The end date for the test. Defaults to None.

    Returns:
        dict: A dictionary containing the test results.
    """
    ab_test = ABTesting(data_connect)
    ab_test.preprocess_data()
    ab_test.perform_ab_test(start_date, end_date)
    return ab_test.get_results()

def model_test()-> None:
    """
    Main function to run A/B tests and save results.
    """
    # Set up database connection
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(parent_dir, 'e_commerce')
    data_connect = DatabaseConnector(db_path)
    data_connect.join_tables()

    # Run A/B tests
    test_cases = [
        {"name": "Default A/B Test", "start_date": None, "end_date": None},
        {"name": "A/B Test with Start Date", "start_date": "04/07/2022", "end_date": None},
        {"name": "A/B Test with Start and End Date", "start_date": "04/02/2022", "end_date": "30/04/2023"}
    ]

    for case in test_cases:
        result = run_ab_tests(data_connect, case["start_date"], case["end_date"])
        AB_test = CRUD_Check('a_b_testing_results')
        AB_test.create(result)
        AB_test.end_operation()

model_test()

