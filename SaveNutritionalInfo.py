import urllib
import urllib2
import json
import os
import MySQLdb

api_key = "jwUc1bdSRZafHuqAcQBpJ1u6d4SkNH9VU5UKeya5"
search_url = r"http://api.nal.usda.gov/usda/ndb/search"
nutrition_url = r"http://api.nal.usda.gov/usda/ndb/reports"

def saveNutrition(food_name, ndbno, nutrient_name, measure, unit, value):
    print("Food name: " + food_name)
    print("NDBNO: " + ndbno)
    print("Nutrient name: " + nutrient_name)
    print("Measure: " + measure)
    print("Units: " + unit)
    print("Value: " + value)

    #save to database
    conn = MySQLdb.connect(host= "mysql-user",
                                user="depotte8",
                                passwd="A36490765",
                                db="depotte8")
    x = conn.cursor()
    try:
        x.execute("""INSERT IGNORE INTO NutritionInfo (ndbno, name, nutrient, measure, unit, value) VALUES (%s,%s,%s,%s,%s,%s)""",(ndbno, food_name, nutrient_name, measure, unit, value))
        conn.commit()
    except Exception as e:
        conn.rollback()
    conn.close()


def fetchNutrition(ndbno):
    values = {'api_key' : api_key,
              'format' : 'json',
              'type' : 'b', # options: b-basic, f-full, s-stats
              'ndbno' : ndbno }
    data = urllib.urlencode(values)
        
    req = urllib2.Request(nutrition_url + "?" + data)
    response = urllib2.urlopen(req)
    json_response = response.read()
    #json_response = json_response.decode()
        
    result = json.loads(json_response)
        
    food_name = result["report"]["food"]["name"]
    for nutrient in result["report"]["food"]["nutrients"]:
        # we only care about Energy (calories) at this point
        if nutrient["nutrient_id"] == "208":
            n_name = nutrient["name"]
            n_unit = nutrient["unit"]
            for measure in nutrient["measures"]:
                saveNutrition(food_name, ndbno, n_name, measure["label"], n_unit, measure["value"])

def searchNutrition(searchString):
    try:
        values = {'api_key' : api_key,
                  'format' : 'json',
                  'q' : searchString }
        data = urllib.urlencode(values)
        #data = data.encode('utf-8')
        
        req = urllib2.Request(search_url + "?" + data)
        response = urllib2.urlopen(req)
        json_response = response.read()
        #json_response = json_response.decode()
        
        result = json.loads(json_response)
        
        foods = result["list"]["item"]
        for food in foods:
            ndbno = food["ndbno"]
            fetchNutrition(ndbno)

    except Exception as e:
        print(e)

searchStrings = ["hamburger", "steak", "french fries"]
for search in searchStrings:
	searchNutrition(search)
