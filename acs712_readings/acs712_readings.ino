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

// Setup the essentials for your circuit to work. It runs first every time your circuit is powered with electricity.
void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(115200);
    while (!Serial) ; // wait for serial port to connect. Needed for native USB
    Serial.println("start");
    
    //Manually calibarte the ACS712 current sensor.
    //Connet the ACS to your board, but do not connect the current sensing side.
    //Follow serial monitor instructions. This needs be done one time only.
    cal(acs712calFactor);
    menuOption = menu();
    
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

// Main logic of your circuit. It defines the interaction between the components you selected. After setup, it runs over and over again, in an eternal loop.
void loop() 
{
    
    
    if(menuOption == '1') {
    // Current Sensor Module ACS712 - Test Code
    //Get averaged current measurment.
    float acs712Currrent  = acs712.getCurrent();
    voltage= (acs712Currrent/1024)*5000;
    Serial.print(acs712Currrent); Serial.println(F(" [mA]"));
    Serial.print(voltage); Serial.println(F(" [mV]"));

    }
    
    if (millis() - time0 > timeout)
    {
        menuOption = menu();
    }
    
}



// Menu function for selecting the components to be tested
// Follow serial monitor for instrcutions
char menu()
{

    Serial.println(F("\nWhich component would you like to test?"));
    Serial.println(F("(1) Current Sensor Module ACS712"));
    Serial.println(F("(menu) send anything else or press on board reset button\n"));
    while (!Serial.available());

    // Read data from serial monitor if received
    while (Serial.available()) 
    {
        char c = Serial.read();
        if (isAlphaNumeric(c)) 
        {   
            
            if(c == '1') 
          Serial.println(F("Now Testing Current Sensor Module ACS712"));
            else
            {
                Serial.println(F("illegal input!"));
                return 0;
            }
            time0 = millis();
            return c;
        }
    }
}