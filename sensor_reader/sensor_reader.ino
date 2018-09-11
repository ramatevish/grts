// 2 analog pins for writing I2C (pins 4 and 5)


// digital input pins
const int digitalInputPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
const unsigned int numDigitalInputPins = 12;


void setup() {
  // initialize all digital input pins to INPUT
  for (int i = 0; i < numDigitalInputPins; i++) {
    pinMode(digitalInputPins[i], INPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
