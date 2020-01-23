import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

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

    tr_history = pd.read_csv(path)
    tr_history.date_time = pd.to_datetime(tr_history.date_time, format='%Y%m%d %H:%M:%S.%f')

    # features related to event type
    eve_tp_features = tr_history[['user_id', 'event_type', 'amount']].groupby(['user_id', 'event_type']).agg(
        'count').unstack(level=-1, fill_value=0)
    eve_tp_features.columns = ['CARD_PIN_CHANGE',
                               'CLIENT_DEFINED',
                               'DEPOSIT',
                               'PAYMENT',
                               'UPDATE_USER',
                               'VIEW_STATEMENT',
                               'WITHDRAW']

    eve_tp_features.drop(['CARD_PIN_CHANGE', 'CLIENT_DEFINED', 'UPDATE_USER'], axis=1, inplace=True)


    # features related to sub_type
    sub_type_features = tr_history[['user_id', 'sub_type', 'amount']].groupby(['user_id', 'sub_type']).agg(
        'count').unstack(level=-1, fill_value=0)
    sub_type_features.columns = list(map(lambda x: x[1], sub_type_features.columns))
    sub_type_features = sub_type_features[['ATM_BALANCE',
                                           'ATM_P2P_CREDIT',
                                           'ATM_P2P_DEBIT',
                                           'POS_PURCHASE',
                                           'POS_RETURN']]


    # mcc features

    mcc_distr = tr_history.groupby(['user_id', 'mcc_group']).agg(['mean', 'count']).amount
    mcc_distr = mcc_distr.unstack(fill_value=0)
    mcc_distr.columns = list(map(lambda x: x[0] + ' ' + x[1], mcc_distr.columns))

    mcc_distr_count = mcc_distr[["count A", "count C", "count F", "count H", "count J", "count O", "count Q", "count R",
                                "count T", "count U", "count X", "count Z"]]
    mcc_distr_price = mcc_distr.drop(
        ["count A", "count C", "count F", "count H", "count J", "count O", "count Q", "count R",
         "count T", "count U", "count X", "count Z"], axis=1)

    aggregated_features = pd.concat([eve_tp_features.apply(lambda x: x.sum(), axis = 1),
                                     sub_type_features.apply(lambda x: x.sum(), axis = 1),
                                     mcc_distr_price.apply(lambda x: x.sum(), axis = 1),
                                     mcc_distr_count.apply(lambda x: x.sum(), axis = 1)], axis=1)

    aggregated_features = StandardScaler().fit_transform(aggregated_features)
    aggregated_features = pd.DataFrame(aggregated_features)
    aggregated_features.set_index(sub_type_features.index, inplace = True)

    mcc_distr_price = row_scaling(mcc_distr_price)
    mcc_distr_count = row_scaling(mcc_distr_count)
    sub_type_features = row_scaling(sub_type_features)
    eve_tp_features = row_scaling(eve_tp_features)

    aggregated_features_norm = pd.concat([eve_tp_features, sub_type_features, mcc_distr_price,
                                          mcc_distr_count, pd.DataFrame(aggregated_features)], axis=1)

    return aggregated_features_norm

