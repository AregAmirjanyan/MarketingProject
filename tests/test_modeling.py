
from payment_optimizer.modeling.models import *



# Example usage:
if __name__ == "__main__":
    data_connect = DatabaseConnector('e_commerce')
    data_connect.join_tables()
    
    #Testing A/B test
    print('---------------Testing A/B test')

    # Initialize ABTesting instance with joined datasets
    ab_test = ABTesting(data_connect)
    ab_test.preprocess_data()
    ab_test.perform_ab_test()
    res = ab_test.results()
    print(res)

    # Testing ModelBuilder
    print('---------------Testing ModelBuilder')
    model_builder = ModelBuilder(data_connect)
    data = model_builder.preprocess_data()

    # Spliting data into features (X) and target variable (y) and traning
    X = data[['payment_method_id', 'quantity', 'price']]
    y = data['rating_id']
    model_builder.train_model(X, y)

    # Making predictions and adding to dataframe
    predictions = model_builder.predict(X)
    print(predictions)

    #data['predictions'] = predictions
