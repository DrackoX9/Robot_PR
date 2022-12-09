#include "PinChangeInterrupt.h"

#include "motorControl.h" //libreria para el control de los motores



/////////////////////////// CONTROLADOR PID //////////////////



unsigned long lastTime, sampleTime = 100;  //tiempo de muestreo
motorControl motor1(sampleTime);          //creando objetos de los motores
motorControl motor2(sampleTime);

///////////////////// COMUNICACION SERIAL ////////////////

String inputString = "";          //cadena con los datos enviados desde python
bool stringComplete = false;
const char separator = ',';
const int dataLength = 2;
double data[dataLength];        //almacena los datos una vez extraidos de la cadena 

//////////////////////MOTOR DERECHO///////////////////////////////

//// Ojo se ha invertido canales////////
const int    C1R = 2;    // Entrada de la señal A del encoder.
const int    C2R = 3;    // Entrada de la señal B del encoder.
int outValueR = 0;      //valor de la potencia del motor

//// Puente H L298N ////
const int    in1 = 7;                 
const int    in2 = 8;         
const int    enA = 6;               

volatile int countR = 0;    //contador que indica la direccion de giro
volatile int antR   = 0;
volatile int actR   = 0;

double wR = 0;              //variable de proceso
double w1Ref = 0;

//////////////////////MOTOR IZQUIERDO///////////////////////////////
const byte    C1L = A5;                  // Entrada de la señal A del encoder.
const byte    C2L = A4;                  // Entrada de la señal B del encoder.
int outValueL = 0;

//// Puente H L298N ////
const int    in3 = 9;                 
const int    in4 = 10;                 
const int    enB = 11;               

volatile int countL = 0;
volatile int antL      = 0;
volatile int actL      = 0;

double wL = 0;
double w2Ref = 0;


//////// VARIABLES PARA CALCULAR VELOCIDADES ANGULARES /////////
double constValue = 3.85; // (1000*2*pi)/R ---> R = 1980 Resolucion encoder cuadruple

//////////////////////// ROBOT /////////////////////////
double uRobot  = 0;       //velocidad lineal del robot
double wRobot  = 0;       //velocidad angular del robot
double phi = 0;           //angulo de orientacion
const double R = 0.0381; // radio de la llanta
const double d = 0.22352; // Distancia entre llantas

/////////////////////////// BATTERY /////////////////////////
// const int batteryPin = A6;
// const int buzzer = 12;


void setup()
{
  Serial.begin(9600);

  ////////////////// SINTONIA FINA PID //////////////////
  motor1.setGains(0.29, 0.05, 0.05); // sintonia para setear los valores de control de potencia

  ////////////////// Limites de señales //////////////////
  motor1.setCvLimits(255,20);//valores reales de potencia
  motor1.setPvLimits(15,0); //valores transformados de potencia

  motor2.setGains(0.29, 0.05, 0.05); // sintonia para setear los valores de control de potencia;
  ////////////////// Limites de señales //////////////////
  motor2.setCvLimits(255,20);
  motor2.setPvLimits(15,0);

  pinMode(C1R, INPUT);
  pinMode(C2R, INPUT);
  pinMode(C1L, INPUT);
  pinMode(C2L, INPUT);

  pinMode(in1, OUTPUT);       
  pinMode(in2, OUTPUT);   
  pinMode(in3, OUTPUT);       
  pinMode(in4, OUTPUT);   



  digitalWrite(in1, false);       
  digitalWrite(in2, false);   
  digitalWrite(in3, false);       
  digitalWrite(in4, false); 

  attachInterrupt(digitalPinToInterrupt(C1R), encoderR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(C2R), encoderR, CHANGE);

  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(C1L), encoderL, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(C2L), encoderL, CHANGE);             

  // /////////////////////////// BATERIA /////////////////////////
  // pinMode(buzzer,OUTPUT);
  // digitalWrite(buzzer,LOW);

  lastTime = millis();
}



void loop() {
   ////////// SI RECIBE DATOS /////////////

  if (stringComplete)     //lectura de los datos enviados desde python
  {
    for (int i = 0; i < dataLength ; i++)
    {
      int index = inputString.indexOf(separator);
      data[i] = inputString.substring(0, index).toFloat();
      inputString = inputString.substring(index + 1);
     }

    velocityMotor(data[0],data[1]); //transforma las velocidades de referencia enviadas desde python a valores reales de control

    inputString = "";
    stringComplete = false;
  }

  /////////////////// CONTROLADOR PID ////////////////
  if(millis()-lastTime >= sampleTime)
  {
    wR = (constValue*countR)/(millis()-lastTime); //transforma la lectura de los encoders en velocidad para saber la velocidad de los motores
    wL = (constValue*countL)/(millis()-lastTime);
    lastTime = millis();
    countR = 0;
    countL = 0;

    velocityRobot(wR,wL);   //obtiene la velocidad global del robot 
    phi = phi+wRobot*0.1;   //obtiene el angulo de referencia del robot

    
    // outValueR = motor1.compute(data[0],wR);
    // outValueL = motor2.compute(data[1],wL);
    outValueR = motor1.compute(w1Ref,wR);   //asigna la velocidad de los motores 
    outValueL = motor2.compute(w2Ref,wL);
    Serial.println(w1Ref);
    Serial.println(w2Ref);

    if (outValueR > 0) clockwise(in2,in1,enA,outValueR); else anticlockwise(in2,in1,enA,abs(outValueR));     
    if (outValueL > 0) anticlockwise(in3,in4,enB,outValueL); else clockwise(in3,in4,enB,abs(outValueL));

    //battery();
  }

}



/////////////// RECEPCION DE DATOS /////////////////////

void serialEvent() {        //recibe los valores enviados desde python y los asigna a una cadena de lectura
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}



void encoderR(void)
{
    antR=actR;             
    actR=PIND & 12; 

    if(antR==0  && actR== 4)  countR++;
    if(antR==4  && actR==12)  countR++;
    if(antR==8  && actR== 0)  countR++;
    if(antR==12 && actR== 8)  countR++;

    if(antR==0 && actR==8)  countR--;
    if(antR==4 && actR==0)  countR--;
    if(antR==8 && actR==12) countR--;
    if(antR==12 && actR==4) countR--;     

}

void encoderL(void)
{
    antL=actL;               
    actL=PINC & 48;                 

    if(antL==0  && actL==16)  countL++;
    if(antL==16 && actL==48)  countL++;
    if(antL==32 && actL== 0)  countL++;
    if(antL==48 && actL==32)  countL++;

    if(antL==0  && actL==32)  countL--;
    if(antL==16 && actL== 0)  countL--;
    if(antL==32 && actL==48)  countL--;
    if(antL==48 && actL==16)  countL--;

}



void clockwise(int pin1, int pin2,int analogPin, int pwm)
{

  digitalWrite(pin1, LOW); 
  digitalWrite(pin2, HIGH);     
  analogWrite(analogPin,pwm);
}



void anticlockwise(int pin1, int pin2,int analogPin, int pwm)
{
  digitalWrite(pin1, HIGH); 
  digitalWrite(pin2, LOW);     
  analogWrite(analogPin,pwm);
}



void velocityRobot(double w1, double w2)    //calculo de la velocidad global del robot 
{
  uRobot = (R*(w1+w2))/2;
  wRobot = (R*(w1-w2))/d;
}

void velocityMotor(double u, double w)  //calculo de la velocidad de cada rueda 
{
  w1Ref = (u+(d*w/2))/R;
  w2Ref = (u-(d*w/2))/R;
}