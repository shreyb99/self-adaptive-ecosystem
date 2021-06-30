import paho.mqtt.client as mqtt

def on_publish(client, userdata, rc):
    print("Data published")
    pass

client = mqtt.Client()
client.on_publish = on_publish
client.connect("localhost", 1883, 60)

client.publish("Topic/path", "Message")

