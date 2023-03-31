import requests

api_endpoint_w = " https://api.ambeedata.com/weather/latest/by-lat-lng"
api_key = "ee9363b0b9197d12bab864bcc73394ff28a8265a67d499cd80e53c5a7dba045e"
par = {
        "lat":12.3,
        "lng": 76.6
    }
h = {
        "x-api-key":api_key
    }

data = requests.get(api_endpoint_w,params=par,headers=h)
con = data.json()["data"]
for item in con:
    print(item)
    print(con[item])