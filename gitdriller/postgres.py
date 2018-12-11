import psycopg2

class Postgres(object):
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = object.__new__(cls)

		return cls._instance

	def connect(self, dbname, host='localhost',
				user='postgres', password='postgres',
				port=5432):
		db_config = {'dbname': dbname, 'host': host,
					'password': password, 'port': port, 'user': user}
		try:
			self.connection = psycopg2.connect(**db_config)
			self.connection.autocommit = True
			self.cursor = self.connection.cursor()
		except (Exception, psycopg2.DatabaseError) as error:
			raise Exception('Connection not established {}'.format(error))

		return True

	def close(self):
		if self.connection:
			self.cursor.close()
			self.connection.close()

	def createdb(self, dbname):
		try:
			self.cursor.execute('CREATE DATABASE {};'.format(dbname))
			self.connection.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			raise Exception('Error while creating database: {}.'.format(error))

		return True

	def dropdb(self, dbname):
		if self.existsdb(dbname):
			try:
				self.cursor.execute('DROP DATABASE {};'.format(dbname))
				self.connection.commit()
			except (Exception, psycopg2.DatabaseError) as error:
				raise Exception('Error while dropping database: {}.'.format(error))

			return True
		return False

	def existsdb(self, dbname):
		try:
			self.cursor.execute('SELECT datname FROM pg_catalog.pg_database WHERE datname=\'{}\';'.format(dbname))
			self.connection.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			raise Exception('Error while checking if database exists: {}.'.format(error))

		return self.cursor.fetchone() != None

	def create_release_table(self):
		try:
			self.cursor.execute('CREATE TABLE release (id integer PRIMARY KEY,'
								+ ' name varchar);')
			self.connection.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			raise Exception('Error while creating release table: {}.'.format(error))

	def insert_into_release_table(self, id, name):
		raise Exception('not implemented yet')

	def create_source_file_table(self):
		try:
			self.cursor.execute('CREATE TABLE source_file (id integer PRIMARY KEY,'
								+ 'tagid integer,'
								+ 'path varchar,'
								+ ' added_lines integer);')
			self.connection.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			raise Exception('Error while creating source_file table: {}.'.format(error))

	def table_exists(self, table):
		self.cursor.execute('SELECT EXISTS(SELECT * FROM'
							+ ' information_schema.tables WHERE table_name=%s)', (table,))
		return self.cursor.fetchone()[0]
