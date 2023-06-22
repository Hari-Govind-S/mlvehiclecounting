# Vehicle Counting with Image Processing and Machine Learning
This project consists of two types

1) Front-end created using react js
2) Back-end created using flask

To run this project, you have run both the parts of the project in two different terminals simultaneously. 
# Running React js part
To run the front-end of the project, open a ternimal in the folder containing the files for front-end. Then type 'npm install' to install all the necessary modules. 
```
npm install
```
After this is done you can run it using 'npm start' command
```
npm start
```
# Running Flask
Goto the directary containing flask files and open a ternimal. Install virtualenv on windows by using following command.
```
python -m pip install virtualenv
```
After it is completed, create a virtual environment
```
python -m venv venv
```
Activite the virtual environment 
```
.\venv\Scripts\activate
```
Next we have to install all the necessary python libraries using pip command
```
pip install flask
pip install flask_cors
pip install ultralytics
pip install cvzone
pip install scikit-image
pip install filterpy
```
Finially you can run the server.py file using the command
```
python server.py
```
