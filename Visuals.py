import DataCleaning as dc
import random

PhoneDB, TabletDB, LaptopDB = dc.Cleaning()

#Main Page information and visuals

def MainPhone(Phone=None,flag=0):
    
    if flag == 0:
        Phone = PhoneDB.copy()
    
    Phone = Phone.sort_values(by=['Ratings','Stars'],ascending=False)
    Phone = Phone[['Name', 'Price', 'Image','Link','RAM','ROM']][:12]
    Phone.reset_index(drop=True,inplace=True)
    Phone = Phone.sample(frac=1).reset_index(drop=True)
    
    PhoneList = []
    
    for row in range(len(Phone)):
        record = []
        for col in Phone.columns:
            record.append(Phone[col][row])
        PhoneList.append(record)
    
    Phone = PhoneList
    
    return Phone

def MainLaptop(Laptop=None,flag=0):
    
    if flag == 0:
        Laptop = LaptopDB.copy()
    
    Laptop = Laptop.sort_values(by=['Ratings','Stars'],ascending=False)
    Laptop = Laptop[['Name', 'Price', 'Image','Link','RAM','ROM']][:12]
    Laptop.reset_index(drop=True,inplace=True)
    Laptop['Name'] = Laptop['Name'].apply(lambda x : x.split("(")[0].strip())
    Laptop = Laptop.sample(frac=1).reset_index(drop=True)
    
    LaptopList = []
    
    for row in range(len(Laptop)):
        record = []
        for col in Laptop.columns:
            record.append(Laptop[col][row])
        LaptopList.append(record)
    
    Laptop = LaptopList
    
    return Laptop

def MainTablet(Tablet=None,flag=0):
    
    if flag == 0:
        Tablet = TabletDB.copy()

    Tablet = Tablet.sample(frac=1).reset_index(drop=True)
    Tablet = Tablet[['Name', 'Price', 'Image','Link','RAM','ROM']][:12]    
        
    TabletList = []
    
    for row in range(len(Tablet)):
        record = []
        for col in Tablet.columns:
            record.append(Tablet[col][row])
        TabletList.append(record)
    
    Tablet = TabletList
    
    return Tablet

TopPhone = MainPhone()
TopLaptop = MainLaptop()
TopTablet = MainTablet()

Top = TopPhone+TopLaptop+TopTablet
random.shuffle(Top)
Top = Top[:6]

#User selection information and visuals
def PhoneFilter(Brand,RAM,ROM):
    
    results = PhoneDB.copy()
    
    results = dc.first_filter(Brand,RAM,ROM,PhoneDB)
    
    if len(results) == 0:
        results,flag = dc.phone_category_alternative(Brand,RAM,ROM,PhoneDB)
        results = MainPhone(results,1)
    else:
        results = MainPhone(results,1)
        flag = 0
    
    return results,flag

def LaptopFilter(Brand,RAM,ROM):
    
    results = LaptopDB.copy()
    
    results = dc.first_filter(Brand,RAM,ROM,results)
    
    if len(results) == 0:
        results,flag = dc.laptop_category_alternative(Brand,RAM,ROM,LaptopDB)
        results = MainLaptop(results,1)
    else:
        results = MainLaptop(results,1)
        flag = 0
    
    return results,flag

def TabletFilter(Brand,RAM,ROM):
    
    results = TabletDB.copy()
    
    results = dc.first_filter(Brand,RAM,ROM,results)
    
    if len(results) == 0:
        results,flag = dc.tablet_category_alternative(Brand,RAM,ROM,TabletDB)
        results = MainTablet(results,1)
    else:
        results = MainTablet(results,1)
        flag = 0
    
    return results,flag

def PredictionVisuals(Prediction):
        
    UserType,flag = dc.PredictionModel(Prediction)
    Data = []
    
    if flag != 1:
        DataFrames = {'Personal Computers': LaptopDB,'Mobile Phones':PhoneDB,'Tablet Phones':TabletDB }
        Device = Prediction['Device'][0]
        Data = DataFrames[Device]
        Data = Data[Data['Device Type'] == UserType]
        
        def CostEstimator(Data):
            if Prediction['Cost'][0] == 'Less than 15,000':
                Data = Data[Data['Price'] <= 15000]
                return Data
            elif Prediction['Cost'][0] == 'Between 15,000 - 30,000':
                Data = Data[(Data['Price'] > 15000) & (Data['Price'] <= 30000)]
                return Data
            elif Prediction['Cost'][0] == 'Over 30,0000':
                Data = Data[Data['Price'] > 30000]
                return Data
            else:
                pass
        
        Data =  CostEstimator(Data)
        
        if len(Data) == 0:
            Data = DataFrames[Device]
            Data = CostEstimator(Data)
        
        if 'Ratings' in Data.columns:
           Data = Data.sort_values(by=['Ratings','Stars'],ascending=False)
           Data = Data[['Name', 'Price', 'Image','Link']].head(4)

        else:
            Data = Data.sample(frac=1).reset_index(drop=True)
            Data = Data[['Name', 'Price', 'Image','Link']].head(4) 
            
        DatatList = []
        Data.reset_index(drop=True,inplace=True)
        
        for row in range(len(Data)):
            record = []
            for col in Data.columns:
                record.append(Data[col][row])
            DatatList.append(record)
               
        Data = DatatList
        
    return Data,flag