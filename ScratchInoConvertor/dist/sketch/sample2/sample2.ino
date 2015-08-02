#include <ARTK.h>
void consumer1() {
   while(1){
      Printf("0 x DEADBEEF\n");
if ( digitalRead( 3 ) ) {
            digitalWrite( 2, HIGH );
      }
      else {
            digitalWrite( 2, LOW );
      }
      ARTK_Yield();
   }
}
void consumer2() {
   while(1){
      Printf("0 x DEADBEEF\n");
      ARTK_Sleep(100.0);
      digitalWrite( 7, HIGH );
      ARTK_Sleep(100.0);
      digitalWrite( 7, LOW );
   }
}
void Setup() {
   pinMode( 3, INPUT );
   pinMode( 2, OUTPUT );
   pinMode( 7, OUTPUT );
   ARTK_SetOptions(0, 10) ;
   ARTK_CreateTask(consumer1);
   ARTK_CreateTask(consumer2);
}
