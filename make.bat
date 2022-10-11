powershell -Command "& {pyuic5 -x ui/gui.ui -o ui/gui.py}"
powershell -Command "& {pyinstaller run.spec --noconfirm}"
pause 