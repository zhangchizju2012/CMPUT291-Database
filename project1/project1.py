#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 13:04:36 2017

@author: zhangchi
"""

# mini project 1

import sqlite3
import getpass
#import hashlib

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def checkRegister(userId):
    global connection, cursor
    result = cursor.execute("select * from customers where cid='%s'"%userId)
    userlList = result.fetchall()
    connection.commit()
    return len(userlList) == 0

def customerRegister():
    global connection, cursor
    userId = raw_input("Enter the ID you like: ")
    while checkRegister(userId) is False:
        print("Sorry you can not use this ID.")
        userId = raw_input("Please re-enter the ID you like: ")
    name = raw_input("Enter your name: ")
    address = raw_input("Enter your address: ")
    pwd = getpass.getpass("Enter your password: ")
    cursor.execute("insert into customers values ('%s','%s','%s','%s');"%(userId,name,address,pwd))
    connection.commit()
    return True

def customerLogin(userId, pwd):
    global connection, cursor
    
    result = cursor.execute("select * from customers where cid='%s' and pwd='%s';"%(userId,pwd))
    userlList = result.fetchall()
    
    connection.commit()
    return userlList

def agentLogin(userId, pwd):
    global connection, cursor
    
    result = cursor.execute("select * from agents where aid='%s' and pwd='%s';"%(userId,pwd))
    userlList = result.fetchall()
    
    connection.commit()
    return userlList

def login():
    global connection, cursor
    
    print("You are a customer or an agent?")
    people = raw_input("c for customer, a for agent, e to exit: ")
    while people not in "cae":
        print("Wrong input!")
        print("You are a customer or an agent?")
        people = raw_input("c for customer, a for agent, e to exit: ")
        
    if people == "e":
        print("Log out. Bye bye ~")
        return False
    elif people == "c":
        register = raw_input("Did you register before? y for yes, n for no: ")
        if register == "n":
            return customerRegister()
        else:   
            userId = raw_input("Enter your ID: ")
            pwd = getpass.getpass("Enter your password: ")
            result = customerLogin(userId, pwd)
    else:
        userId = raw_input("Enter your ID: ")
        pwd = getpass.getpass("Enter your password: ")
        result = agentLogin(userId, pwd)
    return len(result) == 1

def main():
    global connection, cursor
    path="./mini.db"
    connect(path)
    if login():
        print("Log in successfully.")
    else:
        print("Fail.")
    
    
main()
