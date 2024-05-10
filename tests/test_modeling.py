import os
from payment_optimizer.modeling.models import *
import pandas as pd

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

def main()-> None:
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

    results = []
    for case in test_cases:
        print(f'---------------{case["name"]}')
        result = run_ab_tests(data_connect, case["start_date"], case["end_date"])
        results.append(result)

    # Save results to CSV and insert into database
    a_b_testing_results = pd.DataFrame(results)
    a_b_testing_results['result_id'] = range(1, len(a_b_testing_results) + 1)

    data_path = os.path.join(parent_dir, 'data')
    result_path = os.path.join(data_path, 'a_b_testing_results.csv')
    a_b_testing_results.to_csv(result_path, index=False)

    res_handler = SqlHandler(db_path, 'a_b_testing_results')
    res_data = pd.read_csv(result_path)
    res_handler.insert_many(res_data)
    res_handler.close_cnxn()

if __name__ == "__main__":
    main()

