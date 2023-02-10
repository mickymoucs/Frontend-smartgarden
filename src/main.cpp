#include <Arduino.h>
#include <Bounce2.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>
#define analog_Pin 32
#define BUTTON1 27 // for trun on servo and bozer
#define BUTTON2 26
Servo myservo;
TaskHandle_t TaskA = NULL;
TaskHandle_t TaskB = NULL;
Bounce button1 = Bounce();
Bounce button2 = Bounce();
int count = 0;
int buzzer = 12;
int status_button1 = 0;
int sprinkle_1_pin = 33;
int sprinkle_2_pin = 25;
int val_soil_moisture = 0;
int ststus_servo = 1;
void auto_watering_system();
void insect_repellent();
void soil_moisture_detection();
void sunroof_control();
void manual_watering_system(void *pam);

// moisture
int moist_sensor = 0;

// sprinkle
boolean auto_sprinkle_1 = false;
boolean is_activate_sprinkle_1 = false;
boolean auto_sprinkle_2 = false;
boolean is_activate_sprinkle_2 = false;

// buzzer & sunroof
boolean buzzer_is_activate = false;
boolean sunroof_is_open = true;
boolean user_ignore = true;

const String baseUrl = "https://ecourse.cpe.ku.ac.th/exceed08/";

void POST_buzzer_sunroof()
{
  String json;
  DynamicJsonDocument doc(2048);
  doc["buzzer"] = 1;
  doc["sunroof"] = 0;
  serializeJson(doc, json);

  const String url = baseUrl + "update/buzzer-sunroof";
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(json);
  if (httpResponseCode >= 200 && httpResponseCode < 300)
  {
    ;
  }
  else
  {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
}
// tast 0
void All_Switch(void *param)
{
  while (1)
  {
    button1.update();
    if (button1.fell())
    {
      sunroof_is_open = !sunroof_is_open;
      Serial.println(sunroof_is_open);
    }
    vTaskDelay(2 / portTICK_PERIOD_MS);
    button2.update();
  }
}

void all_system(void *param)
{
  while (1)
  {
    if (!sunroof_is_open || buzzer_is_activate) // ปิดฝา
    {
      if (count == 0)
      {
        is_activate_sprinkle_1 = false;
        is_activate_sprinkle_2 = false;
        sunroof_is_open = false;
        digitalWrite(sprinkle_1_pin, is_activate_sprinkle_1);
        digitalWrite(sprinkle_2_pin, is_activate_sprinkle_2); // ปิดน้ำก่อน
        POST_buzzer_sunroof();
        myservo.write(90);
        delay(100);
      }
      else
      {
        insect_repellent();
        delay(1);
      }
      count++;
    }
    else // เปิดฝา
    {
      count = 0;
      myservo.write(0);
      sunroof_is_open = true;
      delay(100);
      if (auto_sprinkle_1)
      {
      }
      if (auto_sprinkle_2)
      {
        if (moist_sensor)
        {
          digitalWrite(sprinkle_1_pin, HIGH);
        }
        else
        {
          digitalWrite(sprinkle_1_pin, LOW);
        }
      }
      if (!auto_sprinkle_1)
      {
        digitalWrite(sprinkle_1_pin, is_activate_sprinkle_1);
      }
      if (!auto_sprinkle_2)
      {
        digitalWrite(sprinkle_2_pin, is_activate_sprinkle_2); // ปิดน้ำก่อน
      }
    }
    vTaskDelay(1 / portTICK_PERIOD_MS);
  }
}
void insect_repellent() // ไล่แมลง
{
  digitalWrite(buzzer, HIGH);
  delay(1);
  digitalWrite(buzzer, LOW);
  delay(1);
}
void soil_moisture_detection() // วัดค่าความชื้น
{
  val_soil_moisture = map(analogRead(analog_Pin), 1200, 4096, 100, 0);
  Serial.print("val_soil_moisture = ");
  Serial.println(val_soil_moisture);
}

void Connect_Wifi();

void POST_moisture()
{
  String json;
  DynamicJsonDocument doc(2048);
  soil_moisture_detection();
  doc["moisture_value"] = val_soil_moisture;
  serializeJson(doc, json);

  const String url = baseUrl + "update/moisture";
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(json);
  if (httpResponseCode >= 200 && httpResponseCode < 300)
  {
    ;
  }
  else
  {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
}

void GET_moisture()
{
  DynamicJsonDocument doc(2048);
  const String url = baseUrl + "garden/moisture";
  HTTPClient http;
  http.begin(url);
  int httpResponseCode = http.GET();
  if (httpResponseCode >= 200 && httpResponseCode < 300)
  {
    String payload = http.getString();
    deserializeJson(doc, payload);
    moist_sensor = doc["moisture"].as<int>();
    Serial.print("moist_sensor = ");
    Serial.println(moist_sensor);
  }
  else
  {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
}

void GET_buzzer_sunroof()
{
  DynamicJsonDocument doc(2048);
  const String url = baseUrl + "garden/buzzer-sunroof";
  HTTPClient http;
  http.begin(url);
  int httpResponseCode = http.GET();
  if (httpResponseCode >= 200 && httpResponseCode < 300)
  {
    String payload = http.getString();
    deserializeJson(doc, payload);
    int buzzer_is_activate = doc["buzzer"].as<int>();
    int sunroof_is_open = doc["sunroof"].as<int>();
    Serial.print("buzzer_is_activate = ");
    Serial.println(buzzer_is_activate);
    Serial.print("sunroof_is_open = ");
    Serial.println(sunroof_is_open);
  }
  else
  {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
}

const char *ssid = "M";
const char *password = "leesoome123";

void Connect_Wifi()
{
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.print("OK! IP=");
  Serial.println(WiFi.localIP());
}

void GET_SPRINKLE()
{
  DynamicJsonDocument doc_sprinkle(2048);
  const String url = baseUrl + "garden/sprinkle";
  HTTPClient http;
  http.begin(url);
  int httpResponseCode = http.GET();

  if (httpResponseCode >= 200 && httpResponseCode < 300)
  {
    String payload = http.getString();
    deserializeJson(doc_sprinkle, payload);

    auto_sprinkle_1 = doc_sprinkle["sprinkle_1"]["is_auto"].as<boolean>();
    auto_sprinkle_2 = doc_sprinkle["sprinkle_2"]["is_auto"].as<boolean>();

    is_activate_sprinkle_1 = doc_sprinkle["sprinkle_1"]["is_activate"].as<boolean>();
    is_activate_sprinkle_2 = doc_sprinkle["sprinkle_2"]["is_activate"].as<boolean>();

    Serial.print("auto_sprinkle_1 = ");
    Serial.println(auto_sprinkle_1);

    Serial.print("auto_sprinkle_2 = ");
    Serial.println(auto_sprinkle_2);

    Serial.print("is_active_sprinkle_1 = ");
    Serial.println(is_activate_sprinkle_1);

    Serial.print("is_active_sprinkle_2 = ");
    Serial.println(is_activate_sprinkle_2);
    delay(500);
  }
  else
  {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
}

void setup()
{
  Serial.begin(115200);
  Connect_Wifi();
  GET_moisture();
  GET_buzzer_sunroof();
  POST_moisture();
  POST_buzzer_sunroof();
  button1.interval(25);
  button2.interval(25);
  pinMode(buzzer, OUTPUT);
  pinMode(sprinkle_1_pin, OUTPUT);
  pinMode(sprinkle_2_pin, OUTPUT);
  button1.attach(BUTTON1, INPUT_PULLUP);
  button2.attach(BUTTON2, INPUT_PULLUP);
  myservo.attach(19);
  xTaskCreatePinnedToCore(All_Switch, "All_Switch", 1000, NULL, 1, &TaskA, 0);
  xTaskCreatePinnedToCore(all_system, "all_system", 10240, NULL, 1, &TaskB, 1);
}

void loop()
{
  GET_moisture();
  GET_SPRINKLE();
  GET_buzzer_sunroof();
  POST_buzzer_sunroof();
  POST_moisture();
}