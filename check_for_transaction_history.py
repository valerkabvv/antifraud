import pandas as pd


def check_for_hist(path_A, path_B):
    '''
    Deleting all rows with unique user_id

    :param path_A: path for transaction history csv file
    :param path_B: path for tagged transactions csv file
    :return: A, B - DataFrames with containing same user_id
    '''

    tr_history = pd.read_csv(path_A)
    tr = pd.read_csv(path_B)

    usr_hst = set(tr_history.user_id)
    usr_tr = set(tr.user_id)
    usr_rec_tr = set(tr.rec_user_id)

    rec_id_to_stay = usr_rec_tr - (usr_rec_tr - usr_hst)
    usr_id_to_stay = usr_tr - (usr_tr - usr_hst)

    tr = tr[tr.rec_user_id == rec_id_to_stay & tr.user_id == usr_id_to_stay]

    return tr.event_id
