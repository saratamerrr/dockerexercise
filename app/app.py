# Import necessary libraries
from flask import Flask, render_template
import redis
import os
import csv

# Initialize Flask app
app = Flask(__name__, static_url_path='/static')
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/titanic')
def titanic():
    # Define the path to the Titanic dataset CSV file
    dataset_path = os.path.join(os.getcwd(), 'Dataset_Titanic.csv')

    # Check if the file exists
    if not os.path.exists(dataset_path):
        return "Dataset file not found."

    # Load Titanic dataset from the CSV file
    with open(dataset_path, 'r') as file:
        reader = csv.reader(file)
        # Extract first 5 rows
        first_5_rows = [row for idx, row in enumerate(reader) if idx <= 5]

 # Calculate the number of men and women who survived
    men_survived = sum(1 for row in first_5_rows[1:] if row[4] == 'male' and row[1] == '1')
    women_survived = sum(1 for row in first_5_rows[1:] if row[4] == 'female' and row[1] == '1')


   # Render Titanic template with first 5 rows and survivor counts
    return render_template('titanic.html', data=first_5_rows, men_survived=men_survived, women_survived=women_survived)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
