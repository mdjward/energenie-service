# Energenie Service #

RESTful microservice - written in Python, on the Flask framework - and based on [MiniGirlGeek/energenie-demo](https://github.com/MiniGirlGeek/energenie-demo).

## Starting the application ##

Usage (from within ./src):

```
python energenie_service.py /path/to/your/config/file [listen-host] [listen-port]
```

Where:
- **/path/to/your/config/file** is the path to your YAML-based configuration file, as shown in [the sample](https://github.com/mdjward/energenie-service/blob/master/sample-config.yml)
- **listen-host** is the address on which the web server will listen
- **listen-port** is the port on which the web server will listen

Example:

```
python energenie_service.py /etc/energenie-service.yml 0.0.0.0 8080
```

In practice, Systemd, no-hup, Supervisord or other process control mechanisms can automate startup and shutdown.

## Endpoints ##

#### /configuration ####

_Returns the contents of the configuration file used to start the service._

- Allowed method(s):
  - **GET**
- Arguments: _none_
- Aliases: **/config**

#### /switch/_\<state\>_/all ####

_Switches all configured plug sockets on or off._
- Allowed method(s):
  - **POST**
- Arguments:
  - **_string_ state** - desired state; may be one of "on" or "off"
- Aliases: _none_

Returns:
```
POST /switch/off/all

{
  "items": "all", 
  "result": "success", 
  "room": "all", 
  "state": "off"
}
```

#### /switch/_\<state\>_/_\<room\>_/_\<item\>_ ####

_Switches all - or [a] specific configured - plug socket(s) in a particular room on or off._

- Allowed method(s):
  - **POST**
- Arguments:
  - **_string_ state** - desired state; may be one of "on" or "off"
  - **_string_ room** - room in question; must be configured
  - **_string_ item** - item in question; must be configured, or "all" for all in the room in question
- Aliases: _none_

Returns:
```
POST /switch/on/living_room/table_lamp

{
  "items": "table_lamp", 
  "result": "success", 
  "room": "living_room", 
  "state": "on"
}
```

## Error management ##

Any errors are returned in the form shown in the following "405 Method Not Allowed" example:

```
GET /switch/on/living_room/table_lamp
{
  "message": "405: Method Not Allowed", 
  "result": "error"
}
```
