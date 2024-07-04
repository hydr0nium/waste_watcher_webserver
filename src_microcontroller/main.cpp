#include <Arduino.h>
#include "SoftwareSerial.h"
#include <Adafruit_Fingerprint.h>
#include <Servo.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <SoftwareSerial.h>
#include <hcsr04.h>
#include <stdlib.h>
#define OPEN 1000
#define CLOSE 2000

// D4 = yellow, D3=white
SoftwareSerial mySerial(D4, D3);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

uint8_t getFingerprintID();
Servo servo;

const char *ssid = "Honor 9 Lite K";
const char *password = "saarsec1337";

String Servername = "https://wastewatcher.patchwork-security.de:8000";
String pass = "pass=Uo0TymQfjJJ8US9csma92wYQyy9rKFFkPdtN0heV4OpBPHvd33EZpN-h";

const int trigPin1 = D8;
const int echoPin1 = D7;
const int trigPin2 = D5;
const int echoPin2 = D6;
HCSR04 ultrasonic_1 = HCSR04(trigPin1, echoPin1);
HCSR04 ultrasonic_2 = HCSR04(trigPin2, echoPin2);
float base_distance;
float base_depth;
float currentfillstate = 0.0;

void initUltrasonicBaseDistance();
float getFillstate(int);
void send_full_notify();
float getBaseDepth(int);

void setup()
{
  Serial.begin(9600);

  //servo.attach(D0);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  while (!Serial)
    ; // For Yun/Leo/Micro/Zero/...
  delay(100);
  Serial.println("\n\nAdafruit finger detect test");

  // set the data rate for the sensor serial port
  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword())
  {
    Serial.println("Found fingerprint sensor!");
  }
  else
  {
    Serial.println("Did not find fingerprint sensor :(");
    while (1)
    {
      delay(1);
    }
  }

  Serial.println(F("Reading sensor parameters"));
  finger.getParameters();
  initUltrasonicBaseDistance();
  Serial.print("Measured base depth");
  Serial.println(base_depth);
  Serial.print("Measuring base distance: ");
  Serial.println(base_distance);

  finger.getTemplateCount();

  if (finger.templateCount == 0)
  {
    Serial.print("Sensor doesn't contain any fingerprint data. Please run the 'enroll' example.");
  }
  else
  {
    Serial.println("Waiting for valid finger...");
    Serial.print("Sensor contains ");
    Serial.print(finger.templateCount);
    Serial.println(" templates");
  }
  servo.attach(D0);
  servo.writeMicroseconds(CLOSE);
  Serial.println("Looking for fingerprint...");
}

void loop() // run over and over again
{
  getFingerprintID();
  delay(50); // don't ned to run this at full speed.
}

uint8_t getFingerprintID()
{
  uint8_t p = finger.getImage();
  switch (p)
  {
  case FINGERPRINT_OK:
    Serial.println("Image taken");
    break;
  case FINGERPRINT_NOFINGER:
    // Serial.println("No finger detected");
    return p;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  case FINGERPRINT_IMAGEFAIL:
    Serial.println("Imaging error");
    return p;
  default:
    Serial.println("Unknown error");
    return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p)
  {
  case FINGERPRINT_OK:
    Serial.println("Image converted");
    break;
  case FINGERPRINT_IMAGEMESS:
    Serial.println("Image too messy");
    return p;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  case FINGERPRINT_FEATUREFAIL:
    Serial.println("Could not find fingerprint features");
    return p;
  case FINGERPRINT_INVALIDIMAGE:
    Serial.println("Could not find fingerprint features");
    return p;
  default:
    Serial.println("Unknown error");
    return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK)
  {
    Serial.println("Found a print match!");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("Communication error");
    return p;
  }
  else if (p == FINGERPRINT_NOTFOUND)
  {
    Serial.println("Did not find a match");
    return p;
  }
  else
  {
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #");
  Serial.print(finger.fingerID);
  Serial.print(" with confidence of ");
  Serial.println(finger.confidence);
  WiFiClient client;
  HTTPClient http;
  String serverpath;
  int responsecode;
  float dist;

  float amount = getFillstate(15);
  if (amount >= 90) {
    send_full_notify();
    return -1;
  }


  servo.writeMicroseconds(OPEN);
  // This opens the trashcan and waits for something the be thrown in and closes after a certain amount of time
  for (int i = 0; i < 4000; i++)
  {
    delay(1);
    dist = ultrasonic_1.dist();
    Serial.print("Measured Distance:");
    Serial.println(dist);
    if (dist < base_distance)
    {

      serverpath = Servername + "/commit?id=" + finger.fingerID + "&" + pass;
      Serial.println(serverpath);
      http.begin(client, serverpath.c_str());
      responsecode = http.GET();
      Serial.println(responsecode);
      Serial.print("Response: ");
      Serial.println(http.getString());


      break;
    }
  }

  servo.writeMicroseconds(CLOSE);
  delay(1000); // Wait one second

  // Set fill amount
  amount = getFillstate(15);
  serverpath = Servername + "/set_fill_amount?amount=" + amount + "&" + pass;
  Serial.println(serverpath);
  http.begin(client, serverpath.c_str());
  responsecode = http.GET();
  Serial.println(responsecode);
  Serial.print("Response: ");
  Serial.println(http.getString());

  // Check if "full"
  if (amount >= 90) {
    send_full_notify();
  }

  return finger.fingerID;
}



float getFillstate(int timesToPing)
{

  if (timesToPing > 15)
  {
    timesToPing = 15;
  }

  float biggest = -1.0;
  for (int i = 0; i < timesToPing; i++)
  {
    delay(1);
    float depth = ultrasonic_2.dist();
    if (depth > biggest)
    {
      biggest = depth;
    }

  }
  float temp=base_depth - biggest;
  if(temp < 0.0){
    temp=0;
  }
  // returns how much the trashcan is full 0 = empty, 100 = full
  return (((temp) / base_depth) * 100.0);
}

void initUltrasonicBaseDistance()
{
  base_distance = ((ultrasonic_1.dist() + ultrasonic_1.dist()) / 2) - 1;
  base_depth = getBaseDepth(15);//((ultrasonic_2.dist() + ultrasonic_2.dist()) / 2) - 1;
}


void send_full_notify() {

  WiFiClient client;
  HTTPClient http;
  String serverpath = Servername + "/notify?" + pass;
  Serial.println(serverpath);
  http.begin(client, serverpath.c_str());
  int responsecode = http.GET();
  Serial.println(responsecode);
  Serial.print("Response: ");
  Serial.println(http.getString());
}

float getBaseDepth(int timesToPing){
  if (timesToPing > 15)
  {
    timesToPing = 15;
  }

  float biggest = -1.0;
  for (int i = 0; i < timesToPing; i++)
  {
    delay(1);
    float depth = ultrasonic_2.dist();
    if (depth > biggest)
    {
      biggest = depth;
    }

  }
  return biggest;
}