#include <AccelStepper.h>
#include <EEPROM.h> 

/**

 CODIGO DE MOVIMENTACAO DE MESA DE IMPRESSORA 3D USANDO CNC SHIELD
 MOVIMENTOS NO EIXO X E Y NO INTERVALO DE 0 A 30 CM
 SENSORES DE PARADA NA POSICAO 0 E PERSISTENCIA DA POSICAO NA EEPROM

 **/

AccelStepper stepper1(1, 2 ,5);
AccelStepper stepper2(1, 3 ,6);


int distancia_um_centimetro = 51.282051282;
int distancia_cinco_centimetros = 256.41025641;  
int distancia_dez_centimetros = 512.820512821; 

int e_AddressX  = 0;
int e_AddressY  = 512;

int positionX = 0;
int positionY = 0;

int x_sensor = 9;
int y_sensor = 10;
int z_sensor = 11;




void setup()
{ 
    Serial.begin(9600);

    pinMode(x_sensor, INPUT_PULLUP);
    pinMode(y_sensor, INPUT_PULLUP);
    pinMode(z_sensor, INPUT_PULLUP);

    stepper1.setMaxSpeed(8000.0);
    stepper1.setAcceleration(8000.0);
    //stepper1.moveTo(movement);
   
    stepper2.setMaxSpeed(8000.0);
    stepper2.setAcceleration(8000.0);
    
    positionX = EEPROM.read(e_AddressX);
    positionY = EEPROM.read(e_AddressY);
    //stepper2.moveTo(movement);
}

char inBuffer = "";

void stopX()
{
  stepper1.stop();
  stepper1.setCurrentPosition(0);
  stepper1.move(0);
  positionX = 0;
  EEPROM.write(e_AddressX, positionX);
}


void stopY()
{
  stepper2.stop();
  stepper2.setCurrentPosition(0);
  stepper2.move(0);
  positionY = 0;
  EEPROM.write(e_AddressY, positionY);
}


void loop()
{

    if(Serial.available()>0)
    {
      inBuffer = Serial.read();
    }

     ////////////////////////////////////////////////////////////////////
    //                      MOVIMENTOS NO EIXO X                      //
   ////////////////////////////////////////////////////////////////////
   /**
   *        VOCABULARY
   *        a = axis:x , distance: -10
   *        b = axis:x , distance: 10
   *        c = axis:x , distance: -5
   *        d = axis:x , distance: 5
   *        e = axis:x , distance: -1
   *        f = axis:x , distance: 1
   *        
   **/
   
    if (inBuffer == 'a')
    {
      
      if(digitalRead(x_sensor) == 1)
      {
        stopX();
      }
      else
      {
        if(positionX >= 10)
        {
          stepper1.move(-distancia_dez_centimetros);
          positionX = positionX - 10;
          EEPROM.write(e_AddressX, positionX);
        }
      }
    }

    if (inBuffer == 'b')
    {  
       if(positionX < 30)
       {
           stepper1.move(distancia_dez_centimetros);
           positionX = positionX + 10;
           EEPROM.write(e_AddressX, positionX);
       } 
    }

    if (inBuffer == 'c')
    {
      
      if(digitalRead(x_sensor) == 1)
      {
        stopX();
      }
      else
      {
        if(positionX >= 5)
        {
          stepper1.move(-distancia_cinco_centimetros);
          positionX = positionX - 5;
          EEPROM.write(e_AddressX, positionX); 
        } 
      }
    }

    if (inBuffer == 'd')
    {  
       if(positionX < 30)
       {
           stepper1.move(distancia_cinco_centimetros);
           positionX = positionX + 5;
           EEPROM.write(e_AddressX, positionX);
       } 
    }

    if (inBuffer == 'e')
    {
      
      if(digitalRead(x_sensor) == 1)
      {
        stopX();
      }
      else
      {
        if(positionX >= 1)
        {
          stepper1.move(-distancia_um_centimetro);
          positionX = positionX - 1;
          EEPROM.write(e_AddressX, positionX);
        }  
      }
    }

    if (inBuffer == 'f')
    {  
       if(positionX < 30)
       {
           stepper1.move(distancia_um_centimetro);
           positionX = positionX + 1;
           EEPROM.write(e_AddressX, positionX);
       } 
    }

  
     ////////////////////////////////////////////////////////////////////
    //                      MOVIMENTOS NO EIXO Y                      //
    ///////////////////////////////////////////////////////////////////
    /**
     *        VOCABULARY
     *        g = axis:y , distance: -10
     *        h = axis:y , distance: 10
     *        i = axis:y , distance: -5
     *        j = axis:y , distance: 5
     *        k = axis:y , distance: -1
     *        l = axis:x , distance: 1
     *        
     **/
    
    if (inBuffer == 'g')
    {
      
      if(digitalRead(y_sensor) == 1)
      {
        stopY();
      }
      else
      {
        if(positionY >= 10)
        {
          stepper2.move(-distancia_dez_centimetros);
          positionY = positionY - 10;
          EEPROM.write(e_AddressY, positionY);
        }
      }
    }

    if (inBuffer == 'h')
    {  
       if(positionY < 30)
       {
           stepper2.move(distancia_dez_centimetros);
           positionY = positionY + 10;
           EEPROM.write(e_AddressY, positionY);
       } 
    }

    if (inBuffer == 'i')
    {
      
      if(digitalRead(y_sensor) == 1)
      {
        stopY();
      }
      else
      {
        if(positionY >= 5)
        {
          stepper2.move(-distancia_cinco_centimetros);
          positionY = positionY - 5;
          EEPROM.write(e_AddressY, positionY); 
        } 
      }
    }

    if (inBuffer == 'j')
    {  
       if(positionY < 30)
       {
           stepper2.move(distancia_cinco_centimetros);
           positionY = positionY + 5;
           EEPROM.write(e_AddressY, positionY);
       } 
    }

    if (inBuffer == 'k')
    {
      
      if(digitalRead(y_sensor) == 1)
      {
        stopY();
      }
      else
      {
        if(positionY >= 1)
        {
          stepper2.move(-distancia_um_centimetro);
          positionY = positionY - 1;
          EEPROM.write(e_AddressY, positionY);
        }  
      }
    }

    if (inBuffer == 'l')
    {  
       if(positionY < 30)
       {
           stepper2.move(distancia_um_centimetro);
           positionY = positionY + 1;
           EEPROM.write(e_AddressY, positionY);
       } 
    }

    

    // CONTROL RUN

     if(inBuffer == 'a' && positionX == 0 )
     {
          
     }
     else
     {
       stepper1.run();
     }

     if(inBuffer == 's' && positionY == 0 )
     {
          
     }
     else
     {
       stepper2.run();
     }
          
    inBuffer = ""; 
    
}
