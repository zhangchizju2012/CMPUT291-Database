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
        return "exit"
    elif people == "c":
        register = raw_input("Did you register before? y for yes, n for no: ")
        if register == "n":
            if customerRegister():
                return people
        else:   
            userId = raw_input("Enter your ID: ")
            pwd = getpass.getpass("Enter your password: ")
            result = customerLogin(userId, pwd)
    else:
        userId = raw_input("Enter your ID: ")
        pwd = getpass.getpass("Enter your password: ")
        result = agentLogin(userId, pwd)
        
    if len(result) == 1:
        return people
    else:
        return "fail"
    
def search(item):
    global connection, cursor
    result = cursor.execute("select * from products where name like '%"+item+"%';")
    searchList = result.fetchall()
    connection.commit()
    return searchList

    
def searchTask():
    print("You can enter as many keywords as possible, enter 'exit' to stop")
    keywordList = []
    keyword = raw_input("Enter the keyword, enter 'exit' to stop: ")
    while keyword != "exit":
        keywordList.append(keyword)
        keyword = raw_input("Enter the keyword, enter 'exit' to stop: ")
    dic = {}
    for item in keywordList:
        searchList = search(item)
        for i in searchList:
            if i[0] in dic:
                dic[i[0]] += 1
            else:
                dic[i[0]] = 1
    print dic

    
def doCustomerTask():
    print("What do you want to do?")
    print("Search for products? Place an order? List orders?")
    task = raw_input("s for search, p for place, l for list: ")
    if task == "s":
        searchTask()
        
def main():
    global connection, cursor
    path="./mini.db"
    connect(path)
    peopleType = login()
    if peopleType == "c":
        print("customer log in successfully.")
        doCustomerTask()
    elif peopleType == "a":
        print("agent log in successfully.")
    else:
        print("Fail.")
    
    
main()
