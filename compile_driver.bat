python .\setup.py sdist --format=zip
pip install .\ -U
pyinstaller --onefile driver.spec