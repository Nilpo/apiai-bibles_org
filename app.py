#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from flask import Markup
from bibles_apy import BiblesAPI

# Flask app should start in global layout
app = Flask(__name__)


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
        #print (apiai_result)
        apiai_parameters = apiai_result.get("parameters")
        #print (apiai_parameters)
        book_name = apiai_parameters.get("book")
        print (book_name,type(book_name))
        book_number = apiai_parameters.get("book-number")
        print (book_number)
        chapter = apiai_parameters.get("chapter")
        print(chapter)
        start_verse = apiai_parameters.get("start-verse")
        print(start_verse)
        end_verse = apiai_parameters.get("end-verse")
        print (end_verse)
    
        if(not book_name):
            resolvedQuery = apiai_result.get("resolvedQuery")
            #for now lets assume 2nd
            queryParts = resolvedQuery.split(" ")
            print (queryParts)
            if(len(queryParts) > 2):
                book_name = queryParts[1]
                print (book_name)
            else:
                return {}
        if(not chapter):
            return {}
        if(not start_verse):
            start_verse = 1
    
        data = bibleapi.passages(str(book_number)+book_name,chapter,start_verse,end_verse)
    
        res = makeWebhookResult(data)
        return res
    except Exception as e:
        import traceback
        traceback.print_exc()
        print "ERROR!",e
        print "FINISHED TASKS"
        raise e





def makeWebhookResult(data):
    #print("bible result",data)
    # body = data.get('body')
#     if body is None:
#         return {}

    response = data.get('response')
    #print (response)
    if response is None:
        return {}

    search = response.get('search')
    #print (search)
    if search is None:
        return {}
        
    result = search.get('result')
    #print (result)
    if result is None:
        return {}  
    
    passages = result.get('passages')
    #print (passages)
    if passages is None:
        return {}  
    
    passage = passages[0]

    passage_html = passage.get('text')
    passage_html = passage_html.encode('ascii', 'ignore').decode('ascii')
    passage_txt = Markup(passage_html).striptags()
    print passage_txt #.encode('ascii', 'ignore').decode('ascii')
    if (passage_txt is None):
        return {}

    # print(json.dumps(item, indent=4))

    speech = passage_txt

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-bibles_org"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
