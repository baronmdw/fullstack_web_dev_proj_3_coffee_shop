# Coffee Shop Backend

## Getting Started to run the project submission

This project runs on pyhton 3.11.1 so please make sure that you have this version installed and activated.
It is highly recommended to work with a virtual environment (e.g. with virtualenv). 
Since this project is only to be run on my machine or on a machine of a udacity reviewer I hereby assume that everyone running it knows how to set up a virtual environment and the correct version of python.

After having set your virtual environment run
```bash
pip install -r requirements.txt
```
The requirements document has been updated according to the packages that are used in this project and their versions that work with python 3.11.1.

To run the server cd into ./src and run following commands as a Mac-User:
```bash
export FLASK_APP=api.py
flask run
```

As a Windows User run:
```bash
set FLASK_APP=api.py
flask run
```