
import json
import os

class JsonHandeler:
    def __init__(self,path:str):
        self.path = os.path.abspath(path)

    def fetch_data(self) -> dict:
        """ returns data inside the json file"""
        with open(self.path,"r") as file:
            return json.load(file)

    def save(self,data):
        r"""This method is used to save the data into the database"""
        with open(self.path,"w") as file:
            json.dump(data,file)

    def destroy(self):
        """destroy the database"""
        os.remove(self.path)
        del self.path

    def clear(self):
        "cleans the database"
        self.save({})


    def get_info(self)-> dict:
        """To convet time in float(sec from epoch) to str use time.ctime()
        retuns dict of [modified,last_access,size]"""
        return {"modified": os.path.getmtime(self.path),"last_access": os.path.getatime(self.path),"size": os.path.getsize(self.path)}