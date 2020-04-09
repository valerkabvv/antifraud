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
        get = ['user_id', col, 'amount_original']
        by = ['user_id', col]
        features = tr_history[get].groupby(by).agg(
        ['count','mean']).unstack(level=-1, fill_value=0)
        
        cols = [' '.join([col, i, j]) for _,i,j in features.columns]
        features.columns = cols
        
        distr_features = pd.concat([row_scaling(features[cols[:len(cols)//2]]),
                                    row_scaling(features[cols[len(cols)//2:]])], axis = 1)
        
        distr_features.columns = [" ".join([c,"distr"]) for c in distr_features.columns]
        
        features_list.append(features)
        features_list.append(distr_features)
        
    aggregated_features = pd.concat(features_list, axis = 1)
    
    
    return aggregated_features