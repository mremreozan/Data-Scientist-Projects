# organize dataset into a useful structure
from os import makedirs
from os import listdir
import os
from shutil import copyfile
from random import seed
from random import random
import pandas as pd


benignlst = []
malignant = []

df = pd.read_csv('dataset/dataHealth.csv', sep=";")

df2 =df.drop(columns=["klin. Diagn.", "nr", "Histo performed", "Diagnose red."])





df2['kat.Diagnose'] = df2['kat.Diagnose'].replace(1,0)
df2['kat.Diagnose'] = df2['kat.Diagnose'].replace([2,3,'?'],1)

df2['id'] = df2['id'].str.capitalize()
df2['id'] = [str(col) + '.BMP' for col in df2['id']]

ids = df2['id'].tolist()
diag = df2['kat.Diagnose'].tolist()

for i in range(len(ids)-1):
    if diag[i] == 0:
        benignlst.append(ids[i])
    else:
        malignant.append(ids[i])

sets = ["SET_D", "SET_E", "SET_F"]


# create directories
dataset_home = 'dataset/'
subdirs = ['train/', 'test/']
for subdir in subdirs:
    # create label subdirectories
    labeldirs = ['benign/', 'malignant/']
    for labldir in labeldirs:
        newdir = dataset_home + subdir + labldir
        makedirs(newdir, exist_ok=True)
# seed random number generator
seed(1)
# define ratio of pictures to use for validation
val_ratio = 0.25
# copy training dataset images into subdirectories
for set in sets:
    src_directory = f'dataset/skin cancer/{set}/'
    for file in listdir(src_directory):
        src = src_directory + file
        dst_dir = 'train/'
        filename = os.path.basename(src)
        if random() < val_ratio:
            dst_dir = 'test/'
        
        if filename in benignlst:
            dst = dataset_home + dst_dir + 'benign/'  + file
            copyfile(src, dst)
        elif filename in malignant:
            dst = dataset_home + dst_dir + 'malignant/'  + file
            copyfile(src, dst)







