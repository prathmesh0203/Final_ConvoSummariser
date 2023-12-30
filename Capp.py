import http.client
import json
from typing import List
import matplotlib.pyplot as plt
import streamlit as st
def request_automatic(conversation: List):
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "text": f"{conversation}"
      }
    }
    )
    headers = {
        'accept' : 'application/json',
      'X-API-Key': st.secrets["automation_xapi_key"],
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)

    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))["data"]["app_output"]["dictionary_of_labels"]



def manual_label_generator(conversation: List):
    
    conn = http.client.HTTPConnection("34.147.4.82")
    payload = json.dumps({
      "data": {
        "text": f"{conversation}"
      }
    }
    )
    # print("1-HELLO")
    headers = {
        'accept' : 'application/json',
      'X-API-Key': st.secrets["manual_xapi_key"],
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/conversation", payload, headers)
    # print("2-HELLO")

    res = conn.getresponse()
    data = res.read()
    # return data.decode("utf-8")

    return json.loads(data.decode("utf-8"))["data"]["app_output"]["labels"]
