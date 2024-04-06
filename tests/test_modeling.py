
from payment_optimizer.modeling.models import *



# Example usage:
if __name__ == "__main__":
    #Testing A/B test

    # Initialize ABTesting instance with database path
    ab_test = ABTesting('e_commerce.db')
    
    # Retrieve data from the database and preprocess
    ab_test.retrieve_data()
    ab_test.preprocess_data()
    
    # Performing A/B test
    ab_test.perform_ab_test()
    
    # Storing results back to the database
    ab_test.store_results()
    
    # Closing connection
    ab_test.close_connection()


    # Testing ModelBuilder
    db_connector = DatabaseConnector('e_commerce.db')
    db_connector.connect()

    model_builder = ModelBuilder(db_connector)

    # Retrieving and processing data
    data = model_builder.retrieve_data()
    data = model_builder.preprocess_data(data)

    # Spliting data into features (X) and target variable (y) and traning
    X = data[['payment_method_id', 'quantity', 'price']]
    y = data['rating_id']
    model_builder.train_model(X, y)

    # Making predictions and adding to dataframe
    predictions = model_builder.predict(X)
    data['predictions'] = predictions

    # Storeing results back to the database
    model_builder.store_results(data, 'model_output')
    db_connector.close()
