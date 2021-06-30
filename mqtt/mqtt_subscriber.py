import paho.mqtt.client as mqtt
import csv
from datetime import datetime

job = "get:acs1"

# TODO: Setup the functions to handle the different data rceived from the different sensors


def on_publish(user, userdata, rc):
    print("Message published")
    pass

def on_connect(clients, userdata, flags, rc):
    print("Connected with code " + str(rc))
    # if (time.time() - start_time) == 10:
    client.subscribe([("nodemcu1/acs1", 2), ("nodemcu1/acs2", 2), ("nodemcu1/acs1", 2), ("nodemcu2/acs1", 2), ("nodemcu2/acs2", 2)])
    client.publish("nodemcu1/acs1", "1")

    # if job == "get:acs1":
    #     client.subscribe("nodemcu1/"+job.split(":")[1])
    #     client.publish("nodemcu1/"+job.split(":")[1], "send_data")
    #     job = "none"


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(payload, message.topic)

    if 'relay' in message.topic:
        return relayHandler(payload, message.topic)

    append_to_csv(payload, datetime.now(), message.topic)
    # if payload == "Got your message":
    #     print("They got your message")
    # else:
    #     print("They didn't get your message")
    # msg = payload.split(":")
    # TODO: Check for the sensor field of the msg and call suitable functions

def relayHandler(payload, topic):
    client.publish(topic, "1")
    pass

def append_to_csv(data, timestamp, topic):
    dt = str(datetime.fromtimestamp(timestamp)).split(' ')
    with open('dataset.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([dt[0], dt[1], data, topic])



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
# start_time = time.time()