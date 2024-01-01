import http.client
import json
from typing import List
import matplotlib.pyplot as plt
import streamlit as st
def manual_new(labels_list, convo_list):
    
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "labels_list": labels_list,
        "conversation_list": convo_list
      }
    }
    )
    headers = {
        'accept' : 'application/json',
      'X-API-Key': st.secrets["manual_new_xapi_key"],
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))["data"]["app_output"]["dictionary_of_labels"]


# Reasoning app for automatic

def automatic_with_reasoning(conversation: List):
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "text": f"{conversation}"
      }
    }
    )
    headers = {
        'accept' : 'application/json',
      'X-API-Key': '604qxcVVt81n7pHgGL1wISMEiShBXXxo',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    output1 = data.decode("utf-8")
    output2 = json.loads(output1)
    output3 = output2["data"]
    output4 = output3["app_output"]
    return output4

def talk_with_data(query, convo_list):
    
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "user_query": query,
        "conversation_list": convo_list
      }
    }
    )
    headers = {
        'accept' : 'application/json',
      'X-API-Key': st.secrets["talk_with_data_xapi_key"],
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    output = json.loads(data.decode("utf-8"))["data"]["app_output"]
    return output

def query_new_for_each_conversation(query1, convo_list):
    
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "query": query1,
        "conversation_list": convo_list
      }
    }
    )
    headers = {
        'accept' : 'application/json',
      'X-API-Key': 'IEdYvcPJmt5moRZFsDsDcHliTfGKwyQp',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    output1 = json.loads(data.decode("utf-8"))["data"]["app_output"]
    return output1


# def manual_label_citation(conversation_list, labels_list):
    
#     conn = http.client.HTTPConnection("34.147.4.82")
#     payload = json.dumps({
#       "data": {
#         "convo": conversation_list,
#         "labels": labels_list
#       }
#     }
#     )
#     headers = {
#         'accept' : 'application/json',
#       'X-API-Key': '6CqMfz20ao9AdGifhxkH0QL2U09R0cyQ',
#       'Content-Type': 'application/json'
#     }
#     conn.request("POST", "/conversation", payload, headers)

#     res = conn.getresponse()
#     data = res.read()
#     output1 = data.decode("utf-8")
#     output2 = json.loads(output1)
#     output3 = output2["data"]
#     output4 = output3["app_output"]
#     return output4


def create_top_labels(labels_list,conversation_list):
    
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "labels_list": labels_list,
        "conversation_list": conversation_list
      }
    }
    )
    headers = {
        'accept' : 'application/json',
      'X-API-Key': 'KHILvh8M5GE6atPXEzDxN1pRBmUEeyFQ',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    # return data.decode("utf-8")
    output1 = data.decode("utf-8")
    output2 = json.loads(output1)
    output3 = output2["data"]
    output4 = output3["app_output"]['labels']
    return output4


def create_top_ten_labels(labels_list):
    
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "label_list": labels_list,
      }
    }
    )
    headers = {
        'accept' : 'application/json',
      'X-API-Key': 'CdgswDj1W17ftPFDKY7zv2xEFKM2OGVy',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    # return data.decode("utf-8")
    output1 = data.decode("utf-8")
    output2 = json.loads(output1)
    output3 = output2["data"]
    output4 = output3["app_output"]['labels']
    return output4


def query_answer_summarizer(convo_list):
    
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "query_answer": convo_list
      }
    }
    )
    headers = {
        'accept' : 'application/json',
      'X-API-Key': 'c1QREfu6DpczYyFhzYiXmTzIP6e7wvlq',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    output = json.loads(data.decode("utf-8"))["data"]["app_output"]["summary"]
    return output