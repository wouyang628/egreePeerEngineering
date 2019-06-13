# We need to import request to access the details of the POST request
#used for Appformix Northstar version only
from flask import Flask, request
from flask_restful import abort
import commands
import json
import pprint
import requests
import os
import user_functions
requests.packages.urllib3.disable_warnings() 


AppFormixInterfaceL3IncompleteEventID='e6ff8690-b706-11e8-ba3d-0242ac120003'
AppFormixCPUEventID='d6d168f2-fa6c-11e8-a98f-0242ac120005'
AppFormixChangeDemandMappingEventID='d1c02276-8d75-11e9-80b0-0242ac120003'

# Initialize the Flask application
app = Flask(__name__)

@app.route('/', methods=['POST'])
def app_message_post():
    print "#################  Start  #######################"
    global AppFormixInterfaceL3IncompleteEventID
    global AppFormixCPUEventID
    if request.headers['Content-Type'] != 'application/json':
        abort(400, message="Expected Content-Type = application/json")
    try:
        data = request.json
        status = data['status']
        spec = data['spec']
        state = status['state']
        device_id = status['entityId']
        event_rule_id = spec['eventRuleId']
        print "state " + state + " device id " + device_id + "  event id " + event_rule_id
        #if spec['eventRuleId'] == g_rule_id:
        #    state = status['state']
        #    device_id = status['entityId']
        #    if state == "active" and device_id == g_device_id:
        #        print 'DATA_ACTIVE :: ', pprint.pprint(data)
        #        user_functions.move_traffic()
        #        print 'traffic detoured and Slack was notified'
        #    elif state == "inactive":
        #        #print 'DATA_INACTIVE :: ', pprint.pprint(data)
        #        print 'LSP path can be changed back'
        #return json.dumps({'result': 'OK'})
        if event_rule_id == AppFormixCPUEventID:
            print "received cpu high alert"
            print state
            print device_id
            if state == "active":
                print 'CPU HIGH UTIL DETECTED for ' + device_id
                print 'PERFORMING EXHUASTIVE LINK FAILURE SIMULATION for ' + device_id
                #create maintenance for simulation purpose
                rest_index_number = user_functions.get_node_info(device_id)
                rest_payload = user_functions.generate_node_maitenance_json(rest_index_number, 'for_simulation') 
                maintenance_event = user_functions.create_maintenance(rest_payload)
                maintenance_index = maintenance_event.json()['maintenanceIndex']
                check_simulation = user_functions.check_if_simulation_pass()
                print "simulation result " + check_simulation
                user_functions.delete_maintenance(maintenance_index)
                print "delete temp maintenace"
                if check_simulation == 'true':
                    print 'CPU HIGH UTIL DETECTED PUT NODE UNDER MAINTENANCE::'
                    # pprint.pprint(data)
                    #print "rest_node_name, rest_index_number" +  rest_node_name +  rest_index_number
                    rest_payload = user_functions.generate_node_maitenance_json(rest_index_number, 'for_maint')
                    print rest_payload
                    user_functions.create_maintenance(rest_payload)
                else:
                    print 'CANNOT PUT ' + device_id + ' UNDER MAINTENANCE. EXHUASTIVE FAILURE SIMULATION NOT PASSED' 
            elif state == "inactive":
                #print 'DATA_INACTIVE :: ', pprint.pprint(data)
                print 'CPU util back to normal. '
        print '###############################'
        if event_rule_id == AppFormixInterfaceL3IncompleteEventID:
            print "Received interface l3 incomplete alert"
            if state == "active":
                rest_payload = user_functions.generate_link_maitenance_json()
                print rest_payload
                user_functions.create_maintenance(rest_payload)
                print 'Put problematic link into maintenance mode'
            elif state == "inactive":
            # print 'DATA_INACTIVE :: ', pprint.pprint(data)
                print 'link back to normal. you can complete the maintenance event'
        if event_rule_id == AppFormixChangeDemandMappingEventID:
            print "High CPU detected on ASBR108. Switching demand to ASBR109"
            user_functions.change_demand_mapping()
            print "Demand switched to ASBR109"
        return json.dumps({'result': 'OK'})
    except Exception as e:
        abort(400, message="Exception processing request: {0}".format(e))
        print '...'


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("10000")
    )
