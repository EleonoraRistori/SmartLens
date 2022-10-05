import pickle
import json
import sys
import os
import mysql.connector
import numpy
import pymysql

# open pickle file
with open('./features/MobileNetV3Small_convolutions_features.pck', 'rb') as infile:
    obj = pickle.load(infile)
json_obj = json.loads(json.dumps(obj, default=str))
list = []
for i in range(0, len(obj)):
    list.append([])
    list[i].append(obj[i][1])
    list[i].append(json.dumps(obj[i][0].tolist()))

# convert pickle object to json object


# write the json file
with open(
        os.path.splitext('./features/MobileNetV3Small_convolutions_features.pck')[0] + '.json',
        'w',
        encoding='utf-8'
) as outfile:
    json.dump(json_obj, outfile, ensure_ascii=False, indent=4)


mydb = mysql.connector.connect(
    host="localhost",
    user="smartlensv1",
    password="smartlensv1",
    database="smartlensv1"
)


file = './features/MobileNetV3Small_convolutions_features.json'
json_data = open(file).read()


def to_db(list):
    mycursor = mydb.cursor()

    sql = "INSERT INTO pythonfeatures (artwork, features, distance) VALUES (%s, %s, %s)"

    for i in range(0, len(list)):
        mycursor.execute(sql, (list[i][0], list[i][1], 17))

    mydb.commit()


to_db(list)
