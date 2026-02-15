# Example - Call VI from Python

## Overview
This example demonstrates how to call a LabVIEW VI from Python using the vi.Call2() Method and a LabVIEW Executable that exposes it's ActiveX-Server.

## How to run
Run 'executable\Application.exe' and keep the application open
Then in CMD type
'python Call-In-Executable.py'
to run the (external) SubVI in the context of the running exe and send a random number to a Queue. This number is then displayed on the LabVIEW User Interface.