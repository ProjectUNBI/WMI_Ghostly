# WMI_Ghostly
WMI plugin for Eventghost to measure the CPU temperature,usage,etc....


# How to add???

Note: You need to download this "https://openhardwaremonitor.org/downloads/" and have to run it to make WMI work. 

Okey... you must install the eventghost
Clone these files and move to your event ghost file.

 Move these flollowing file [which is in this repo] to your Eventghost installaton directory
 
/EventGhost/lib27/site-packages/WMI-1.4.9.dist-info/INSTALLER<br />
/EventGhost/lib27/site-packages/WMI-1.4.9.dist-info/METADATA<br />
/EventGhost/lib27/site-packages/WMI-1.4.9.dist-info/RECORD<br />
/EventGhost/lib27/site-packages/WMI-1.4.9.dist-info/top_level.txt<br />
/EventGhost/lib27/site-packages/WMI-1.4.9.dist-info/WHEEL<br />
/EventGhost/lib27/site-packages/wmi.py<br />
/EventGhost/lib27/site-packages/wmi.pyc<br />
/EventGhost/plugins/WMI/__init__.py<br />

eg: move "/EventGhost/lib27/site-packages/wmi.py" in "C:\Program Files (x86)\EventGhost\lib27\site-packages"

Restart the Eventghost

add the plugin in "Autostart"->"Add Plugin"->"General Plugins"->"WMI Ghostly" and set the time

# Modifications:

If you need to trigger by only one sensor data, for example lets says "Temperature",--> then-> uncomment "line 39-41" and comment the "line 38" like the following:


            data=w.Sensor()
            for sensor in data:
              #self.plugin.TriggerEvent("WMI_Sense_"+sensor.SensorType+"_"+sensor.Name, sensor.Value)
               if sensor.SensorType == u'Temperature':
                 print(sensor.Name)
                 print(sensor.Value)
            self.event.clear()
            self.event.wait(self.updatetime)
            
            
  
            
