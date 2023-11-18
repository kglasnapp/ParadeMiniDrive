netsh interface set interface wi-fi "DISABLED"
SLEEP 1
netsh interface set interface wi-fi "ENABLED"
SLEEP 1
netsh wlan connect name = 3932_Mini
echo Connected