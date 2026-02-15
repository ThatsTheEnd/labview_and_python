import win32com.client  # Python ActiveX Client
import os
current_file_path = os.path.dirname(os.path.abspath(__file__))
vi_path = current_file_path + '\\test_no_connector_pane.vi'
LabVIEW = win32com.client.Dispatch("Labview.Application")
VI = LabVIEW.getvireference(vi_path)
VI._FlagAsMethod("Call")

VI.setcontrolvalue('Input 1', 100)
VI.setcontrolvalue('Input 2', 200)
VI.Call()
result = VI.getcontrolvalue('Sum')

print(result)


