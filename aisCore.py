# -------------------------------------------------------
# Core classes/components for AIS
# Stein Ove Erikstad
# March 2021
# -------------------------------------------------------

import pandas as pd
import datetime

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