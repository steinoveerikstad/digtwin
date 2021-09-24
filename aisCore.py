# -------------------------------------------------------
# Core classes/components for AIS
# Stein Ove Erikstad
# March 2021
# -------------------------------------------------------

import pandas as pd
import datetime
from datetime import timezone
import sqlite3

class Vessel:
    def __init__(self, mmsi, imo, callsign, name):
        self.mmsi = mmsi
        self.imo = imo
        self.callsign = callsign
        self.name = name
        
        self.route = {}
        
    def addObs(self,t,lat,lon):
        dt = datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
        self.route[t] = (dt,lat,lon)

    # Adds vessel positions from datatable. Must contain columns unixtime, latitude, longitude
    def posFromTable(self, dtPos):
        for row in dfPos.iterrows():
        self.addObs(row[1]['unixtime'],row[1]['latitude'],row[1]['longitude'])
        
    def getRoute(self):
        lst = [self.route[key] for key in self.route]
        df = pd.DataFrame(lst,columns=['dt','lat','lon'])
        return df
    
    def getFirstPosOnRoute(self):
        return list(self.route.values())[0]
    
    def __repr__(self):
        return 'Vessel: MMSI %s, Name: %s, IMO: %s, Callsign: %s' % (str(self.mmsi), str(self.name), str(self.imo), str(self.callsign))


class Fleet:
    def __init__(self, name):
        self.name = name
        self.vessels = {}
    
    def getFirstPos(self):
        lst = [v.getFirstPosOnRoute() for v in list(self.vessels.values())]
        dfRet = pd.DataFrame(lst, columns=['dt','lat','lon'])
        dfRet['name'] = [v.name for v in list(self.vessels.values())]
        return dfRet

# DB functions

def extractAISData(mmsi, fromDate, toDate):
    
    # Connect to the database, and get cursor
    database = 'c:/aisdata.db'
    con = sqlite3.connect(database)
    cur = con.cursor()
    
    # Convert the datetime objects to utc timestamps
    utc_from = int(fromDate.replace(tzinfo=timezone.utc).timestamp())
    utc_to = int(toDate.replace(tzinfo=timezone.utc).timestamp())

    # Create SQL statements
    sqlPos = "SELECT * FROM messagetype1 WHERE mmsi = {} AND unixtime BETWEEN {} AND {}".format(mmsi, utc_from, utc_to)
    
    # Read relevant data from database
    dfPos = pd.read_sql_query(sqlPos, con)
    #dfShips = pd.read_sql_query("SELECT * FROM messagetype5 WHERE unixtime BETWEEN 1517270400 AND 1517356800", con)

    return dfPos