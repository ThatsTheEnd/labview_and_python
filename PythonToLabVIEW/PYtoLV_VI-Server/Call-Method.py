import win32com.client  # Python ActiveX Client
import os
current_file_path = os.path.dirname(os.path.abspath(__file__))
vi_path = current_file_path + '\\test_no_connector_pane.vi'
print("Dispatching LabVIEW")
LabVIEW = win32com.client.Dispatch("Labview.Application")
print("Getting VI reference")
VI = LabVIEW.getvireference(vi_path)
VI._FlagAsMethod("Call")

print("Setting control values")
VI.setcontrolvalue('Input 1', 100)
VI.setcontrolvalue('Input 2', 200)
print("Calling VI") 
VI.Call()
print("Getting result")
result = VI.getcontrolvalue('Sum')

print(f"Result: {result}")
