# 2022 Mini Drive Station Instructions

To clone the software needed for the mini drive station you need to create a directory for the code and then run the command 

```
https://thedirtymechanics.com/bitbucket/scm/rob22/2022-mini-drive-station.git
```

You need to put circuit python on the pico. You need to download the uf2 at [Circuit Python](https://circuitpython.org/board/raspberry_pi_pico/).

After download is complete hold the bootsel button and plug in the pico to your PC. You can then copy the uf2 to pico. You need to power off / on the pico. Once the pico comes up in circut python you copy code.py to it. Code.py is in folder you cloned.

You will also need to copy the file lib/neopixel.mpy to lib folder on the pico. The folder is avaialbe in the folder you cloned above.

You will need to install python on your PC [download link](https://www.python.org/downloads/).

You need to install the python libraries pynput, pyserial and pynetwork tables libraries on your pc.

```
pip install pynput
pip install pyserial
pip install pynetworktables
```

You will need to add this code in robot.java in the robotPeriodic() method
```
   // Code for the mini drive station
    int disableCount = (int) SmartDashboard.getNumber("Disable", -1);
    if (disableCount == 3932) {
      logf("!!!!!!!!!!!!!! Will Disable the robot from mini drive station !!!!!!!!!!!!!\n");
      // Set Bat Volts to 0 to indicate to the mini drive station that the robot is
      // disabled
      SmartDashboard.putNumber("BatVolts", 0);
      System.exit(0); // Disable the robot
    }

    if (count % 100 == 0) {
      boolean dis = isDisabled();
      if (PDH != null) {
        SmartDashboard.putNumber("BatVolts",  (!dis) ? round2(PDH.getVoltage()) + Math.random() * .1 : -Math.random() * .1 );
      } else {
        SmartDashboard.putNumber("BatVolts", (!dis) ? 12.0 + Math.random() * .1 : 0 - Math.random() * .1);
      }
    }
  }


```

You will need to add this code at the declares for the variables in robot.java

```
PowerDistribution PDH = new PowerDistribution();
```

You will need to add this code in robot.java in the disabledInit() method

```
// Set Bat Volts to 0 to indicate to the mini drive station that the robot is disabled
    SmartDashboard.putNumber("BatVolts", 0);
```


This is optional -- can not put it on Kevin as it uses a differnet UPDReceiver.java
You will need to update robot.java to support upd 
Start by copying the file upd.java to the utilities directory
Then add code to the robot.java 
```
// Add to imports
import frc.robot.utilities.UDPReceiver;

// Add to declares
public static UDPReceiver udp;

// Add to the end of  robotInit()
try {
      udp = new UDPReceiver("Test");
      Thread t = new Thread(udp);
      t.start();
    } catch (Exception e) {
    }

```


To use Mini Drive Station the command 'python getBattery.py" must be run in the folder you cloned.

The program getBattery.py uses network tables to receive battery voltage from the RoboRio and tells the pico what color to display. When the disable button is hit on the pico, the pico sends 3932 to the RoboRio and it will then disable the robot by doing a system.exit()
