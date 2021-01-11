#include <AccelStepper.h>
#include <EEPROM.h> 

/**

 CODIGO DE MOVIMENTACAO DE MESA DE IMPRESSORA 3D USANDO CNC SHIELD
 MOVIMENTOS NO EIXO X E Y NO INTERVALO DE 0 A 30 CM
 SENSORES DE PARADA NA POSICAO 0 E PERSISTENCIA DA POSICAO NA EEPROM

 RECEBE NA PORTA SERIAL UMA MENSAGEM TIPO 'M-1-1-30', ONDE: 
 M : ACAO DE MOVIMENTO
 1 : MOTOR A SER ACIONADO (1 : EIXO X , 2 : EIXO Y)
 1 : SENTIDO DO MOVIMENTO NO CARTESIANO ( 1 : SENTIDO POSITIVO, 0: SENTIDO NEGATIVO )
 30: QUANTIDADE DE MOVIMENTO EM CENTIMETROS

 **/

AccelStepper stepper1(1, 2 ,5);
AccelStepper stepper2(1, 3 ,6);


int distancia_um_centimetro = 51.282051282;


int e_AddressX  = 0;
int e_AddressY  = 512;

int x_sensor = 9;
int y_sensor = 10;
int z_sensor = 11;

String action;
String axis;
String direct;
String value;

int LIMIT = 30;

void setup()
{ 
    Serial.begin(115200);

    pinMode(x_sensor, INPUT_PULLUP);
    pinMode(y_sensor, INPUT_PULLUP);
    pinMode(z_sensor, INPUT_PULLUP);

    stepper1.setMaxSpeed(8000.0);
    stepper1.setAcceleration(8000.0);
   
    stepper2.setMaxSpeed(7000.0);
    stepper2.setAcceleration(7000.0);

    if(digitalRead(x_sensor) == 1 || EEPROM.read(e_AddressX) > 30)
    {
      EEPROM.write(e_AddressX, 0);
    }

    if(digitalRead(y_sensor) == 1 || EEPROM.read(e_AddressY) > 30)
    {
      EEPROM.write(e_AddressY, 0);
    }

}


void stopX()
{
  stepper1.stop();
  stepper1.setCurrentPosition(0);
  stepper1.move(0);
  EEPROM.write(e_AddressX, 0);
}

void stopY()
{
  stepper2.stop();
  stepper2.setCurrentPosition(0);
  stepper2.move(0);
  EEPROM.write(e_AddressY, 0);
}



void setRun(){
  
  if (axis == "1" && direct == "0")
  {  
      if(digitalRead(x_sensor) == 1)
      {
        stopX();
        Serial.println(EEPROM.read(e_AddressX));
         
      }
      else
      {
        int dist = value.toInt();
        stepper1.move(-dist * distancia_um_centimetro);
        EEPROM.write(e_AddressX, EEPROM.read(e_AddressX) - dist);
        Serial.println(EEPROM.read(e_AddressX));
      }
      
    }

  if (axis == "1" && direct == "1")
    {  
      if(EEPROM.read(e_AddressX) < LIMIT)
      {
       int dist = value.toInt();
       
       // verifica se a quantidade de movimento é maior que o limite da mesa
       // se for irá movimentar apenas a distancia que falta para atigir o limite  
       if(dist + EEPROM.read(e_AddressX) > 30){
        dist = 30 - EEPROM.read(e_AddressX);
       }
       
       stepper1.move(dist * distancia_um_centimetro);
       EEPROM.write(e_AddressX, EEPROM.read(e_AddressX) + dist);
       Serial.println(EEPROM.read(e_AddressX));
      }
      else
      {
        Serial.println(EEPROM.read(e_AddressX));
      }   
    }




    if (axis == "2" && direct == "0")
  {  
      if(digitalRead(y_sensor) == 1)
      {
        stopY();
        Serial.println(EEPROM.read(e_AddressY));
         
      }
      else
      {
        int dist = value.toInt();
        stepper2.move(-dist * distancia_um_centimetro);
        EEPROM.write(e_AddressY, EEPROM.read(e_AddressY) - dist);
        Serial.println(EEPROM.read(e_AddressY));
      }
      
    }

  if (axis == "2" && direct == "1")
    {  
      if(EEPROM.read(e_AddressY) < LIMIT)
      {
       int dist = value.toInt();
       // verifica se a quantidade de movimento é maior que o limite da mesa
       // se for irá movimentar apenas a distancia que falta para atigir o limite  
       if(dist + EEPROM.read(e_AddressY) > 30){
          dist = 30 - EEPROM.read(e_AddressY);
        }
       stepper2.move(dist * distancia_um_centimetro);
       EEPROM.write(e_AddressY, EEPROM.read(e_AddressY) + dist);
       Serial.println(EEPROM.read(e_AddressY));
      }
      else
      {
        Serial.println(EEPROM.read(e_AddressY));
      }   
    }

   
}


void leStringSerial()
{
  
  char caracter;
  int i = 0;
  String val;
  
  while(Serial.available() > 0)
  {
    caracter = Serial.read();
    if(caracter != '\n'){
      if(i == 0)
      {
        action = caracter;
      }
      else if(i == 2)
      {
        axis = caracter;
      }
      else if(i == 4)
      {
        direct = caracter;
      }
      else if( i == 6 || i == 7)
      {
        val.concat(caracter);
        value = val;
      }
    }
    delay(10);
    i = i + 1;
  }

  setRun();
}


void loop()
{

    if(Serial.available()>0)
    {
      leStringSerial();
    }
     
      stepper1.run();
      stepper2.run();     
}
