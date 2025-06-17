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