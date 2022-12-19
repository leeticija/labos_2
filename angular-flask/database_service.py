import sqlite3

class DatabaseService():

  def __init__(self, FILE):
    try:
      self.fields = ['order_id','order_name', 'order_common_name', 'wings', 'total_order_species', 'total_order_families', 'metamorphosis', 'insect_id', 'genus', 'specie', 'binomial_name', 'order_id'] 
      self.connection = sqlite3.connect(FILE, check_same_thread=False)
      #self.cursor = self.connection.cursor()
      print("Established connection to database!")
    except sqlite3.Error as error:
      print("Database error occured.")

  def get_all_insects(self):
    query = """SELECT * FROM insects;"""
    cur = self.connection.cursor()
    cur.execute(query)
    r = [dict((cur.description[i][0], value) \
    for i, value in enumerate(row)) for row in cur.fetchall()]
    return r
  
  def get_all_joined_insects_and_orders(self):
    query = """SELECT * FROM insects
               JOIN orders
               WHERE insects.order_id = orders.order_id;"""
    cursor = self.connection.cursor()
    cursor.execute(query)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r

  def get_joined_where(self, attribute, value):
    query = """SELECT * FROM insects
                JOIN orders ON orders.order_id = insects.order_id
                WHERE """
    if attribute == "wildcard":
      print("in wildcard")
      query = query + """genus LIKE '%s' OR specie LIKE '%s' OR binomial_name LIKE '%s' OR order_name LIKE '%s' OR order_common_name LIKE '%s'
              OR wings LIKE '%s' OR total_order_species LIKE '%s' OR total_order_families LIKE '%s' OR metamorphosis LIKE '%s';"""
      query = query%('%'+value+'%','%'+value+'%','%'+value+'%','%'+value+'%','%'+value+'%','%'+value+'%','%'+value+'%','%'+value+'%','%'+value+'%')
    else:
      print("not wildcard")
      query = query + "%s LIKE '%s';"
      query = query%(attribute, '%'+value+'%')

    print("STATEMENT:", query)
    cursor = self.connection.cursor()
    cursor.execute(query)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r

  def get_csv_rows_from_jsons_list(self, jsonsList):
    columnsInsect = self.getAllColumnsFromTable("insects") # dobivanje svih columna iz tablice insects
    columnsOrders = self.getAllColumnsFromTable("orders") # dobivanje svih columna iz tablice insects
    columns = []
    columns.extend(columnsInsect)
    columns.extend(columnsOrders)
    print("curr columns: ", columns)
    csvRows = ["; ".join(columns)] # prvi redak je csv header s imenima columna
    for jsn in jsonsList:
      row = []
      for column in columns:
        row.append(str(jsn[column]))
      s = "; ".join(row)
      csvRows.append(s)
    return csvRows
  
  def getAllColumnsFromTable(self, tableName):
    query = "SELECT * FROM %s;"%tableName
    cursor = self.connection.cursor()
    cursor.execute(query)
    return list(map(lambda x: x[0], cursor.description))
  
  # post new insect
  # throws exception if required data is not given
  def insert_new_insect(self, form):
    cursor = self.connection.cursor()
    order_name = form['order_name']
    form.pop('order_name')
    q = "SELECT * FROM orders WHERE order_name LIKE '%s'" %order_name
    cursor.execute(q)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    order_id = r[0]['order_id']

    columns = ','.join(list(form.keys()))
    values = ','.join(list(f"'{form[x]}'" for x in list(form.keys())))
    print("columns: ", columns)
    print("values: ", values)
    query = "INSERT INTO insects (order_id,%s) VALUES (%s,%s);"%(columns, order_id, values)
    cursor.execute(query)
    self.connection.commit()

    # za vracanje objekta novog insekta:
    select = f"SELECT * FROM insects WHERE insect_id = {cursor.lastrowid};"
    cursor.execute(select)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r[0]
  
  def delete_existing_insect(self, id):
    cursor = self.connection.cursor()
    select = f"SELECT * FROM insects where insect_id={id}"
    cursor.execute(select)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]

    if len(r) == 0:
      return {"error_message" : "No insect with given id!"}

    q = f"DELETE FROM insects WHERE insect_id = {id}"
    cursor.execute(q)
    self.connection.commit()
    return {"message" : "Insect deleted successfully!"}
  
  def update_existing_insect(self, id, form):
    cursor = self.connection.cursor()
    select = f"SELECT * FROM insects WHERE insect_id = {id};"
    cursor.execute(select)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    if len(r) == 0:
      return {"error_message" : "No insect with given id!"}
    
    equals = ','.join(list(f"{x}='{form[x]}'" for x in list(form.keys())))
    q = f"UPDATE insects SET {equals} WHERE insect_id={id};"
    cursor.execute(q)
    self.connection.commit()

    select = f"SELECT * FROM insects WHERE insect_id = {id};"
    cursor.execute(select)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    return {"insect" : r[0], "message" : "Updated insect data."}
  
  def get_insect_by_id(self, id):
    cursor = self.connection.cursor()

    if not self.exists("insects", id):
      return {"error_message" : "No insect with requested id."}
    
    q = f"SELECT * FROM insects WHERE insect_id = {id}"
    cursor.execute(q)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r[0]
  
  def get_order_by_id(self, id):
    cursor = self.connection.cursor()

  def get_orders_by_species_count(self, params):
    cursor = self.connection.cursor()
    if 'low' in list(params.keys()) and 'high' in list(params.keys()):
      q = f"SELECT * FROM orders WHERE total_order_species BETWEEN {params['low']} AND {params['high']};"
    elif 'low' in list(params.keys()):
      q = f"SELECT * FROM orders WHERE total_order_species > {params['low']}"
    elif 'high' in list(params.keys()):
      q = f"SELECT * FROM orders WHERE total_order_species < {params['high']}"
    else:
      r = {"error_message" : "No parameters. Required parameters are: low and/or high."}
    try:
      cursor.execute(q)
      r = [dict((cursor.description[i][0], value) \
      for i, value in enumerate(row)) for row in cursor.fetchall()]
      return r
    except:
      return {"error_message" : "No specified low or high."}
  
  def get_metamorphosis_by_order_id(self, id):
    cursor = self.connection.cursor()
    if not self.exists("orders", id):
      return {"error_message" : "No order with given id."}
    
    q = f"SELECT metamorphosis FROM orders WHERE order_id = {id};"
    cursor.execute(q)
    r = [dict((cursor.description[i][0], value) \
      for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r[0]
  
  def get_order_by_id(self, id):
    cursor = self.connection.cursor()
    if not self.exists("orders", id):
      return {"error_message" : "No order with given id."}
    q = f"SELECT * FROM orders WHERE order_id = {id};"
    cursor.execute(q)
    r = [dict((cursor.description[i][0], value) \
      for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r[0]

  def exists(self, table, id):
    cursor = self.connection.cursor()
    select = f"SELECT * FROM orders WHERE order_id = {id};"
    cursor.execute(select)
    r = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    if len(r) == 0:
      return False
    return True