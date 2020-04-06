import pandas as pd
import numpy as np

def row_scaling(A):

    '''
    :param A: DataFrame
    :return: DataFrame with normed rows
    '''
    A = A.copy()
    norming = np.zeros(A.shape[0])

    for col in A.columns:
        norming += A[col].values

    A = A.apply(lambda x: x / norming)
    A.fillna(value=0, inplace=True)

    return A

def agg_features(path):

    '''
    :param path: full path to csv file with transaction history
    :return: DataFrame
    '''

    if type(path)==str:
        tr_history = pd.read_csv(path)
    else:
        tr_history = path
    
    

    # features related to event type
    features_list = []
    
    for col in ['event_type', 'user_defined_event_type', 'mcc_group']:
        features = tr_history[['user_id', 'event_type', 'amount_original']].groupby(['user_id', 'event_type']).agg(
        ['count','mean']).unstack(level=-1, fill_value=0)
        
        cols = features.columns
        
        distr_features = pd.concat([row_scaling(features[cols[:len(cols)//2]]),
                                    row_scaling(features[cols[len(cols)//2:]])], axis = 1)
        
        features_list.append(features)
        features_list.append(distr_features)
        
    aggregated_features = pd.concat(features_list, axis = 1)
    
    
    return aggregated_features