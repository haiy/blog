import pandas as pd

#http://stackoverflow.com/questions/24980437/pandas-groupby-and-then-merge-on-original-table
#http://stackoverflow.com/questions/13854476/pandas-transform-doesnt-work-sorting-groupby-output/13854901#13854901
#
dir_path = "/home/h/Desktop/talking_data/csv/"
def app_label_feature():
    app_labels = pd.read_csv(dir_path + "app_labels.csv")
    grouped_labels = app_labels.groupby("app_id", as_index=False)
    app_label_info = grouped_labels.agg(lambda x: ",".join(list(x['label_id'].apply(str))))
    return app_label_info

def events_group_stat(single_group_df):
    #group_df[]
    single_group_df.ap
    pass

def app_events_cat_info(app_label_feature):
    app_events = pd.read_csv(dir_path + "app_events.csv")
    merged_envents = pd.merge(app_events,app_label_info, how = 'outer', on = 'app_id')
    merged_events[['event_id','app_id', 'is_installed', 'is_active']] = merged_events[['event_id','app_id', 'is_installed', 'is_active']].astype(int)
    grouped_events = merged_events.groupby("event_id", as_index=False)
    app_event_info = grouped_events.apply(events_group_stat)
    return app_event_info


import pandas as pd
from collections import Counter
import json
import sys

#http://stackoverflow.com/questions/24980437/pandas-groupby-and-then-merge-on-original-table
#http://stackoverflow.com/questions/13854476/pandas-transform-doesnt-work-sorting-groupby-output/13854901#13854901
#
#dir_path = "/home/h/Desktop/talking_data/csv/"
dir_path = "/home/dz-h/Desktop/kaggle_test/csv_data/"

def app_label_feature():
    app_labels = pd.read_csv(dir_path + "app_labels.csv")
    grouped_labels = app_labels.groupby("app_id", as_index=False)
    app_label_info = grouped_labels.agg(lambda x: ",".join(list(x['label_id'].apply(str))))
    return app_label_info

def app_events_cat_feature(app_label_info):
    app_events = pd.read_csv(dir_path + "app_events.csv")
    merged_events = pd.merge(app_events,app_label_info, on = 'app_id')
    #merged_events[['event_id','app_id', 'is_installed', 'is_active']] = merged_events[['event_id','app_id', 'is_installed', 'is_active']].astype(int)
    #grouped_events = merged_events.groupby("event_id", as_index=False)
    #app_event_info = grouped_events.apply(events_group_stat)
    #return app_event_info
    return merged_events

def event_group_stat(group_df):
    installed_apps = []
    installed_labels = []

    active_apps = []
    active_labels = []

    for row in group_df.itertuples(index=False):
        #print type(row), row
        (event_id,app_id,is_installed,is_active,labels) = row
        if is_installed == 1:
            installed_apps.append(str(app_id))
            installed_labels.append(str(labels))

        if is_active == 1:
            active_apps.append(str(app_id))
            active_labels.append(str(labels))

    result_dict = {}
    result_dict["installed_apps"] = [",".join(installed_apps)]
    result_dict["installed_labels"] = [str(Counter(",".join(installed_labels).split(",")))]
    result_dict["active_apps"] = [",".join(active_apps)]
    result_dict["active_labels"] = [str(Counter(",".join(active_labels).split(",")))]
    #print result_dict
    return result_dict
    #return pd.DataFrame(result_dict)

def merged_events_features():
    merged_events = pd.read_csv("./merged_events.csv")
    grouped_events = merged_events.groupby("app_id", as_index=False)#.agg(event_group_stat)
    fp = open("merged_events_features.csv", 'w')
    i = 0
    for name, group in grouped_events:
        #print type(name), type(group)
        #print name
        #print group
        single_df = event_group_stat(group)
        single_df["event_id"] = [name]
        json.dump(single_df, fp)
        fp.write("\n")

        #single_df.to_csv("merged_events_features.csv", mode='a')
    #grouped_events.to_csv("merged_events_features.csv")
    fp.close()


def test():
    app_label_info = app_label_feature()
    merged_events = app_events_cat_feature(app_label_info)
    merged_events.to_csv("./merged_events.csv", index=False)

if __name__ == "__main__":
    #test()
    merged_events_features()
