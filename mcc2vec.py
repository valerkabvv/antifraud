from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd

def mcc_dt_agg(df):
    tag_doc = []

    cur_user_id = df.user_id[df.index[0]]
    prev_dt = df.date_time[df.index[0]]
    agg_mcc = ""

    for ind in df.index:
        if df.user_id[ind] == cur_user_id:

            dt = (df.date_time[ind] - prev_dt).seconds / 3600
            if dt > 12:
                agg_mcc += '.'
            else:
                agg_mcc += ' '
            agg_mcc += str(df.atm_mcc[ind])

            prev_dt = df.date_time[ind]
        else:
            tag_doc.append((cur_user_id, agg_mcc + '.'))
            cur_user_id = df.user_id[ind]
            prev_dt = df.date_time[ind]
            agg_mcc = str(df.atm_mcc[ind])

    tag_doc.append((cur_user_id, agg_mcc + '.'))

    return tag_doc


def person2vec(tr_history):

    tr_history.date_time = pd.to_datetime(tr_history.date_time, format='%Y%m%d %H:%M:%S.%f')
    tr_history.atm_mcc.fillna(value=0, inplace=True)
    tr_history.atm_mcc = tr_history.atm_mcc.astype(int)

    df = tr_history[["user_id", "date_time", "atm_mcc"]].sort_values(by=["user_id", "date_time"])
    tag_doc = mcc_dt_agg(df)

    documents = [TaggedDocument(doc, [i]) for i, doc in tag_doc]
    model = Doc2Vec(documents, vector_size=50, window=5, min_count=1, workers=4)

    usrs = [doc[0] for doc in tag_doc]

    doc_vec = [model[us_id] for us_id in usrs]
    doc_vec = pd.DataFrame(doc_vec)
    doc_vec.set_index(pd.Index(usrs), inplace = True)

    return doc_vec
