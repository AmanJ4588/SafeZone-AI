from flask import Flask, render_template, request, jsonify
import firebase_admin 
import firebase_admin.exceptions
from firebase_admin import credentials
from firebase_admin import auth  
from firebase_admin import firestore
from crime_cluster_model.upload_script import upload_to_firestore_with_id
from crime_cluster_model.cluster_model import cluster_and_upload
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


cred = credentials.Certificate("safezone-ai-6019d-firebase-adminsdk-z0oi6-1775d444bd.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def verify_user(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:  
        print("Token verification failed:", e)
        return None

# Custom Flask command to run the upload script
@app.cli.command("upload_data")
def upload_data():
    excel_file = "crime_cluster_model/indore_crime_dataset.xlsx"  # Replace with your Excel file path
    collection_name = "crime_dataset"
    upload_to_firestore_with_id(db, excel_file, collection_name)

# Custom Flask command to run the cluster_and_upload_to_firebase
@app.cli.command("cluster_and_upload_to_firebase") 
def cluster_and_upload_to_firebase(): 
    cluster_and_upload(db) 


@app.route('/') 
@app.route('/index.html')
def index():
    return render_template('index.html') 

@app.route('/homepage.html') 
def homepage():
    return render_template('homepage.html') 

@app.route('/registrationPage.html') 
def regPage():
    return render_template('registrationPage.html')  

@app.route('/signup' , methods=['POST']) 
def signup(): 
    try: 
        username = request.form['username'] 
        fname = request.form['fname']
        lname = request.form['lname'] 
        email = request.form['email']  
        password = request.form['pass']  

        user = auth.create_user(
            uid = username,
            email=email,
            password=password, 
        )

        
        db.collection('users').document(user.uid).set({
        'username': username,
        'first_name': fname, 
        'last_name' : lname, 
        }) 
        return jsonify({'message': 'User created successfully!'}), 201

    except ValueError as e:
        # Handle invalid user input (e.g., missing fields, invalid email format)
        return jsonify({'error': 'Invalid user input: ' + str(e)}), 400

    except firebase_admin.exceptions.FirebaseAuthError as e:
        # Handle Firebase Authentication errors (e.g., email already in use)
        return jsonify({'error': 'Firebase Authentication error: ' + str(e)}), 400

    except Exception as e:  # Catch any other unexpected errors
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

@app.route('/verify_token', methods=['POST'])
def verify_token():
    id_token = request.form['id_token']
    uid = verify_user(id_token)
    if uid:
        return jsonify({"status": "success", "uid": uid}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid token"}), 401

@app.route('/deleteUser' , methods=['POST'])
def deleteUser():
    try:
        username = request.form['username']
        auth.delete_user(username) 
        
        db.collection('users').document(username).delete() 
        return jsonify({'message' : 'User deleted successfully!'}), 200 
    except firebase_admin.exceptions.FirebaseError as e:
        return jsonify({'error': str(e)}), 500 
    
@app.route('/get_red_zone_data', methods=['GET'])
def get_red_zone_data():
    try:
        red_zone_data = []  # List to hold the red zone data

        # Query clustered_data_points for Red Zone locations
        clustered_docs = db.collection('clustered_data_points').stream()

        # Collect the locations from the "Red Zone" and their crime counts
        red_zone_info = {}
        for doc in clustered_docs:
            data = doc.to_dict()
            if data.get("Zone Label") == "Red Zone":
                location = data.get("Location")
                crime_count = data.get("Crime Count", 0)  # Default to 0 if Crime Count is not available
                red_zone_info[location] = {
                    "Crime Count": crime_count
                }

        # Now query crime_dataset for the coordinates of those locations
        crime_docs = db.collection('crime_dataset').stream()
        for doc in crime_docs:
            data = doc.to_dict()
            location = data.get("Location")
            latitude = data.get("Latitude")
            longitude = data.get("Longitude")

            # Only add data for locations in the Red Zone
            if location in red_zone_info and latitude and longitude:
                red_zone_data.append({
                    "Location": location,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Crime Count": red_zone_info[location]["Crime Count"] 
                })
        return jsonify(red_zone_data)  # Send filtered red zone data to the frontend
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/firebase-config")
def firebase_config():
    return jsonify({
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
    })


if __name__ == '__main__':
    app.run(port = 5000 , debug=True)
