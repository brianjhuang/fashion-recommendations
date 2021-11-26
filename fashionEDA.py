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
    
    def getData(self):
        return pd.DataFrame(self.data)

        