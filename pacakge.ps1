python-3.8.5-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
pip install pyinstaller
pyinstaller .\src\mask_visualizer.py --onefile --icon .\assets\images\carnival-mask.ico --add-data .\assets;.\assets
Copy-Item -r .\assets .\dist\
Set-Location .\dist\
tar -czvf mask_visualizer.tar.gz .\assets .\mask_visualizer.exe