unsigned long ultrasonic_Intervalle = 450; // Intervalle de lecture du capteur ultrason
unsigned long derniere_mesure_distance = 0;
#define TRIG_PIN 6
#define ECHO_PIN 7

void setup() {
   pinMode(TRIG_PIN, OUTPUT);
   pinMode(ECHO_PIN, INPUT);
   Serial.begin(9600);
  

}

void loop()
{
   unsigned long temps_actuel = millis();
   if (temps_actuel - derniere_mesure_distance >= ultrasonic_Intervalle)
   {
    derniere_mesure_distance = temps_actuel;
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duree = pulseIn(ECHO_PIN, HIGH);
    float distance = duree * 0.034 / 2;

    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
   } 

}
