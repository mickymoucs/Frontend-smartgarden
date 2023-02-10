#include <Arduino.h>
#include <Bounce2.h>
#define BUTTON1 27 // for trun on servo and bozer
#define BUTTON2 26
TaskHandle_t TaskA = NULL;
TaskHandle_t TaskB = NULL;
Bounce button1 = Bounce();
Bounce button2 = Bounce();

int buzzer = 12;
int status_button1 = 0;
int status_button2 = 0;
int sprinkle_1_pin = 33;
int sprinkle_2_pin = 25;
int analog_Pin = 15;
int val_soil_moisture = 0;

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

void All_Switch(void *param)
{
  while (1)
  {
    button1.update();
    if (button1.fell())
    {
      status_button1 = !status_button1;
      Serial.println(status_button1);
    }
    vTaskDelay(2 / portTICK_PERIOD_MS);
    button2.update();
    if (button2.fell())
    {
      status_button2 = !status_button2;
      Serial.println(status_button2);
    }
    if (status_button1)
    {
      // sunroof_control();
      insect_repellent();
    }
    vTaskDelay(2 / portTICK_PERIOD_MS);
  }
}

void update_soil_moisture_detection(void *param)
{
  while (1)
  { //GET
    vTaskDelay(1 / portTICK_PERIOD_MS);
    soil_moisture_detection();
    vTaskDelay(1 / portTICK_PERIOD_MS);
    //POST
    vTaskDelay(1 / portTICK_PERIOD_MS);

  }
}

void setup()
{
  Serial.begin(115200);
  button1.interval(25);
  button2.interval(25);
  pinMode(buzzer, OUTPUT);
  pinMode(sprinkle_1_pin, OUTPUT);
  pinMode(sprinkle_2_pin, OUTPUT);
  button1.attach(BUTTON1, INPUT_PULLUP);
  button2.attach(BUTTON2, INPUT_PULLUP);
  xTaskCreatePinnedToCore(All_Switch, "All_Switch", 1000, NULL, 1, &TaskA, 0);
  xTaskCreatePinnedToCore(update_soil_moisture_detection, "update_soil_moisture_detection", 1000, NULL, 1, &TaskB, 1);
}

void auto_watering_system()
{
  if (status_button2 == 0 && val_soil_moisture<80)
  {
    user_ignore = 1;
  }
  else if (val_soil_moisture > 50)
  { 
    digitalWrite(sprinkle_1_pin, HIGH);
    digitalWrite(sprinkle_2_pin, HIGH);
    status_button2=1;
  }
  else
  {
    digitalWrite(sprinkle_1_pin, LOW);
    digitalWrite(sprinkle_2_pin, LOW);
  }
  delay(1);
}

void manual_waterong_system() // ปิดเปิดเอง
{
  if (val_soil_moisture >= 80) // ความชื้นน้อยมากๆ
  {
    user_ignore = 0;
  }
  else if (status_button2)
  {
    digitalWrite(sprinkle_1_pin, HIGH);
    digitalWrite(sprinkle_2_pin, HIGH);
  }
  else
  {
    digitalWrite(sprinkle_1_pin, LOW);
    digitalWrite(sprinkle_2_pin, LOW);
  }
  delay(1);
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
  val_soil_moisture = map(analogRead(analog_Pin), 1200, 4096, 0, 100);
  Serial.print("val_soil_moisture = ");
  Serial.println(val_soil_moisture);
}

void sunroof_control() // ควบคุมการเปิด-ปิดฝา
{
}

void loop()
{
  if (user_ignore)
  {
    manual_waterong_system();
  }
  else
  {
    auto_watering_system();
  }
}