from time import sleep
import requests
from requests.exceptions import HTTPError
from haversine import Haversine as hav
_HEADERS={
    #"X-Device-Id":"", # From my testing, this is unnecesarry
    #"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36", # also seems not required
    "Authorization":"Bearer <>" # Insert your token there. Sniff it from their website if you need to.
}
_TARGET_CIRCLE_NAME = "Circle" # Target circle to enable proximity alerts on
_USER_FIRST_NAME = "Name"       # First/last name exactly as appears in L360
_USER_LAST_NAME = "Name"      # NOTE: Ensure your name is set correctly - some users full name is in their First Name field.
                                 # Is not important for anyone else

                                 
def get_circles():
    # returns array of circles
    try:
        r = requests.get(
            "https://api-cloudfront.life360.com/v3/circles",
            headers=_HEADERS
        )
        return r.json()
    except HTTPError as http_err:
        print("HTTP error occured: %s" % http_err)
    except Exception as other:
        print("Other error occured: %s" % other)

def get_people(circle):
    # using circle ID as circle, returns array of people in circle
    try:
        r = requests.get(
            "https://api-cloudfront.life360.com/v3/circles/{}".format(circle),
            headers=_HEADERS
        )

        data = r.json()
        return data['members']




    except HTTPError as http_err:
        print("HTTP error occured: %s" % http_err)
    except Exception as other:
        print("Other error occured: %s" % other)

circles = get_circles()['circles']
target_circle = {}

# Find target circle
for i in circles:
    if i['name'] == _TARGET_CIRCLE_NAME:
        target_circle = i
        break

# Main loop - runs every 10 secs. Lower number, more resolution - but more notifications
while True:
    sleep(10)
    people = get_people(target_circle['id'])

    # Get user location
    user_lat = float(people[0]['location']['latitude']) # too lazy to write a loop to search for the user,
    user_long = float(people[0]['location']['longitude']) # gonna assume it's always the first result. :/

    # Get others locations
    for i in people:
        try:
            t_lat = float(i['location']['latitude'])
            t_long = float(i['location']['longitude'])
            t_first = i['firstName']
            t_last = i['lastName']

            # calculate distance to user
            print(t_first + " " + t_last + " is " + str(round(hav([user_long, user_lat], [t_long, t_lat]).miles,3)) + " miles away.")


        except TypeError as type_error:
            #Location sharing paused/off - no data (Skip)
            continue
            #print("No location data for " + i['firstName'] + " " + i['lastName']) 


