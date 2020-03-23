from app import app
import unittest
import os
from pymongo import MongoClient
import pymongo
import json


class TestCases(unittest.TestCase):
     
    def setUp(self):
        self.app = app.test_client()
        app.testing = True
   
    def test_Database_Configuration(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["cloud"]
        mycollection = mydb["search"]    
        query1=mycollection.find_one({'author':"Various"})
        query2=mycollection.find_one({'author':"Saurabh Dey"})
        self.assertTrue(query1)
        self.assertFalse(query2)
       
    def test_Collection_Data(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["cloud_assignment"]
        mycollection = mydb["books"]    
        query1=mycollection.find_one({'author':"Various"})
        query2=mycollection.find_one({'author':"Saurabh Dey"})
        self.assertFalse(query1)
        self.assertFalse(query2)

    def test_Collection_If_Record_Empty(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["cloud"]
        mycollection = mydb["search"]    
        query1=mycollection.find_one({'author':""})
        self.assertFalse(query1)

    def test_Search_pages(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertTrue(response.status_code, 200)

    def test_Search_Author_Exist(self):
        with open('Catalogue.json') as f:
            data = json.load(f)
            for i in data:
                if i['author']== "Various":
                    self.assertTrue(i['author']== "Various")
                    self.assertFalse(i['author']=="Saurabh Dey")

    def test_Search_If_Author_Empty(self):
         with open('Catalogue.json') as f:
            data = json.load(f)
            for i in data:
                if i['author']=="":
                   self.assertFalse(i['author']== "")

    def test_Search_BookTittle(self):
        with open('Catalogue.json') as f:
            data = json.load(f)
            for i in data:
                if i['title']== "The Archives of Dentistry":
                    self.assertTrue(i['title']== "The Archives of Dentistry")
                    self.assertFalse(i['author']=="")

    def test_Note_Submitted(self):
        multikeys=[]
        with open('Catalogue.json') as f:
            data = json.load(f)
            for i in data:
                if i['author']== "Various":
                    inputed= {'author': "Various" , 'Note': "New note for the author"}
                    multikeys.append(inputed)
                    with open('NoteTest.json', 'w', encoding='utf-8') as f:
                        json.dump(multikeys, f, ensure_ascii=False, indent=4)
       
        with open('NoteTest.json') as f:
            data = json.load(f)          
            for i in data:
                if i['Note']== "New note for the author":
                    self.assertTrue(i['Note']=="New note for the author")

    def test_Note_for_Empty_Author(self):
        multikeys=[]
        with open('Catalogue.json') as f:
            data = json.load(f)
            for i in data:
                if i['author']== "":
                    entry= {'author': "" , 'Note': "New note for the author"}
                    multikeys.append(entry)
                    with open('NoteTest.json', 'w', encoding='utf-8') as f:
                        json.dump(multikeys, f, ensure_ascii=False, indent=4)
       
        with open('NoteTest.json') as f:
            data = json.load(f)          
            for i in data:
                if i['Note']== "New note for the author":
                    self.assertFalse(i['Note']=="")

if __name__ == '__main__':
    unittest.main() 