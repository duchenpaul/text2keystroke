SET appName=text2keystroke
pyinstaller --onefile .\%appName%.py 
move dist\%appName%.exe %cd%

del /s /f /q  text2keystroke.spec

REM walkaround RD bug
timeout 1
RD /S /Q   dist\ build\