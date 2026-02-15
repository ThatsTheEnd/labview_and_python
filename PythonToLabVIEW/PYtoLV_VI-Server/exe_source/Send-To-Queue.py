import pythoncom
import win32com.client  # Python ActiveX Client
from win32com.client import VARIANT
import os

current_file_path = os.path.dirname(os.path.abspath(__file__))
vi_path = current_file_path + '\\sendqueue.vi'

Input1 = 100
Input2 = 200
LabVIEW = win32com.client.Dispatch("MyLvApp.Application") # "MyLvApp" was defined in the LabVIEW buildspec (advanced tab)
vi = LabVIEW.getvireference(vi_path)
vi._FlagAsMethod("Call2")

param_names  = VARIANT(
    pythoncom.VT_BYREF | pythoncom.VT_ARRAY | pythoncom.VT_BSTR,
    ()
)

param_values = VARIANT(
    pythoncom.VT_BYREF | pythoncom.VT_ARRAY | pythoncom.VT_VARIANT,
    ()
)

vi.Call2(param_names, param_values,
        False,   # open FP?
        False,   # close FP after call?
        False,   # suspend on call?
        False)   # bring LabVIEW to front?

print(param_values)