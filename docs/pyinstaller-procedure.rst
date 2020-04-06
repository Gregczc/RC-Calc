Compiling the project into an unique exe file
=============================================

notes:
Do not forget to properly set the path vatriable
`set FLASK_APP=hello.py`
I have encountered issues with setuptools>45. Downgrading it made pyinstaller work fine.

Pyinstaller intresting parameters:

- F: To bundle everything in a single file
- w: to avoid displaying the console
- --add-data: to add folders to the build directory
- i: to add an icon

Command usage:

For now :

pyinstaller -F -i logo/rc-calc-256.ico RC_Calc.py

