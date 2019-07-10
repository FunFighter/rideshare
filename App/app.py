from flask import Flask, render_template, jsonify
import pymysql
app = Flask(__name__ , template_folder= 'templates')

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "toor1234"
        db = "ride_share"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        
    def rideshare_heat(self):
        self.cur.execute("select end_location_lat, end_location_long from rideshare where completed_on > '2017-01-24 00:00:00'")
        result = self.cur.fetchall()
        return result

    def color_count(self):
        self.cur.execute("select color, count(*) from rideshare where completed_on > '2017-01-24 00:00:00' group by(color)  order by count(*) desc limit 8")
        result = self.cur.fetchall()
        return result

    def make_count(self):
        self.cur.execute("select make, count(*) from rideshare where completed_on > '2017-01-24 00:00:00' group by(make)  order by count(*) desc limit 15")
        result = self.cur.fetchall()
        return result

    def rideshare_aritra(self):
        self.cur.execute("select make, model, completed_on from rideshare where completed_on > '2017-01-24 00:00:00'")
        result = self.cur.fetchall()
        return result
'''
select color, count(*) from rideshare where completed_on > '2017-01-24 00:00:00' group by(color) 
select make, count(*) from rideshare where completed_on > '2017-01-24 00:00:00' group by(make)  order by count(*) desc limit 15


{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [125.6, 10.1]
  },
  "properties": {
    "name": "Dinagat Islands"
  }
}
'''
#------ Landing page ----------------------
@app.route('/')
def landing():
    return render_template('/index.html')

#------------------Heat Map-------------------------------------
@app.route('/geoJsonData')
def geodatar():
    def db_query():
        db = Database()
        emps = db.rideshare_heat()
        return emps
    res = db_query()


    json_data_dict = []
    

    for data in res:
        dict_data = {
        'geometry' : { "coordinates": [data['end_location_lat'],data['end_location_long'] ]}
        }
        json_data_dict.append(dict_data)

    dict_struc = {
        'type': "FeatureCollection",
        'features' : json_data_dict}

    return jsonify(dict_struc)

@app.route('/heatmap')
def heatmap():
    return render_template('/austin.html')


#---------------Pie Chart------------------

@app.route("/pieChart")
def pieChart():
    return render_template('pie.html')

@app.route("/pie")
def pieData():
    def db_query():
        db = Database()
        emps = db.color_count()
        return emps
    res = db_query()

    data_list = []
    color_list = []
    color_count= []

    for value in res:
        color_list.append(value['color'])
        color_count.append(value['count(*)'])

    pie_data_struct = {
            "labels" : color_list,
            "values" : color_count,
            "type" : "pie"
        }

    data_list.append(pie_data_struct)
    return jsonify(data_list)


#-------------Bar Chart--------------

@app.route("/barChart")
def barChart():
    return render_template('bar.html')


@app.route("/bar")
def barData():
    def db_query():
        db = Database()
        emps = db.make_count()
        return emps
    res = db_query()

    data_list = []
    make_list = []
    make_count= []

    for value in res:
        make_list.append(value['make'])
        make_count.append(value['count(*)'])

    bar_data_struct = {
            "x" : make_list,
            "y" : make_count,
            "type" : "bar"
        }

    data_list.append(bar_data_struct)
    return jsonify(data_list)

#------------ aritra ------------------
@app.route('/aritra')
def arirta():
    def db_query():
        db = Database()
        emps = db.rideshare_aritra()
        return emps
    res = db_query()
    # print(res)
    return render_template('index.html', result=res, content_type='application/json')


#---- start server ---
if __name__ == '__main__':
    app.run(debug = True)