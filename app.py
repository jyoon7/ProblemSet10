from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    # Temporary list for search results, and a final list without duplicates
    temp = []
    venues = []

    # Convert input from the form into string
    keyword = str(request.form.get("name"))
    category = str(request.form.get("categories"))

    # Return error if no keyword or category is given (and no javascript)
    if not keyword:
        return render_template("failure.html")
    if category == "None":
        return render_template("failure.html")

    # Set integer "row" to the corresponding column number in the .cvs file (to search for the keyword within column)
    if category == "LICCATDESC":
        row = 5
    elif category == "DBANAME":
        row = 8
    elif category == "Neighborhood":
        row = 16
    elif category == "CITY":
        row = 24

    #Open csv file in Unicode
    file = open("entertainment-licenses.csv", "r", encoding="utf-8")
    reader = csv.reader(file)
    all_venues = list(reader)

    #Search for keyword in .csv, and append "venues" list with matching rows
    for x in all_venues:
        if keyword.capitalize() in x[row]:
                temp.append(x)

    # Remove duplicates and add it to final results list
    for y in range((len(temp))-1):
        if temp[y][8] not in temp[y+1][8]:
            venues.append(temp[y])
            
    
    # Return "venues" list to results.html
    return render_template("result.html", venues=venues, category = category, keyword = keyword)
