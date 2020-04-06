from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd

def mcc_dt_agg(df):
    tag_doc = []
    
    df.index = list(range(df.shape[0]))
    cur_user_id = df.user_id[df.index[0]]
    prev_dt = df.event_time[df.index[0]]
    agg_mcc = ""

    for id, time, mcc in zip(df["user_id"], df["event_time"], df["atm_mcc"]):
        if id == cur_user_id:
            
            dt = (time - prev_dt)/ 3600000
            if dt > 12:
                tag_doc.append((cur_user_id, agg_mcc))
                agg_mcc = str(mcc)
            else:
                agg_mcc+=(" "+str(mcc))
            prev_dt = time
            
        else:
            tag_doc.append((cur_user_id, agg_mcc))
            cur_user_id = id
            prev_dt = time
            agg_mcc = str(mcc)

    tag_doc.append((cur_user_id, agg_mcc))

    return tag_doc


def person2vec(tr_history):

    #tr_history.date_time = pd.to_datetime(tr_history.date_time, format='%Y%m%d %H:%M:%S.%f')
    tr_history.atm_mcc.fillna(value=0, inplace=True)
    tr_history.atm_mcc = tr_history.atm_mcc.astype(int)

    df = tr_history[["user_id", "event_time", "atm_mcc"]].sort_values(by=["user_id", "event_time"])
    tag_doc = mcc_dt_agg(df)

    documents = [TaggedDocument(doc, [i]) for i, doc in tag_doc]
    model = Doc2Vec(documents, vector_size=50, window=5, min_count=1, workers=4, epochs = 10)

    usrs = [doc[0] for doc in tag_doc]

    doc_vec = [model[us_id] for us_id in usrs]
    doc_vec = pd.DataFrame(doc_vec)
    doc_vec.set_index(pd.Index(usrs), inplace = True)

    return doc_vec
