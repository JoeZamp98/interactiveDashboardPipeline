from boxsdk import JWTAuth, Client
import copy
import certifi
import io
import pandas as pd
from pickle import TRUE
import pymongo
import statistics
import re
import requests

## -- DEFINE GLOBAL VARIABLES -- ##

specific_survey = 'SURVEY_ID'
supplemental_survey = 'SURVEY_ID'
interval = 'DATE/INTERVAL_ID'

## -- ESTABLISH CONNECTION TO MONGODB -- ##

def connect_to_mongo():

    ca = certifi.where()

    client = pymongo.MongoClient(f"MONGO_CLIENT", tlsCAFile=ca) #Mongo Client hidden from public repository for security

    #Database connection
    brand_db = client['BrandDatabase']

    #Collection connections (within database) – each holds data that is ultimately structured slightly differently from data in other collections
    collection_attributes = brand_db['Attributes']
    collection_perceptions = brand_db['Perceptions']
    collection_formation = brand_db['Formation']
    collection_desirability_A = brand_db['Desirability-A']
    collection_desirability_B = brand_db['Desirability-B']
    collection_forceRank_A = brand_db['ForceRank-A']
    collection_forceRank_B = brand_db['ForceRank-B']
    collection_strategies = brand_db['Strategies']
    collection_demographics = brand_db['Demographics']
    collection_Interaction = brand_db['Interaction']
    collection_attributes_competitors = brand_db['Attributes-Competitors']
    collection_populations = brand_db['Populations']
    collection_deepDives_c = brand_db['DeepDives-C']
    collection_deepDives_d = brand_db['DeepDives-D']
    collection_custom_questions = brand_db['CustomQuestions']

    #Placeholder MongoDB commands to more easily delete data if needed

    # collection_attributes.delete_many({'Company': 'holder'})
    # collection_perceptions.delete_many({'Company': 'holder'})
    # collection_formation.delete_many({'Company': 'holder'})
    # collection_desirability_A.delete_many({'Company': 'holder'})
    # collection_desirability_B.delete_many({'Company': 'holder'})
    # collection_forceRank_A.delete_many({'Company': 'holder'})
    # collection_forceRank_B.delete_many({'Company': 'holder'})
    # collection_strategies.delete_many({'Company': 'holder'})
    # collection_demographics.delete_many({'Company': 'holder'})
    # collection_Interaction.delete_many({'Company': 'holder'})
    # collection_attributes_competitors.delete_many({'Company': 'holder'})
    # collection_populations.delete_many({'Company': 'holder'})
    # collection_deepDives_c.delete_many({'Company': 'holder'})
    #collection_deepDives_d.delete_many({})
    #collection_custom_questions.delete_many({'Company': 'holder'})

    return [collection_attributes, collection_perceptions, collection_formation, collection_desirability_A, collection_desirability_B, collection_forceRank_A, collection_forceRank_B, collection_strategies, collection_demographics, collection_Interaction, collection_attributes_competitors, collection_populations, collection_deepDives_c, collection_deepDives_d, collection_custom_questions]

## -- ESTABLISH CONNECTION TO BOX -- ##

def establish_box_connection():

    auth = JWTAuth.from_settings_file(r'box_json.json') #file is hidden from public repository
    box_client = Client(auth)

    service_account = box_client.user().get()

    print(f"Connected to: {service_account}")

    return box_client

## -- CONNECT TO QUALTRICS API AND IMPORT DATA FOR SPECIFIED INSTRUMENTS -- ##

def import_data():

    #Core Qualtrics import script
    fileFormat = 'csv'
    dataCenter = 'DATA_CENTER'
    useLabels = 'True'

    all_ids = [specific_survey, supplemental_survey]

    headers = {
        'content-type': 'application/json',
        'x-api-token': 'API_TOKEN_HERE'
    }

    counter = 1

    for id in all_ids:

        base_url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(dataCenter, id) #this URL isn't sensitive

        downloadRequestUrl = base_url

        downloadRequestPayload = '{"format":"csv", "useLabels":"True"}'
        downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
        progressId = downloadRequestResponse.json()["result"]["progressId"]
        print(downloadRequestResponse.text)

        requestCheckProgress = 0.0
        progressStatus = 'inProgress'

        while progressStatus != "complete" and progressStatus != "failed":
            print("progressStatus=", progressStatus)
            requestCheckUrl = base_url + progressId
            requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
            requestCheckProgress = requestCheckResponse.json()['result']["percentComplete"]
            print("Download is " + str(requestCheckProgress) + " complete")
            progressStatus = requestCheckResponse.json()['result']['status']

        if progressStatus == "failed":
            raise Exception("Export failed in Qualtrics-Python connection.")

        fileId = requestCheckResponse.json()['result']['fileId']

        requestDownloadUrl = base_url + fileId + '/file'
        requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=TRUE)

        df_segment = pd.read_csv(io.BytesIO(requestDownload.content), compression='zip')
        df_segment = pd.DataFrame(df_segment)

## -- FUNCION CALLS -- ##

# - Connection/Import Functions - # 

# - Structure/Cleaning Functions - #

# - Aggregation Functions - #
