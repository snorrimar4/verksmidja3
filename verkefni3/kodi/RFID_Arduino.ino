
#include "SPI.h"
#include "MFRC522.h"

#define SS_PIN 10
#define RST_PIN 9
#define LED_PIN 8 
#define LED_PIN 7

MFRC522 rfid(SS_PIN, RST_PIN);

MFRC522::MIFARE_Key key;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT);
  Serial.println("I am waiting for card...");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial())
    return;

  // Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  // Serial.println(rfid.PICC_GetTypeName(piccType));

  // Check is the PICC of Classic MIFARE type
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
      piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
      piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }
  String strID = "";
  for (byte i = 0; i < 4; i++) {
    strID +=
      (rfid.uid.uidByte[i] < 0x10 ? "0" : "") +
      String(rfid.uid.uidByte[i], HEX) +
      (i != 3 ? ":" : "");
  }

  strID.toUpperCase();
  Serial.print("Tap card key: ");
  Serial.println(strID);
  delay(1000);

  if (strID.indexOf("7C:DB:CF:38") >= 0) {  //put your own tap card key;
    Serial.println("********************");
    Serial.println("**Authorised acces**");
    Serial.println("********************");
    digitalWrite(8, HIGH);
    delay (5000);
    digitalWrite(8, LOW);
    return;
  }
  else {
    Serial.println("****************");
    Serial.println("**Acces denied**");
    Serial.println("****************");
    digitalWrite(7, HIGH);
    delay (5000);
    digitalWrite(7, LOW);
    return;
  }
  
}
