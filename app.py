from flask import Flask, render_template
from scrape_mars import scrape

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.  
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars.drop()

data = scrape()

# Creates a collection in the database and inserts two documents
db.mars.insert_many(
    [
        data
    ]
)




# Set route
@app.route('/')
def index():

    return render_template('index.html', data=data)


@app.route('/scrape/')
def update_data():
    # Store the entire team collection in a list
    data = scrape()
    print(data)

    # Return the template with the teams list passed in
    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
