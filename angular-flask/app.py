from flask import Flask, render_template, make_response, send_file
import json
from flask_cors import CORS, cross_origin
from flask import request
from flask import Response
import csv
from database_service import DatabaseService
from typing import Any


# da bi aplikacija mogla biti servirana potrebno je:
# ng build --base-href /static/ (izvesti tu komandu u angular projektu)
# on nakon toga generira zapakiranu aplikaciju u svom /dist/ folderu
# od tamo kopirati sve .js datoteke i styles.css u static folder od app.py
# kopirati i index.html iz dist u templates od app.py
# tako bi sve trebalo dobro raditi
# moram jos isprobati jel budu assets tak radili isto

database_service = DatabaseService("insects.db")

app = Flask(__name__)
# if app.debug:
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

white = ['http://127.0.0.1:4200']

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.get('/data/<type>')
def get_product(type):
  j = ""
  if type == "json":
    with open("static/files/json/insects.json", "r") as f:
      j = json.load(f)
    return json.dumps(j)
  elif type == "csv":
    print("GETTING CSV DATA")
    c = ""
    with open("static/files/csv/insects.csv", "r") as f:
      c = f.read()
    return json.dumps({"csv" : c})

@app.route('/download/<type>')
def download_file(type):
  params: dict[str, Any] = request.args.to_dict()
  attribute = list(params.keys())[0]
  value = params[attribute]

  print("GOT PARAMS: ", params)
  data = database_service.get_joined_where(attribute, value)
  # json format:
  if type == 'json':
    print("PREPARING JSON")
    s = json.dumps({"data": data})
    print("json: ", data)
    return Response(str.encode(s), mimetype='application/json', headers={'Content-Disposition':'attachment;filename=insects.json'})
  # csv format:
  elif type == 'csv':
    print("PREPARING CSV")
    print("make csv from: ", data)
    rows = database_service.getCsvRowsFromJsonsList(data)
    print("I got rows: ", rows)
    s = "\n".join(rows)
    response = Response(str.encode(s), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=insects.csv'
    return response
  return (json.dumps({"data":"No given file type!"}))
 
@app.get('/insects')
def get_data_table():
  params: dict[str, Any] = request.args.to_dict()
  if len(list(params.keys())) == 0:
    print("NEMA QUERY PARAMETARA! vracam sve!")
    data = database_service.get_all_joined_insects_and_orders()
    print("got data: \n", data)
    return json.dumps({"data":data})

  attribute = list(params.keys())[0]
  value = params[attribute]
  print("SEARCHING IN DATABASE FOR: ", attribute, " ", value)
  fetch = database_service.get_joined_where(attribute, value)
  for f in fetch:
    print(f)
  return json.dumps({"data": fetch})

app.run(port=8080, debug=True)