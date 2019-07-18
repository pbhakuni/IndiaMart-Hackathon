#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:31:28 2019

@author: Priyanka Bhakuni
@Team: Spark
"""

import pandas as pd
from nltk.stem import PorterStemmer 
import configuration as config
import numpy as np

ps = PorterStemmer()
#Provide the excel filepath
xls = pd.ExcelFile('/home/hduser/Desktop/Hackathon/IndiaMart/Latest/HackathonPrice.xlsx')

#Read sheet 1st:
df1 = pd.read_excel(xls, sheets=0)

 #Changing the datatype from series 
df1["Mcat Name"]= df1["Mcat Name"].astype(str) 
df1["Unit"]= df1["PC_ITEM_MOQ_UNIT_TYPE"].astype(str) 
df1["ISQ Name"]= df1["PC_ITEM_NAME"].astype(str) 
df1["Price"]= df1["PC_ITEM_FOB_PRICE"].astype(int) 

#Mcat name -> unit -> min/max
#pc item name -> unit -> min/max

#Make the units similar in case of spelling mistakes
def clean(x):
        if '(s)' in x:
            new_unit = x.replace("(s)","")
            #modified_unit = ps.stem(new_unit)
            for word in new_unit.split():
                if word.lower() in config.contractions:
                   final_unit = new_unit.replace(new_unit, config.contractions[word.lower()])
                   return(final_unit.lower())
                else:
                    return(new_unit.lower())
        elif 'per' in x:
            new_unit = x.replace('per ','')
            for word in new_unit.split():
                 if word.lower() in config.contractions:
                    final_unit = new_unit.replace(new_unit, config.contractions[word.lower()])
                    return(final_unit.lower())
                 else:
                    return(new_unit.lower())
        elif x.lower() in config.contractions:
               final_unit = x.replace(x, config.contractions[x.lower()])
               return(final_unit.lower())
        else:
               return(x.lower())
   
df1['Unit'] = df1['Unit'].apply(clean)
df1['Unit'] = df1['Unit'].apply(clean)

for item in df1["Mcat Name"].unique():
    filtered_data = df1[df1['Mcat Name'] == item]
    unique_unit = filtered_data['Unit'].unique()
    for indexes in unique_unit:
           q1, q3= np.percentile(filtered_data[filtered_data['Unit']==indexes]['Price'],[25,75])
           iqr_value = q3 - q1
           lower_bound = q1 -(1.5 * iqr_value) 
           upper_bound = q3 +(1.5 * iqr_value) 
           df_result = filtered_data[filtered_data['Price'].between(lower_bound, upper_bound, inclusive=True)]
           print("The price of",item,"per",indexes,"ranges from Rs",df_result['Price'].min(),"to Rs", df_result['Price'].max())

