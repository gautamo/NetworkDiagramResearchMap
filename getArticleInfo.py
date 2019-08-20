import bs4 as bs
import urllib.request
import urllib
import re
from time import sleep
import nltk
import heapq
from textSummarizer import create_summary

#get token from proxycrawl.com, make a free account
token = ''

##################################################

#takes topic as input, returns article urls from sciencedirect.com related to topic.
def getArticlesFromSearch(topic, author="", year=2019, show=25, sort="date"):
    global token

    #replaces space characters with %20 used in URLs
    topic = urllib.parse.quote(topic)
    author = urllib.parse.quote(author)

    #scinecedirect.com URL with correct queries
    url = f'https://www.sciencedirect.com/search/advanced?qs={topic}&date={year}&authors={author}&articleTypes=FLA&show={show}&sortBy={sort}'
    print(url)

    #open URL via proxycrawl so we aren't mistaken as a bot (otherwise you'll get 403 Forbidden Errors)
    crawlerurl = urllib.parse.quote_plus(url)
    print(crawlerurl)
    handler = urllib.request.urlopen(f'https://api.proxycrawl.com/?token={token}&url=' + crawlerurl)

    #beautifulsoup object
    soup = bs.BeautifulSoup(handler, 'lxml', from_encoding=handler.info().get_param('charset'))

    #stores intermediate links found
    linklist = []
    for link in soup.find_all('a', href=True):
        linklist.append(link['href'])

    print(linklist)

    #filters for specific article type and turns relative URL to absolute URL
    articlelist = [i for i in linklist if i.startswith('/science/article')]
    articlelist = ['https://www.sciencedirect.com{0}'.format(i) for i in articlelist]

    print(f'Found {len(articlelist)} Articles: {articlelist}')

    return articlelist

##################################################

#takes article URL as input, returns title, description, keyword, authors, location, emails
def getArticleInfo(articleurl):
    global token

    #try statement used to avoid errors
    try:

        # open URL via proxycrawl so we aren't mistaken as a bot (otherwise you'll get 403 Forbidden Errors)
        crawlerurl = urllib.parse.quote_plus(articleurl)
        handler = urllib.request.urlopen(f'https://api.proxycrawl.com/?token={token}&url=' + crawlerurl)

        # beautifulsoup object
        soup = bs.BeautifulSoup(handler, 'lxml', from_encoding=handler.info().get_param('charset'))

        # get meta description
        metadesc = soup.find("meta", property="og:description")
        metadesc = metadesc["content"].rsplit(' ',1)[0]

        # get title without science direct branding
        title = soup.find('title').text
        title = title.replace('- ScienceDirect', '').replace('- Science Direct', '')

        #get first and last name
        firstnamehtml = soup.findAll('span', {'class': 'text given-name'})
        lastnamehtml = soup.findAll('span', {'class': 'text surname'})

        firstname = [x.text for x in firstnamehtml]
        lastname = [x.text for x in lastnamehtml]
        names = list(zip(firstname, lastname))

        #get article keywords
        keyword = soup.findAll('div', {'class': 'keyword'})
        keyword = [x.text for x in keyword]

        #location and emails are found in script object
        script = soup.body.script
        #print(script)

        alt = f'{script}'
        qu = alt.split("{")

        #search for city, country, email
        que1 = str([s for s in qu if "city" in s])
        que2 = str([s for s in qu if "country" in s])
        que3 = str([s for s in qu if "email" in s])
        que4 = str([s for s in qu if metadesc in s])


        #parse using regex, get email
        precity = re.findall(r"\"_\":\"(.*?)\"", que1)
        precountry = re.findall(r"\"_\":\"(.*?)\"", que2)
        email = re.findall(r"\"_\":\"(.*?)\"", que3)
        description = re.findall(r"\"_\":\"(.*?)\"", que4)

        #get location
        city = precity[0:int(len(precity) / 2)]
        country = precountry[0:int(len(precountry) / 2)]
        location = list(zip(city, country))

        #if can't find desc, use meta desc
        if description == []:
            description = [metadesc]

        #summarize the description with max of x sentences
        description = create_summary(description[0],3)

        print(f'Title: {title}')
        print(f'Description: {description}')
        print(f'{len(keyword)} Keywords: {keyword}')
        print(f'{len(names)} Names: {names}')
        print(f'{len(location)} Locations: {location}')
        print(f'{len(email)} Emails: {email}')

        return [title, description, keyword, names, location, email]

    except Exception as e:
        return 0

def post_to_vr(url, data):
    data = data.encode() #turn to bytes
    req = urllib.request.Request(url, data=data) #send request
    response = urllib.request.urlopen(req) #receive response
    return response.read()

if __name__ == "__main__":
    #URL to send POST request to
    DLGURL = ''

    #uncomment to use
    #match = getArticlesFromSearch("quantum computing")

    #here for convenience (same urls from above match)
    match = ['https://www.sciencedirect.com/science/article/pii/S0957417419305226', 'https://www.sciencedirect.com/science/article/pii/S0377042719302547', 'https://www.sciencedirect.com/science/article/pii/S0304885319310753', 'https://www.sciencedirect.com/science/article/pii/S0022286019309810', 'https://www.sciencedirect.com/science/article/pii/S0957417419304658', 'https://www.sciencedirect.com/science/article/pii/S0304885319318323', 'https://www.sciencedirect.com/science/article/pii/S0096300319305685', 'https://www.sciencedirect.com/science/article/pii/S0022286019309238', 'https://www.sciencedirect.com/science/article/pii/S0167278919301289', 'https://www.sciencedirect.com/science/article/pii/S1385894719315657', 'https://www.sciencedirect.com/science/article/pii/S1385894719315086', 'https://www.sciencedirect.com/science/article/pii/S0022286019309573', 'https://www.sciencedirect.com/science/article/pii/S0022286019309494', 'https://www.sciencedirect.com/science/article/pii/S0022286019309858', 'https://www.sciencedirect.com/science/article/pii/S0304389419307988', 'https://www.sciencedirect.com/science/article/pii/S0096300319306083', 'https://www.sciencedirect.com/science/article/pii/S138614251930678X', 'https://www.sciencedirect.com/science/article/pii/S002228601930897X', 'https://www.sciencedirect.com/science/article/pii/S0022286019308208', 'https://www.sciencedirect.com/science/article/pii/S0022286019309111', 'https://www.sciencedirect.com/science/article/pii/S1386142519307024', 'https://www.sciencedirect.com/science/article/pii/S0022286019308592', 'https://www.sciencedirect.com/science/article/pii/S1386142519307188', 'https://www.sciencedirect.com/science/article/pii/S0022286019309044', 'https://www.sciencedirect.com/science/article/pii/S0022286019309329']

    #number of articles to parse
    numArticles = 1

    infoFound = []
    count = 0
    while count < numArticles:
        print(f'\nArticle: {count+1}/{numArticles}')
        ans = getArticleInfo(match[count])
        if ans == 0:
            print(f'Error on article {count+1}. Retrying.')
        else:
            infoFound.append(ans)
            count+=1
        sleep(5)

    print(f'\nAll Info: {infoFound}')

    post_to_vr(DLGURL, str(infoFound))





