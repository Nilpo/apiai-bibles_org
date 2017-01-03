
import requests


class BiblesAPI(object):
    
    _BIBLES_API_KEY = ""
    _API_URL = "https://bibles.org/v2/"
    _BIBLE_VERSION = "ESV"
    _LANGUAGE = "eng"
    
    
    def __init__(self,api_key,bible_version="ESV"):
        self._BIBLES_API_KEY = api_key;
        self._BIBLE_VERSION = bible_version;
        print ("Bibles API Key",self._BIBLES_API_KEY)
        
    def doRequest(self,url,payload={}):
        #payload = {'key1': 'value1', 'key2': 'value2'}
        
        r = requests.get(url, params=payload, auth=(self.BIBLES_API_KEY, 'pass'))
        #r.raise_for_status()
        if reqFormat == "json":
            return r.json()

        return r.text
        
    def verses(self,book_id,chapter_number):
        #GET /chapters/#{version_id}:#{book_id}.#{chapter_number}/verses.js?include_marginalia=true
        #https://bibles.org/v2/chapters/eng-KJVA:1Cor.2/verses.js
        url = self._BIBLES_API_KEY+"chapters/eng-"+self._BIBLE_VERSION+":"+book_id+"."+str(chapter_number)+"/verses.js"
        return self.doRequest(url)
        
    def passages(self,book_name,chapter_number,start_verse,end_verse=None):
        # GET /passages.xml?q[]=#{passage_specifier_list}
        # GET /passages.xml?q[]=#{passage_specifier_list}&version=#{version_id_list}
        # GET /passages.xml?q[]=#{passage_specifier_list}&version=#{version_id_list}&include_marginalia=true
        #The passage specifier is in the form "Book+chapters:verses". Multiple specifiers can be included in a comma-separated list. 
        #Examples: "John+3", "John+3-5", "John+3:12", "John+3:12-15", "John+3,Luke+2".
        q = book_name+"+"+str(chapter_number)+":"+str(start_verse)
        if(end_verse):
            q += "-"+str(end_verse)
            
        url = self._BIBLES_API_KEY+"passages.js" #+":"+book_id+"."+chapter_number+"/verses.js"
        
        paylod = {"version":self._LANGUAGE+"-"+self._BIBLE_VERSION,
            "include_marginalia":True,
            "q[]":q
        }
        print ("Get Passage",url,paylod)
        return self.doRequest(url,paylod)