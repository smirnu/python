import requests
import time
import json
import csv
import os
import pandas as pd

# connect to the API with url builded from parameters, returns json in bytes or False/True if pull of the data didn't happen
def connectToApi(apiAddress, page, params, apiKey):
    attempt = 0
    responseCode = 0
    # we are going to retry to call the API in case if sth went wrong in the first time
    while attempt < 2 and responseCode !=200:
        try:
            responseApi = requests.get(apiAddress + str(page) + params + apiKey)
            responseCode = responseApi.status_code
            if responseApi.status_code != 200:
                raise Exception(str(responseApi) + str(responseApi.content))
            else:
                return responseApi.content
        except Exception as e:
            if attempt < 1:
                attempt += 1
                time.sleep(2)
            else:
                if responseCode == 429:
                    print('Status code is 429. Too Many Requests response status code indicates the user has sent too many requests' +
                    ' in a given amount of time. With the developer key you can do 500 calls a day. We need to stop the load, you  can restart the system tomorrow.')
                    # has to be False, I changed that as I need to work with the file even after I will reach the limit per day
                    # there is elif that is going to catch this state and send file to make descending order
                    return True
                elif responseCode == 401:
                    print('Status code is 401. Invalid authentication credentials.')
                    return False
                else:
                    print('The status code is ' + str(e))
                break

def mainProcess():
    currPage = 1 # page counting starts from 1
    maxPage = 0 # we will update this number after the first query
    pageMemory = [] # keep the truck which page we tried to call 
    isGoodState = True # introducng the boolean isGoodState that means we can progress

    # check if didn't finish previous load
    if maxPage == 0 and len(pageMemory) == 0:
        checkPrevSessionInterrupted(pageMemory)

    # going through all the pages in our query
    while maxPage == 0 or currPage < maxPage:
        currPage = getPageNumber(currPage, maxPage, pageMemory)
        if currPage == -1:
            break
        # response from the API in bytes
        responseByte = formTheCall(currPage)
        # checking if it is a valid response
        isGoodState = analyseTheResponse(responseByte, maxPage, currPage, pageMemory)
        
        if not isGoodState:
            break # if there is a serious issues we won't continue to call the API
        
        response = json.loads(responseByte.decode("utf-8"))

        # checking that we recieved a valid json
        if response['response']['status'] == 'ok':
            # if it is the first call we would like to know how many pages are there
            if maxPage == 0:
                maxPage = response['response']['pages']
                if maxPage > 3800:
                    maxPage = 3800 # the API has limit, it will proccess pages till 3800
            
                # after we have the max amount of pages we can fill our pageMemory with false for each page that we haven't visit yet
                for i in range(len(pageMemory), maxPage + 2):
                    pageMemory.append(False)
    
            jsonToCsv(response['response'], pageMemory, currPage)
        else:
            fillState(False, currPage, pageMemory) # if somethng wrong with json we will add currPage into errors file

    # we went through all pages, it is the time to check if we had errors with some pages
    if isGoodState:
        runThroughErrors(pageMemory)
        # running through errors once. Can't decide what to do if there is still errors. I can offer one option to inform the user
        # that we still have errors. We need some support from the human side
        # at the moment we will continue to process the file
        workWithCsv()

# takes number of the page and calls connectToApi with parameters, returns response from the API (bytes or boolean)
def formTheCall(page):
    apiAddress = 'https://content.guardianapis.com/search?page='
    apiKey = 'deleted to keep privacy'
    filterWithOr = ['elections', 'brexit']
    currPage = 1 # to test on 0 we can receve a code 400, page has to be > 0
    maxPage = 0 # we will update this number after the first query
    pageMemory = []
    
    # it is possible to play here with AND and OR
    params = '&q=' if len(filterWithOr) != 0 else ''
    for i in range(0, len(filterWithOr)):
        params += filterWithOr[i]
        if i != len(filterWithOr) - 1:
            params += '%20OR%20' 
    params += '&api-key='

    responseByte = connectToApi(apiAddress, page, params, apiKey)

    return responseByte

# depends on the response from the API we will change boolean isGoodState, that shows should we run the script or stop it
def analyseTheResponse(responseByte, maxPage, currPage, pageMemory):
    if responseByte == False or (responseByte == None and maxPage == 0):
        print('We are stopping here, if we can\'t even start. Please, fix the connection.')
        return False
    elif responseByte == True:
        # sending file directly to make the order and generate a new file with aggregation
        workWithCsv()
        return False
    elif responseByte == None:
        fillState(False, currPage, pageMemory)
        return True
    else:
        return True

def checkPrevSessionInterrupted(pageMemory):
    # for iteration through pages we are gong to use an array, that shows if we processed the page or not
    # in case when process was interrupted we will come in the state when we don't have data in array and we have data in the files
    # we will fill the data in array and will proceed from the next page that is not in success and errors 
    if not os.path.exists('success_load.txt'):
        with open('success_load.txt', 'a') as file:
            pass

    if not os.path.exists('error_load.txt'):
        with open('error_load.txt', 'a') as file:
            pass

    if os.path.getsize('success_load.txt') > 0 or os.path.getsize('error_load.txt') > 0:
        # that means we have been interrupted during the process and now we are going to proceed from the break point
        # we are gong to fill pageMemory with the pages that we already processed in prev.time
        pageMemory.append(True) # appending true for page 0, which doesn't exist
        if os.path.getsize('success_load.txt') > 0:
            with open('success_load.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    nextTrue = int(line.strip())
                    while len(pageMemory) <= nextTrue:
                        pageMemory.append(False)
                    pageMemory[nextTrue] = True

        if os.path.getsize('error_load.txt') > 0:
            with open('error_load.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    nextTrue = int(line.strip())
                    while len(pageMemory) <= nextTrue:
                        pageMemory.append(False)
                    pageMemory[nextTrue] = True

def getPageNumber(currPage, maxPage, pageMemory):
    if len(pageMemory) == 0: # it is a first run when we don't know maxPage yet
        return currPage
    elif len(pageMemory) > 0 and maxPage == 0: # when we returned back to the broken session
        for i in range(0, len(pageMemory)):
            if pageMemory[i] == False:
                return i
            if i == len(pageMemory) - 1:
                return i + 1
    else:
        while currPage < len(pageMemory) - 1 and pageMemory[currPage] == True: # normal way of looking for the number page
            currPage += 1
        if pageMemory[currPage] == True: # the situation then we loaded all the pages
            return -1
        else:
            return currPage

# basic state managment is implemented here. Keeping the pages that we went through in array and files (files will be used if the load was interrupted)
def fillState(isOkay, page, pageMemory):
    # firstly, we are are going to change the state
    pageMemory[page] = True
    if isOkay:
        with open('success_load.txt', 'a') as file:
            file.write(str(page) + '\n')
    else:
        with open('error_load.txt', 'a') as file:
            file.write(str(page) + '\n')

# transformation from json to csv, appending new lines in the file result.csv
def jsonToCsv(response, pageMemory, page):

    fillState(response['status'] == 'ok', page, pageMemory)

    if response['status'] == 'ok':
        jsonRes = response['results']
        # Check if the CSV file already exists
        fileExists = os.path.exists('result.csv')

        with open('result.csv', 'a', newline='', encoding='utf-8') as dataFile:
            csvWriter = csv.writer(dataFile)
            for line in jsonRes:
                # If the file doesn't exist, write headers
                if not fileExists:
                    header = line.keys()  
                    csvWriter.writerow(header)
                    fileExists = True

                csvWriter.writerow(line.values())

# when we went through all the pages, we are checking if there were errors. If error_load is not empty we will run ths function once.
# it will load only the pages from the file
def runThroughErrors(pageMemory):
    if os.path.exists('error_load.txt') and os.path.getsize('error_load.txt') > 0:
        with open('error_load.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                page = int(line.strip())
                responseByte = formTheCall(page)

                if responseByte != True and responseByte != False and responseByte != None:
                    response = json.loads(responseByte.decode("utf-8"))

                    if response['response']['status'] == 'ok':
                        jsonToCsv(response['response'], pageMemory, page)

# creating to new files one is a sorted file and another file with aggregation info
def workWithCsv():

    # sorting csv
    dataFrame = pd.read_csv('result.csv')
    
    dataFrame['webPublicationDate'] = pd.to_datetime(dataFrame['webPublicationDate'], infer_datetime_format = True)
    dataFrame.sort_values(by = 'webPublicationDate', ascending = False, inplace = True)
    dataFrame.to_csv('result_sorted.csv', index=False)

    # dataFrame['webPublicationDate'] = pd.to_datetime(dataFrame['webPublicationDate'])
    dataFrame['year_month'] = dataFrame['webPublicationDate'].dt.to_period('M')
    grouped = dataFrame.groupby(['pillarName', 'year_month']).size().reset_index(name='article_count')
    pivotTable = grouped.pivot(index='year_month', columns='pillarName', values='article_count').fillna(0)
    pivotTable.to_csv('aggregation_pillarname.csv')

if __name__ == "__main__":
    mainProcess()
