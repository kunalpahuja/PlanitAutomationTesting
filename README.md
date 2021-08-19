Create a virtual environment
============================
virtualenv env

Activate environment
====================
source env/bin/activate

Install requirements
====================
pip install -r requirements.txt

Download selenium web driver for the browser we want to test
=============================================================
Chrome selenium downloads can be found here:
https://sites.google.com/a/chromium.org/chromedriver/downloads

Place the selenium web driver in the current project path

Run the tests
=============
pytest test.py