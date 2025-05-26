# Basic Concepts

## What is Docker?
Docker is a platform that allows you to package applications and their dependencies into containers. Containers are lightweight, portable, and ensure consistency across different environments.

## Why Use Docker?
- **Consistency:** Run the same application in development, testing, and production.
- **Isolation:** Each container runs independently, avoiding conflicts.
- **Portability:** Containers can run on any system with Docker installed.

## Project Structure
- `app.py`: Main Flask application. This is where the core logic of the web app resides, including routes, data fetching, and rendering.
- `requirements.txt`: Python dependencies. Lists all the packages needed to run the app, ensuring reproducibility.
- `Dockerfile`: Instructions to build the Docker image. Defines how to package the app and its dependencies into a container.
- `templates/`: HTML templates for the web app. Used by Flask to render dynamic web pages.

## Key Dependencies and Their Roles
- **Flask:** A lightweight web framework for Python. It handles HTTP requests, routing, and rendering HTML templates.
- **pandas:** A powerful library for data manipulation and analysis. Used to process and clean stock data.
- **matplotlib:** A plotting library for creating static, animated, and interactive visualizations in Python.
- **yfinance:** A library to fetch historical market data from Yahoo Finance.
- **pymongo:** A Python driver for MongoDB, enabling the app to interact with a MongoDB database if needed.
- **pandas-ta:** Technical Analysis Indicators for pandas, useful for financial data analysis.
- **numpy:** Fundamental package for scientific computing with Python, often used for numerical operations.

## Foundational Concepts
### REST APIs
A REST API (Representational State Transfer Application Programming Interface) allows different software systems to communicate over HTTP. In this project, Flask can expose REST endpoints to serve data or receive input from users or other systems.

### Flask
Flask is a micro web framework for Python. It allows you to build web applications quickly and with minimal code. Flask apps are structured around routes (URLs) and views (functions that handle requests and return responses).

### MongoDB
MongoDB is a NoSQL database that stores data in flexible, JSON-like documents. It is useful for storing unstructured or semi-structured data and is often used with Python via the pymongo library.

## How the App Works
- Fetches stock data using yfinance.
- Processes data with pandas and pandas-ta.
- Visualizes data with matplotlib.
- (Optionally) Stores or retrieves data from MongoDB using pymongo.
- Serves a dashboard via Flask, rendering HTML templates from the templates/ directory.

This architecture ensures modularity, scalability, and ease of deployment, especially when combined with Docker for consistent environments.