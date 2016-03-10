import sys
from com.mattdw.energenie_service.energenie_proxy import EnergenieProxy, EnergenieProxyManager, NotFoundError
from com.mattdw.energenie_service.configuration import YamlConfigurationFactory, ConfigurationValidator
from com.mattdw.energenie_service.flask_utils import configure_app
from flask import Flask
from flask_responses import json_response
from werkzeug.routing import BaseConverter



argc = len(sys.argv)
if (argc) < 2:
    print "Usage: %s configfile [listen-host] [listen-port]" % sys.argv[0]
    sys.exit(1)



config = YamlConfigurationFactory(sys.argv[1])
manager = EnergenieProxyManager(EnergenieProxy(), ConfigurationValidator(), YamlConfigurationFactory(sys.argv[1]).build())



app = configure_app(Flask(__name__))


def convert_state(state):
    return EnergenieProxyManager.STATE_ON if state == 'on' else EnergenieProxyManager.STATE_OFF

def handle_success(data):
    data.update({'result': 'success'})

    return json_response(data, 200)

def handle_error(ex, code):
    return json_response({'result': 'error', 'message': str(ex)}, code)

def handle_not_found_error(ex):
    return handle_error(ex, 404)



@app.errorhandler(404)
@app.errorhandler(405)
def handle_http_error(ex):
    return handle_error(ex, 404)

@app.errorhandler(BaseException)
def handle_other_error(ex):
    return handle_error(ex, 500)

@app.route("/switch/<regex('(on)|(off)'):state>/all", methods = ['POST'])
def switch_all(state):
    state = convert_state(state)
    manager.switch_all(state)

    return handle_success({'room': 'all', 'items': 'all', 'state': state})

@app.route("/switch/<regex('(on)|(off)'):state>/<string:room>/<string:item>", methods = ['POST'])
def switch_room_all(state, room, item):
    try:
        state = convert_state(state)

        if (item == 'all'):
            manager.switch_room_all(room, state)
        else:
            manager.switch(room, item, state)

        return handle_success({'room': room, 'items': item, 'state': state})
    except NotFoundError as ex:
        return handle_not_found_error(ex);

 

@app.route('/config', methods = ['GET'])
@app.route('/configuration', methods = ['GET'])
def get_configuration():
    return handle_success({'configuration': manager.get_configuration()})



host = str(sys.argv[2]) if argc >= 3 else '0.0.0.0'
port = int(sys.argv[3]) if argc >= 4 else 8080

app.run(host=host, port=port)

