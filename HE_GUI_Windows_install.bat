rem assumes python 2.7 has already been installed in default directory


set PATH=%PATH%C:\Python27;
set PATH=%PATH%C:\Python27\Scripts
set PYTHONPATH=%PYTHONPATH%;C:/Python27/
python -m pip install -U pip setuptools


pip install --upgrade pip


pip install wheel


pip install -- upgrade wheel


pip install Pillow


pip install --upgrade Pillow
rem pip install scipy


rem pip install --upgrade scipy


pip install numpy


pip install --upgrade numpy


rem pip install pb_tool


rem pip install --upgrade pb_tool
pip install matplotlib
pip install --upgrade matplotlib
echo %PATH%