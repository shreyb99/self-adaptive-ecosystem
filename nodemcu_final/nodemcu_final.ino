#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ACS712.h>
#include <AnalogReader.h>

 // Pin Definitions
#define ACS712_PIN_VO  A0

// Global variables and defines
const int acs712calFactor = 513;
// object initialization
ACS712 acs712(ACS712_PIN_VO);
float voltage;


// define vars for testing menu
const int timeout = 2000;       //define timeout of 10 sec
char menuOption = 0;
long time0;


// Update these with values suitable for your network.

const char* ssid = "ramiz";
const char* password = "undenujunga2002";
const char* mqtt_server = "192.168.43.49";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void cal(int calFactor)
{
 long rawVal =0;
  for(int i=0 ; i<1000 ; i++)
    rawVal += analogRead(A0);
  int cal = rawVal / 1000;
  Serial.println(cal);
  if(abs(cal - calFactor) < 1)
  {
    Serial.print("Your calibration factor is good!");
  }
  else
  {
    Serial.print("Your calibration factor is: ");
    Serial.println(cal);
  }
  calFactor = cal;

}

void callback(char* topic, byte* payload, unsigned int length) {
//   Serial.print("Message arrived [");
//   Serial.print(topic);
//   Serial.print("] ");
//   for (int i = 0; i < length; i++) {
//     Serial.print((char)payload[i]);
//   }
//   Serial.println();
  int data = (int)payload;
  if (data == 1) {
	  client.publish("nodemcu1/acs1", "ACS Reading sent");
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("nodemcu1/acs1", "hello world");
      // ... and resubscribe
      client.subscribe("nodemcu1/acs1");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  cal(acs712calFactor);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

    float acs712Currrent  = acs712.getCurrent();
    float acs_reading = String(acs712Currrent);
    char * acs_val = acs_reading.toCharArray(MSG_BUFFER_SIZE, acs_reading.length());
    client.publish("nodemcu1/acs1", acs_val);
	  client.subscribe("nodemcu1/acs1");
    delay(15000)
}