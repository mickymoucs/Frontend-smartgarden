
    if (auto_sprinkle_1)
    {
      if (val_soil_moisture > 50)
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
    else if (val_soil_moisture >= 80) // ความชื้นน้อยมากๆ
    {
      is_activate_sprinkle_1 = !is_activate_sprinkle_1;
    }
    else
    {
      
    }