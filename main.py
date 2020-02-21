import serial
import RPi.GPIO as GPIO
import httplib
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)
pin = 21
GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
ser.flushInput()
ser.flushOutput()
lat = ''
lon = ''

#number = 

def convert_gps(lat, lon):
    lat = float(lat)
    lon = float(lon)

    lat /= 100
    lon /= 100

    part1 = int(str(lat)[:-1].split('.')[1]) * 1667
    part2 = int(str(lon)[:-1].split('.')[1]) * 1667

    lat = str(lat)[:-1].split('.')[0] + '.' + str(part1)
    lon = str(lon)[:-1].split('.')[0] + '.' + str(part2)
    return lat, lon

def send_sms(to, msg):
    try:
        conn = httplib.HTTPSConnection("api.msg91.com")

	payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": " \
                  "\""+msg+"\", \"to\": [\""+to+"\"] }] }"

        headers = {'authkey': "", 'content-type': "application/json"}

        conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

    except Exception as e:
        print(e)



while True:
    if  GPIO.input(pin) == 0:
        print("pin triggered")
        gps = ser.readline()
        if gps[0:6] == '$GPGGA':
            lat = gps[17:26]
            print('LAT:', lat)
            lon = gps[31:40]
            print('LON:', lon)
            lat, lon = convert_gps(lat, lon)
            print(lat, lon)
            #url = "Lat: "+str(lat)+" Lon: "+str(lon)+" Map: "+"http://maps.google.com/maps?q=' + lat + ',' + lon"
            #send_sms(str(number), url)
            #print("sms sent")
