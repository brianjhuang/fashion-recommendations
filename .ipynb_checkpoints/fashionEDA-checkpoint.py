import pandas as pd
import numpy as np
import gzip 
import math
import string
import regex as re
from dateutil.parser import parse

class fashionCleaner:
    '''
    Clean our fashion dataset in one line with this fancy 
    class!
    '''
    runway = []
    modcloth = []
    data = []
    
    def __init__(self):
        runway_data = 'renttherunway_final_data.json.gz'
        modcloth_data = 'modcloth_final_data.json.gz'
        
        self.runway = list(self.parseData(runway_data))
        self.modcloth = list(self.parseData(modcloth_data))
        self.data = self.cleaner(self.runway)
        self.data = self.getData()
        self.data['bust_cat'] = self.data['bust'].apply(self.bust_category)
        self.data['cup_cat'] = self.data['cup'].apply(self.cup_category)
    
    def parseData(self, fname):
        '''
        Parse in the data from the file path/link
        '''
        total = 0
        for l in gzip.open(fname):
            try:
                yield eval(l)
            except NameError:
                total += 1
                print(f"Scrapping Data, Null Entry: {total}")
    
    def bustSplitter(self, s):
        '''
        Split our bust measurement into measurement and cup size.
        '''
        bust = s[:2]
        cup = s[2:]
        return int(bust), cup
    
    def cleaner(self, runway):
        
        unusable_data = 0
        columns = set(list(runway[0].keys()))
        for review in runway:
            if len(set(list(review.keys())).intersection(columns)) < len(columns):
                unusable_data += 1
        
        #split bust into measurement and cup size
        data = []
        for review in runway:
            if len(set(list(review.keys())).intersection(columns)) < len(columns): 
                #if they're missing a column
                continue
            review['bust'], review['cup'] = self.bustSplitter(review['bust size']) 
            data.append(review)
        
        for d in data:
            d['weight'] = int(re.sub("[^0-9]", "", d['weight']))
            d['rating'] = int(d['rating'])
            d['size'] = int(d['size'])
            d['age'] = int(d['age'])
            d['review_date'] = parse(d['review_date'])
            heights = [int(num.strip('\'').strip('\"')) for num in d['height'].split()]
            d['height'] = (heights[0] * 12) + heights[1]
            
        return data
    
    def bust_category(self, bust):
        #encodes bust size into classes 1-10
        if bust == 28:
            return 0
        elif bust == 30:
            return 1
        elif bust == 32:
            return 2
        elif bust == 34:
            return 3
        elif bust == 36:
            return 4
        elif bust == 38:
            return 5
        elif bust == 40:
            return 6
        elif bust == 42:
            return 7
        elif bust == 44:
            return 8
        elif bust == 46:
            return 9
        else:
            return 10
    
    def cup_category(self, cup):
         #encodes cup size into classes 1-12
        if cup == "aa":
            return 0
        elif cup == "a":
            return 1
        elif cup == "b":
            return 2
        elif cup == "c":
            return 3
        elif cup == "d":
            return 4
        elif cup == "d+":
            return 5
        elif cup == "dd":
            return 6
        elif cup == "ddd/e":
            return 7
        elif cup == "f":
            return 8
        elif cup == "g":
            return 9
        elif cup == "h":
            return 10
        elif cup == "i":
            return 11
        else:
            return 12
    
    def getData(self):
        return pd.DataFrame(self.data)
    
    
class predictionConverter:
    '''
    Help us convert our labels in our predictions as well as conduct predictions
    '''
    cup = []
    bust = []
    busts = []
    
    def __init__(self, cup, bust):
        self.cup = [self.convertCup(c) for c in cup]
        self.bust = [self.convertBust(b) for b in bust]
        
    def convertCup(self, cup):
        if cup == 0:
            return "aa"
        elif cup == 1:
            return "a"
        elif cup == 2:
            return "b"
        elif cup == 3:
            return "c"
        elif cup == 4:
            return "d"
        elif cup == 5:
            return "d+"
        elif cup == 6:
            return "dd"
        elif cup == 7:
            return "ddd/e"
        elif cup == 8:
            return "f"
        elif cup == 9:
            return "g"
        elif cup == 10:
            return "h"
        elif cup == 11:
            return "i"
        elif cup == 12:
            return "j"
    
    def convertBust(self, bust):
        if bust == 0:
            return 28
        elif bust == 1:
            return 30
        elif bust == 2:
            return 32
        elif bust == 3:
            return 34
        elif bust == 4:
            return 36
        elif bust == 5:
            return 38
        elif bust == 6:
            return 40
        elif bust == 7:
            return 42
        elif bust == 8:
            return 44
        elif bust == 9:
            return 46
        elif bust == 10:
            return 48
    def getBust(self):
        return self.bust
    
    def getCup(self):
        return self.cup
    
    def bustCombiner(self):
        busts = []
        for b, c in zip(self.getBust(), self.getCup()):
            bc = str(b) + str(c)
            busts.append(bc)
            
        self.busts = busts
        return busts