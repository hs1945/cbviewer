
import sys
import psycopg2
import cb_global
import datetime

def insert_organization(cb, organization, page_no, index_no ):

	con = cb_global.con
	cur = cb_global.cur
	log = cb_global.log
	log.info('insert_organization %s', organization.permalink)


	country = None
	region = None
	headquarters = organization.headquarters
	if(str(headquarters) != 'NoneRelationship'): 
		country = headquarters.items[0].data["country"]
		region = headquarters.items[0].data["region"]

	if (str(organization.ipo) == 'NoneRelationship'):
		ipo = False
	else:
		ipo = True
		insert_ipo(cb, organization)

	if (str(organization.funding_rounds) == 'NoneRelationship'):
		funding = False
	else:
		funding = True
		insert_funding(cb, organization)

	if (str(organization.investments) == 'NoneRelationship'):
		investments = False
	else:
		investments = True

	if (str(organization.closed_on) == 'None'):
		closed_on = None
	else:
		closed_on = str(organization.closed_on)

	if (str(organization.founded_on) == 'None'):
		founded_on = None
	else:
		founded_on = str(organization.founded_on)
	 
	categories = organization.categories
	competitors = organization.competitors

	log.info('inserting into company %s', organization.permalink)
	try:
		cur.execute("""INSERT INTO Company 
			(permalink,name,closed_on,found_on,homepage,region,country,ipo,funding,investments)            
	        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",       \
	        (organization.permalink,                      \
	        organization.name,                \
	        closed_on,                 \
	        founded_on,            \
	        organization.homepage_url,           \
	        region,         \
	        country,		\
	        ipo,                \
			funding,			\
			investments		\
			))

		
	except psycopg2.DatabaseError, e:
	    
	    if con:
	        con.rollback()
	    
	    log.error('Error %s',e)     
	    sys.exit(1)

	insert_category(organization)
	insert_founders(organization)
	insert_competitors(organization)
	log.info('company inserted')
		

	con.commit()
	#-----------------------------------------------------------------------------------------------------------

def insert_funding(cb, organization):

	con = cb_global.con
	cur = cb_global.cur
	log = cb_global.log
	log.info('insert_funding %s', organization.permalink)

	funding_rounds = organization.funding_rounds

	for funding_round in funding_rounds:
	        uuid = funding_round.uuid
	        funding = cb.funding_round(uuid)
	        company = organization.permalink
	        money = funding.money_raised_usd
	        date = funding.announced_on
	        code = funding.announced_on_trust_code
	        series = funding.series
	        ftype = funding.funding_type
	        pre_valuation = funding.pre_money_valuation_usd     
	        post_valuation = funding.post_money_valuation_usd

	        insert_investment(funding.investments, uuid, organization.permalink)

	    	log.info('insert into funding %s', uuid)
    
	        try:
	            cur.execute("""INSERT INTO Funding          
	                (uuid, company, type, money_raised, series, announced_on, trust_code, pre_valuation, post_valuation)            
	                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);""",       \
	                (uuid,                      \
	                company,                \
	                ftype,              \
	                money,                 \
	                series,            \
	                date,           \
	                code,         \
	                pre_valuation,        \
	                post_valuation                \
	                ))

	            
	        except psycopg2.DatabaseError, e:
	        
	                if con:
	                    con.rollback()
	        
	                log.error('Error %s',e)     
	                sys.exit(1)

	#-----------------------------------------------------------------------------------------------------------
def insert_investment(investments, uuid, company):
	con = cb_global.con
	cur = cb_global.cur
	log = cb_global.log
	log.info('insert_investment %s %s', company, uuid)

	for investment in investments:
	    money = investment.money_invested
	    investor_path = investment.investor.path
	    investor = str(investment.investor)
	    investor_permalink= investor_path[investor_path.index('/')+1:len(investor_path)]
	    investor_type = investment.investor.type

	    log.info('insert into investors %s', uuid)

	    try:
	        cur.execute("""INSERT INTO investors          
	            (uuid, company, investor, investor_permalink, investor_type, money_raised)            
	            VALUES (%s,%s,%s,%s,%s,%s);""",       \
	            (uuid,                      \
	            company,                \
	            investor,              \
	            investor_permalink,                 \
	            investor_type,            \
	            money           \
	            ))

	        

	    except psycopg2.DatabaseError, e:  
	        if con:
	            con.rollback()

	        log.error('Error %s',e)     
	        sys.exit(1)

	#-----------------------------------------------------------------------------------------------------------


def insert_ipo(cb, organization):
	con = cb_global.con
	cur = cb_global.cur
	log = cb_global.log
	log.info('insert_ipo %s', organization.permalink)

	ipo_uuid = organization.ipo[0].uuid
	ipo = cb.ipo(ipo_uuid)
	date = ipo.went_public_on
	shares_sold = ipo.shares_sold
	opening_price = ipo.opening_share_price_usd
	stock_symbol = ipo.stock_symbol
	money_raised = ipo.money_raised_usd
	opening_valuation = ipo.opening_valuation_usd
	stock_exchange = ipo.stock_exchange_symbol
	trust_code = ipo.went_public_on_trust_code
	shares_outstanding = ipo.shares_outstanding


	log.info('insert into ipo %s', ipo_uuid)
	try:
	    cur.execute("""INSERT INTO ipo 
	        (uuid,company,opening_price,shares_sold,shares_outstanding,money_raised,
	            stock_symbol,stock_exchange,date_ipo,opening_valuation,trust_code)
	        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",       \
	        (ipo_uuid,                      \
	        organization.permalink,                \
	        opening_price,                 \
	        shares_sold,            \
	        shares_outstanding,           \
	        money_raised,         \
	        stock_symbol,        \
	        stock_exchange,                \
	        date,            \
	        opening_valuation,     \
	        trust_code
	        ))

	    
	except psycopg2.DatabaseError, e:
	    
	    if con:
	        con.rollback()
	    
	    log.error('Error %s',e)     
	    sys.exit(1)

	#-----------------------------------------------------------------------------------------------------------

def insert_category(organization):
	con = cb_global.con
	cur = cb_global.cur
	log = cb_global.log
	log.info('insert_category %s', organization.permalink)

	categories = organization.categories

	for category in categories:
		log.info('insert into category %s', organization.permalink)

		try:
			cur.execute("""INSERT INTO category
	            (company, category)
	            VALUES (%s,%s);""",       \
	            (organization.permalink,                      \
	            category.name
	            ))

		except psycopg2.DatabaseError, e:
		    
		    if con:
		        con.rollback()
		    
		    log.error('Error %s',e)     
		    sys.exit(1)


	#-----------------------------------------------------------------------------------------------------------
def insert_founders(organization):
	con = cb_global.con
	cur = cb_global.cur
	log = cb_global.log
	log.info('insert_founders %s', organization.permalink)

	founders = organization.founders

	for founder in founders:
	    link = founder.path
	    name = link[link.index('/')+1:len(link)]
	    try:
	    	log.info('insert into founders %s', organization.permalink)

	        cur.execute("""INSERT INTO founders
	            (company, founder)
	            VALUES (%s,%s);""",       \
	            (organization.permalink,                      \
	            name
	            ))

	        
	    except psycopg2.DatabaseError, e:
	        
	        if con:
	            con.rollback()
	        
	        log.error('Error %s',e)         
	        sys.exit(1)


	#-----------------------------------------------------------------------------------------------------------

def insert_investments(organization):
	con = cb_global.con
	cur = cb_global.cur
	log = cb_global.log
	log.info('insert_investments %s', organization.permalink)

	investments = organization.investments

	for investment in investments:
	    funding_link = investment.funding_round.get('path')
	    funding_uuid = funding_link[funding_link.index('/')+1:len(funding_link)] 
	    invested_link = investment.invested_in.path
	    invested_in = invested_link[invested_link.index('/')+1:len(invested_link)] 
	    invested_type = invested_link[0:invested_link.index('/')]
	    money = investment.money_invested_usd

	    try:
	    	log.info('insert into investments %s', funding_uuid)

	        cur.execute("""INSERT INTO investments
	            (uuid, company, invested_company, invested_company_type, money_invested)
	            VALUES (%s,%s,%s,%s,%s);""",       \
	            (funding_uuid,                      \
	            organization.permalink,              \
	            invested_in,                    \
	            invested_type,                  \
	            money
	            ))

	        
	    except psycopg2.DatabaseError, e:
	        
	        if con:
	            con.rollback()
	        
	        log.error('Error %s',e)         
	        sys.exit(1)



	#-----------------------------------------------------------------------------------------------------------

def insert_competitors(organization):
	con = cb_global.con
	cur = cb_global.cur
	log = cb_global.log
	log.info('insert_competitors %s', organization.permalink)

	competitors = organization.competitors

	try:
	    cur.execute("""SELECT MAX(group_no) from competitors""")
	    max_id = cur.fetchone()[0] + 1

	    cur.execute("""SELECT group_no from competitors WHERE company = %s""", [organization.permalink])
	    res = cur.fetchone()


	    if(res==None):
	    	log.info('insert into competitors %s', organization.permalink)
	    	cur.execute("""INSERT INTO competitors values(%s,%s)""", (organization.permalink, max_id))

	    for competitor in competitors:
			path = competitor.path
			company = path[path.index('/')+1:len(path)]

			cur.execute("""SELECT group_no from competitors WHERE company = %s""", [company])
			res = cur.fetchone()
			
			log.info('insert into competitors %s', organization.permalink)

			if(res==None):
				cur.execute("""INSERT INTO competitors values(%s,%s)""", (company, max_id))
		


	except psycopg2.DatabaseError, e:
	        
	        if con:
	            con.rollback()
	        
	        log.error('Error %s',e)         
	        sys.exit(1)

	


