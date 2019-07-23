from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "REDACTED"
foursquare_client_secret = "REDACTED"
version = "20130815"

def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	lat, lon = getGeocodeLocation(location)
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	h = httplib2.Http()
	url = ("https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=%s&ll=%f,%f&query=%s" % 
		(foursquare_client_id, foursquare_client_secret, version, lat, lon, mealType))
	result = json.loads(h.request(url, 'GET')[1])
	if result['response']['venues']:
		#3. Grab the first restaurant
		firstRes = result['response']['venues'][0]
		idRes = firstRes['id']
		name = firstRes['name']
		resAddress = firstRes['location']['formattedAddress']
		address = ""
		for i in resAddress:
			address += i + " "
		resAddress = address
		#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		picsURL = ("https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=%s" %
			(idRes, foursquare_client_id, foursquare_client_secret, version))
		pics = json.loads(h.request(picsURL, 'GET')[1])
		if pics['response']['photos']['items']:
			#5. Grab the first image
			firstPic = pics['response']['photos']['items'][0]
			pre = firstPic['prefix']
			suf = firstPic['suffix']
			picURL = pre + '300x300' + suf
		else:
			#6. If no image is available, insert default a image url
			picURL = "none"

			#7. Return a dictionary containing the restaurant name, address, and image url	
		resInfo = {'name':name, 'address':resAddress, 'pic':picURL}
		print "Restaurant Name: %s" % resInfo['name']
		print "Restaurant Address: %s" % resInfo['address']
		print "Image: %s \n" % resInfo['pic']
		return resInfo
	else:
		print "Nothing found for %s" % location
		return "none"
if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")
