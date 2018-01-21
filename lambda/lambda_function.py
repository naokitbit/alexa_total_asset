# -*- coding: utf-8 -*-
from __future__ import print_function
import asset_info

"""
API Information
安全のためAPIキーの設定は取引ができないようにしておきましょう
"""
key_zaif = "**********"
secret_zaif = "**********"
info = asset_info.AssetInfo(key_zaif=key_zaif, secret_zaif=secret_zaif)

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, should_end_session):
    if should_end_session:
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'shouldEndSession': should_end_session
        }
    else:
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
                'title': title,
                'content': output
            },
            'shouldEndSession': should_end_session
        }


def build_response(speechlet_response):
    return {
        'version': '1.0',
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def handle_session_end_request():
    card_title = ""
    speech_output = ""
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, should_end_session))

def get_total_asset():
    card_title = '総資産'
    should_end_session = False
    try:
        speech_output = "現在の総資産は" + str(info.get_zaif_asset()) + "円です"
    except:
        speech_output = "チャート取得に失敗しました．リトライしますか？"
    return build_response(build_speechlet_response(
        card_title, speech_output, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_total_asset()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "TotalAsset":
        return get_total_asset()
    elif intent_name == "AMAZON.HelpIntent":
        return get_total_asset()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.NoIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.YesIntent":
        return get_total_asset()
    else:
        return get_total_asset()


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    """
    
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


