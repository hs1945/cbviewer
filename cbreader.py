
import sys
import psycopg2
import datetime
import time

import requests
requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()

import insert_db
import cb_global
cb_global.init()
log = cb_global.log
con = cb_global.con
cur = cb_global.cur
log.info("%s", datetime.datetime.now())

import pycrunchbase
reload(pycrunchbase)


#from crunchbase_db import createDB
#createDB()

page_no = -1
index_no = -1
try:
    cur.execute("""select page_no, max(index_no) from pageindex group by page_no having  page_no = 
        (select max(page_no) from pageindex );""")
    res = cur.fetchone()
    page_no = res[0]
    index_no = res[1]
    if (index_no == None):
        index_no = 0

    cb = pycrunchbase.CrunchBase(cb_global.key)
    log.info("created crunchbase object..")

    while(True): 
        log.info("PAGE_NO %s",page_no)
        companies = cb.companies(page_no)
        if(companies == None):
            log.error('Last page reached %s', (index_no -1 )) 
            sys.exit(1)

        temp_index = 0
        for com in companies:
            log.info("INDEX_NO %s",index_no)
            if(temp_index > index_no):
                timenow = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                organization = cb.organization(com.permalink)     
                insert_db.insert_organization(cb, organization, page_no, index_no-1)
                log.info('company inserted - 2')
                time.sleep(15)                
                index_no = index_no + 1
            temp_index = temp_index + 1

        if (index_no == 999):
            index_no = 0
        page_no = page_no + 1

        cur.execute("""INSERT INTO pageindex(page_no, index_no) values(%s,%s)""",   \
            (page_no, index_no))

        log.info("Page no %s, last index %s", page_no, index_no)
        

        con.commit()
        
except psycopg2.DatabaseError, e:    
    if con:
        con.rollback()
    
    log.error('Error %s',e)    
    sys.exit(1)

    #-----------------------------------------------------------------------------------------------------------
    



    




