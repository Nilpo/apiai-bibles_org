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


    BiblesAPI(os.getenv("BIBLES_API_KEY",""))
    apiai_result = req.get("result")
    apiai_parameters = result.get("parameters")
    book_name = apiai_parameters.get("book")
    book_number = apiai_parameters.get("book-number")
    chapter = apiai_parameters.get("chapter")
    start_verse = apiai_parameters.get("start-verse")
    end_verse = apiai_parameters.get("end-verse")
    
    if( book_name is None or chapter is None):
        return {}
    if(start_verse is None):
        start_verse = 1
    
    result = BiblesAPI.passages(str(book_number)+book_name,chapter,start_verse,end_verse)
    
    res = makeWebhookResult(data)
    return res





def makeWebhookResult(data):
    body = data.get('body')
    if body is None:
        return {}

    response = body.get('response')
    if response is None:
        return {}

    search = response.get('search')
    if search is None:
        return {}
        
    result = search.get('result')
    if result is None:
        return {}  
    
    passages = result.get('result')
    if passages is None:
        return {}  
    
    passage = passages[0]

    passage_html = passage.get('text')
    passage_txt = Markup(passage_html).striptags()
    
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
