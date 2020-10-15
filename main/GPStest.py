GPS = "5648.878692,N,00929.595150,E,131020,112711.0,35.6,0.0,0.0"
PreLatitude = ""
Latitude = ""
Longitude = ""
GPSSTRING = ""
nActive = False


def isolateFirstDigits(body):
    if int(body[0:3]) <= 180:
        GPSstr = body[0:3] + ' ' + body[3:100]
    elif int(GPSSTRING[0:2]) <= 180:
        GPSstr = body[0:2] + ' ' + body[2:100]
    return GPSstr


def convertGPS(GPS):
    global GPSSTRING
    global Latitude
    global Longitude
    global nActive
    index = 0
    for char in GPS:
        if char == 'E':
            GPSSTRING = GPSSTRING + char
            break
        else:
            GPSSTRING = GPSSTRING + char
    for char in GPSSTRING:
        if char == ',':
            break
        else:
            Latitude = Latitude + char
        index = index + 1
    for char in GPSSTRING:
        if char == 'N':
            nActive = True
        if nActive == True and char != 'N' and char != 'E' and char != ',':
            Longitude = Longitude + char
    return str(isolateFirstDigits(Latitude) + ', ' + isolateFirstDigits(Longitude))


Coordinates = convertGPS(GPS)
print(Coordinates)
