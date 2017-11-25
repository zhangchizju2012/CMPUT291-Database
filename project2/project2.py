#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:04:59 2017

@author: zhangchi
"""

from bsddb import db

database_te = db.DB()
database_te.set_flags(db.DB_DUP)
database_te.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)

database_ye = db.DB()
database_ye.set_flags(db.DB_DUP)
database_ye.open('ye.idx', None, db.DB_BTREE, db.DB_CREATE)

database_re = db.DB()
database_re.set_flags(db.DB_DUP)
database_re.open('re.idx', None, db.DB_HASH, db.DB_CREATE)

def search_title():
    curs = database_te.cursor()
    iter = curs.first()
    while (iter):
        title = raw_input("Enter the title name: ")
        if(title == "q"): #Termination Condition
            break
        
        result = curs.set(("t-"+title).encode("utf-8")) 
        #In the presence of duplicate key values, result will be set on the first data item for the given key. 
       
        if(result != None):
            print("List of records have the term " + title+ ":\n")
            print("Term: " + str(result[0].decode("utf-8")[2:]) + ". Key: " + str(result[1].decode("utf-8")))
            print("Record: " + database_re.get(result[1]))
            print
            
            #iterating through duplicates:
            dup = curs.next_dup()
            while(dup != None):
                print("Term: " + str(dup[0].decode("utf-8")[2:]) + ". Key: " + str(dup[1].decode("utf-8")))
                print("Record: " + database_re.get(result[1]))
                print
                dup = curs.next_dup()
        else:
            print("No Entry Found.")
                
    
    curs.close()
    

search_title()

database_te.close()
database_ye.close()
database_re.close()
