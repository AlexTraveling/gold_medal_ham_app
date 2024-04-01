import mysql.connector


database_name = 'gold_medal_ham'


def get_table(table_name):

   global database_name
   connection = mysql.connector.connect(
      host="localhost",
      user="root",
      database=database_name
   )

   if connection.is_connected():
      # get
      print("Connected to MySQL database")
      cursor = connection.cursor()
      # Table
      cursor.execute(f"SELECT * FROM {table_name}")
      content = cursor.fetchall()
      print(content)
      # close
      cursor.close()
      connection.close()
      print("Connection closed")
      return content
   
   else:
      print("Failed to connect to MySQL database")
      return None


def get_if_user_exist(username):

   for user in get_table('user'):
      if user[0] == username:
         return True, user[1]

   return False, None


def get_user_identity(username):

   for user in get_table('user'):
      if user[0] == username:
         return user[2]

   return False, None


def get_if_ham_exist(ham_id, ham_state):

   for ham in get_table('ham'):
      if ham[0] == ham_id and ham[4] == ham_state:
         return True

   return False


def add_ham(ham_id, ham_username, ham_time, ham_place, ham_state):

   if get_if_ham_exist(ham_id, ham_state):
      return 'already existed'
      
   global database_name
   connection = mysql.connector.connect(
      host="localhost",
      user="root",
      database=database_name
   )

   if connection.is_connected():
      print("Connected to MySQL database")
      cursor = connection.cursor()

      # 准备 SQL 插入语句
      # ham_id | ham_username | ham_time            | ham_place    | ham_state |
      table_name = 'ham'
      column1 = 'ham_id'
      column2 = 'ham_username'
      column3 = 'ham_time'
      column4 = 'ham_place'
      column5 = 'ham_state'
      sql_insert = f"INSERT INTO {table_name} ({column1}, {column2}, {column3}, {column4}, {column5}) VALUES (%s, %s, %s, %s, %s)"

      # 插入数据
      add_data = (ham_id, ham_username, ham_time, ham_place, ham_state)
      cursor.execute(sql_insert, add_data)
      connection.commit()

      cursor.close()
      connection.close()
      print("Connection closed")

      return 'success'
   
   else:
      return "Failed to connect to MySQL database"


def add_evaluate(id, quality):

   # if get_if_ham_exist(ham_id, ham_state):
   #    return 'already existed'
      
   global database_name
   connection = mysql.connector.connect(
      host="localhost",
      user="root",
      database=database_name
   )

   if connection.is_connected():
      cursor = connection.cursor()

      # 准备 SQL 插入语句
      table_name = 'evaluate'
      column1 = 'id'
      column2 = 'quality'
      sql_insert = f"INSERT INTO {table_name} ({column1}, {column2}) VALUES (%s, %s)"

      # 插入数据
      add_data = (id, quality)
      cursor.execute(sql_insert, add_data)
      connection.commit()

      cursor.close()
      connection.close()

      return 'success'
   
   else:
      return "Failed to connect to MySQL database"
      

def select_from_table(table_name, where_order):

   global database_name
   connection = mysql.connector.connect(
      host="localhost",
      user="root",
      database=database_name
   )

   if connection.is_connected():
      # get
      print("Connected to MySQL database")
      cursor = connection.cursor()
      # Table
      cursor.execute(f"SELECT * FROM {table_name} WHERE {where_order}")
      content = cursor.fetchall()
      print(content)
      # close
      cursor.close()
      connection.close()
      print("Connection closed")
      return content
   
   else:
      print("Failed to connect to MySQL database")
      return None


def get_quality_from_id(id_list):
   
   quality_list = []

   for id in id_list:
      quality = select_from_table('evaluate', f"id = '{id}'")[0][1]
      quality_list.append(quality)

   return quality_list

      
if __name__ == "__main__":

   # get_table('ham')
   # print(if_exist('Harden'))
   # print(add_user('James', 'iamjames'))
   # get_user()

   # add_ham(1002, 'Alex', '2024-03-31-14:59:55', 'Xuanwei City', 'made')

   select_from_table('ham', "ham_username = 'Bob'")