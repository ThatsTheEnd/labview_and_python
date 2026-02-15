# Call LabVIEW Webservice from Python

This simple example consists of a LabVIEW Webservice with an "add"-Get-Method and a python script that calls that method using the "requests" library.

## How to run

Run LabVIEW as an Administrator
Open the LabVIEW Project and on the Webservice select Rightclick -> Start
In the demo folder, click the adressbar and type in CMD then hit enter.
This should give you a CMD window with the path to the demo directory.
Then run
python CallLVWebservice.py

It should call the "add" function and display the result of an addition.