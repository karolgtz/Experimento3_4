#include <NewPing.h>

#define TRIGGER 5         // pin D1 en la placa del ESP8266
#define ECHO    4         // pin D2  en la placa del ESP8266
#define MAX_DISTANCE 200  // Configurar a máximo 2 metros

// Crear un objeto "sonar" para el manejo del sensor
NewPing sonar(TRIGGER, ECHO, MAX_DISTANCE);

// Declarar variable para el comando recibido desde puerto serial (python)
byte comando = 0;

// Declarar variable para el tiempo de espera enntre cada lectura
int TiempoEspera=1;
int dist1=0;
int dist2=0;
float veli0=0;
float veli1=0;
float veli2=0;
float veli3=0;
float veli4=0;

float medirdistancia(){
      // Obtener medicion de tiempo de viaje del sonido y guardar en variable uS
    int uS = sonar.ping_median();
    // Calcular la distancia d como la relación entre el tiempo uS y la velocidad de propagación 
    float d = ( uS / US_ROUNDTRIP_CM );
    return(d);
}
void setup() // Built-in initialization block
{
  Serial.begin(115200);
}

void loop() {// Main loop auto-repeats
 // if (Serial.available() > 0) {   // Hay datos recibidos?
    // Leer el comando
    //comando = Serial.read(); //leer el comando recibido
  
  //if (comando == 101)      // si el comando es "e" entonces enviar la distancia medida
    comando=Serial.read();
    if (comando==97){
    dist1=medirdistancia();
    delay(756);
    dist2=medirdistancia();
    veli0=(dist1-dist2)/0.756;
    Serial.println(veli0);
   }

      if (comando==98){
    dist1=medirdistancia();
    delay(756);
    dist2=medirdistancia();
    veli0=(dist1-dist2)/0.756;
    Serial.println(veli0);
   }


       if (comando==99){
    dist1=medirdistancia();
    delay(756);
    dist2=medirdistancia();
    veli0=(dist1-dist2)/0.756;
    Serial.println(veli0);
   }


       if (comando==100){
    dist1=medirdistancia();
    delay(756);
    dist2=medirdistancia();
    veli0=(dist1-dist2)/0.756;
    Serial.println(veli0);
   }


    if (comando==101){
    dist1=medirdistancia();
    delay(756);
    dist2=medirdistancia();
    veli0=(dist1-dist2)/0.756;
    Serial.println(veli0);
   }  
  
  // Esperar
  delay(TiempoEspera);
}
