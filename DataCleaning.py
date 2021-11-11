import pandas as pd
import numpy as np

InputPath = "../Website/static/excel/"

MobilePhoneData = str(InputPath) + str("MobilePhone.xlsx") 
LaptopData = str(InputPath) + str("laptops.xlsx") 
TabletData = str(InputPath) + str("TabletPhone.xlsx") 

#Scrapped Data Processed and Cleant
def Cleaning(Data=None):

    Phone = pd.read_excel(MobilePhoneData)
    Phone.drop_duplicates('Name',inplace=True)
    
    Tablet = pd.read_excel(TabletData)
    Tablet.drop_duplicates('Name',inplace=True)
    
    Laptop = pd.read_excel(LaptopData)
    Laptop.drop_duplicates('Name',inplace=True)
    
   # Phone Data Wrangling
    Phone['Name'].fillna('', inplace=True)
    Phone['Name'] = Phone['Name'].apply(lambda x : x.replace("Price","").strip())
    
    Phone['Brand'] = Phone['Name'].apply(lambda x : x.split(" ")[0])
    Phone['Brand'] = Phone['Brand'].apply(lambda x : 'I Kall' if x == 'I' else x)
    
    Phone['ROM'].fillna('', inplace=True)
    Phone['Expandable'] = Phone['ROM'].apply(lambda x : x.split(",")[1].strip().title() if len(x.split(",")) > 1 else '')
    Phone['ROM'] = Phone['ROM'].apply(lambda x : x.split(",")[0].strip() if x != '' else '')
    Phone['ROM'] = Phone['ROM'].apply(lambda x : x.replace("internal storage","").strip())
    
    Phone['RAM'].fillna('', inplace=True)
    Phone['RAM'] = Phone['RAM'].apply(lambda x : x.replace("RAM","").strip())
    
    Phone['Battery'].fillna('', inplace=True)
    Phone['Battery'] = Phone['Battery'].apply(lambda x : x.split("battery")[0].strip() if x != '' else '')
    Phone['Battery'] = Phone['Battery'].apply(lambda x : int(x.split("mAh")[0].strip()) if x != '' else 0)
    Phone['Expandable'] = Phone['Expandable'].apply(lambda x : x.split("Upto")[1].strip().upper() if len(x.split("Upto")) > 1 else x)
    
    Phone['Price'].fillna('0', inplace=True)
    Phone['Price'] = Phone['Price'].apply(lambda x : int(x.replace(",","").replace("Rs.","")))
    
    Phone = Phone[Phone['Price'] != 0]
    
    for i in range(len(Phone['Brand'].value_counts().index)):
        rec = Phone['Brand'].value_counts().index[i]
        try:
            recmode = Phone[Phone['Brand'] == rec]['OS'].mode()[0]
        except:
            recmode = ''
        Phone.loc[Phone['OS'].isnull() & Phone['Brand'].eq(rec),'OS'] = recmode
    
    for i in range(len(Phone)):
        record = Phone.index[i]
        if Phone['OS'][record] == '':
            if (Phone['RAM'][record] != '') | (Phone['ROM'][record] != ''):
                Phone.loc[Phone.index == record,'OS'] = 'Android'
    
    Phone['Ratings'].fillna(0, inplace=True)
    Phone['Ratings'] = Phone['Ratings'].apply(lambda x : int(x))
    Phone['Stars'].fillna(0, inplace=True)
    Phone['Stars'] = Phone['Stars'].apply(lambda x : 0 if x == '\xa0\xa0\xa0\xa0\xa0' else x)
    Phone['Stars'] = Phone['Stars'].astype('float')
    
    Phone = Phone[Phone['OS'] != '']
    
    RAMDatabase  = ['18 GB', '12 GB', '10 GB','8 GB','6 GB']  
    ROMDatabase  = ['512 GB','256 GB','128 GB'] 

    Phone['RAMDetails'] = Phone['RAM'].apply(lambda x : 1 if x in RAMDatabase else 0)
    Phone['ROMDetails'] = Phone['ROM'].apply(lambda x : 1 if x in ROMDatabase else 0)
    Phone['BatteryDetails'] = Phone['Battery'].apply(lambda x : 1 if x >= 30000 else 0)
    Phone['Specifications'].fillna('',inplace=True)
    Phone['CameraDetails'] = Phone['Specifications'].apply(lambda x : 1 if 'camera' in x.lower() else 0)
    Phone['Score'] = Phone['RAMDetails'] + Phone['ROMDetails'] + Phone['BatteryDetails'] + Phone['CameraDetails']
    Phone['Device Type'] = Phone['Score'].apply(lambda x : 'Low Ended User' if x <= 1 else ('Medium Ended User' if x == 2 else 'High Ended User'))

    Phone.drop(['RAMDetails','ROMDetails','BatteryDetails','CameraDetails'], inplace=True, axis=1)

    Phone.dropna(inplace=True)
    Phone.reset_index(drop=True,inplace=True)
    
    # Tablet Data Wrangling
    Tablet['Name'].fillna('', inplace=True)
    Tablet['Name'] = Tablet['Name'].apply(lambda x : x.replace("Price","").strip())
    Tablet['Brand'] = Tablet['Name'].apply(lambda x : x.split(" ")[0])
    
    Tablet['ROM'].fillna('', inplace=True)
    Tablet['ROM'] = Tablet['ROM'].apply(lambda x : x.split(",")[0].strip() if x != '' else '')
    Tablet['ROM'] = Tablet['ROM'].apply(lambda x : x.replace("Storage","").strip())
    
    Tablet['RAM'].fillna('', inplace=True)
    Tablet['RAM'] = Tablet['RAM'].apply(lambda x : x.replace("RAM","").strip())
    
    Tablet['Screen'].fillna('', inplace=True)
    Tablet['Screen'] = Tablet['Screen'].apply(lambda x : x.replace("inch Screen","").strip())
    
    Tablet['Battery'].fillna('', inplace=True)
    Tablet['Battery'] = Tablet['Battery'].apply(lambda x : x.replace("mAh","").strip())
    Tablet['Battery'] = Tablet['Battery'].apply(lambda x : np.nan if x == '' else int(x))
    
    Tablet['Price'].fillna('0', inplace=True)
    Tablet['Price'] = Tablet['Price'].apply(lambda x : int(x.replace(",","").replace("Rs.","")))
    
    Tablet['OS'] = Tablet['Brand'].apply(lambda x : 'iOS' if x == 'Apple' else ('Windows' if ((x == 'Microsoft')|(x == 'Notion')) else 'Android'))
    
    Tablet = Tablet[Tablet['Price'] != 0]
    
    Tablet = Tablet[Tablet['OS'] != '']
    
    RAMDatabase  = ['8GB','6GB', '4GB']
    ROMDatabase  = ['256GB', '128GB', '64GB', '16GB']

    Tablet['RAMDetails'] = Tablet['RAM'].apply(lambda x : 1 if x in RAMDatabase else 0)
    Tablet['ROMDetails'] = Tablet['ROM'].apply(lambda x : 1 if x in ROMDatabase else 0)
    Tablet['Battery'].fillna(0,inplace=True)
    Tablet['Battery'] = Tablet['Battery'].astype('int64') 
    Tablet['BatteryDetails'] = Tablet['Battery'].apply(lambda x : 1 if x >= 5000 else 0)
    Tablet['Score'] = Tablet['RAMDetails'] + Tablet['ROMDetails'] + Tablet['BatteryDetails'] 
    Tablet['Device Type'] = Tablet['Score'].apply(lambda x : 'Low Ended User' if x == 0 else ('High Ended User' if x == 3 else 'Medium Ended User'))

    Tablet.drop(['RAMDetails','ROMDetails','BatteryDetails'], inplace=True, axis=1)

    Tablet.dropna(inplace=True)
    Tablet.reset_index(drop=True,inplace=True)
    
    # Laptop Data Wrangling
    Laptop['Name'].fillna('', inplace=True)
    Laptop['Name'] = Laptop['Name'].apply(lambda x : x.replace("Price","").strip())
    
    Laptop['Name'] = Laptop['Name'].apply(lambda x : x.split("(")[0].strip() if x != '' else '')
    
    Laptop['Brand'] = Laptop['Name'].apply(lambda x : x.split(" ")[0].title())
    
    Laptop['Price'].fillna('0', inplace=True)
    Laptop['Price'] = Laptop['Price'].apply(lambda x : int(x.replace(",","").replace("Rs.","")))
    
    Laptop = Laptop[Laptop['Price'] != 0]
    
    Laptop['RAM'].fillna('', inplace=True)
    Laptop['RAM'] = Laptop['RAM'].apply(lambda x : x.replace("RAM","").strip())
    
    Laptop['ROM'].fillna('', inplace=True)
    Laptop['ROM'] = Laptop['ROM'].apply(lambda x : x.replace("SSD","").replace("HDD","").strip())
    
    Laptop['Battery'].fillna("0", inplace=True)
    Laptop['Battery'] = Laptop['Battery'].apply(lambda x : float(x.replace("Hrs","").strip()))
    Laptop['Battery'] = Laptop['Battery'].apply(lambda x : np.nan if x == 0 else x)
    Laptop['Battery'].fillna(round(Laptop['Battery'].mean()), inplace=True)
    
    for i in range(len(Laptop['Brand'].value_counts().index)):
        rec = Laptop['Brand'].value_counts().index[i]
        try:
            recmode = Laptop[Laptop['Brand'] == rec]['OS'].mode()[0]
        except:
            recmode = 'Windows 10'
        Laptop.loc[Laptop['OS'].isnull() & Laptop['Brand'].eq(rec),'OS'] = recmode
        
    for i in range(len(Laptop['Brand'].value_counts().index)):
        rec = Laptop['Brand'].value_counts().index[i]
        try:
            recmode = Laptop[Laptop['Brand'] == rec]['Processor'].mode()[0]
        except:
            recmode = 'Intel Core i3 (10th Gen)'
        Laptop.loc[Laptop['Processor'].isnull() & Laptop['Brand'].eq(rec),'Processor'] = recmode
        
    for i in range(len(Laptop[['OS','Processor']].value_counts().index)):
        rec = Laptop[['OS','Processor']].value_counts().index[i]
        recmode = Laptop[(Laptop['OS'] == rec[0]) | (Laptop['Processor'] == rec[1])]['Webcam'].mode()[0]
        Laptop.loc[Laptop['Webcam'].isnull() & Laptop['OS'].eq(rec[0]) & Laptop['Processor'].eq(rec[1]),'Webcam'] = recmode 
        
    Laptop['RAM'].fillna(Laptop['RAM'].mode()[0], inplace=True)
    Laptop['ROM'].fillna(Laptop['ROM'].mode()[0], inplace=True)
    Laptop['Ratings'].fillna(0, inplace=True)
    Laptop['Ratings'] = Laptop['Ratings'].apply(lambda x : int(x))
    
    Laptop['Stars'].fillna(0, inplace=True)
    Laptop['Stars'] = Laptop['Stars'].apply(lambda x : 0 if x == '\xa0\xa0\xa0\xa0\xa0' else x)
    Laptop['Stars'] = Laptop['Stars'].astype('float')
        
    Laptop = Laptop[Laptop['OS'] != '']
    
    RAMDatabase  = ['32GB', '16GB','8GB']
    ROMDatabase  = ['2 TB','1 TB','750 GB','512 GB','500 GB']

    Laptop['RAMDetails'] = Laptop['RAM'].apply(lambda x : 1 if x in RAMDatabase else 0)
    Laptop['ROMDetails'] = Laptop['ROM'].apply(lambda x : 1 if x in ROMDatabase else 0)
    Laptop['Battery'].fillna(0,inplace=True)
    Laptop['Battery'] = Laptop['Battery'].astype('int64') 
    Laptop['BatteryDetails'] = Laptop['Battery'].apply(lambda x : 1 if x >= Laptop['Battery'].mean() else 0)
    Laptop['Specifications'].fillna('',inplace=True)
    Laptop['CameraDetails'] = Laptop['Specifications'].apply(lambda x : 1 if 'hd' in x.lower() else 0)

    Laptop['Score'] = Laptop['RAMDetails'] + Laptop['ROMDetails'] + Laptop['BatteryDetails'] + Laptop['CameraDetails']
    Laptop['Device Type'] = Laptop['Score'].apply(lambda x : 'Low Ended User' if x <= 1 else ('Medium Ended User' if x == 2 else 'High Ended User'))

    Laptop.drop(['RAMDetails','ROMDetails','BatteryDetails','CameraDetails'], inplace=True, axis=1)

    Laptop.dropna(inplace=True)
    Laptop.reset_index(drop=True,inplace=True)
    
    return Phone, Tablet, Laptop

#Basic Filtration
def first_filter(Brand,RAM,ROM,df):
    
    results = df.copy()
    
    if len(Brand) != 0:
        query = ' | '.join(['(Brand=="{}")'.format(k) for k in Brand])
        results = results.query(query)
    
    if len(RAM) != 0:
        query = ' | '.join(['(RAM=="{}")'.format(k) for k in RAM])
        results = results.query(query)
        
    if len(ROM) != 0:    
        query = ' | '.join(['(ROM=="{}")'.format(k) for k in ROM])
        results = results.query(query)    
    
    return(results)

#Alternate Category Filtration - Recommendation System I
def phone_category_alternative(Brand,RAM,ROM,df):
    
    BrandOG = Brand

    RAMDatabase  = ['18 GB', '12 GB', '10 GB','8 GB','6 GB','4 GB','3 GB','2 GB', '1.5 GB', '1 GB',
                    '768 MB', '512 MB','256 MB', '128 MB','64 MB', '32 MB', '16 MB', '8 MB','4 MB']  
    ROMDatabase  = ['512 GB','256 GB','128 GB','64 GB', '32 GB', '16 GB','8 GB','4 GB','2 GB', '1 GB',
                    '512 MB', '256 MB','245 MB', '128 MB','64 MB', '32 MB', '24 MB' ,'16 MB','9 MB','8 MB','4 MB',
                    '500 KB','60 KB','32 KB','20 KB']   
    BrandDatabase = ['Samsung','OPPO','Apple','Vivo','Realme','OnePlus']
    
    results = df.copy()
        
    try:
        alt1index_RAM = RAMDatabase.index(RAM[0])
    except:
        alt1index_RAM = RAMDatabase.index('6 GB')
        
    alt1_RAM = RAMDatabase[alt1index_RAM]
    alt1_ROM = ROMDatabase[alt1index_RAM-1]
        
    try:
        alt2index_ROM = ROMDatabase.index(ROM[0])
    except:
        alt2index_ROM = ROMDatabase.index('64 GB')
        
    alt2_RAM = RAMDatabase[alt2index_ROM+1]
    alt2_ROM = ROMDatabase[alt2index_ROM]
    
    Brand = list(set(Brand + BrandDatabase))
        
    if Brand != '':
        query = ' | '.join(['(Brand=="{}")'.format(k) for k in Brand])
        results = results.query(query)
            
    results = results[((results['RAM'] == alt1_RAM) & (results['ROM'] == alt1_ROM)) | 
            ((results['RAM'] == alt2_RAM) & (results['ROM'] == alt2_ROM))]
    
    if len(results) == 0:
       results = df.copy()
       query = ' | '.join(['(Brand=="{}")'.format(k) for k in BrandOG])
       results = results.query(query)
            
    results = results[results['RAM'] != '']
    results = results.sort_values(by=['Ratings','Stars'],ascending=False)
    results = results.reset_index(drop=True)
    return(results,1)


def laptop_category_alternative(Brand,RAM,ROM,LaptopDB):
    
    results = LaptopDB.copy()

    if len(Brand) != 0:
        query = ' | '.join(['(Brand=="{}")'.format(k) for k in Brand])
    
    if len(RAM) != 0:
        query = query + ' | ' +' | '.join(['(RAM=="{}")'.format(k) for k in RAM])

    if len(ROM) != 0:    
        query = query + ' | ' +' | '.join(['(ROM=="{}")'.format(k) for k in ROM])

    results = results.query(query)
    
    if len(results) == 0:
       results = LaptopDB.copy()
       query = ' | '.join(['(Brand=="{}")'.format(k) for k in Brand])
       results = results.query(query)
            
    results = results[results['RAM'] != '']
    results = results.sort_values(by=['Ratings','Stars'],ascending=False)
    results = results.reset_index(drop=True)
    return(results,1)
        
def tablet_category_alternative(Brand,RAM,ROM,TabletDB):
    
    results = TabletDB.copy()

    if len(Brand) != 0:
        query = ' | '.join(['(Brand=="{}")'.format(k) for k in Brand])
    
    if len(RAM) != 0:
        query = query + ' | ' +' | '.join(['(RAM=="{}")'.format(k) for k in RAM])

    if len(ROM) != 0:    
        query = query + ' | ' +' | '.join(['(ROM=="{}")'.format(k) for k in ROM])

    results = results.query(query)
    
    if len(results) == 0:
       results = TabletDB.copy()
       query = ' | '.join(['(Brand=="{}")'.format(k) for k in Brand])
       results = results.query(query)
            
    results = results[results['RAM'] != '']
    results = results.reset_index(drop=True)
    return(results,1)


#Machine Learning Data Model
import pickle

def PredictionModel(Prediction):
    
    flag = 0
    
    try:
        UserInput = [Prediction['Function'][0],Prediction['Photograph'][0],Prediction['Usage'][0]]
    except:
        print("Kindly enter all details")
        flag = 1

    if flag != 1:
        rmodel = pickle.load(open("ZelleModel.pickle","rb"))
        
        DecodedValues = ['Storage','Speed','Both','Yes','No','Maybe','Less than an hour','Between 3 - 4 hours','More than 4 hours']
        CodededValues = [0,1,2,0,1,2,0,1,2]
        
        def encryption(value):
            valueindex = DecodedValues.index(value)
            encodedvalue = CodededValues[valueindex]
            return encodedvalue
        
        EncodedValues = map(encryption, UserInput)
        EncodedValues = list(EncodedValues)
        
        Inputs = [EncodedValues]
        Predictions = rmodel.predict(Inputs)
        
        Users = {0:'Low Ended User',1:'Medium Ended User',2:'High Ended User'}
        UserType = Users[Predictions[0]]
        
        return UserType,flag
            
    else:
        UserType = None
        return UserType,flag