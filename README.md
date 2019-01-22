# ha-blueiris

Custom component for Home Assistant which connects to your blue iris server.

Configuring the base component in your configuration file will allow it to automatically add your cameras by using the blue_iris platform. (This is set up similar to how the [zoneminder](https://www.home-assistant.io/components/zoneminder/) component is set up.)

## Features Roadmap
Both planned and completed, as indicated by checkboxes.

**Server Component**
- [x] Provides platform for the cameras
- [x] Shows how many cameras it detects
- [x] Shows Blue Iris version
- [x] Shows available profiles
- [x] Shows available schedules
- [x] Shows whether the login provided is admin or not
- [x] Is named after what you named your Blue Iris server
- [x] Shows the JSON Endpoint that its using
- [ ] Service calls
  - [ ] Setting the signal
  - [ ] Setting the global profile
  - [ ] Retrieving logs

**Camera**
- [x] Connects an mjpeg stream to your camera
- [x] Responds to the standard camera component commands:
  - [x] Enable
  - [x] Disable
  - [x] Motion_On
  - [x] Motion_Off
- [ ] Service calls
  - [ ] Trigger recording
  - [ ] Trigger 'motion'
  - [ ] PTZ Commands
  
I believe there are some more calls available to the JSON API, which should be considered planned for the future -- it'd be nice to have this component be able to do everything the API allows.

## Installation

To use, download this repository and unpack into `/config/custom_components/` on your Home Assistant.

Then, in your configuration yaml:

```yaml
# Custom Component
blue_iris:
  username: HA_BLUEIRIS_USERNAME
  password: HA_BLUEIRIS_PASSWORD
  host: HA_BLUEIRIS_IP_OR_DNS
  protocol: HTTP_OR_HTTPS
  port: BLUEIRIS_PORT

camera:
  - platform: blueiris
```
### Configuration Details

**username**: username for hass to use to authenticate to your server

**password**: password used for the username

**host**: blue iris host IP or FQDN

**port** *(optional)*: exposed blueiris port, defaults to match protocol (80 for http, 443 for https)

**protocol** *(optional)*: unless you set up https access via a reverse proxy or the tunnel settings in blue iris. defaults to http

**name** *(optional)*: define a name for the blue iris entity (defaults to 'server')
