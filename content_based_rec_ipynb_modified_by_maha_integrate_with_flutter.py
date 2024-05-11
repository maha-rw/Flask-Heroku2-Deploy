# -*- coding: utf-8 -*-
"""content-based-rec-ipynb modified by maha - INTEGRATE WITH FLUTTER.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m2UyLSRj8AaDgCXQXdmq5iQig7_LEZXk
"""
"""For testing of Tfidf"""
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, jsonify, request
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import warnings
import warnings
warnings.filterwarnings("ignore", message="The behavior of Series.argsort in the presence of NA values is deprecated.")




# -*- coding: utf-8 -*-
"""content-based-rec-ipynb modified by maha - INTEGRATE WITH FLUTTER.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m2UyLSRj8AaDgCXQXdmq5iQig7_LEZXk
"""
"""For testing of Tfidf"""
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, jsonify, request
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import warnings
import warnings
warnings.filterwarnings("ignore", message="The behavior of Series.argsort in the presence of NA values is deprecated.")


# Function to load data from Firestore and preprocess it
# Function to load data from Firestore and preprocess it
def load_data(questionsDF, default_total_upvotes=0, default_no_of_answers=0):
    if not questionsDF:
        return None

    # Initialize lists to store document data
    question_ids = []
    categories = []
    total_upvotes = []
    noOfAnswerss = []
    postedDates = []
    

    # Loop over all question documents
    for question in questionsDF:
        # Append document data to respective lists
        question_ids.append(question.get('questionDocId', ''))
        categories.append(question.get('selectedInterests', []))
        total_upvotes.append(question.get('totalUpvotes', default_total_upvotes))
        noOfAnswerss.append(question.get('noOfAnswers', default_no_of_answers))
        postedDates.append(question.get('postedDate', ''))


    # Create DataFrame
    data = {
        'question_id': question_ids,
        'category': categories,
        'totalUpvotes': total_upvotes,
        'noOfAnswers': noOfAnswerss,
        'postedDate': postedDates
    }
    df = pd.DataFrame(data)
    return df




# Function to recommend questions
def recommend_questions(questions_data, user_skills, user_interests, top_n=10):
    # Preprocess user input
    user_input = ' '.join(user_skills) + ' ' + ' '.join(user_interests)

    # Convert category lists to strings
    questions_data['selectedInterests'] = questions_data['category'].apply(lambda x: ' '.join(x))

    # Calculate TF-IDF similarity scores for categories
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(questions_data['selectedInterests'])

    # Calculate TF-IDF similarity scores for combined user skills and interests
    user_combined = ' '.join(user_skills + user_interests)
    user_tfidf_matrix = vectorizer.transform([user_combined])

    # Calculate similarity scores for categories
    similarity_scores = cosine_similarity(user_tfidf_matrix, tfidf_matrix).flatten()

    # Normalize total upvotes and number of answers
    max_upvotes = questions_data['totalUpvotes'].max()
    max_answers = questions_data['noOfAnswers'].max()
    questions_data['normalized_upvotes'] = questions_data['totalUpvotes'] / max_upvotes
    questions_data['normalized_answers'] = questions_data['noOfAnswers'] / max_answers
    
    # Remove timezone information from postedDate
    questions_data['postedDate'] = pd.to_datetime(questions_data['postedDate']).dt.tz_localize(None)

    # Calculate difference in days between current date and question timestamp (with timezone awareness)
    current_date = datetime.now().replace(tzinfo=None)
    questions_data['days_since_posted'] = (current_date - questions_data['postedDate']).dt.days


    # Define weights for each factor
    weights = {
        'selectedInterests': 0.5,                 # Weight for category
        'total_upvotes': 0.1 ,          # Weight for total upvotes
        'noOfAnswers': 0.2,              # Weight for number of answers
       'days_since_posted': 0.4       # Weight for days since posted
    }

    # Weight for days since posted using exponential decay
    max_days = questions_data['days_since_posted'].max()
    questions_data['weighted_days_since_posted'] = np.exp(-questions_data['days_since_posted'] / max_days)
   


    # Combine similarity scores and additional factors with weights
    weighted_similarity = (similarity_scores * weights['selectedInterests']) + \
                          (questions_data['normalized_upvotes'] * weights['total_upvotes']) + \
                          (questions_data['normalized_answers'] * weights['noOfAnswers']) + \
                          (questions_data['weighted_days_since_posted'] * weights['days_since_posted'])

    # Get top recommended question IDs
    sorted_indices = np.argsort(weighted_similarity)[::-1]  # Sort indices in descending order

    # Keep track of selected IDs
    selected_question_ids = set()
    recommended_question_ids = []
    print('************++++++++++++++********0000')
    # Select unique IDs until reaching the desired count
    for index in sorted_indices:
        question_id = questions_data.iloc[index]['question_id']
        if question_id not in selected_question_ids:
            recommended_question_ids.append(question_id)
            selected_question_ids.add(question_id)
            print(recommended_question_ids)
            print('************++++++++++++++*****87777777')
            if len(recommended_question_ids) == top_n:
                print(recommended_question_ids)
                print('************++++++++++++++*****87777777')
                break

    return recommended_question_ids


##### COURSES AND EVENTS BELOW >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def create_user_profiles(user_info_list):
    user_profiles = []

    for user_info in user_info_list:
        interests = user_info.get('interests', [])
        # Assuming each user has only one interest, so no need for Counter
        user_profile = {
            'user_id': user_info.get('email'),
            'username': user_info.get('username'),
            'interests': interests if interests else None,  # Directly assigning the interest
            'skills': user_info.get('skills'),  # No change for skills
            'attendancePreference' : user_info.get('attendancePreference'),
            'country': user_info.get('country').split(' ', 1)[1],
            'state': user_info.get('state'),
            'city': user_info.get('city'),
        }
        user_profiles.append(user_profile)

    # Print user profiles
    for profile in user_profiles:
        print("User ID:", profile['user_id'])
        print("Username:", profile['username'])
        print("Interests:", profile['interests'])
        print("Skills:", profile['skills'])
        print("Countryyyy", profile['country'])
        print("STATEEE", profile['state'])
        print("CITYYY", profile['city'])
    return user_profiles



# FUNCTION to measure similarity between two user profiles
def measure_similarity(user1, user2, user_info_list):
    # Combine interests and skills into a single string for each user
    user1_skills = user1.get('skills', [])
    user1_interests = user1.get('interests', [])
    user1_text = ' '.join(user1_skills + user1_interests)

    user2_skills = user2.get('skills', [])
    user2_interests = user2.get('interests', [])
    user2_text = ' '.join(user2_skills + user2_interests)

    # Convert user data to TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user1_text, user2_text])

    # Calculate cosine similarity between TF-IDF vectors
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    return similarity_score



def recommend_CE_to_user(all_courses, user_profiles, user_id, top_n=10):
    specific_user = None
    for user in user_profiles:
        if user['user_id'] == user_id:
            specific_user = user
            break

    if specific_user is None:
        print("User not found!")
        return []

    similar_users = []
    for user in user_profiles:
        if user != specific_user:
            similarity_score = measure_similarity(user, specific_user, all_courses)
            if similarity_score >= 0.5:
                similar_users.append((user, similarity_score))
      
       

    print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')  
    print(similar_users)
    print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')  
    print(specific_user)  
    recommended_courses = []
    for ce in all_courses:  # Changed variable name to 'ce' to avoid confusion with 'doc'
        ce_id = ce['CE_Id']  # Using 'CE_Id' from the data
        ce_attendance_type = ce['attendanceType']
        ce_country = ce['country']
        ce_state = ce['state']
        ce_city = ce['city']

        similarity_score = measure_similarity(ce, specific_user, all_courses)  # Passing 'ce' instead of 'user'

        for similar_user, _ in similar_users:
            if similar_user['user_id'] in ce.get('clickedBy', []):  # Using 'get' method to handle None
                similarity_score += 0.1

        if ce_attendance_type == specific_user.get('attendancePreference'):
            similarity_score += 0.05

        if ce_country and specific_user.get('country'):  # Checking for None and preprocessing if necessary
            if ce_country.strip().lower() == specific_user.get('country').strip().lower():  # Preprocessing and comparison
                similarity_score += 0.02

        if ce_state and specific_user.get('state'):  # Checking for None and preprocessing if necessary
            if ce_state.strip().lower() == specific_user.get('state').strip().lower():  # Preprocessing and comparison
                similarity_score += 0.02

        if ce_city and specific_user.get('city'):  # Checking for None and preprocessing if necessary
            if ce_city.strip().lower() == specific_user.get('city').strip().lower():  # Preprocessing and comparison
                similarity_score += 0.05

        recommended_courses.append((ce_id, similarity_score))

    recommended_courses.sort(key=lambda x: x[1], reverse=True)

    # Return only the course IDs
    return [course[0] for course in recommended_courses[:top_n]]






######### RRRRRRUUUUUUUNNNNN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

app = Flask(__name__)

@app.route('/', methods=['POST'])
def recommend():
    # Get user skills, interests, and questions input from request JSON
    user_skills = request.json.get('user_skills')
    user_interests = request.json.get('user_interests')
    questionsDF = request.json.get('all_questions')
    
    # Log the received data
    print("Received user skills:", user_skills)
    print("Received user interests:", user_interests)
    print("Received questions data:", questionsDF)
    print("/n/n/n/")

    # Load data and recommend questions
    questions_data = load_data(questionsDF)
    recommended_question_ids = recommend_questions(questions_data, user_skills, user_interests)

    # Convert Series of question IDs to JSON and return as response
    print(recommended_question_ids)
    return recommended_question_ids

@app.route('/recommendCE', methods=['POST'])  # Corrected route path
def recommendCE():
    user_Email = request.json.get('user_Email')
    users_Data = request.json.get('all_users')
    CoursesEvents_Data = request.json.get('all_CE')
    print('-----++++++++++++++++++++++++++++++    ',user_Email )
    print(CoursesEvents_Data)
    print('-----++++++++++++++++++++++++++++++')

    # Load data and recommend questions
    users_DF = create_user_profiles(users_Data)
    recommended_CE_ids = recommend_CE_to_user(CoursesEvents_Data, users_DF, user_Email)

    # Convert Series of question IDs to JSON and return as response
    print('|||||||||||||||||||||||||||||||||||||\n|||||||||||||||||  recommended_CE_ids HERREE ',recommended_CE_ids)
    return recommended_CE_ids

if __name__ == '__main__':
    app.run(debug=True)#, host='0.0.0.0', port=5000)












