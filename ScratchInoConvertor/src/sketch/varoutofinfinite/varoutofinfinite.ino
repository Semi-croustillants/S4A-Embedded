#include <ARTK.h>
void consumer1() {
   int lol = 0;
   while(1){
      lol = 1;
      ARTK_Sleep(1000);
      lol = 2;
      ARTK_Sleep(1000);
   }
}
void consumer2() {
3;
   while(1){
      lol = 4;
      ARTK_Sleep(1000);
      lol = 5;
      ARTK_Sleep(1000);
   }
}
void SetupARTK() {
   ARTK_SetOptions(0) ;
   ARTK_CreateTask(consumer1);
   ARTK_CreateTask(consumer2);
}
