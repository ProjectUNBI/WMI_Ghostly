import threading
from time import sleep
import eg
import wx.lib.scrolledpanel as scrolled

eg.RegisterPlugin(
    name="WMI Ghostly",
    author="Glu",
    guid="{1B1428D4-86BC-4A4E-941F-A90125262613}",
    version="0.1.1",
    kind="other",
    description="WMI module + Open Hardware Monitor. Please install and run Open Hardware Monitor. (https://openhardwaremonitor.org/documentation/)."
)



import wmi

def wmi_log(data):
  print("WMI: "+data)

class ThreadedSensor(object):
    def __init__(self,plugin,update_time):
        self.plugin = plugin
        self.is_sensing=True
        self.updatetime=update_time
        self.event= threading.Event()

    def sense(self):
        threading.Thread(target=self.selfsense).start()

    def selfsense(self):
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        while self.is_sensing:
            # wmi_log("Sensing")
            data=w.Sensor()
            for sensor in data:
              self.plugin.TriggerEvent("WMI_Sense_"+sensor.SensorType+"_"+sensor.Name, sensor.Value)
              # if sensor.SensorType == u'Temperature':
              #   self.plugin.TriggerEvent("WMI_Sense_"+sensor.SensorType+"_"+sensor.Name, sensor.Value)
              #   print(sensor.Name)
              #   print(sensor.Value)
            self.event.clear()
            self.event.wait(self.updatetime)
        wmi_log("Sensing has stoped")
    def wake(self):
        self.event.set()



class ScrollPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)




class WMI_Sense(eg.PluginBase):
    def __init__(self):
        self.threadedsensor=None
        pass

    def addLine(self, label, control, width=400):
        if (label is not None):
            self.boxsizer.Add(wx.StaticText(self.panel, -1, label + ":"), 0, wx.TOP, 3)
        try:
            control.Size.SetWidth(width)
        except AttributeError:
            print("no Width: " + str(label))
        self.boxsizer.Add(control, 0)
        return control

    def addGroup(self, label):
        sb = wx.StaticBox(self.spanel, label=label)
        self.boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        self.panel.sizer.Add(self.boxsizer)

    def Configure(self, update_time='5'):
        panel = eg.ConfigPanel(resizable=False)
        self.panel = panel
        self.spanel = ScrollPanel(panel)
        self.spanel.SetupScrolling()
        panel.sizer.Add(self.spanel, 1, wx.ALL | wx.EXPAND)
        self.addGroup("EventGhost Properties")
        # publicIpCtrl = self.addLine("Your Public IP or Host Name (like a dyndns host name). Leave blank to get it automatically", "")
        # textControl = wx.TextCtrl(panel, -1, myport)
        text = 'Please select the update frequency.'
        u_time = self.addLine(text + "Seconds per update", panel.SpinIntCtrl(update_time, min=1, max=65535))
        # panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(u_time.GetValue())

    def __start__(self, update_time):
        if(update_time>1):
            wmi_log("Updating sensor data for every " +str(update_time)+" seconds" )
        else:
            wmi_log("Updating sensor data for every " +str(update_time)+" second" )
        self.updatetime = update_time
        if(self.threadedsensor is not None):
            self.__stop__()

        wmi_log("Sensing has started")
        self.threadedsensor = ThreadedSensor(self,int(self.updatetime))
        threading.Thread(target=self.threadedsensor.sense(), ).start()

    def __stop__(self):
        wmi_log("Stoping sensor....")
        self.threadedsensor.is_sensing=False
        self.threadedsensor.wake()


