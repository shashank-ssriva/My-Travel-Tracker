# Import the neccessary modeules
from flask import Flask, render_template, json, request, redirect
import pymysql
from tables import Results
from flaskext.mysql import MySQL
import dateutil.parser as parser

# Invoke MySQL
mysql = MySQL()
app = Flask(__name__)

# MySQL database details
app.config['MYSQL_DATABASE_USER'] = 'TravelDetailsUser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Amix@2109'
app.config['MYSQL_DATABASE_DB'] = 'MyTravelTracker'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3307
mysql.init_app(app)

# Define the homepage. This page controls the data to be submitted.
@app.route('/')
def main():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM TravelDetails")
        tripcount = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM TravelDetails WHERE trip_type = 'International'")
        internationalflights = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM TravelDetails WHERE trip_type = 'Domestic'")
        domesticflights = cursor.fetchone()[0]
        if internationalflights > domesticflights:
            diffint = internationalflights - domesticflights
        else:
            diffint = domesticflights - internationalflights
        cursor.execute("SELECT destination_airport, COUNT(*) as count FROM TravelDetails WHERE trip_type = 'International' GROUP BY destination_airport ORDER BY count DESC LIMIT 1")
        mostvisiteddest = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) as count FROM TravelDetails WHERE trip_type = 'International' GROUP BY destination_airport ORDER BY count DESC LIMIT 1")
        mostvisiteddestcount = cursor.fetchone()[0]
        cursor.execute("SELECT destination_airport, COUNT(*) as count FROM TravelDetails WHERE trip_type = 'Domestic' GROUP BY destination_airport ORDER BY count DESC LIMIT 1")
        mostvisiteddomdest = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) as count FROM TravelDetails WHERE trip_type = 'Domestic' GROUP BY destination_airport ORDER BY count DESC LIMIT 1")
        mostvisiteddomdestcount = cursor.fetchone()[0]
        cursor.execute("select source_airport from TravelDetails ORDER BY travel_date DESC LIMIT 1;")
        lastsource = cursor.fetchone()[0]
        cursor.execute("select destination_airport from TravelDetails ORDER BY travel_date DESC LIMIT 1;")
        lastdestination = cursor.fetchone()[0]
        cursor.execute("select travel_date from TravelDetails ORDER BY travel_date DESC LIMIT 1;")
        lastdate = cursor.fetchone()[0]

        cursor.execute("SELECT destination_airport, COUNT(*) as count FROM TravelDetails WHERE trip_type = 'International' GROUP BY destination_airport ORDER BY count DESC")
        dataarray = cursor.fetchall()
        labels = []
        values = []
        for i in dataarray:
            labels.append(i[0])
            values.append(i[1])

        cursor.execute("SELECT destination_airport, COUNT(*) as count FROM TravelDetails WHERE trip_type = 'Domestic' GROUP BY destination_airport ORDER BY count DESC")
        dataarraydom = cursor.fetchall()
        labelsdom = []
        valuesdom = []
        for i in dataarraydom:
            labelsdom.append(i[0])
            valuesdom.append(i[1])

        # Code to find the years & their respective trip counts
    
        cursor.execute("SELECT travel_date FROM TravelDetails")
        yearArray = cursor.fetchall()
        yearlist = []
        yearlistarray = []
        for item in yearArray:
            yearlist.append(item[0])
        for x in yearlist:
            y = parser.parse(x).year
            yearlistarray.append(y)
        uniqueyearlist = []
        tripcountlist = []
        for x in yearlistarray:
            if x not in uniqueyearlist:
                uniqueyearlist.append(x)
        uniqueyearlist.sort()
        for x in uniqueyearlist:
            cursor.execute("SELECT COUNT(*) FROM TravelDetails WHERE travel_date LIKE %s", ("%" + str(x) + "%",))
            tripcountarray = cursor.fetchall()
            for z in tripcountarray:
                tripcountlist.append(z[0])
        conn.close()

        return render_template('index.html',
        tripcount = tripcount, internationalflights = internationalflights,
        domesticflights = domesticflights, mostvisiteddest = mostvisiteddest,
        mostvisiteddestcount = mostvisiteddestcount,
        mostvisiteddomdest = mostvisiteddomdest, mostvisiteddomdestcount = mostvisiteddomdestcount,
        lastsource = lastsource, lastdestination = lastdestination, lastdate = lastdate,
        diffint = diffint, labels = labels, values = values, labelsdom = labelsdom, valuesdom = valuesdom,
        uniqueyearlist = uniqueyearlist, tripcountlist = tripcountlist
    )
    except Exception as e:
        return json.dumps({'error': str(e)})

# addDetails route takes the values from the homepage & POSTs to the add-details.html page.
@app.route('/addDetails', methods=['POST', 'GET'])
def addDetails():
    try:
        _tookoff = request.form['took-off-from']  # GET data from the text-box.
        _landedon = request.form['landed-on']  # GET data from the text-box.
        _tripdate = request.form['trip-date']  # GET data from the text-box.
        _triptype = request.form['trip-category']  # GET data from the text-box.

        if _tookoff and _landedon and _tripdate and _triptype and request.method == 'POST':  # If none of the text-boxes is empty & we are clicking the submit button.
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "INSERT INTO TravelDetails(source_airport, destination_airport, travel_date, trip_type) VALUES(%s, %s, %s, %s)"
            data = (_tookoff, _landedon, _tripdate, _triptype,)
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/')
        else:
            return 'Please fill all the details...', 400
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/tripDetails')
def tripDetails():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM TravelDetails")
        rows = cursor.fetchall()
        table = Results(rows)
        table.border = True
        return render_template('trip-details.html', table=table)
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run(port=5001, debug=True)