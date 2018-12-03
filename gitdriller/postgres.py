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
