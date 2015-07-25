#include <ARTK.h>
void consumer1() {
   while(1){
      Printf("0 x DEADBEEF\n");
if ( ( digitalRead( 6 ) ) && ( digitalRead( 8 ) ) ) {
            digitalWrite( 7, HIGH );
      }
      else {
            digitalWrite( 7, LOW );
      }
      ARTK_Yield();
   }
}
void consumer2() {
   while(1){
      Printf("0 x DEADBEEF\n");
      digitalWrite( 5, HIGH );
      ARTK_Sleep(100.0);
      digitalWrite( 5, LOW );
      ARTK_Sleep(100.0);
   }
}
void Setup() {
   ARTK_SetOptions(0, 10) ;
   ARTK_CreateTask(consumer1);
   ARTK_CreateTask(consumer2);
}
