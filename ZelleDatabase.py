import psycopg2

dbusername = '<postgresql_username>'
dbpassword = '<postgresql_password>'
dbhost = '<postgresql_host>'
dbport = '<postgresql_port>'
dbname = '<postgresql_database_name>'

# =============================================================================
# # CODE TO CREATE A TABLE IN POSTGRESQL
# 
# connection = psycopg2.connect(user=dbusername,password=dbpassword,host=dbhost, port=dbport, database=dbname)
#
# # PREDICTION DATABASE
# cursor = connection.cursor()
# cursor.execute("CREATE table predictiondatabase(device TEXT, function TEXT, photograph TEXT, usage TEXT, cost TEXT);")
# print("Table Created")
# connection.commit()    
# 
# # FEEDBACK DATABASE
# cursor = connection.cursor()
# cursor.execute("CREATE table feedbackdatabase(heard TEXT, recommendation TEXT, satisfaction TEXT, experience TEXT, changes TEXT);")
# print("Table Created")
# connection.commit()   
# =============================================================================

# Connect to an existing database
def dataforprediction(device=None,function=None,photograph=None,usage=None,cost=None):
    
    device = ",".join(device)
    function = ",".join(function)
    photograph = ",".join(photograph)
    usage = ",".join(usage)
    cost = ",".join(cost)
    
    try:
        connection = psycopg2.connect(user=dbusername,
                              password=dbpassword,
                              host=dbhost,
                              port=dbport,
                              database=dbname)
        
        cursor = connection.cursor()
    
        postgres_insert_query = """ INSERT INTO predictiondatabase (DEVICE, FUNCTION, PHOTOGRAPH, USAGE, COST) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (device,function,photograph,usage,cost)
        cursor.execute(postgres_insert_query, record_to_insert)
    
        connection.commit()
    
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record", error)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
        
def dataforfeedback(heard=None, recommendation=None, satisfaction=None, experience=None, Change=None):
    
    heard = ",".join(heard)
    recommendation = ",".join(recommendation)
    satisfaction = ",".join(satisfaction)
    experience = ",".join(experience)
    Change = ",".join(Change)
    
    try:
        connection = psycopg2.connect(user=dbusername,
                              password=dbpassword,
                              host=dbhost,
                              port=dbport,
                              database=dbname)
        
        cursor = connection.cursor()
    
        postgres_insert_query = """ INSERT INTO feedbackdatabase (HEARD, RECOMMENDATION, SATISFACTION, EXPERIENCE, CHANGES) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (heard,recommendation,satisfaction,experience,Change)
        cursor.execute(postgres_insert_query, record_to_insert)
    
        connection.commit()
    
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record", error)
    
    finally:
        if connection:
            cursor.close()
            connection.close()