# SafeZone-AI

An AI-powered project aimed at improving urban safety by mapping crime hotspots. The system uses machine learning to predict crime-prone areas, supporting informed decision-making for individuals and law enforcement.

---

## Features

- Crime hotspot mapping using machine learning.
- Integration with Firebase for authentication and database management.
- An interactive map for visualizing crime hotspots for better clarity.

---

## ⚠️ Warning

The dataset included in this repository is **synthetic data** and is not authentic. It has been created solely for the purpose of demonstrating the working of this project. The dataset should not be used as a source of real-world information or relied upon for decision-making.

---

## Local Setup Instructions

Follow these steps to set up the project locally:

### Step 1: Clone the Repository
1. Open a terminal or command prompt.
2. Run the following command to clone the repository:
   - `git clone https://github.com/AmanJ4588/SafeZone-AI.git`


### Step 2: Set Up the Virtual Environment and Install Dependencies
1. Navigate to the cloned repository folder. 
2. Create a Python virtual environment.  
3. Activate the virtual environment
4. Install the required dependencies from `requirements.txt`


### Step 3: Create a Firebase Project
1. Go to the Firebase Console
   - `https://console.firebase.google.com`
2. Create a new Firebase project.
3. Set up **Cloud Firestore** and **Firebase Authentication**:
   - Enable Cloud Firestore in the database section.
   - Configure Firebase Authentication (email/password).


### Step 4: Configure Firebase in `app.py` and `index.html`
1. Retrieve the **Firebase configuration object** from your Firebase project's settings.
2. Update the following files with your Firebase project's secret keys:
   - **`app.py`**: Add your Firebase Admin SDK private key and other required settings.
   - **`index.html`**: Add your Firebase configuration object in the appropriate `<script>` tag.


### Step 5: Upload the crime dataset to Cloud Firestore  
1. Execute the following command on the terminal with activated virtual env.
   - `flask upload_data`

### Step 6: Cluster the crime datapoints and upload it to Cloud Firestore
1. Execute the following command on the terminal with activated virtual env. 
   - `flask cluster_and_upload_to_firebase`

### Step 7: 
1. Open the terminal in your project directory.
2. Make sure your virtual environment is activated.
3. Run the Flask app using the following command:
   - `flask run`
4. By default, the app will run on `http://127.0.0.1:5000`



