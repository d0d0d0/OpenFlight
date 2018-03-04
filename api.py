import json
import urllib2
import copy
import datetime
import pprint

from pymongo import MongoClient

from conf import *

class OpenFlightAPIException:
	'''
		Exception class for OpenFlightAPIValidator
	'''
	pass

class OpenFlightAPIValidator:
	'''
		Validator class for OpenFlightAPI
	'''
	def __init__(self):
		pass

	# TODO: Throw exception instead of return value
	def valDate(self, date):
		try:
			datetime.datetime.strptime(date, '%Y-%m-%d')
			return True
		except ValueError as e:
			print str(e)
			return False

	# TODO: Add airpot code list
	def valAirport(self, airport):
		return True

	# TODO: Throw exception instead of return value
	def valPrice(self, price):
		try:
			pric = int(price)
			if pric >0:
				return pric
			else:
				pass

		except ValueError:
			pric = float(price)	
			if pric >0:
				return pric
			else:
				pass
		except Exception as e:
			print str(e)

class OpenFlightAPI:
	'''
		API class
	'''
	def __init__(self):
		self.req = urllib2.Request(REQ_URL % (API_KEY))
		self.req.add_header('Content-Type', 'application/json')
		self.validator = OpenFlightAPIValidator()

	# Makes google-api calls using data as json object
	def send(self, data):
		try:
			query = {'request': data}
			response = urllib2.urlopen(self.req, json.dumps(query))
			
			return json.load(response)
		except Exception as e:
			print str(e)
			
	# Create individual flight dictionary
	def makeFlight(self, org, dest, passen, date):
		try:	 
			if self.validator.valAirport(org) and self.validator.valAirport(dest) and \
				self.validator.valDate(date):
				
				fly = copy.deepcopy(FLIGHT)
				fly['origin'] = org
				fly['destination'] = dest
				fly['date'] = date

				return fly
			else:
				print "Unexpected error."
				return 0

		except Exception as e:
			print str(e)
			return 0

	# Main search function
	def search(self, org, dest, passen, istrip, outDate, inDate="", maxPrice="0"):		
		try:
			req = copy.deepcopy(REQ)
			req['passengers']['adultCount'] = passen
			resp = 0

			# Trick for one-way
			inFly = True
			
			if istrip:
				inFly = self.makeFlight(dest, org, passen, inDate)
				req['slice'].append(inFly)

			if self.validator.valPrice(maxPrice) >= 0:
				req['maxPrice'] = maxPrice

			outFly = self.makeFlight(org, dest, passen, outDate)
			req['slice'].append(outFly)

			if inFly and outFly:
				resp = self.send(req)

			return resp

		except Exception as e:
			print str(e)

	def saveFlight(self, flight, host=HOST, port=PORT, db=DATABASE, collect=COLLECTION):
		try:
			# TODO: Keep it connected instead of reopening for every flight
			client = MongoClient(host, port)
			db = client[db]
			fid = db.collect.insert_one(flight).inserted_id

		except Exception as e:
			print str(e)


	def readFlight(self, host=HOST, port=PORT, db=DATABASE, collect=COLLECTION):
		'''
		Reads all tweets from db
		'''
		try:
			# TODO: Keep it connected instead of reopening for every flight
			client = MongoClient(host, port)
			db = client[db]
			cursor = db.collect.find()
			flights = []
			for document in cursor:
				flights.append(document)

			return flights
		except Exception as e:
			print str(e)	


if __name__ == "__main__":
	api = OpenFlightAPI()

	# One way BOS-LAX for a person at 2017-11-12
	print "######### ONE WAY ##########"
	resp = api.search("BOS", "LAX", 1, False, "2017-11-12")

	if resp:
		# Save flights to db
		api.saveFlight(resp)

		# Read flights from db
		flights = api.readFlight()
		for f in flights:
			pprint.pprint(f)

	'''
	# One way BOS-LAX for a person at 2017-11-12
	print "######### ONE WAY WITH MISWRITTEN DATE ##########"
	api.search("BOS", "LAX", 1, False, "2017-11/12")

	# One way BOS-LAX for a person at 2017-11-12 for max 700USD
	print "######### ONE WAY WITH MAX PRICE ##########"
	api.search("BOS", "LAX", 1, False, "2017-11-12", 700)

	# Trip BOS-LAX for a person at 2017-10-12 and 2017-11-12
	print "######### TRIP ##########"
	api.search("BOS", "LAX", 1, False, "2017-10-12", "2017-11-12")
	'''

