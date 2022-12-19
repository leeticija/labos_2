from flask import Flask, render_template, make_response, send_file
import json
from flask_cors import CORS, cross_origin
from flask import request
from flask import Response
import csv
from database_service import DatabaseService
from typing import Any
import traceback


# da bi aplikacija mogla biti servirana potrebno je:
# ng build --base-href /static/ (izvesti tu komandu u angular projektu)
# on nakon toga generira zapakiranu aplikaciju u svom /dist/ folderu
# od tamo kopirati sve .js datoteke i styles.css u static folder od app.py
# kopirati i index.html iz dist u templates od app.py
# tako bi sve trebalo dobro raditi
# moram jos isprobati jel budu assets tak radili isto
# update: asseti rade, samo je potrebno dodati putanju u angular.json

database_service = DatabaseService("insects1.db")

app = Flask(__name__)
# if app.debug:
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

white = ['http://127.0.0.1:4200']

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/openapi.yaml')
def yaml():
  return render_template("spec.yaml")

@app.get('/data/<type>')
def get_product(type):
  j = ""
  if type == "json":
    with open("static/files/json/insects.json", "r") as f:
      j = json.load(f)
    return json.dumps(j)
  elif type == "csv":
    c = ""
    with open("static/files/csv/insects.csv", "r") as f:
      c = f.read()
    response = Response(json.dumps({"csv": c}), 200, None, 'application/json')
    # return json.dumps({"csv" : c})
    return response

@app.route('/download/<type>', methods = ['GET'])
def download_file(type):
  params: dict[str, Any] = request.args.to_dict()
  attribute = list(params.keys())[0]
  value = params[attribute]

  data = database_service.get_joined_where(attribute, value)
  # json format:
  if type == 'json':
    s = json.dumps({"data": data})
    return Response(str.encode(s), mimetype='application/json', headers={'Content-Disposition':'attachment;filename=insects.json'})
  # csv format:
  elif type == 'csv':
    rows = database_service.get_csv_rows_from_jsons_list(data)
    s = "\n".join(rows)
    response = Response(str.encode(s), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=insects.csv'
    response.headers['Status'] = 200
    return response
  return (json.dumps({"data":"No given file type!"}))

@app.route('/insects/<id>', methods = ['DELETE'])
def delete_existing_insect(id):
  r = database_service.delete_existing_insect(id)
  response = Response(json.dumps({"data" : r}), mimetype='application/json')
  response.status = 'error_message' in r.keys() and 404 or 200
  return response

# update postojeceg insekta
# required request data: insect id (in url), data(in body) that has to be altered.
@app.route('/insects/<id>', methods = ['PUT'])
def update_existing_insect(id):
  form: dict[str, Any] = request.form.to_dict()
  r = database_service.update_existing_insect(id, form)
  response = Response(json.dumps({"data" : r}), mimetype='application/json')
  response.status = 'error_message' in r.keys() and 404 or 200
  return r

# treba vratiti novo stvoreni objekt s njegovim identifikatorom.
# obavezna polja koja moraju doci u requestu: valid order_name, genus, specie.
# ostala polja bi bilo dobro da ima, ali nisu krucijalna.
@app.route('/insects', methods = ['POST'])
def post_new_insect():
  form: dict[str, Any] = request.form.to_dict()
  try:
    new_insect = database_service.insert_new_insect(form)
    return json.dumps({"insect" : new_insect})

  except:
    traceback.print_exc()
    response = Response(json.dumps({"error_message":"Request is invalid! Required in body: order_name, genus, specie."}))
    response.status = 400
    response.mimetype = 'application/json'
    return response

# speciesCount?low=0&high=0
@app.route('/orders/speciesCount', methods = ['GET'])
def get_orders_where_species_count():
  params: dict[str, Any] = request.args.to_dict()
  r = database_service.get_orders_by_species_count(params)
  response = Response(json.dumps({"data": r}))
  response.status = 200
  response.mimetype = 'application/json'
  return response

@app.route('/orders/<id>/metamorphosis', methods = ['GET'])
def get_metamorphosis_by_order_id(id):
  # ako resurs ne postoji, vratiti 404 i poruku o greski.
  r = database_service.get_metamorphosis_by_order_id(id)
  response = Response(json.dumps({"data" : r}))
  response.status = 'error_message' in r.keys() and 404 or 200
  response.mimetype = 'application/json'
  return response

@app.route('/orders/<id>', methods = ['GET'])
def get_order_by_id(id):
  # ako resurs ne postoji, vratiti 404 i poruku.
  r = database_service.get_order_by_id(id)
  response = Response(json.dumps({"data" : r}))
  response.status = 'error_message' in r.keys() and 404 or 200
  response.mimetype = 'application/json'
  return response

@app.route('/insects/<id>', methods = ['GET'])
def get_insect_by_id(id):
  # ako resurs ne postoji, vratiti 404 i poruku o greski.
  r = database_service.get_insect_by_id(id)
  response = Response(json.dumps({"data" : r}))
  response.status = 'error_message' in r.keys() and 404 or 200
  response.mimetype = 'application/json'
  return response

@app.route('/insects', methods = ['GET'])
def get_data_table():
  params: dict[str, Any] = request.args.to_dict()
  if len(list(params.keys())) == 0:
    data = database_service.get_all_joined_insects_and_orders()
    response = Response(json.dumps({"data": data}))
    response.status = 200
    response.mimetype = 'application/json'
    return response
    
  attribute = list(params.keys())[0]
  value = params[attribute]
  fetch = database_service.get_joined_where(attribute, value)
  for f in fetch:
    print(f)
  response = Response(json.dumps({"data": fetch}), 200, None, 'application/json')
  return response

app.run(port=8080, debug=True)