#include <Wire.h> // i2c library

// analog input pins (pins 4 and 5 are used for writing by i2c library)
const int analogInputPinNums[] = {0, 1, 2, 3};

// digital input pins
const int digitalInputPinNums[] = {2, 3, 4, 5, 6, 7, 8, 9};

// digital output pins - may use later for diagnostics, etc.
const int digitalOutputPinNums[] = {10, 11, 12, 13};


const unsigned int NUM_PIN_STATES = 4;
struct pin
{
  int pin;
  int states[NUM_PIN_STATES]; // queue of the past states
};


struct analogReading
{
  byte bytes[2]; // 2 bytes for each of the readings
};

struct digitalReading
{
  byte bytes; // 1 byte for each of the readings
};

struct wireBytes
{
  analogReading analogReadings[sizeof(analogInputPinNums) / sizeof(int)];
  digitalReading digitalReadings[sizeof(digitalInputPinNums) / sizeof(int)];
};


pin analogInputPins[sizeof(analogInputPinNums) / sizeof(int)];
pin digitalInputPins[sizeof(digitalInputPinNums) / sizeof(int)];


// push a new state on to the front of the states queue
void pushNewState(int states[], int newState) {
  for (int i = NUM_PIN_STATES - 1; i > 0; i--) {
    states[i] = states[i - 1];
  }

  states[0] = newState;
}


// initialize the array of structs for the given group of pins as specified
void setupPinGroup(const int pinNums[], int numPins, pin pins[], int mode, int initialStateValue) {
  for (int i = 0; i < numPins; i++) {
    pinMode(pinNums[i], mode);

    int zero_states[NUM_PIN_STATES] = {initialStateValue};
    pins[i] = pin{pinNums[i], *zero_states};
  }
}

analogReading getAnalogReading(int index) {
  pin analogPin = analogInputPins[index];
  int sum = 0;
  for (int i = 0; i < NUM_PIN_STATES; i++) {
    sum += analogPin.states[i];
  }
  unsigned int average = sum / NUM_PIN_STATES;

  // the reading is only 10 bits, but we have 16 to work with, 
  // the reading will sit in the 10 rightmost bits
  return analogReading{{highByte(average), lowByte(average)}};
}

digitalReading getDigitalReading(int index) {
  pin digitalPin = digitalInputPins[index];
  byte reading = 1;
  for (int i = 0; i < NUM_PIN_STATES; i++) {
    if (digitalPin.states[i] == 0) {
      reading = 0;
    }
  }

  return digitalReading{reading};
}

void setup() {
  // initialize all analog input pins to INPUT_PULLUP
  setupPinGroup(analogInputPinNums, sizeof(analogInputPinNums) / sizeof(int), analogInputPins, INPUT_PULLUP, 0);

  // initialize all digital input pins to INPUT_PULLUP
  setupPinGroup(digitalInputPinNums, sizeof(digitalInputPinNums) / sizeof(int), digitalInputPins, INPUT_PULLUP, LOW);

  // initialize all digital output pins to OUTPUT
  for (int i = 0; i < sizeof(digitalOutputPinNums) / sizeof(int); i++) {
    pinMode(digitalOutputPinNums[i], OUTPUT);
  }
  
//  Wire.begin(); // join i2c bus (address optional for master)
  Serial.begin(9600);
  delay(2000);
}

void loop() {
  Serial.println("========================LOOP START===========================");
  wireBytes message = {0};

  // read the analog input pins
  for (int i = 0; i < sizeof(analogInputPins) / sizeof(pin); i++) {
    pushNewState(analogInputPins[i].states, analogRead(analogInputPins[i].pin));
    message.analogReadings[i] = getAnalogReading(i);
    Serial.println(word(message.analogReadings[i].bytes[0],message.analogReadings[i].bytes[1]));
  }

  // read the digital input pins
  for (int i = 0; i < sizeof(digitalInputPins) / sizeof(pin); i++) {
    pushNewState(digitalInputPins[i].states, digitalRead(digitalInputPins[i].pin));
    message.digitalReadings[i] = getDigitalReading(i);
    Serial.println(message.digitalReadings[i].bytes);
  }

//  Wire.beginTransmission(8); // transmit to device #8
//  Wire.write((byte *) &message, sizeof (message));
//  Wire.endTransmission();    // stop transmitting

  delay(500);
}
