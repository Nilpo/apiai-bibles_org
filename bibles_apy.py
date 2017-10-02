
import requests, os


class BiblesAPI(object):
    
    _BIBLES_API_KEY = os.environ['BIBLES_API_KEY']
    _API_URL = "https://bibles.org/v2/"
    _BIBLE_VERSION = "ESV"
    _LANGUAGE = "eng"
    
    
    def __init__(self,api_key,bible_version="ESV"):
        self._BIBLES_API_KEY = api_key;
        self._BIBLE_VERSION = bible_version;
        print ("Bibles API Key",self._BIBLES_API_KEY)
    
    @property
    def bible_version(self):
        return self._BIBLE_VERSION

    @bible_version.setter
    def bible_version(self,value):
        self._BIBLE_VERSION = value
    
    def doRequest(self,url,payload={}):
        #payload = {'key1': 'value1', 'key2': 'value2'}
        
        r = requests.get(url, params=payload, auth=(self._BIBLES_API_KEY, 'pass'))
        print (r.url,r.headers)
        #r.raise_for_status()
        return r.json()

        #return r.text
        
    def verses(self,book_id,chapter_number):
        #GET /chapters/#{version_id}:#{book_id}.#{chapter_number}/verses.js?include_marginalia=true
        #https://bibles.org/v2/chapters/eng-KJVA:1Cor.2/verses.js
        url = self._API_URL+"chapters/"+self._LANGUAGE+"-"+self._BIBLE_VERSION+":"+book_id+"."+str(chapter_number)+"/verses.js"
        payload = {"version":self._LANGUAGE+"-"+self._BIBLE_VERSION,
            "include_marginalia":True,
            #"q[]":q
        }
        return self.doRequest(url,payload)
        
    def passages(self,book_name,chapter_number,start_verse,end_verse=None):
        # GET /passages.xml?q[]=#{passage_specifier_list}
        # GET /passages.xml?q[]=#{passage_specifier_list}&version=#{version_id_list}
        # GET /passages.xml?q[]=#{passage_specifier_list}&version=#{version_id_list}&include_marginalia=true
        #The passage specifier is in the form "Book+chapters:verses". Multiple specifiers can be included in a comma-separated list. 
        #Examples: "John+3", "John+3-5", "John+3:12", "John+3:12-15", "John+3,Luke+2".
        q = book_name+"+"+str(chapter_number)+":"+str(start_verse)
        if(end_verse):
            q += "-"+str(end_verse)
            
        url = self._API_URL+"passages.js?q[]="+q #+":"+book_id+"."+chapter_number+"/verses.js"
        
        payload = {"version":self._LANGUAGE+"-"+self._BIBLE_VERSION,
            "include_marginalia":True,
            #"q[]":q
        }
        print ("Get Passage",url,payload)
        return self.doRequest(url,payload)
        
    def search(self,search_phrase):
        
        url = self._API_URL+"search.js"
        
        payload = {"version":self._LANGUAGE+"-"+self._BIBLE_VERSION,
            "include_marginalia":True,
            "query":search_phrase
        }
        print ("Get Passage",url,payload)
        return self.doRequest(url,payload)
        
    def votd(self):
        #https://labs.bible.org/api/?passage=votd&type=json&version=eng-ESV
        url = "https://labs.bible.org/api/"
        payload = {"passage":"votd","type":"json","version":"eng-ESV"}
        return self.doRequest(url,payload)
        