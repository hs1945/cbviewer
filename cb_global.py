import logging
import psycopg2
import sys

def init():
	global con 
	global cur
	global log
	global key

	key = '844895ab00a3e40cf2c92dd3c2b8409d'
	apikey = 'xs8mctd74m'

	logging.basicConfig(filename='output.log',level=logging.DEBUG)
	log = logging.getLogger("cruncbase")

	log.info("initializing globals..")
	try:
		log.info("creating connections..")
		con = psycopg2.connect(database="crunchbase", user="Mactard", password="", host="127.0.0.1", port="5432")
		cur = con.cursor()

	except psycopg2.DatabaseError, e:        
	    if con:
	        con.rollback()
	        
	    log.Error('Error %s',e)    
	    sys.exit(1)

