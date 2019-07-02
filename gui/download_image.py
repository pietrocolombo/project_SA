import os
import urllib
#import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from random import randint
import re

#this function will create a soup and retuens which is the parsed html format for extracting html tags of the webpage
def makeSoup(url):
    #This will load the webpage for the given url
    #page = requests.get(url) 
    #this BeautifulSoup below will parse the html file
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page=urlopen(req).read()

    soup = BeautifulSoup(page, "html5lib")
    return soup


#This function will be called every new keyword line is encountered and will start scraping the amazon web page of the search result according to the text mention in the keywords text file
def perfromScraping(urlReceived, product_id):
    breaki = 1
    breakPointNumber = 1
    url = urlReceived
    soup = makeSoup(url)
    print('entrati')
    i = 1
    title = soup.findAll(id = 'productTitle')
    print(title)
    title_str = ''
    #if title:
    #    print('entrato nel primo')
    #    tag = re.findall('>[^<]*<', str(title))
    #    title_str = tag[0]
    #    title_str = title_str.replace('\n', '')
    #    title_str = title_str[1:-1]
    #    title_str = title_str.strip()
    #if not soup.findAll('img', alt = title_str):
    #    print('entrato nel secondo')
    #    title = soup.findAll(meta = 'title')
    #    print(title)
    #    title_str = title.get('title')
    
    titolo = soup.findAll('title')
    print(len(titolo))
    title_arr = re.split(':',str(titolo[0]))
    print(title_arr)
    title_str = title_arr[1]
    title_str = title_str.strip()

    print(title_str)
    for image in soup.findAll('img', alt = title_str):
        if(breaki <= breakPointNumber): #This statement checks the number of images that were restricted to which were supposed to be downloaded
            #print(image)
            #print("Image number ", i ," : \n", image.get('src'), "\n")
            nameOfFile = product_id# + str(i)
            i = i+1
            
            img = image.get('src')
            print(img)
            tempCheck = img.split('.')
            check = str(tempCheck[len(tempCheck) - 1])
            ImageType = ".jpeg"
            if (check == "jpg" or check == "jpeg" or check == "png"):

                if check == "jpg" or check == "jpeg":
                    ImageType = ".jpeg"
                    if check == "jpg":
                        img = re.sub("[0-9]+_.jpg$", "600_.jpg", img)
                    else:
                        img = re.sub("[0-9]+_.jpeg$", "600_.jpeg", img)
                else:
                    ImageType = ".png"
                    img = re.sub("[0-9]+_.png$", "600_.png", img)

                filename = nameOfFile
                folderIndividualName = "AmazonImages/" #Creates the path where the images will be stored
                #Create The folder according to search name
                if not os.path.exists(folderIndividualName):
                    os.makedirs(folderIndividualName)
                imageFile = open(folderIndividualName + filename + ImageType, 'wb')
                imageFile.write(urllib.request.urlopen(img).read()) #This will read the image file from the link and download it and save it in the folder mentioned all at the same time
                imageFile.close()
                breaki = breaki + 1
