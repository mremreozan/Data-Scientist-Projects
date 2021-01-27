import numpy as np
import pandas as pd 
import pickle

#import sklearn modules
from sklearn.model_selection import train_test_split
from sklearn import ensemble


def model_func():
    data = pd.read_csv('../Datasets/def_dataset.csv')
    
    # Make a dictionary to only have Apartments, houses and others in the property subtype
    dico = {'MIXED_USE_BUILDING': 'OTHERS', 'House':'HOUSE', 'apartment':'APARTMENT', 'APARTMENT_BLOCK': 'APARTMENT', 'HOUSE': 'House', 'EXCEPTIONAL_PROPERTY': 'OTHERS', 'MANSION': 'HOUSE', 'VILLA': 'HOUSE', 'OTHER_PROPERTY': 'OTHERS', 'TOWN_HOUSE' : 'HOUSE', 'COUNTRY_COTTAGE': 'HOUSE', 'BUNGALOW': 'HOUSE', 'FARMHOUSE': 'HOUSE', 'MANOR_HOUSE': 'HOUSE', 'APARTMENT': 'APARTMENT', 'FLAT_STUDIO': 'APARTMENT', 'LOFT': 'APARTMENT', 'DUPLEX': 'APARTMENT', 'PENTHOUSE': 'APARTMENT', 'GROUND_FLOOR': 'OTHERS', 'KOT': 'OTHERS', 'TRIPLEX': 'APARTMENT', 'SERVICE_FLAT': 'APARTMENT' }

    # Make a dictionary to re-work the names of the building_state column
    dico_building_state = {'GOOD': 'GOOD', 'TO_RENOVATE':'TO RENOVATE', 'JUST_RENOVATED': 'JUST RENOVATED',  'AS_NEW': 'NEW', 'TO_RESTORE': 'TO REBUILD'}

    # Pre dropping all the obvious columns 
    df = data.drop(['source' , 'basement'], axis=1)

    #Here I'm dropping all the rows that have a required value as null 
    df = df[df['price'].notna()]        
    df = df[df['area'].notna()]         
    df = df[df['building_state_agg'].notna()]

    df['building_state_agg'].replace(dico_building_state, inplace= True)
    df['property_subtype'].replace(dico, inplace= True)

    # get dummies
    df2 = pd.get_dummies(df['property_subtype'])
    df3 = pd.get_dummies(df['building_state_agg'])
    df.drop(['property_subtype', 'building_state_agg'], axis=1, inplace=True)
    df = pd.concat([df, df2, df3], axis=1)  

    # Prediction target
    y = df.price

    # Choose features 
    features = ['postcode', 'area', 'rooms_number',
           'garden', 'garden_area', 'terrace', 'terrace_area', 'land_surface',
           'open_fire', 'swimming_pool_has', 'equipped_kitchen_has', 'furnished' ,
           'APARTMENT', 'HOUSE', 'OTHERS', 'GOOD',
           'JUST RENOVATED', 'NEW', 'TO REBUILD', 'TO RENOVATE']

    X = df[features]


    # Dividing the data into train/test
    feature_train, feature_test, label_train, label_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

    # Applying machine learning algorithm

    model = ensemble.GradientBoostingRegressor(
        n_estimators=400, max_depth=5, min_samples_split=7, learning_rate=0.1, loss='ls')

    model.fit(X, y) 

    pickle.dump(model, open('models/model.pkl','wb'))

model_func()