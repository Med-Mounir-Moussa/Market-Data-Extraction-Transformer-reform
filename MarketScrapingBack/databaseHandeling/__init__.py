from flask import Flask
from flask import request
import json
from flask import Response
import time
from flask import jsonify
import SiblingsTags
import selenium
from XPathGettingWithBS import *
from selenium import webdriver
from flask_pymongo import PyMongo
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
app = Flask(__name__)
"""app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.config["MONGO_DBNAME"] = "db" 
mongo = PyMongo(app,"db")"""
@app.route('/api/add', methods = ['POST'])
def add():
    user = client.db.web
    res = request.get_json()
    url =res["url"]
    xpath1 = res["productXPATH"]
    xpath2 = res['valueXPATH']
    timer = res['timer']

    try :
        if(timer >0):
            while(True):
                parsing = SiblingsTags.parseWebsite(url,xpath1,xpath2)
                newEntry = dict()
                newEntry = {"url": url, "productXPATH": xpath1, "valueXPATH": xpath2}
                newEntry["dataSet"] = parsing
                user.insert(newEntry)
                time.sleep(timer)
    except SiblingsTags.AccessingWebsiteError:
        return Response("{Error occured while trying to access the website}", status=300, mimetype='application/json')
    except SiblingsTags.ProductXPATHError:
        return Response("{Error occured while trying to parse the product XPATH}", status=301, mimetype='application/json')
    except SiblingsTags.ValueXPATHError:
        return Response("{Error occured while trying to parse the price XPATH}", status=302,
                        mimetype='application/json')
    except SiblingsTags.ExtractionAlgorithmError:
        return Response("{Error occured while finding the siblings", status=303,
                        mimetype='application/json')
    """except:
        return  Response("{Error occured}", status=304,
                        mimetype='application/json')
    #for x in user.find({"url" : url}):"""
    print (json.dumps(parsing))
    return Response(json.dumps(parsing), status=200, mimetype='application/json')

#@app.route('/api/update',methods = )
@app.route('/api/find',methods = ['GET'])
def find():
    user = client.db.web
    cursor = str(list(user.find()))
    print(cursor)
    return (cursor)



app.run(debug=True)


"""
from flask import Flask, request
from pymongo import MongoClient
import pprint
from XPathGettingWithBS import getBsObjectWithSelenium
from XPathGettingWithBS import AbsolutePathForXpath
from SiblingsTags import getListOfSiblingsXpaths
app = Flask('__main__')


@app.route('/api/G', methods=['GET'])
def afficher_dataBase():
    client = MongoClient('localhost',27017)
    dataBase = client.stage14
    l=""
    for post in dataBase.posts.find():
        for key in post:
            if (key != '_id'):
                l=l+post[key]+'\n'
    print(l)
    return(l)

@app.route('/api/P', methods=['POST'])
def traiter_donnees():
    print(request.data)
    url=request.json['url']
    xpath1=request.json['XPATH1']
    xpath2=request.json['XPATH2']
    print(url,xpath1,xpath2)
    client = MongoClient('localhost',27017)
    dataBase = client.stage14
    bsObj = getBsObjectWithSelenium(url)
    xpath_1 = AbsolutePathForXpath(xpath1,bsObj)
    xpath_2 = AbsolutePathForXpath(xpath2,bsObj)
    (tag1ListOfXpaths ,tag2ListOfXpaths) = getListOfSiblingsXpaths(xpath_1,xpath_2,bsObj)
    posts = dataBase.posts
    posts.insert(tag1ListOfXpaths)
    return ("good Job")

app.run()
"""
#"C:\Program Files\MongoDB\Server\4.0\bin\mongod.exe" --dbpath="c:\data\db"