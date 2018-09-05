from bs4 import BeautifulSoup
from XPathGettingWithBS import getBsObjectWithSelenium
from XPathGettingWithBS import xpathToBSObj
from XPathGettingWithBS import AbsolutePathForXpath

"""
*****************************************************************************************************************

		The reason for adding custom exceptions instead of using the already built ones is that every exception here
	regroup multiple exceptions. for example opening the driver, accessing the url, taking the source code 
	and using it for preparing a beautifulSoup object is called AccessingWebsiteError
	
*****************************************************************************************************************
"""

class Error(Exception):
	"""Base class for other exceptions"""
	pass

class AccessingWebsiteError(Error):
	"""Raised when the system is enable to get the bsobject from the url"""
	pass

class ProductXPATHError(Error):
	"""Raised when the data xpath given cannot be accessed"""
	pass
   
class ValueXPATHError(Error):
	"""Raised when the value xpath given cannot be accessed"""
	pass

class ExtractionAlgorithmError(Error): # effectively those errors are system related!
	"""Raised when the algorithm fails to identify the siblings of the given tags, to identify some unkown tags, 
	to make the absolute xpath of a relative xpath or to manipulate correctly the found tags"""
	pass

def CoordinateOfLastSimilarity(xpath1, xpath2):
	minLength = min(len(xpath1),len(xpath2))
	lastSimilarityPos =0
	preLastSimilarityPos =0
	for i in range(0,minLength):
		if(xpath1[i] == xpath2[i]):
			if(xpath1[i]== '/'):
				preLastSimilarityPos = lastSimilarityPos
				lastSimilarityPos=i
		else:
			return(preLastSimilarityPos, lastSimilarityPos)
	return preLastSimilarityPos,lastSimilarityPos
	
def getListOfUnclesXpaths(xpath1,xpath2,bsObj,preLastSimilarityPos,lastSimilarityPos):
	# = CoordinateOfLastSimilarity(xpath1,xpath2)
	parentTag = xpath1[preLastSimilarityPos+1:lastSimilarityPos] #parent tag mean here the first tag commune to both xpaths
	bracketPos = parentTag.find('[')
	if( bracketPos != -1):
		parentTag= parentTag[:bracketPos]
	print(parentTag)
	grandParentXpath = xpath1[:preLastSimilarityPos]
	print(grandParentXpath)
	grandParentbsObj = xpathToBSObj(grandParentXpath,bsObj)
	numberOfUncles =len(list(grandParentbsObj.findAll(parentTag,recursive= False))) #this will give the number of siblings of the parent tag
	print(numberOfUncles)
	listOfUnclesXpaths = []
	for i in range(numberOfUncles):
		uncleXpath= grandParentXpath + "/" + parentTag + "[" + str(i+1) + "]"
		listOfUnclesXpaths.append(uncleXpath)
	return listOfUnclesXpaths
	
def getListOfSiblingsXpaths(xpath1,xpath2,bsObj):
	preLastSimilarityPos,lastSimilarityPos = CoordinateOfLastSimilarity(xpath1,xpath2)
	listOfUnclesXpaths = getListOfUnclesXpaths(xpath1,xpath2,bsObj,preLastSimilarityPos,lastSimilarityPos)
	while(len(listOfUnclesXpaths)==1 and preLastSimilarityPos != 0):
		lastSimilarityPos = preLastSimilarityPos
		for i in range(lastSimilarityPos-1,-1,-1):
			if(xpath1[i] == '/'):
				preLastSimilarityPos = i
				break
		listOfUnclesXpaths = getListOfUnclesXpaths(xpath1,xpath2,bsObj,preLastSimilarityPos,lastSimilarityPos)
	tag1UniqueXpath = xpath1[lastSimilarityPos:]
	tag2UniqueXpath = xpath2[lastSimilarityPos:]
	listOfSiblings1Xpaths = []
	listOfSiblings2Xpaths = []
	for x in listOfUnclesXpaths:
		siblingXpath1 = x+ tag1UniqueXpath
		siblingXpath2 = x+ tag2UniqueXpath
		listOfSiblings1Xpaths.append(siblingXpath1)
		listOfSiblings2Xpaths.append(siblingXpath2)
	return(listOfSiblings1Xpaths,listOfSiblings2Xpaths)
	
def parseWebsite(url,xpath1,xpath2):
	try:
		bsObj =getBsObjectWithSelenium(url)
		if (bsObj== None):
			raise AccessingWebsiteError
	except:
		raise AccessingWebsiteError
	#add code here if you want to check the type and the availibility of the data and value 
	try:
		productSample = xpathToBSObj(xpath1,bsObj).text
	except:
		raise ProductXPATHError
	try:
		valueSample = xpathToBSObj(xpath2,bsObj).text
	except:	
		raise ValueXPATHError
	try: # the algorithm here gives up whenever there is a false sibling's XPATH. It s beneficial when the algorithm bases are not met.
		xpath1 = AbsolutePathForXpath(xpath1,bsObj)
		xpath2 = AbsolutePathForXpath(xpath2,bsObj)
		(tag1ListOfXpths ,tag2ListOfXpaths) =getListOfSiblingsXpaths(xpath1,xpath2,bsObj)
		parsingResult ={}
		for x,y in zip(tag1ListOfXpths,tag2ListOfXpaths):
			data = xpathToBSObj(x,bsObj).text
			value = xpathToBSObj(y,bsObj).text
			parsingResult[data]=value
	except:
		raise ExtractionAlgorithmError
	return parsingResult

