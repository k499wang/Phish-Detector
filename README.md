# Phishing URL Classifier

This project classifies URLs as either phishing or benign using Logistic Regression. It features a React-based frontend, a Flask API backend, and is deployed using Docker on Render.

The original notebook can be found here: https://colab.research.google.com/drive/1PEUx_5g7xRI5RkcvffeyYdsYpRFmHMon

The Deployed website can be found here: https://phish-detector-1.onrender.com/

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview
The **Phishing URL Classifier** is a machine learning application designed to distinguish phishing URLs from legitimate ones. The core classifier is built using Logistic Regression, trained on features scraped from websites. The project integrates a web-based interface for user interaction and a backend API for prediction services.

## Features
- Logistic Regression-based URL classification.
- Scrapes features from websites dynamically.
- Interactive web-based UI built with React.
- Scalable and containerized application using Docker.
- Deployed on Render for seamless access.
- API for classification services.

## Architecture
The application consists of three main components:
1. **Frontend**: A React application providing an intuitive user interface for URL classification.
2. **Backend**: A Flask API that scrapes website features, processes requests, and classifies URLs.
3. **Model**: A Logistic Regression model trained on features extracted from URLs.


## Technologies Used
- **Frontend**: React, HTML, CSS, JavaScript.
- **Backend**: Python, Flask.
- **Web Scraping**: BeautifulSoup, requests.
- **Machine Learning**: Logistic Regression (scikit-learn).
- **Deployment**: Docker, Render.

## Setup

### Prerequisites
- Install [Git](https://git-scm.com/).
- Install [Docker](https://www.docker.com/).
- Install [Node.js and npm](https://nodejs.org/).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/phishing-url-classifier.git
   cd phishing-url-classifier
   ```
2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
3. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:5000`

## Usage
1. Open the web application.
2. Enter a URL into the input field.
3. Click the "Classify" button.
4. The application scrapes features from the provided URL, processes them, and displays the prediction result (e.g., "Phishing" or "Benign").

## Deployment
This application is deployed on [Render](https://render.com). Follow these steps for deployment:

1. **Dockerize the Application**:
   - Ensure the `Dockerfile` and `docker-compose.yml` are correctly configured.

2. **Push to GitHub**:
   - Push your code to a GitHub repository.

3. **Set Up Render**:
   - Create a Render account and link your GitHub repository.
   - Configure separate services for the frontend and backend.

4. **Deploy**:
   - Render automatically builds and deploys your application.


