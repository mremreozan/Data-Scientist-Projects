import numpy as np
import pandas as pd 
import os
import re
import json

""" 
Peprocess your client data
this program works for one entry (value); or list of entries for each feature
and return a dictionary, that has the same structure of the input JSON dictionary
"""

class Cleaner_SalesData:
    """ Utility class that cleans real estate sale offers data from a CSV file into a pandas DataFrame for further work on it"""
    def __init__(self, json_file):
        # self.url = url
        self.json_file = json_file
        self.columns = ['area', 'property-type', 'rooms-number', 'zip-code', 'land-area',
                        'garden', 'garden-area', 'equipped-kitchen', 'full-address',
                        'swimmingpool', 'furnished', 'open-fire', 'terrace', 'terrace-area',
                        'facades-number', 'building-state']
        self.sales_data = pd.DataFrame(columns=self.columns)
        self.cleaned = False


    def cleaning_feature(self):

        ###################################
        #######    Check Obligation Features
        ###################################
        ###################################
        #Obligation, area
        for key, property_dict in self.json_file.items():

            one_property = pd.DataFrame([property_dict])
            try:
                area = property_dict['area']
            except:
                return "We can not provide prediction, please input area feature in your data. Please check: https://github.com/adamflasse/Api_deployment/blob/main/README.md for more info"
            try:
                zipcode = property_dict['zip-code']
            except:
                return "We can not provide prediction, please input zip-code feature in your data. Please check: https://github.com/adamflasse/Api_deployment/blob/main/README.md for more info"
            try:
                propertytype = property_dict['property-type']
            except:
                return "We can not provide prediction, please input property-type feature in your data. Please check: https://github.com/adamflasse/Api_deployment/blob/main/README.md for more info"
            try:
                rooms = property_dict['rooms-number']
            except:
                return "We can not provide prediction, please input rooms-number feature in your data. Please check: https://github.com/adamflasse/Api_deployment/blob/main/README.md for more info"

            #check if you entered proper feature
            ### zip-code checking
            postcode = property_dict['zip-code']
            if postcode < 1000 or postcode > 10000:
                return "Wrong zipcode"

            default_model = Cleaner_SalesData.building_default_model(one_property['property-type'].values[0], one_property['area'].values[0])

            ###################################
            ###################################
            #######    Boolean Features
            ###################################
            ###################################
            #Optional, equipped-kitchen
            if  'equipped-kitchen' in one_property.columns:
                one_property['equipped-kitchen']=one_property['equipped-kitchen'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
                #If I have missing value, I replace it with the highest frequency value
                one_property['equipped-kitchen']=one_property['equipped-kitchen'].fillna(one_property['equipped-kitchen'].mode().iloc[0])
                #cast to boolean
                one_property['equipped-kitchen'] = one_property['equipped-kitchen'].apply(lambda x: bool(x))
            else:
                one_property['equipped-kitchen'] = default_model['equipped-kitchen']

            # Optional, furnished
            if  'furnished' in one_property.columns:
                one_property['furnished']=one_property['furnished'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
                one_property['furnished']=one_property['furnished'].fillna(one_property['furnished'].mode().iloc[0])
            else:
                one_property['furnished'] = default_model['furnished']

            # Optional, swimmingpool
            if  'swimmingpool' in one_property.columns:
                one_property['swimmingpool']=one_property['swimmingpool'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
                one_property['swimmingpool']=one_property['swimmingpool'].fillna(one_property['swimmingpool'].mode().iloc[0])
                one_property['swimmingpool'] = one_property['swimmingpool'].apply(lambda x: bool(x))
            else:
                one_property['swimmingpool'] = default_model['swimmingpool']

            #Optional, open-fire
            if  'open-fire' in one_property.columns:
                one_property['open-fire']=one_property['open-fire'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
                one_property['open-fire']=one_property['open-fire'].fillna(one_property['open-fire'].mode().iloc[0])
                one_property['open-fire'] = one_property['open-fire'].apply(lambda x: bool(x))
            else:
                one_property['open-fire'] = default_model['open-fire']

            #Optional, terrace
            if  'terrace' in one_property.columns:
                one_property['terrace']=one_property['terrace'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
                one_property['terrace']=one_property['terrace'].fillna(one_property['terrace'].mode().iloc[0])
                one_property['terrace'] = one_property['terrace'].apply(lambda x: bool(x))
            else:
                one_property['terrace'] = default_model['terrace']

            #Optional, garden
            if  'garden' in one_property.columns:
                one_property['garden']=one_property['garden'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
                one_property['garden']=one_property['garden'].fillna(one_property['garden'].mode().iloc[0])
                one_property['garden'] = one_property['garden'].apply(lambda x: bool(x))
            else:
                one_property['garden'] = default_model['garden']

            ###################################
            ###################################
            #######    Area Features
            ###################################
            ###################################
            #area, remove m2
            one_property['area'] = self.manage_AreaFeature(one_property['area'])

            #land-area": Optional[int],
            if 'land-area' in one_property.columns:
                one_property['land-area']=self.manage_AreaFeature(one_property['land-area'])
            else:
                one_property['land-area'] = default_model['land-area']

            #"terrace-area": Optional[int],
            if 'terrace-area' in one_property.columns:
                one_property['terrace-area']=self.manage_AreaFeature(one_property['terrace-area'])
            else:
                one_property['terrace-area'] = default_model['terrace-area']

            #garden-area": Optional[int],
            if 'garden-area' in one_property.columns:
                one_property['garden-area']=self.manage_AreaFeature(one_property['garden-area'])
            else:
                one_property['garden-area'] = default_model['garden-area']
            ###################################
            ###################################
            #######    Number Features
            ###################################
            ###################################
            #"rooms-number": int,
            #remove outliers
            to_be_deleted_filter = one_property['rooms-number'].apply(lambda x: x == 0 or x >= 100)
            one_property.loc[to_be_deleted_filter, 'rooms-number'] = None
            one_property['rooms-number'] = one_property['rooms-number'].fillna(one_property['rooms-number'].mode().iloc[0])
            one_property['rooms-number'] = one_property['rooms-number'].apply(lambda x: int(x))


            #facades-number": Optional[int],
            if 'facades-number' in one_property.columns:
                to_be_deleted_filter = one_property['facades-number'].apply(lambda x: x == 0 or x > 4)
                one_property.loc[to_be_deleted_filter, 'facades-number'] = None
                one_property['facades-number'] = one_property['facades-number'].fillna(one_property['facades-number'].mode().iloc[0])
                one_property['facades-number'] = one_property['facades-number'].apply(lambda x: int(x))
            else:
                one_property['facades-number'] = default_model['facades-number']

            ###################
            ######### TO DO, need TO CHECK AGAIN
            #################
            #"zip-code": int, we could have nan input
            one_property['zip-code'] = one_property['zip-code'].fillna(0)
            one_property['zip-code'] = one_property['zip-code'].apply(lambda x: int(x))

            # #"property-type": "APARTMENT" | "HOUSE" | "OTHERS",
            one_property['property-type']=one_property['property-type'].apply(lambda x: Cleaner_SalesData.property_or_keep(x))
            one_property['property-type']= one_property['property-type'].fillna(0)

            #"full-address": Optional[str],
            if 'full-address' in one_property.columns:
                one_property['full-address'] = one_property['full-address'].apply(lambda x: str(x))
                one_property['full-address'] = one_property['full-address'].fillna(0)
            else:
                one_property['full-address'] = default_model['full-address']

            #building-state": Optional
            if 'building-state' in one_property.columns:
                one_property['building-state'] = one_property['building-state'].apply(lambda x: Cleaner_SalesData.categorize_state(x))
                one_property['building-state'] = one_property['building-state'].fillna(0)
            else:
                one_property['building-state'] = default_model['building-state']

            self.sales_data = self.sales_data.append(one_property, ignore_index=True)

        return self.sales_data

    @staticmethod
    def categorize_state(value):
        to_renovate = ['TO_RENOVATE', 'TO_BE_DONE_UP', 'TO_RESTORE', 'old', 'To renovate', 'To be done up',
                       'To restore', "TO RENOVATE"]
        good = ['GOOD', 'Good', 'AS_NEW', 'As new']
        renovated = ['JUST_RENOVATED', 'Just renovated', "JUST RENOVATED"]
        new = ['New',"NEW"]
        to_rebuild=["TO REBUILD","TO_REBUILD", "To rebuild"]
        category = None  # default category (corresponds to values = '0')
        if value in to_renovate:
            category = "TO RENOVATE"
        elif value in good:
            category = "GOOD"
        elif value in renovated:
            category = "JUST RENOVATED"
        elif value in new:
            category = "NEW"
        elif value in to_rebuild:
            category = "TO REBUILD"
        else:
            category = 'GOOD'
        return category

    def manage_AreaFeature(self, Ser):
        #remove m2
        Ser= Ser.apply(lambda x: Cleaner_SalesData.area_remove_m2(x))
        #fill in the empty cells
        #Ser.fillna(Ser.median(), inplace=True)
        Ser= Ser.fillna(Ser.median())
        #cast to int
        Ser = Ser.apply(lambda x: int(x))
        return (Ser)

    @staticmethod
    def property_or_keep(x):
        try:
            if x in ["APARTMENT", "Apartment"]:
                return ("APARTMENT")
            elif x in ["HOUSE", "House"]:
                return ("HOUSE")
            elif str(x).isdigit():
                return None
            elif x not in ["APARTMENT", "Apartment","HOUSE", "House"]:
                return ("OTHERS")
        except ValueError:
                 return None

    @staticmethod
    def bool_or_keep(x):
        try:
            if x in [1, "1", "TRUE", "true", "True",True,"YES", "yes", "Yes"]:
                return (True)
            elif x in [0, "0", "FALSE", "false", "False",False,"NO", "no", "No"]:
                return (False)
        except ValueError:
            return (None)

    @staticmethod
    # a single integer number is extracted from area to remove the m2 measurement units.
    # this simple method was adopted since no commas were found in area field.
    def area_remove_m2(x):
        try:
            return int(x)
        except ValueError:
            x=str(x)
            numbers = [int(s) for s in x.split() if s.isdigit()]
            if len(numbers) == 1:
                return int(numbers[0])
            elif len(numbers) > 1:
                return False
            else:
                return None

    @staticmethod
    def building_default_model(building_type, area):
        building_type = building_type
        area = area
        if building_type == 'APARTMENT':
            appartment_dico = {"land-area": area + 20,
                           "garden": False,
                           "garden-area": 0,
                           "equipped-kitchen": True,
                           "swimmingpool": False,
                           "furnished": False,
                           "open-fire": False,
                           "terrace": True,
                           "terrace-area": 20,
                           "building-state": "GOOD"}
            return appartment_dico

        elif building_type == 'HOUSE':

            houses_dico = {"land-area": area + 75,
                       "garden": True,
                       "garden-area": 75,
                       "equipped-kitchen": True,
                       "swimmingpool": False,
                       "furnished": False,
                       "open-fire": False,
                       "terrace": False,
                       "terrace-area": 0,
                       "building-state": "GOOD"}
            return houses_dico

        else :
           other_dico = {"land-area": area,
                     "garden": False,
                     "garden-area": 0,
                     "equipped-kitchen": False,
                     "swimmingpool": False,
                     "furnished": False,
                     "open-fire": False,
                     "terrace": False,
                     "terrace-area": 0,
                     "building-state": "GOOD"}
           return other_dico    

def preprocess(json_file):
    #url_json = 'input_data.json'
    ss=Cleaner_SalesData(json_file)
    cleaned_df_or_error_json = ss.cleaning_feature()

    if type(cleaned_df_or_error_json)==str:
        return cleaned_df_or_error_json

    cleaned_json_df = pd.DataFrame()
    cleaned_json_df['postcode'] = cleaned_df_or_error_json['zip-code']
    cleaned_json_df['area'] = cleaned_df_or_error_json['area']
    cleaned_json_df['rooms_number'] = cleaned_df_or_error_json['rooms-number']
    cleaned_json_df['garden'] = cleaned_df_or_error_json['garden']
    cleaned_json_df['garden_area'] = cleaned_df_or_error_json['garden-area']
    cleaned_json_df['terrace'] = cleaned_df_or_error_json['terrace']
    cleaned_json_df['terrace_area'] = cleaned_df_or_error_json['terrace-area']
    cleaned_json_df['land_surface'] = cleaned_df_or_error_json['land-area']
    cleaned_json_df['open_fire'] = cleaned_df_or_error_json['open-fire']
    cleaned_json_df['swimming_pool_has'] = cleaned_df_or_error_json['swimmingpool']
    cleaned_json_df['equipped_kitchen_has'] = cleaned_df_or_error_json['equipped-kitchen']
    cleaned_json_df['furnished'] = cleaned_df_or_error_json['furnished']
    cleaned_json_df['property_subtype'] = cleaned_df_or_error_json['property-type']
    cleaned_json_df['building_state'] = cleaned_df_or_error_json['building-state']

    cleaned_json_df[['APARTMENT', 'HOUSE', 'OTHERS', 'GOOD',
           'JUST RENOVATED', 'NEW', 'TO REBUILD', 'TO RENOVATE']] = 0

    for i in range(len(cleaned_json_df)):
        property_name = cleaned_json_df.loc[i, 'property_subtype']
        building_state_name = cleaned_json_df.loc[i, 'building_state']
        cleaned_json_df.loc[i, property_name] = 1
        cleaned_json_df.loc[i, building_state_name] = 1

    cleaned_json_df.drop(['property_subtype', 'building_state'], axis=1, inplace=True)
    cleaned_json_df = cleaned_json_df.astype('float64')

    return cleaned_json_df
