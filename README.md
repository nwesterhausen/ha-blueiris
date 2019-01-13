# ha-blueiris

Custom component for Home Assistant which connects to your blue iris server.

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
