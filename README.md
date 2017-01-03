# Api.ai - Bibles.rg API in Python

This is a really simple webhook implementation that gets Api.ai classification JSON (i.e. a JSON output of Api.ai /query endpoint) and returns a fulfillment response.

More info about Api.ai webhooks could be found here:
[Api.ai Webhook](https://docs.api.ai/docs/webhook)

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What does the service do?
Read the specified Bible passage [Bibles.org API](https://bibles.org/pages/api/documentation/verses).

The service packs the result in the Api.ai webhook-compatible response JSON and returns it to Api.ai.

