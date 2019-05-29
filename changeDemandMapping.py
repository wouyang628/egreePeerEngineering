import json
from pprint import pprint
import os
from jinja2 import Environment, FileSystemLoader
import datetime
import time
import requests


def change_DemandMapping(**kwargs):
    url = 'http://100.123.16.0:8091/Northstar/API/v2/tenant/1/topology/1/'
    demand_ID = '32'
    node_url_test = url + 'nodes'

    node_url = url + 'nodes'
    link_url = url + 'links'
    lsp_url = url + 'te-lsps'
    token_url = 'https://100.123.16.0:8443/oauth2/token'
    maintenance_url = url + 'maintenances'
    changeDemand_url = url + 'demands/' + demand_ID
    run_simulation_url = url + 'rpc/simulation'
    hearders_token = {'Content-Type': 'application/json'}
    user = 'admin'
    password = '******'

    print("changeDemand_url:" + changeDemand_url)

    r = requests.post(token_url, auth=('admin', 'Embe1mpls'), data='{"grant_type":"password","username":"admin","password":"Embe1mpls"}', headers=hearders_token, verify=False)
    token = r.json()['access_token']
    print("token: " + token)
    headers = {'Authorization': str('Bearer ' + token), 'Content-Type': 'application/json'}
    print(headers)
    payload = '{"plannedProperties":{"pathName":"11.0.0.103","bindingLSP":"sr-101-103-sr99","design":{"routingMethod":"default","adminGroups":{}}},"name":"vMX-1_11.0.0.110/32_IP","from":{"topoObjectType":"ipv4","address":"11.0.0.101"},"pathType":"primary","to":{"topoObjectType":"ipv4","address":"11.0.0.103"},"demandIndex":32,"prefix":{"topoObjectType":"ipv4","address":"11.0.0.110","length":32}}'
    print(payload)
    r = requests.put(changeDemand_url, data=payload, headers=headers, verify=False)
    print(r)


