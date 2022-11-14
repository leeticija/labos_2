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

  def getCsvRowsFromJsonsList(self, jsonsList):
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