import psycopg2
import cb_global


def createDB():
	log = cb_global.log
	log.info ("creating db...")

	con = None 
	cur = None 

	try:
	    con = psycopg.connect(database="crunchbase", user="Mactard", password="", host="127.0.0.1", port="5432")
	    cur = con.cursor()

	    cur.execute("CREATE TABLE IF NOT EXISTS Company         \
               (id serial,    \
                permalink varchar(40) primary key, \
                name varchar(30),                \
                closed_on date,           \
                found_on date,            \
                homepage varchar(50),           \
                region varchar(30),             \
                country varchar(30),            \
                ipo bool,                		\
                funding bool,                   \
                investments bool,               \
                acquisitions bool				\
                )")

	    con.commit()

	    cur.execute("CREATE TABLE IF NOT EXISTS funding				\
	    	( id serial primary key, 			\
	    	  uuid varchar(35), 		\
	    	  company varchar(30),		\
	    	  type varchar(20),			\
	    	  money_raised bigint,		\
	    	  series varchar(10),			\
	    	  announced_on	date,		\
	    	  trust_code integer,			\
	    	  pre_valuation bigint,			\
	    	  post_valuation bigint		\
	    	)")

	    con.commit()

	    cur.execute("CREATE TABLE IF NOT EXISTS investors				\
	    	( id serial primary key, 			\
	    	  uuid varchar(35), 		\
	    	  company varchar(30),		\
	    	  investor varchar(30),			\
	    	  investor_permalink varchar(30),		\
	    	  investor_type varchar(20),			\
	    	  money_raised bigint		\
	    	)")

	    con.commit()

	    cur.execute("CREATE TABLE IF NOT EXISTS ipo 			\
	    	( id serial primary key, 			\
	  		  uuid varchar(40),					\
	  		  company varchar(30),				\
	  		  opening_price integer,			\
	  		  shares_sold bigint,				\
	  		  shares_outstanding bigint,		\
	  		  money_raised bigint, 			\
	  		  stock_symbol varchar(5),			\
	  		  stock_exchange varchar(10),		\
	  		  date_ipo	date,					\
	  		  opening_valuation bigint,		\
	  		  trust_code integer				\
	    	)")

	    con.commit()


	    cur.execute("CREATE TABLE IF NOT EXISTS competitors 			\
	    	(company varchar(30),				\
	  		  group_no integer					\
	  		  )")

	    con.commit()

	    cur.execute("CREATE TABLE IF NOT EXISTS category 			\
	    	( id serial primary key, 			\
	  		  category varchar(30),					\
	  		  company varchar(30)				\
	  		  )")

	    #insert dummy-value if newly created
	    con.commit()


	    cur.execute("CREATE TABLE IF NOT EXISTS founders 			\
	    	( id serial primary key, 			\
	  		  founder varchar(30),					\
	  		  company varchar(30)				\
	  		 )")

	    con.commit()


	    cur.execute("CREATE TABLE IF NOT EXISTS investments 			\
	    	( id serial primary key, 			\
	  		  uuid varchar(35),					\
	  		  company varchar(30),				\
	  		  invested_company varchar(30),			\
	  		  invested_company_type varchar(20),		\
	  		  money_invested bigint			\
	  		  )")

	    con.commit()

	except psycopg2.DatabaseError, e:    
	    if con:
	        con.rollback()
	    
	    log.error('Error %s',e)    
	    sys.exit(1)


createDB()
