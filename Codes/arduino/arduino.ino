void setup() {
  Serial.begin(9600);
}

void loop() {
  float ir = random(30, 80) / 100.0;
  float dielectric = random(100, 200) / 10.0;
  float moisture = random(600, 800) / 10.0;

  Serial.print(ir);
  Serial.print(",");
  Serial.print(dielectric);
  Serial.print(",");
  Serial.println(moisture);

  delay(2000);
}
