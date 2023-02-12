#include <Arduino.h>
#include <Bounce2.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>
#define analog_Pin 32
#define BUTTON1 27 // for trun on servo and bozer
Servo myservo;
TaskHandle_t TaskA = NULL;
TaskHandle_t TaskB = NULL;
Bounce button1 = Bounce();
boolean statu_post = true;
int buzzer = 12;
int sprinkle_1_pin = 33;
int sprinkle_2_pin = 25;
int LED_MODE = 26;
int val_soil_moisture = 0;
int count_for_sunroof = 0;
int counT_manual_action = 0;
void auto_watering_system();
void insect_repellent();
void soil_moisture_detection();
void sunroof_control();
void GET_buzzer_sunroof();
void POST_moisture();
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
boolean sunroof_is_open_befor = sunroof_is_open;
boolean buzzer_is_activate_befor = buzzer_is_activate;

const String baseUrl = "https://ecourse.cpe.ku.ac.th/exceed08/";

void POST_buzzer_sunroof()
{
  statu_post = false;
  String json;
  DynamicJsonDocument doc(2048);
  doc["buzzer"] = buzzer_is_activate;
  doc["sunroof"] = sunroof_is_open;
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
    if (button1.fell() &&  statu_post)
    {
      Serial.print("statu_post_in if= ");
      Serial.println(statu_post);
      sunroof_is_open = !sunroof_is_open;
    }
    vTaskDelay(1 / portTICK_PERIOD_MS);
  }
}
void all_system(void *param)
{
  while (1)
  {
    if (buzzer_is_activate) // ถ้าเปิดเสียงต้องปิดsunroof
    {
      Serial.println("turn on buzzer");
      sunroof_is_open = false;
      myservo.write(90);
      vTaskDelay(10 / portTICK_PERIOD_MS);
      insect_repellent();
      vTaskDelay(10 / portTICK_PERIOD_MS);
    }
    if (!buzzer_is_activate) // ถ้าปิดเสียงแล้วจะเปิดหรือปิด sunroof ก็ได้
    {
      if (sunroof_is_open)
      {
        myservo.write(0);
        // Serial.println("Servo->0");
        vTaskDelay(100 / portTICK_PERIOD_MS);
        if (auto_sprinkle_1)
        {
          if (val_soil_moisture < moist_sensor)
          {
            digitalWrite(sprinkle_1_pin, HIGH);
          }
          else
          {
            digitalWrite(sprinkle_1_pin, LOW);
          }
        }
        if (auto_sprinkle_2)
        {
          if (val_soil_moisture < moist_sensor)
          {
            digitalWrite(sprinkle_2_pin, HIGH);
          }
          else
          {
            digitalWrite(sprinkle_2_pin, LOW);
          }
        }
        if (!auto_sprinkle_1)
        {
          digitalWrite(sprinkle_1_pin, is_activate_sprinkle_1);
        }
        if (!auto_sprinkle_2)
        {
          digitalWrite(sprinkle_2_pin, is_activate_sprinkle_2);
        }
      }
      else
      {
        digitalWrite(sprinkle_1_pin, LOW);
        digitalWrite(sprinkle_2_pin, LOW);
        sunroof_is_open = false; // ปิดฝา
        myservo.write(90);
        // Serial.println("server ->0 ");
        vTaskDelay(100 / portTICK_PERIOD_MS);
      }
    }
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
    moist_sensor = doc["moist_default"].as<int>();
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
    buzzer_is_activate = doc["buzzer"].as<boolean>();
    sunroof_is_open = doc["sunroof"].as<boolean>();
    Serial.print("buzzer_is_activate_befor = ");
    Serial.println(buzzer_is_activate_befor);
    Serial.print("buzzer_is_activate = ");
    Serial.println(buzzer_is_activate);
    Serial.print("sunroof_is_open_befor = ");
    Serial.println(sunroof_is_open_befor);
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
  POST_buzzer_sunroof;
  button1.interval(25);
  pinMode(buzzer, OUTPUT);
  pinMode(sprinkle_1_pin, OUTPUT);
  pinMode(sprinkle_2_pin, OUTPUT);
  pinMode(LED_MODE, OUTPUT);
  button1.attach(BUTTON1, INPUT_PULLUP);
  myservo.attach(19);
  xTaskCreatePinnedToCore(All_Switch, "All_Switch", 10240, NULL, 1, &TaskA, 1);
  xTaskCreatePinnedToCore(all_system, "all_system", 10240, NULL, 1, &TaskB, 0);
}

void loop()
{ statu_post=false;
  int count_krean = 0;
  GET_moisture();
  GET_SPRINKLE();
  POST_moisture();
  digitalWrite(LED_MODE, LOW);
  GET_buzzer_sunroof();
  digitalWrite(LED_MODE, HIGH);
  statu_post=true;
  delay(2000);
  digitalWrite(LED_MODE, LOW);
  if (((buzzer_is_activate_befor != buzzer_is_activate) || (sunroof_is_open_befor != sunroof_is_open)))
  { statu_post=false;
    Serial.println("stop");
    POST_buzzer_sunroof();
    Serial.println("update_post");
    sunroof_is_open_befor = sunroof_is_open;
    buzzer_is_activate_befor = buzzer_is_activate;
    digitalWrite(LED_MODE, LOW);
    delay(1000);
  }
}
