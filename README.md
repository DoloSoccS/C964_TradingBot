# C964_TradingBot
Capstone Project for Computer Science B.S.

The purpose of this project is to predict whether a particular stock should be bought or sold. The model used is XGBoost. The database used to hold the model data is MongoDB. Git for version control and Docker for portability and efficiency. The front end was built using the Flask framework.

IMPORTANT:
In order to run the TA-lib module, Microsoft Visual C++ dependencies will need to be installed.
https://visualstudio.microsoft.com/visual-cpp-build-tools/
Download the build tools installer and be sure to add the "Desktop Development C/C++" package.

MongoDB Compass was downloaded and installed alongside to visually verify the database accuracy. This could be accomplished in the command line but this is a more efficient way if able to use.

Had to run "docker run -d --name mongodb -p 27017:27017 mongo" to get mongo service started. Would not allow database
connection otherwise.

Tools:
PyCharm version 24.1.3+
Python 3.12
Docker version 28.0.4, build b8034c0
Docker Desktop version 4.40.0(187762)
MongoDB Compass version 1.46.3
Git version 2.45.1.windows.1

There are a few specific things to be aware of when installing this program, specifically the use of MongoDB and TA-Lib. For MongoDB, Docker will be the easiest way to start the mongod service. Required for running pymongo library. After installing Docker, simply pull the latest mongodb/mongodb-community-server image and run the container. Technically, you do not need to install a MongoDB gui application. However, this will be helpful to ensure database connections are successfully created instead of running the necessary troubleshooting through the command line.
For TA-Lib, this is much more involved. First, install the MS Visual Studio build tools. https://visualstudio.microsoft.com/downloads/?q=build+tools You will need to install the Desktop Development with C++ and .Net Desktop Build Tools modules. After that, TA-Lib will need to be installed via an .exe file. https://ta-lib.org/install/ has the list of available executables. Preferably this is being done on Windows in which case use the “recommended” executable installer. Once that is done, go into command line and run “pip install TA-Lib”. This should complete the install at which point the import statements should work.
The steps for successfully running the program are below.

Install Python – Choose a version compatible with 3.12
Install TA-Lib (See notes above for installation guide.)
Install Docker -> Pull “mongodb/mongodb-community-server” image -> run container
Install pip
Run ‘pip install -r requirements.txt’ from the project’s root directory
The passphrase is located in the backend.py file to login to the app
After successfully accessing the application, select from the list of tickers available to get responses on that company.
