'''
Author: Yixiang Wang Email: yixiang.wang@yale.edu Wechat: tsinghuawyx
version: .02	Date: 04/12/2018
WARNING: THIS IS NOT AN APP FOR COMMERCIAL USE
'''
from bs4 import BeautifulSoup
import urllib
from urllib import request, error
from datetime import datetime
import csv
import time
import os
import random

def iterGet(inputBox):
    '''
    	Get the stripped text from a list of class 'bs4.element.Tag'
    	This function is not used in current version (for potential future application)
    
    	Inputs:
    		inputBox 			A list of class 'bs4.element.Tag'
    	Outputs:
    		boxData				A list of plain texts extracted from the inputBox
    '''
    boxData = []
    for item in inputBox:
        boxData.append(item.text.strip())
    print(len(boxData))
    return boxData



def pullOutInfo(inputList):
    '''
    	Pull out information from specific tags (housing, hdr(title text), price, hood, posted time, hdrlink)
    
    	Inputs:
    		inputList			<class 'bs4.element.ResultSet'>
    	Outputs:
    		curData				a list of tuples that store the text info from specific tags 
    '''
	
    housing = []
    hdrtitle = []
    price =[]
    hood = []
    time = []
    hdrlnk = []
    curData = []
	
    for element in inputList:
        try:
            housing_box = element.find_next('span', attrs={'class': 'housing'}) #not a direct child, use find_next()
            housing = "".join(housing_box.text.split())
        except:
            housing = 'Not posted'

        try:
            hdrtitle_box = element.find('a', attrs={'class': 'result-title hdrlnk'})
            hdrtitle = hdrtitle_box.text.strip()
        except:
            hdrtitle = 'Not posted'

        try:
            price_box = element.find('span', attrs={'class': 'result-price'})
            price = price_box.text.strip()
        except:
            price = 'Not posted'

        try:
            hood_box = element.find_next('span', attrs={'class': 'result-hood'})
            hood_box.text.strip()
        except:
            hood = 'Not posted'

        try:
            time_box = element.find('time', attrs={'class': 'result-date'})
            time = time_box.text.strip()
        except:
            time = 'Not posted'

        try:
            hdrlnk_box = element.find('a')['href']
            hdrlnk = hdrlnk_box
        except:
            hdrlnk = 'Not posted'
        
        curData.append((housing,hdrtitle,price,hood,time,hdrlnk))
        
        return curData



def getFilename():
    '''
    	This function is to pull out the date info and return the .csv filename
    '''
    todayStr = str(datetime.today())
    filename = todayStr + '.csv'
    filenameList = list(filename)
    flag = True
    while flag:
        try:
            filenameList.remove(':')
        except:
            flag = False
            filename = ''.join(filenameList)
    
    filename = filename[0:10] + '.csv'
    return filename



def outputCSV(data):
    '''
    	This function is to output the csv file
    '''

    with open(getFilename(), 'w', encoding = 'utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # The for loop
        for i in range(len(data)):
            #print(name,price)
            writer.writerow(data[i])



def findNext(web_base,soup):
    '''
    	This function is to find the hyperlink pointing to the next page
    
    	Inputs:
    		web_base			A base string shared by all hyperlinks
    		soup 				soup data of the current page
    
    	Outputs:
    		next 				URL of the next page
    		flag 				A flag indicate whether it is the last page
    '''	
    flag = True
    next = []
    try:
        next_box = soup.find('a', attrs={'title': 'next page'})['href']
        next = web_base + next_box
    except TypeError:
        flag = False
    
    return (next, flag)



def getSoup(quote_page):
    '''
    	This function is to get the soup data with current URL
    '''
    head = {}
    #Change the user-agent to a popular one. To cheat the anti-scraping mechanisms
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'

	# Not using proxy here but can be modified in the future
	#proxy = {'http':'111.155.116.239'}
	#proxy_support = request.ProxyHandler(proxy)
	#opener = request.build_opener(proxy_support)
	#opener.addheaders = [('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36')]
	#request.install_opener(opener)
	#print(soup.encode("utf-8")) 

    page_req = request.Request(quote_page, headers = head)
    page_resp = request.urlopen(page_req)
    page_resp = page_resp.read()
    soup = BeautifulSoup(page_resp,"html.parser")
	
    return soup

	

def runCrawler(quote_page):
    '''
    	Scraping the first 5 pages starting from the input page  
    '''
    data = []
    web_base = quote_page[:quote_page.find('search')-1]
	
    n = 0
    soup = getSoup(quote_page)
    time_out = time.time() + 60 #For breaking the while loop if the scraping is blocked or delayed
    
    while (findNext(web_base, soup)[1]) and (n<5): 
        soup = getSoup(findNext(web_base, soup)[0])
        li_box = soup.find_all('li', attrs={'class': 'result-row'})
		#li = iterGet(li_box)
        if (data is not None) or (n == 0):
            data.extend(pullOutInfo(li_box))
			#print(str(pullOutInfo(li_box))[:100])

        time.sleep(1 + random.random()) # Randomize sleep time for the next run
        n += 1
        print(str(n))

		#For breaking the while loop if the scraping is blocked or delayed
        if time.time() > time_out:
            print("Session time out")
            break

    if data is not None:			
        outputCSV(data)





'''
Main function
'''		
print("Author: Yixiang_Wang   Versioin:.02   Email:yixiang.wang@yale.edu   Wechat ID: tsinghuawyx")
print("FOR STUDY PURPOSE ONLY. NOT FOR COMMERCIAL USE") 
print("\n")
#quote_page = 'https://newhaven.craigslist.org/search/apa?min_price=1200&max_price=1700&min_bedrooms=2&max_bedrooms=3&min_bathrooms=1&max_bathrooms=2&availabilityMode=0&sale_date=all+dates'
try:
	# Store the url that the user input at the first time as the default url
	if os.path.isfile("Default_URL.txt"):
		file = open('Default_URL.txt','r')
		quote_page = file.read()
		file.close()
		renewFlag = input("Renew URL? (Y/N):\n")
		if (renewFlag == 'Y') or (renewFlag == 'y'):
			os.remove('Default_URL.txt')
			quote_page = input('Please paste the URL here:\n')
			with open('Default_URL.txt','w') as f:
				f.write(quote_page)
				f.close()
		else:
			print("Continue with default URL \n")
	else:
		quote_page = input('Please paste the URL here:\n')
		with open('Default_URL.txt','w') as f:
			f.write(quote_page)
			f.close()
    
    #Specify update frequency
	cycleLength = int(input('Update every ? minutes:\n'))
	print("Program is running...")
except ValueError:
	print("Something wrong with the input, retry please...\n")

# Keep updating if the program is on
while True:
	try:
		runCrawler(quote_page)
	except urllib.error.HTTPError as err:
		if err.code == 403:
			print("Shoot! Seems that we are blocked by the website...How dare they...Sorry but you have to restart your modem and wait 24h until the IP address is renewed :)")
			os.remove('Default_URL.txt')
			#os.remove(getFilename())
	
	except ConnectionResetError:
		print("Emmm...The host forcibly end the request, the program will wait 30mins then try again")
		time.sleep(1800)

	except:
		print("Something wrong, could be an invalid URL input. Please exit and restart with (renew) a correct URL")
		os.remove('Default_URL.txt')
		#os.remove(getFilename())

	print('Successfully scrape 5 pages at ' + str(datetime.today()))
	# Randomize sleep time for the next run. Roughly keep the frequency specified by the user
	x = random.randint(1,10) + random.random()
	time.sleep(cycleLength*60 + x)	



