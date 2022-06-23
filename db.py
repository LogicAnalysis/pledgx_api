import pymysql


class Database:
	def __init__(self, config):
		self.__connection = None
		self.__connection_timeout = config.CONNECTION_TIMEOUT
		self.__dbname = config.DB_NAME
		self.__host = config.DB_HOST
		self.__password = config.DB_PASSWORD
		self.__port = int(config.DB_PORT)
		self.__username = config.DB_USER

		self.__db_creation_attempted = False
		
		self.__open_connection()

	def __del__(self):
		self.__close_connection()

	def __create_database_table(self):
		'''
		Creates database table if it does not exist
		'''
		with self.__connection.cursor() as cursor:
			cursor.execute('''
				CREATE TABLE IF NOT EXISTS users(
					id INT(10) primary key NOT NULL AUTO_INCREMENT,
					first_name VARCHAR(255),
					last_name VARCHAR(255),
					phone_number VARCHAR(50),
					job_title VARCHAR(255),
					country CHAR(2),
					profile_photo TEXT
				)
			''')
			cursor.close()

	def __create_database(self):
		'''
		Creates new database
		'''
		self.__db_creation_attempted = True
		connection = pymysql.connect(
			connect_timeout = self.__connection_timeout,
			host = self.__host,
			password = self.__password,
			port = self.__port,
			user = self.__username
		)
		with connection.cursor() as cursor:
			cursor.execute(f'CREATE DATABASE {self.__dbname}')
			cursor.close()

	def __close_connection(self):
		'''
		Closes the DB connection if self.__connection = True
		'''
		try:
			if self.__connection is not None:
				self.__connection.close()
				self.__connection = None
		except Exception as e:
			raise Exception(f'DB_EXCEPTION. Failed to close DB connection. Error: {e}')

	def __open_connection(self):
		'''
		Connects to MySQL DB
		'''
		try:
			if self.__connection is None:
				self.__connection = pymysql.connect(
					connect_timeout = self.__connection_timeout,
					db = self.__dbname,
					host = self.__host,
					password = self.__password,
					port = self.__port,
					user = self.__username
				)
		except pymysql.MySQLError as sqle:
			if sqle.args[0] == 1049 and not self.__db_creation_attempted:
				self.__create_database()
				self.__open_connection()
				self.__create_database_table()
			else:
				raise pymysql.MySQLError(f'DB_CONNECTION_FAILED. Error: : {sqle}')
		except Exception as e:
			raise Exception(f'DB_EXCEPTION. Error: {e}')

	def __run_query(self, query):
		'''
		Executes SQL query
		'''
		try:
			if not query or not isinstance(query, str):
				raise Exception()

			if not self.__connection:
				self.__open_connection()
				
			with self.__connection.cursor() as cursor:
				cursor.execute(query)
				if 'SELECT' in query.upper():
					entries = cursor.fetchall()
					table_columns = [col[0] for col in cursor.description]
					if entries and (len(entries) == 1) and (len(table_columns) == len(entries[0])):
						table_columns = [col[0] for col in cursor.description]
						entry = entries[0]
						result_dict = {}
						for index, value in enumerate(table_columns):
							result_dict[value] = entry[index]
						result = result_dict
					else:
						result = entries
				else:
					self.__connection.commit()
					result = cursor.lastrowid
				cursor.close()

				return result
		except pymysql.MySQLError as sql_error:
			raise pymysql.MySQLError(f'SQL_ERROR: {sql_error}')
		except Exception as e:
			raise Exception(f'SQL_QUERY_EXCEPTION: {e}')

	@property
	def db_connection_status(self):
		'''
		Returns the DB connection status
		'''
		return True if self.__connection is not None else False

	def add_entry(self, entry_dict):
		'''
		Inserts a new entry into the SQL table
		'''
		dict_keys_string = ', '.join(list(entry_dict.keys()))
		dict_values_string = ', '.join(f"'{key}'" for key in list(entry_dict.values()))
		sql_query = f'INSERT INTO users (id, {dict_keys_string}) VALUES (NULL, {dict_values_string})'
		return self.__run_query(sql_query)

	def get_entry(self, entry_id):
		'''
		Retrieves an entry by ID
		'''
		sql_query = f'SELECT * from users WHERE id={entry_id} LIMIT 1'
		return self.__run_query(sql_query)
	
	def update_entry(self, entry_dict, entry_id):
		'''
		Updates an existing entry in the table
		'''
		#new_params_string = ', '.join([key + ' = ' + f"'{entry_dict[key]}'" for key in list(entry_dict.keys())]) # Does not handle None values properly
		new_params_list = []
		for key in list(entry_dict.keys()):
			if entry_dict[key] is not None:
				new_params_list.append(key + ' = ' + f"'{entry_dict[key]}'")
			else:
				new_params_list.append(f'{key} = NULL')
		self.__run_query(f'UPDATE users SET {", ".join(new_params_list)} WHERE id = {entry_id}')
		return entry_id