import json
import time
import paho.mqtt.client as mqtt
id = '4151cfcf-a611-4419-a330-f6b460face58' # einstakt id fengið t.d hér https://www.uuidgenerator.net/

client_telemetry_topic = id + '/telemetry' # default áskrift en gæti verið t.d /telementary/lightsensor
server_command_topic = id + '/commands' # áskrift command til að kveikja á led annari tölvu
client_name = id + 'nightlight_server' # getur verið hvað sem er sem er lýsandi :-) hvað client er að gera

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()
# fall sem tekur á móti og sendir skilaboð eða skipanir
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    command = { 'led_on' : payload['light'] > 20}# gildi sem kemur frá TSl2591 lightsensor (hágildi :-)
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)# sendir og tekur á móti boðum á 2 sek fresti
 