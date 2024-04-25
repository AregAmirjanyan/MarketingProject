from payment_optimizer.modeling.models import *
import os
import sys


# Example usage:
if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(parent_dir, 'e_commerce')
    data_connect = DatabaseConnector(db_path)
    data_connect.join_tables()
    
    #Testing A/B test
    print('---------------Testing A/B test')

    # Initialize ABTesting instance with joined datasets
    ab_test_1 = ABTesting(data_connect)
    ab_test_1.preprocess_data()
    ab_test_1.perform_ab_test()
    res_1 = ab_test_1.results()
    #print(res_1)


    print('---------------Testing A/B test with start date specifications')

    # Initialize ABTesting instance with joined datasets
    ab_test_2 = ABTesting(data_connect)
    ab_test_2.preprocess_data()
    ab_test_2.perform_ab_test("04/07/2022")
    res_2 = ab_test_2.results()
    #print(res_2)

    print('---------------Testing A/B test with start and end date specifications ')

    # Initialize ABTesting instance with joined datasets
    ab_test_3 = ABTesting(data_connect)
    ab_test_3.preprocess_data()
    ab_test_3.perform_ab_test("04/02/2022","30/04/2023")
    res_3 = ab_test_3.results()
    #print(res_3)

    # Create a DataFrame from the results
    a_b_testing_results = pd.DataFrame([res_1, res_2, res_3])
    print(a_b_testing_results)
    a_b_testing_results['message'] = a_b_testing_results['message'].astype(str)
    print(a_b_testing_results.dtypes)
    # Generate sequential IDs
    a_b_testing_results['result_id'] = range(1, len(a_b_testing_results) + 1)


    data_path = os.path.join(parent_dir, 'data')
    result_path = os.path.join(data_path, 'a_b_testing_results.csv')
    a_b_testing_results.to_csv(result_path, index=False) 


    res_handler=SqlHandler(db_path, 'a_b_testing_results')
    res_data = pd.read_csv(result_path)

    res_handler.insert_many(res_data)
    res_handler.close_cnxn()


    
