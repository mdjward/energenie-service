import os, yaml
from abc import ABCMeta, abstractmethod



class ConfigurationError(Exception):
    __metaclass__ = ABCMeta

    def __init__(self, message):
        super(ConfigurationError, self).__init__(message)
        pass



class ConfigurationFileNotFoundError(ConfigurationError):
    def __init__(self, source_file_path):
        super(ConfigurationFileNotFoundError, self).__init__("Source file '%s' not found" % source_file_path)




class ConfigurationFileNotReadableError(ConfigurationError):
    def __init__(self, source_file_path):
        super(ConfigurationFileNotReadableError, self).__init__("Source file '%s' is not readable" % source_file_path)



class AbstractConfigurationFactory:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def build(self):
        pass



class AbstractFileConfigurationFactory(AbstractConfigurationFactory):

    _source_file_path = ''

    def __init__(self, source_file_path):
        if self._validate_source_file_path(source_file_path):
            self._source_file_path = source_file_path

    def _validate_source_file_path(self, source_file_path):
        if os.path.exists(source_file_path) == False:
            raise ConfigurationFileNotFoundError(source_file_path)
        if os.access(source_file_path, os.R_OK) == False:
            raise ConfigurationFileNotReadableError(source_file_path)
        return True



class YamlConfigurationFactory(AbstractFileConfigurationFactory):

    def build(self):
        with open(self._source_file_path) as f:
            configuration = yaml.load(f)
            f.close()
        
        return configuration



class ConfigurationValidator:

    def __init__(self):
        pass

    def validate(self, configuration):
        configuration_type = type(configuration)

        if configuration_type is not dict:
            raise TypeError("Configuration must be provided as a dictionary; given: %s" % configuration_type.__name__)

        assert ('rooms' in configuration), "Room is top-level key"
        assert (self._validate_rooms(configuration['rooms']) == True), "Rooms configuration is valid"

        return True



    def _validate_rooms(self, rooms):
        for room_id, room in rooms.iteritems():
            assert (self._validate_room(room) == True), "Room %s is valid" % room_id

        return True

    def _validate_room(self, room):
        assert (type(room) is dict), "Room is specified as a dictionary/object"
        assert (len(room) > 0), "At least one item is defined within this room"

        for item_id, item in room.iteritems():
            assert (self._validate_item(item) == True), "Item %s is valid" % item_id

        return True

    def _validate_item(self, item):
        assert (type(item) is dict), "Item is specified as a dictionary/object"
        assert ('energenie_plug' in item), "'energenie_plug' is defined as a key in the item object"
        assert (type(item['energenie_plug']) is int), "'energenie_plug' value is an integer"
        assert (item['energenie_plug'] > 0), "'energenie_plug' identifier is greater than zero"

        return True

