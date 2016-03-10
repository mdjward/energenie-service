from energenie import switch_on, switch_off
from configuration import ConfigurationValidator

class EnergenieProxy:

    def __validate_plug_number(self, number):
        if type(number) is not int:
            raise ValueError('Plug number must be given as a number')
        return True

    def switch_off_plug(self, number = 0):
        if (self.__validate_plug_number(number) == True):
            switch_off(number)

    def switch_off_all(self):
        self.switch_off_plug(0)

    def switch_on_plug(self, number = 0):
        if (self.__validate_plug_number(number) == True):
            switch_on(number)

    def switch_on_all(self):
        self.switch_on_plug(0)



class EnergenieProxyManager:

    STATE_ON = 'on'
    STATE_OFF = 'off'

    def __init__(self, proxy, configuration_validator, configuration):
        if isinstance(proxy, EnergenieProxy) == False:
            raise TypeError('Proxy must be given as an instance of EnergenieProxy')
	if isinstance(configuration_validator, ConfigurationValidator) == False:
            raise TypeError('Validator must be given as an instance of ConfigurationValidator')
        if type(configuration) is not dict:
            raise TypeError('Configuration must be given as a dictionary')

        configuration_validator.validate(configuration)

        self._proxy = proxy
        self._configuration_validator = configuration_validator
        self._configuration = configuration

    def get_configuration(self):
        return self._configuration

    def __check_room(self, room):
        if room not in self._configuration['rooms']:
            raise RoomNotFoundError(room)

        return True

    def __check_item(self, room, item):
#        self.__check_room(room)
        print(item in self._configuration['rooms'][room])
        if (item not in self._configuration['rooms'][room]):
            raise ItemNotFoundError(item, room)
        
        return True

    def __sanitise_given_state(self, given_state):
        if type(given_state) is str:
            if given_state == EnergenieProxyManager.STATE_ON:
                return True
            if given_state == EnergenieProxyManager.STATE_OFF:
                return False
        if type(given_state) is int:
            return (given_state > 0)
        if type(given_state) is bool:
            return (given_state == True)

        raise ValueError('Unable to sanitise given state: ' + given_state)

    def __do_switch(self, room, item, state):
        sanitised_state = self.__sanitise_given_state(state)
        plug = int(self._configuration['rooms'][room][item]['energenie_plug'])

        if (sanitised_state == True):
            self._proxy.switch_on_plug(plug)
        else:
            self._proxy.switch_off_plug(plug)

    def __do_switch_room_all(self, room, state):
        for item_id, item in self._configuration['rooms'][room].iteritems():
            self.__do_switch(room, item_id, state)

    def switch(self, room, item, state):
        self.__check_item(room, item)
        self.__do_switch(room, item, state)

    def switch_room_all(self, room, state):
        self.__check_room(room)
        self.__do_switch_room_all(room, state)

    def switch_all(self, state):
        sanitised_state = self.__sanitise_given_state(state)

        if (sanitised_state == True):
            self._proxy.switch_on_all()
        else:
            self._proxy.switch_off_all()



class NotFoundError(Exception):

    def __init__(self, type, id, extra):
        super(NotFoundError, self).__init__("%s %s not found%s" % (type, id, extra))



class RoomNotFoundError(NotFoundError):
    def __init__(self, id):
        super(RoomNotFoundError, self).__init__("Room", id, "")



class ItemNotFoundError(NotFoundError):
    def __init__(self, item_id, room_id):
        super(ItemNotFoundError, self).__init__("Item", item_id, " in room " + room_id)

