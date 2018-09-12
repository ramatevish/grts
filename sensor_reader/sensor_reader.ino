#include <Wire.h> // i2c library
#include <OneWire.h>
#include <DallasTemperature.h>

#define SLAVE_ADDRESS 0x04

// Data wire is conntec to the Arduino digital pin 2
#define ONE_WIRE_BUS 2

// Address of the temperature sensor data
#define TEMPERATURE_ADDRESS 1

#define NUM_SENSORS 1

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

struct sensorData
{
  byte address;
  byte metadata;
  byte data[2];
};
sensorData message[NUM_SENSORS];


void setup() {
  Serial.begin(9600); // start serial for output
  Wire.begin(SLAVE_ADDRESS); // join i2c bus
  sensors.begin(); // start up the temperature library

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  delay(2000);
  Serial.println("Ready!");
}

void loop() {
  ////////////////////////
  // TEMPERATURE SENSOR //
  ////////////////////////
  // https://randomnerdtutorials.com/guide-for-ds18b20-temperature-sensor-with-arduino/

  // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
  sensors.requestTemperatures(); 

  // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  float celsiusTemperature = sensors.getTempCByIndex(0);
  float fahrenheitTemperature = sensors.getTempFByIndex(0);
  
  Serial.print("Celsius temperature: ");
  Serial.print(celsiusTemperature); 
  Serial.print(" - Fahrenheit temperature: ");
  Serial.println(fahrenheitTemperature);

  int tempInt = (int) celsiusTemperature;
  if (tempInt < 0) {
    tempInt = 0;
  }
  if (tempInt > 255) {
    tempInt = 255;
  }

  sensorData temperatureSensor{TEMPERATURE_ADDRESS, 0, byte(tempInt), 0};
  message[0] = temperatureSensor;

  delay(500);
}

void receiveData(int byteCount){
  // TODO(wlarow) state machine rule following
}

// callback for sending data
void sendData(){
  Wire.write((byte *) &message, sizeof (message));
}
