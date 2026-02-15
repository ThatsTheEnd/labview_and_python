# Example - Call VI from Python

## Overview
This example demonstrates how to call a LabVIEW VI from Python using the vi.Call() and vi.Call2() Methods.

## How to run
In the demo-folder, click the adressbar and type 'CMD', then hit enter.
This should open a CMD Window with the path to the current folder.
Then run:
'python Call-Method.py'
or
'python Call2-Method.py'

These run a SubVI in the context of the LabVIEW Development System and collect the result.


## Tips
The result should be displayed in the CMD window after execution. For Call it's a single Number (300), for Call2 it's a dictionary of different values, the first two being the inputs, the third one the sum of the inputs.

When using a VI with a Connector-Pane, use the VARIANT Containers used in the Call2-Example. If you want to use Controls/Indicators that are not connected to the connector pane, use the Set-/GetCtrlValue Methods.

## About exe
To call a SubVI in the context of a LabVIEW-Executable, you must enable the ActiveX-Server in the Buildspecification (Advanced Tab), and give a unique name to your application.
You can then replace 'Labview.Application' with 'MyApp.Application' and connect to the executables ActiveX Server.