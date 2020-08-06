from flask import Flask, render_template
import sentiment
import pandas as pd
from datetime import date, datetime

app = Flask(__name__)

@app.route('/')
def main():
    #sentiment.getData()
    df = pd.read_pickle("tmp/data.pickle")
    col = df["Date"]
    today = datetime.today()
    diff = (today - (col.max()))
    print(diff)
    print(df)
    if diff.seconds // 3600 > 0 or diff.days > 0:
        sentiment.getData()
    content = {}
    minSent = float(df.loc[len(df)-6]["Sentiment"])
    for i in range(len(df)-1, len(df)-7, -1):
        content["title"+str(-1*(i-len(df)))] = df.loc[i]["Title"]
        content["desc"+str(-1*(i-len(df)))] = df.loc[i]["Description"]
        content["url"+str(-1*(i-len(df)))] = df.loc[i]["URL"]
        content["source"+str(-1*(i-len(df)))] = df.loc[i]["Source"]
        content["img"+str(-1*(i-len(df)))] = df.loc[i]["imgURL"]
        content["sent"+str(-1*(i-len(df)))] = str(round(float(df.loc[i]["Sentiment"])*100, 2)) + "%"
    col = df["Date"]
    return render_template("index.html", content=content)
