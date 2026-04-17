/* 
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
% FILE ........... noise_reader.ino                                          %
% LANGUAGE ....... C language for Arduino                                    %
% DESCRIPTION .... reads a noise signal from Arduino ADC and writes it on    %
                   a serial port that can be read with Python                %
% PLATFORM ....... Arduino UNO R4 Wi-Fi                                      %
% LINK-FILEs ..... none                                                      %
% DATE ........... Apr/17/2024                                               %
% LAST-MFD ....... Apr/17/2024                                               %
% CREATED by ..... Group A1                                                  %
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
 */

#include <math.h>

//
// constant definition
//
const int PIN_READ = A0;                    // noise will be read from A0 (Analog Input)
const int BAUD_RATE = 2000000;              // bit per sec sent by arduino to PC via USB
const int DELAY_DURATION = 1;               // delay between an iteration and the next one
const int ANALOG_READ_RESOLUTION = 14;      // default resolution = 10
const double MAX_VOLTAGE = 4.807;           // max voltage that arduino can read
const int DIGIT_PRECISION = 10;

//
// variable definition
//
double noise = 0;

void setup() {
  // initialize serial read (data sent from Arduino to PC)
  Serial.begin(BAUD_RATE);
  analogReadResolution(ANALOG_READ_RESOLUTION);
}

void loop() {
  // reads analog value and converts it in a integer value (from 0 to 1023)
  noise = fromIntToVolt(analogRead(PIN_READ)); 
  
  //Serial.print("Analog value: ");
  Serial.println(noise, DIGIT_PRECISION); 
  //Serial.println(" V"); 
  
  // pause
  delay(DELAY_DURATION);
}

double fromIntToVolt(uint16_t integerValue) {
  return integerValue / (double) (pow(2, ANALOG_READ_RESOLUTION) - 1) * MAX_VOLTAGE;
}
