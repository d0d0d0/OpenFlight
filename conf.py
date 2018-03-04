### QPX API credits ###
API_KEY = "OBFUSCATED"
REQ_URL = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=%s"

### mongoDB information ###
HOST = "localhost"
PORT = 27017
DATABASE = "openflight"
COLLECTION = "flights"

'''
For database creation,
after connecting mongo,

use openflight
db.createColletion("fligts")
'''

REQ = {
	    "passengers": {
	      "adultCount": 0
	    },
	    "slice": [ ]
}

FLIGHT = {
        "origin": "",
        "destination": "",
        "date": ""
}

'''
### Full request is supposed to look like this ###
### Slice contains all alternative flights ###
{
  "request": {
    "passengers": {
      "adultCount": 1
    },
    "slice": [
      {
        "origin": "BOS",
        "destination": "LAX",
        "date": "2017-11-12"
      }
    ]
  }
}
'''