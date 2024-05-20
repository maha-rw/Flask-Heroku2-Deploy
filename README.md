## **Recommendation System API** 

This repository contains the Python code for a recommendation systems API that is deployed on Heroku and used by the Texel Flutter application.

### **Table of Contents**


Introduction

Features

Technologies Used

Installation and Setup

API Documentation

Deployment

Integration with Texel Flutter App









### **Introduction**

The Recommendation System API is a backend service that provides personalized recommendations to the Texel Flutter application. It uses a combination of techniques, such as content-based filtering and collaborative filtering, to generate relevant recommendations for users.



### **Features**
Retrieves user information and preferences from the Texel Flutter app

Processes user data to generate personalized recommendations of questions, courses and events.

Provides 2 API endpoints for the Texel app to fetch recommended items.

Supports real-time updates and re-training of the recommendation model


### **Technologies Used**

-Python

-Flask 

-Pandas

-Heroku (for deployment)


## **Installation and Setup**
Clone the repository: git clone https://github.com/maha-rw/Flask-Heroku2-Deploy.git

1- Install the required dependencies: pip install -r requirements.txt

2- Set up the necessary environment variables (e.g., database connection details, API keys)

3- Run the Flask application: python app.py


### **API Documentation**
The Recommendation System API provides the following endpoints:

-Endpoint 1: /recommendQ

Method: POST

Input: user_skills, user_interests, and all_questions

Output: recommended question IDs


- Endpoint 2: /recommendCE
  
Method: POST

Input: user_Email, all_users, and all_CE

Output: recommended course/event IDs


### **Deployment**

The Recommendation System API is deployed on Heroku. You can access the deployed application at the following URL:

(https://flask-deploy-gp2-717dffd55916.herokuapp.com/) 


### **Integration with Texel Flutter App**


The Texel Flutter application integrates with the Recommendation System API to fetch personalized recommendations for users. The integration details can be found in the Texel Flutter App, where instead of using local host to send requests to the recommendation systems API, just use the deployed application using Heroku. 

