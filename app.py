#!/usr/bin/env python

import urllib, json, os, re, random

from flask import Flask
from flask import request
from flask import make_response
from flask import Markup
from bibles_apy import BiblesAPI

# Flask app should start in global layout
app = Flask(__name__)

@app.route("/",methods=['GET'])
def main():
    
    iframe = '<iframe width="350" height="430" src="https://console.api.ai/api-client/demo/embedded/thebible"></iframe>'
    return make_response('<!DOCTYPE html><html><head><title>The Bible</title></head><body>'+iframe+'</body></html>')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    try:
        bibleapi = BiblesAPI(os.getenv("BIBLES_API_KEY",""))
        apiai_result = req.get("result")
        apiai_parameters = apiai_result.get("parameters")
        
        bible_version = apiai_parameters.get("bible-version","ESV").upper()
        if(bible_version):
            bibleapi.bible_version = bible_version
        #print(apiai_result)
        apiai_action = apiai_result.get("action")
        if(apiai_action == "lookup.votd"):
            data = bibleapi.votd()
            return makeVOTDResult(data, bible_version)
        
        #print(apiai_parameters)
        search_phrase = apiai_parameters.get("search-phrase")
        if(search_phrase):
            data = bibleapi.search(search_phrase)
            return makeSearchResult(data)
            
        book_name = apiai_parameters.get("bible-book")
        print(book_name,type(book_name))
        book_number = apiai_parameters.get("book-number")
        print(book_number)
        chapter = apiai_parameters.get("chapter")
        print(chapter)
        start_verse = apiai_parameters.get("start-verse")
        print(start_verse)
        end_verse = apiai_parameters.get("end-verse")
        print(end_verse)
    
        if(not book_name):
            resolvedQuery = apiai_result.get("resolvedQuery")
            #for now lets assume 2nd
            queryParts = resolvedQuery.split(" ")
            print(queryParts)
            if(len(queryParts) > 2):
                book_name = queryParts[1]
                print(book_name)
            else:
                return makeDefaultResponse()
        if(not chapter):
            return makeDefaultResponse()
        if(not start_verse):
            start_verse = 1
    
        data = bibleapi.passages(str(book_number)+book_name,chapter,start_verse,end_verse)
    
        res = makeWebhookResult(data)
        return res
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("ERROR!",e)
        print("FINISHED TASKS")
        return makeDefaultResponse()




def makeSearchResult(data):
    response = data.get('response')
    #print(response)
    if response is None:
        return makeDefaultResponse()

    search = response.get('search')
    #print(search)
    if search is None:
        return makeDefaultResponse()
        
    result = search.get('result')
    #print(result)
    if result is None:
        return makeDefaultResponse()
    
    summary = result.get("summary")
    total = summary.get("total",0)
    
    verses = result.get("verses",[])
    #if(not verses):
    #    return makeDefaultResponse("Hmmm. I cannot seem to find any verses.")
    
    speech = "Found "+str(total)
    if(total != 1):
        speech += " verses. "
    else:
        speech += " verse. "
    
    if(total > 3):
        verses = random.sample(verses, 3)
        speech += "Reading three of them. "
    
    for v in verses:
        speech += v['reference']+" "
        speech += cleanPassage(v['text'])+" "
    
        
    print("Response:",speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-bibles_org"
    }
    
    
def makeWebhookResult(data):
    #print("bible result",data)
    # body = data.get('body')
#     if body is None:
#         return {}

    response = data.get('response')
    #print(response)
    if response is None:
        return makeDefaultResponse()

    search = response.get('search')
    #print(search)
    if search is None:
        return makeDefaultResponse()
        
    result = search.get('result')
    #print(result)
    if result is None:
        return makeDefaultResponse() 
    
    passages = result.get('passages')
    #print(passages)
    if (not passages or len(passages) == 0):
        return makeDefaultResponse()
    
    passage = passages[0]

    #passage_html = passage.get('text')
    #passage_html = passage_html.encode('ascii', 'ignore').decode('ascii')
    passage_txt = cleanPassage(passage.get('text'))#Markup(passage_html).striptags()
    print(passage_txt) #.encode('ascii', 'ignore').decode('ascii')
    if (passage_txt is None):
        return makeDefaultResponse()

    # print(json.dumps(item, indent=4))

    speech = passage_txt

    print("Response:",speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-bibles_org"
    }

def makeVOTDResult(data, version):
    if(len(data) == 0):
        return makeDefaultResponse("Apologies could not find verse of the day.")
    #data is an array: {bookname,chapter,verse, text }
    speech = "The Verse of the day is "
    ref = data[0]['bookname']+" "+str(data[0]['chapter'])+":"+str(data[0]['verse'])
    if(len(data) > 1):
        ref += "-"+str(data[len(data)-1]['verse'])
    
    speech += ref+".\n\n"+'"'
    for i,d in enumerate(data):
        if(i > 0):
            speech += str(d['verse'])+" "
        speech += d['text']+'" '+version
        
    return makeDefaultResponse(speech)
        

def cleanPassage(passage_raw):
    passage_html = passage_raw.encode('ascii', 'ignore').decode('ascii')
    #remove the heading
    #print passage_html
    heading_regex = r'<h3.*?>.*?</h3>'
    passage_html = re.sub(heading_regex,"",passage_html,1)
    #print passage_html
    #remove first vers number 
    verse_num_regex = r'<sup.*?>\d+</sup>'
    passage_html = re.sub(verse_num_regex,"",passage_html,1)
    #print passage_html
    passage_txt = Markup(passage_html).striptags()
    return passage_txt

def makeDefaultResponse(other_resp=None):
    if(not other_resp):
        other_resp = "I didn't understand. You can say read John chapter 3 verse 16"
    
    try:
        print(other_resp.encode("utf-8"))
    except:
        print(other_resp)
    return {
        "speech": other_resp,
        "displayText": other_resp,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-bibles_org"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
