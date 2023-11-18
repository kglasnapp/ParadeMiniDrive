import subprocess
import time 
MyWish = subprocess.run (['netsh', 'interface', 'set', 'interface', "wi-fi", "DISABLED"])
MyWish

print("DISABLED")
time.sleep(5)
MyWish = subprocess.run (['netsh', 'interface', 'set', 'interface', "wi-fi", "ENABLED"])
MyWish
print("ENABLED")