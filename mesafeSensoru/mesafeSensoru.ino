#include <Arduino.h>

const int trigPin = 9;  // Ultrasonik sensör trig pin
const int echoPin = 10; // Ultrasonik sensör echo pin
const int motorPin = 3; // Motor pin (şimdilik simüle)
const int buzzerPin = 2; // Zil pin (şimdilik simüle)
const long detectionDelay = 15000; // 15 saniye (milisaniye cinsinden)

const int distanceThreshold = 20; // Mesafe eşiği (cm cinsinden)

void setup() {
  Serial.begin(9600); // Seri haberleşme başlat
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(motorPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  
  Serial.print("Belirtilen mesafe eşiği: ");
  Serial.println(distanceThreshold);
}

void loop() {
  long duration, distance;
  
  // Ultrasonik sensör ölçümü
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; // Mesafeyi cm olarak hesapla

  if (distance < distanceThreshold) { // Engel mesafe eşiğinden daha yakınsa
    Serial.println("Engel algılandı! Motor durdu ve zil çalmaya başladı.");
    digitalWrite(motorPin, LOW); // Motoru durdur

    unsigned long startTime = millis(); // Engel algılama başlangıç zamanı
    int secondsPassed = 0; // Geçen saniyeleri saymak için sayaç

    while (millis() - startTime < detectionDelay) {
      // Buzzer'ı kısa süreliğine açıp kapat
      digitalWrite(buzzerPin, HIGH);
      delay(100); // 0.1 saniye açık tut
      digitalWrite(buzzerPin, LOW);
      delay(100); // 0.1 saniye kapalı tut

      // Engel hala mevcut mu kontrol et
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      duration = pulseIn(echoPin, HIGH);
      distance = duration * 0.034 / 2;

      // Her saniye bir kere güncellenir
      if (millis() - startTime >= (secondsPassed + 1) * 1000) {
        secondsPassed++;
        Serial.print("Geçen saniye: ");
        Serial.println(secondsPassed);
      }

      if (distance >= distanceThreshold) { // Engel kalkmışsa
        Serial.println("Engel kalktı! Yoluna devam ediyor.");
        digitalWrite(buzzerPin, LOW); // Zili kapat
        digitalWrite(motorPin, HIGH); // Motoru çalıştır
        break;
      }
    }

    if (distance < distanceThreshold) { // 15 saniye sonunda engel hala mevcutsa
      Serial.println("Engel hala mevcut! Manevra yapılıyor.");
      // Manevra işlemleri burada yapılacak
    }
  } else {
    Serial.println("Yol açık. Araç hareket halinde.");
    digitalWrite(motorPin, HIGH); // Motoru çalıştır
  }
  
  delay(100); // Döngü tekrarını yavaşlat
}
