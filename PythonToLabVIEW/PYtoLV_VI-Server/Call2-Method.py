import pythoncom
import win32com.client  # Python ActiveX Client
from win32com.client import VARIANT
import os

current_file_path = os.path.dirname(os.path.abspath(__file__))
vi_path = current_file_path + '\\test_with_connector_pane.vi'

LabVIEW = win32com.client.Dispatch("Labview.Application.8")
vi = LabVIEW.getvireference(vi_path)  # Path to LabVIEW VI
vi._FlagAsMethod("Call2")  

# VARIANT array with names of all in- and outputs
param_names  = VARIANT(
    pythoncom.VT_BYREF | pythoncom.VT_ARRAY | pythoncom.VT_BSTR,
    ("Input 1", "Input 2", "Sum")
)

# VARIANT array with values for all inputs, and placeholders for all outputs
param_values = VARIANT(
    pythoncom.VT_BYREF | pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
    (100, 200, 0)
)

# Call the VI
vi.Call2(param_names, param_values,
        True,   # open FP?
        False,   # close FP after call?
        False,   # suspend on call?
        True)   # bring LabVIEW to front?

print(param_values)

