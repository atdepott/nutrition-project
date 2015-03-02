import urllib
import urllib2
import json
import os

api_key = "jwUc1bdSRZafHuqAcQBpJ1u6d4SkNH9VU5UKeya5"
search_url = r"http://api.nal.usda.gov/usda/ndb/search"

def fetchNutrition(searchString):
    try:
        values = {'format' : 'json',
                  'q' : searchString,
                  'api_key' : api_key }
        data = urllib.urlencode(values)
        
        req = urllib2.Request(search_url, data)
        response = urllib2.urlopen(req)
        json_response = response.read()
        
        result = json.loads(json_response)
        print(result)
        #try:
        #    lat_long = result["results"][0]["geometry"]["location"]
        #    print location + str(lat_long)
        #    return lat_long
        #except:
        #    print result
        #    return ""
    except Exception as e:
        print("ERROR! " + e.message)

searchString = "cheddar cheese"
fetchNutrition(searchString)
