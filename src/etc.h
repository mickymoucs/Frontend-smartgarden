#include <ArduinoJson.h>
#include <HTTPClient.h>

// moist
extern int val_soil_moisture_rev;
extern int moist_sensor;

// sprinkle
extern boolean auto_sprinkle_1;
extern boolean is_activate_sprinkle_1;
extern boolean auto_sprinkle_2;
extern boolean is_activate_sprinkle_2;

// buzzer & sunroof
extern boolean buzzer_is_activate;
extern boolean sunroof_is_open;

const String baseUrl = "https://ecourse.cpe.ku.ac.th/exceed08/";

void Connect_Wifi()
{
    const char *ssid = "M";
    const char *password = "leesoome123";

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
// HARDWARE DONT GET MOISTURE

void GET_MOISTURE()
{
    DynamicJsonDocument doc(2048);
    const String url = baseUrl + "garden/moisture";
    HTTPClient http;
    http.begin(url);
    int httpResponseCode = http.GET();
    if (httpResponseCode >= 200 && httpResponseCode < 300)
    {
        Serial.print("moisture");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        deserializeJson(doc, payload);
        int ageAsInt = doc["moisture"].as<int>();
        Serial.println(ageAsInt);
    }
    else
    {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
    }
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
        Serial.print("HTTP ");
        Serial.println(httpResponseCode);
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

void GET_SUNROOF_BUZZER()
{
    DynamicJsonDocument doc(2048);
    const String url = baseUrl + "garden/buzzer-sunroof";
    HTTPClient http;
    http.begin(url);
    int httpResponseCode = http.GET();
    if (httpResponseCode >= 200 && httpResponseCode < 300)
    {
        Serial.print("buzzer-sunroof");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        deserializeJson(doc, payload);
        int buzzer = doc["buzzer"].as<int>();
        int sunroof = doc["sunroof"].as<int>();
        Serial.println(buzzer);
        Serial.println(sunroof);
    }
    else
    {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
    }
}

void POST_MOISTURE()
{
    String json;
    DynamicJsonDocument doc(2048);
    doc["moisture_value"] = 1000;
    serializeJson(doc, json);

    const String url = baseUrl + "update/moisture";
    HTTPClient http;
    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(json);
    if (httpResponseCode >= 200 && httpResponseCode < 300)
    {
        Serial.print("POST");
        Serial.println(httpResponseCode);
    }
    else
    {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
    }
}

void POST_BUZZER_SUNROOF()
{
    ;
}