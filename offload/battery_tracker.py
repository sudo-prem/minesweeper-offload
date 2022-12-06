import pyRAPL
import wmi
from constants import *
from task_profiler import *

class BatteryTracker:
    def __init__(self):
        
        self.EPI = Constants.getInstance().EPI
        self.wmiObj = wmi.WMI(moniker = "//./root/wmi")
        self.taskProfiler = TaskProfiler(self.testFunction)

    
    def get_battery_status(self):
        batteryStatusDict = {}

        batteryInfo = self.wmiObj.ExecQuery('Select * from BatteryStatus where Voltage > 0')
        for i, b in enumerate(batteryInfo):
            batteryStatusDict['Discharging'] = b.Discharging
            batteryStatusDict['RemainingCapacity'] = b.RemainingCapacity
            batteryStatusDict['Active'] = b.Active
            batteryStatusDict['Critical'] = b.Critical
        
        return batteryStatusDict
    
    def get_local_EPI(self):
        return self.EPI

    @pyRAPL.measureit
    def testFunction(self):
        a=1
        for i in range(100000):
            a+=1


    def measureEnergy(self):

        pyRAPL.setup()
        self.measureEnergy()
        print(pyRAPL.get_energy_info())

    def measure_local_epi(self):
        IC = self.taskProfiler.get_instruction_count()
        energy = pyRAPL.get_energy_info()
        epi = energy / IC
        self.EPI = epi

if __name__ == "__main__":
    batteryTracker = BatteryTracker()
    print(batteryTracker.get_battery_status())
    

    




