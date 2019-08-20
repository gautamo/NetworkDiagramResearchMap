import geopy.distance
from geopy.geocoders import Nominatim

regions = {
    "california": (36.778259, -119.417931),
    "texas": (31.000000, -100.000000),
    "new york": (43.000000, -75.000000),
    "oregon": (44.000000, -120.500000)

}

#function takes string address and returns closest region in regiondict
def findClosestPoint(address, regiondict):

    #turns address to coordinates
    geopy.geocoders.options.default_user_agent = "globe-research"
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    coord = (location.latitude, location.longitude)

    shortdist = 10000
    shortloc = ""

    for region in regiondict:
        #get distance
        traveldist = geopy.distance.distance(coord, regiondict[region]).km

        #store region with shortest distance
        if traveldist < shortdist:
            shortdist = traveldist
            shortloc = (region, regiondict[region])

    return shortloc[0], shortloc[1]


#test any address to see function work
addy = "Dallas"

regionpick, coord = findClosestPoint(addy, regions)
print(f'Closest region is {regionpick} at {coord}')




