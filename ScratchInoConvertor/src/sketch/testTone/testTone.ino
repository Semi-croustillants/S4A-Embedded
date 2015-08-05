#include <ARTK.h>
#include <Servo.h>
Servo myservo6;
float note;
void consumer1() {
   while(1){
      if ( ( note * ( 3 + note ) )<note ) {
         note = 1315.5;
         tone( 6, 10 );
         notone( 6 );
         myservo6.write( note );
         note = ( note + 10 );
      }
      ARTK_Yield();
   }
}
void SetupARTK() {
   pinMode( 6, OUTPUT );
   myservo6.attach(6);
   ARTK_SetOptions(0) ;
   ARTK_CreateTask(consumer1);
}
