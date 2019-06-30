from flask import Flask, render_template, jsonify
import pymysql
app = Flask(__name__ , template_folder= '')

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

    def rideshare_aritra(self):
        self.cur.execute("select make, model, completed_on from rideshare where completed_on > '2017-01-24 00:00:00'")
        result = self.cur.fetchall()
        return result

'''
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

@app.route('/')
def landing():
    return render_template('/austin.html')


#-------------------------------------------------------
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
#-------------------------------------------------------

@app.route('/aritra')
def arirta():
    def db_query():
        db = Database()
        emps = db.rideshare_aritra()
        return emps
    res = db_query()
    # print(res)
    return render_template('index.html', result=res, content_type='application/json')



if __name__ == '__main__':
    app.run(debug = True)