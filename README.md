# ha-blueiris

Custom component for Home Assistant which connects to your blue iris server.

Configuring the base component in your configuration file will allow it to automatically add your cameras by using the blue_iris platform. (This is set up similar to how the [zoneminder](https://www.home-assistant.io/components/zoneminder/) component is set up.)

## Currently Working Features
(see [planned features below](#planned-features) for what is planned to be implemented)

**Server Component**
- Provides platform for the cameras
- Shows how many cameras it detects
- Shows Blue Iris version
- Shows available profiles
- Shows available schedules
- Shows whether the login provided is admin or not
- Is named after what you named your Blue Iris server
- Shows the JSON Endpoint that its using

**Camera**
- Connects an mjpeg stream to your camera
- Responds to the standard camera component commands:
  - Enable
  - Disable
  - Motion_On
  - Motion_Off

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

## Planned Features
The following things are planned for this component:

**Server Component**
- Service calls to allow
  - setting the Signal
  - setting the global profile
  - getting logs
  - basically everything non-camera specific the API can do..

**Camera Component**
- Trigger recording
- Set off motion events
- PTZ Control?
- Other camera-specific API commands.
