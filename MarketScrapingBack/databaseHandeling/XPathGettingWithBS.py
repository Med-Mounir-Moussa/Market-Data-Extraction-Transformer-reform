from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from selenium import webdriver
import time

pathToWebDriver = r"C:\Users\HP\Desktop\chromedriver.exe"									#variable containing the path of chrome Webdriver on my pc!
"""variable that determines how much time you estemate necessary for the javascript code to execute 
	when opening webpages. It s only necessary to put a non zero value when the page usesa lot of Ajax."""
javascriptEstimatedLoadingTime = 3		


#this function take an url then open it in the driver and wait the javascriptEstimatedLoadingTime before getting the source page
def getBsObjectWithSelenium(url): 
	try:
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		driver = webdriver.Chrome(pathToWebDriver,chrome_options=options) 					
		driver.get(url)
		time.sleep(javascriptEstimatedLoadingTime)
		pageSource = driver.page_source
		Bsobj = BeautifulSoup(pageSource)
	except:
		print ("loading the page has failed")
		return None
	return Bsobj
		
		
def getBsObject(url) :
	try :
		http = urlopen(url)
	except HTTPError as e:
		print ("couldnt load page")
		return None
	try :
			object = BeautifulSoup(http.read())
	except AttributeError as e:
			print ("sthg wrong with the page",e.message)
			return None
	return object

def is_valid_html_tag(tag_name):  
	tags=["a","abbr","acronym","address","area","b","base","bdo","big","blockquote","body","br","button","caption","cite","code","col","colgroup","dd","del","dfn","div","dl","DOCTYPE","dt","em","fieldset","form","h1","h2","h3","h4","h5","h6","head","html","hr","i","img","input","ins","kbd","label","legend","li","link","map","meta","noscript","object","ol","optgroup","option","p","param","pre","q","samp","script","select","small","span","strong","style","sub","sup","table","tbody","td","textarea","tfoot","th","thead","title","tr","tt","ul","var"]
	return tag_name in tags

def isXpathAbsolute(xpath):
	if(xpath[1] == '/'):
		return(True)
	else:
		return(False)
xpath = "/html/body/div[6]/div[1]/div[1]/table/tbody/tr[2]/td[2]" #The xpath is supposed following the rules for xpaths

def absoluteXpathParsing (xpath,Bsobj): 
	xpath= xpath[1:]
	listOfTags = xpath.split('/')
	BeautifulSoupPath='Bsobj'
	for x in listOfTags:
		pos = x.find('[')
		if( pos == -1):
			x= '.find("'+x+'",recursive=False)'
		else:
			posEnd = x.find(']')
			x=x.replace(x[pos+1:posEnd], str(int(x[pos+1:posEnd])-1))
			x= '.findAll("'+ x[:pos] + '", recursive =False)' +x[pos:]
		BeautifulSoupPath += x
	try:
		result= eval(BeautifulSoupPath)
	except:
		return None
	return result
	

def	relativeXpathParsing (xpath,Bsobj):				# the xpath in relative
	xpath= xpath[2:]
	listOfTags = xpath.split('//')
	BeautifulSoupPath='Bsobj'
	for x in listOfTags:	
		pos =x.find('[')
		if(pos != -1):
			subResult ='.find('
			possibleTag = x[:pos]
			if (is_valid_html_tag(possibleTag)):
				subResult += '"'+ possibleTag +'",{'
				
			else:
				subResult += '"",{'
			equalSignPos = x.find('=')
			endPos = x.find(']')
			subResult += '"' + x[pos+2:equalSignPos] + '":'+ x[equalSignPos+1:endPos] +'})'	
		BeautifulSoupPath+= subResult
	try:
		result= eval(BeautifulSoupPath)
	except:
		return None
	return result

def xpathToBSObj (xpath,Bsobj): #this function take an xpath and return the beautifulSoup object in that location
	if (xpath[1] != '/'): #the xpath is absolute
		result =absoluteXpathParsing(xpath,Bsobj)
	else:#the xpath is relative
		result =relativeXpathParsing(xpath,Bsobj)
	return result

def absoluteXpathFromBSObj (Bsobj): 
	parentTag = Bsobj.parent
	currentTag = Bsobj
	result = '' 
	while (parentTag != None and currentTag.name!= "html"):
		allSimilairTags = parentTag.findAll(currentTag.name,recursive= False)
		if(len(list(allSimilairTags)) >1):
			for i,x in enumerate(allSimilairTags):
				if(x== currentTag):
					currentIndex= i+1
					break
			result = '/' + currentTag.name +  '[' + str(currentIndex) + ']' +result  
		else:
			result = '/' + currentTag.name + result
		currentTag = parentTag
		parentTag = parentTag.parent
	result = '/html'+ result
	return result	

def AbsolutePathForXpath (xpath, Bsobj):
	if(isXpathAbsolute(xpath)):
		return xpath
	else:
		BsTag = xpathToBSObj(xpath,Bsobj)
		return(absoluteXpathFromBSObj(BsTag))

	
"""	
 ***************************************************************************************************************
										an example of usage of those functions
	
BsObj =getBsObjectWithSelenium("https://www.dailyfx.com/forex-rates")
result=xpathToBSObj('//*[@id="dfx-search"]',BsObj)
print("/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/table/tbody/tr[3]/td[2]/span")
print(absoluteXpathFromBSObj(result))
print(result.name)

 ***************************************************************************************************************
"""
