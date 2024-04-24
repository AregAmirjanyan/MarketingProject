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
    ab_test = ABTesting(data_connect)
    ab_test.preprocess_data()
    ab_test.perform_ab_test()
    res = ab_test.results()
    print(res)

    
