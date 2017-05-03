#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
 char t[12][6];
 int col=0,rot=3,fc=0,fl=0,ac=0;
 bool change=false;
 int num[12][6];
 int colA[8],colB[8],action[8],rota[8];
 int trou[6];
 int sur[6];
 bool end=false;
 int futur[8];
void converture(){
    
  for(int i=0;i<12;i++){
      
    for(int j=0;j<6;j++){
        if(t[i][j]=='.'){
            num[i][j]=0;
        }else if(t[i][j]=='0'){
             num[i][j]= -1;
        }else if(t[i][j]=='1'){
             num[i][j]=1;
        }else if(t[i][j]=='2'){
             num[i][j]=2;
        }else if(t[i][j]=='3'){
             num[i][j]=3;
        }else if(t[i][j]=='4'){
             num[i][j]=4;
        }else if(t[i][j]=='5'){
             num[i][j]=5;
        }
        //fprintf(stderr, "%d  i:%d j:%d",num[i][j],i,j);
    }
    // fprintf(stderr, "\n");
  }
}

void  getFirst(){
    
    for(int i=11;i>=0;i--){ 
     for(int j=0;j<6;j++){
         if(num[i][j]==0){
           fc=j;fl=i;  
            i=-1;j=6;
        }
    }
    
 }
 //fprintf(stderr, "%d %d\n",fc,fl);
}
int eval(){
    int s=0,t=0;
    for(int i=1;i<11;i++){
    for(int j=1;j<5;j++){
        t=num[i][j];
      if(!(t==num[i][j+1]&&t==num[i][j-1]
          && t==num[i+1][j]  &&t==num[i-1][j] || t==-1) ||
      !( i>1 && t==num[i][j+1]&&t==num[i][j-1]
      && t==num[i+1][j]  &&t==num[i-1][j] &&num[i-2][j] || t==-1)||
      !(i<10 && t==num[i][j+1]&&t==num[i][j-1]
      && t==num[i+1][j]  &&t==num[i-1][j] &&num[i+2][j] || t==-1)||
      !(t==num[i][j+1]&&t==num[i][j-1]
      && t==num[i+1][j])||
      !(t==num[i][j+1]&&t==num[i][j-1])||
      !(t==num[i][j+1]&&t==num[i][j-1]))
        s+=num[i][j];
    }
    
 }
 return s;
}

int firstLine(){
    int r=11,k=1;
    for(int i=0;i<12;i++){
     for(int j=0;j<6;j++){
         if(num[i][j]==0){k++; }
     }
     if(k==6 && i<11){r=i-1;i=12;}
     k=1;
    }
    return r;
}

int lastLine(){
    int r=11,k=1;
    for(int i=0;i<12;i++){
     for(int j=0;j<6;j++){
         if(num[i][j]!=0){k++; }
     }
     if(k==6 && i<11){r=i;i=12;}
     k=1;
    }
    return r;
}
int videIV(){
    int v=-1;
     converture();
     for(int i=11;i>=0;i--){
        if(num[i][0]==0) {v=0;i=-1;}
         else if(num[i][5]==0){
          v=5; i=-1;   
        }
     }
     return v;
}
void tt(int x,int y){
    
    int l=firstLine(),k=0,n,m;

    for(int i=0;i<12;i++){
     for(int j=0;j<6;j++){
         
         if(num[i][j]==x && num[i-1][j]==0 && i>0){
            rot=1;
            col=j;
         }else if(num[i][j]==y && num[i-1][j]==0 && i>0){
             rot=3;
             col=j;
         }else if(num[i][j]==x && num[i][j-1]==0 && j>0 && num[i+1][j-1]!=0 ){
             rot=1;
             col=j-1;
         }else if(num[i][j]==y && num[i][j-1]==0 && j>0 && num[i+1][j-1]!=0 ){
             rot=3;
             col=j-1;
         }else if(j<5 && i<10 && x==y && num[i][j]==y && num[i+1][j]==y && num[i+2][j+1]!=0){
             rot=3;
             col=j+1;
         } else if(i>0 && j<5 && x==y && num[i][j]==y && num[i][j+1]==y 
                                && num[i-1][j]==0 && num[i-1][j+1]==0){
             rot=2;
             col=j;
         }else{
            if(num[i][j]==0){
                k=eval();
                num[i][j]=x;
               
                if(k>eval()){
                    col=j;
                    rot=3;
                }else{
                    num[i][j]=y;
                    if(k>eval()){
                     col=j;
                     rot=3;
                    }
                }
               num[i][j]=0;  
         }      
     }
    }
   }
}
void classer(int x,int y){
    
    int v=eval(),tmp=0,n,m;
    bool c=false;
    int l=firstLine(),la=lastLine();
    col=fc;
    if(col<5 && col>0)rot=col%3;
    else if(col==0)rot=1;
    else rot=3;
    converture();
    getFirst();
    int i=l-1,j=fc;
    while(i>=l  && j<6 && i<la){
     while(j<5){
         la=lastLine();
            //fprintf(stderr, "%d  %d ",i,j);
      if(x!=y){
             //rot=0
           if(j>0 && (num[i][j]==0 && num[i][j+1]==0) ){
               num[i][j]=x; num[i][j+1]=y;
               tmp=eval();
               if(tmp<v){
                   rot=0;
                   col=j;
                   j=6;i=0;
               } 
               num[i][j]=0;num[i][j+1]=0;   
            }
            //rot 2
            if(j>0 &&j<6  && num[i][j-1]==0 && num[i][j]==0  ){
               num[i][j]=x; num[i][j-1]=y;
               tmp=eval();
               if(tmp<v){            
                   rot=2;
                   col=j;
                   j=6;i=0;  
               }
                num[i][j]=0;num[i][j-1]=0;
            }
            //rot=1
            if(j<6 &&num[i][j]==0){
               num[i][j]=x; num[i-1][j]=y;
               tmp=eval();
               if(tmp<v){
                   rot=1;col=j;
                  // fprintf(stderr, "%d  %d ",col,rot);
                   j=6;i=0;
               }
                num[i][j]=0;num[i][j-1]=0;  
            }
            //rot=3
            if( j<6 && num[i][j]==0){
               num[i][j]=y; num[i-1][j]=x;
               tmp=eval();
               if(tmp<v){
                   rot=3;col=j;
                 //  fprintf(stderr, "%d  %d ",col,rot);
                   j=6;i=0;
               }
                num[i][j]=0;num[i][j-1]=0;
                
            }
            //rot=1
            if(j<6 && (num[i-1][j-1]==x || num[i-1][j+1]==x)){
               num[i][j]=x; num[i-1][j]=y;
               tmp=eval();
               if(tmp<v){
                   rot=1;col=j;
                 //  fprintf(stderr, "%d  %d ",col,rot);
                   j=6;i=0;
               }
                num[i][j]=0;num[i][j-1]=0;  
            }
       }else{
         if(num[i+1][j]==x){
             rot=1;
             col=j;
         }
         else if(j>0 && num[i][j-1]==x){ 
             rot=3;
             col=j-1;
         }else if(j<6 && num[i][j+1]==x){ 
             rot=1;
             col=j+1;
         }else if(j>0 && num[i][j-1]==y){ 
             rot=3;
             col=j+1;
         }else if(j<6 && num[i][j+1]==y){ 
             rot=1;
             col=j+1;
         }else{
          rot=1;
          if(fc==0 && fl==0 && col<6)col++;
         }
         
       }
         j++;
     }
     i++;
    }
}

 void ttAg(){
     int i=0;
     
     if(num[1][col]!=0 ){
         col++;
         if(col>5)col=1;
         rot=3;
         
     }
 }
 

 void decider(){
     int v=0,tmp=0,i=1,k=0;
     getFirst();
     
     while(i<8){
     tmp=eval();
      k=eval();
      if(tmp<v){
         for(int i=fc;i<6;i++){
             classer(colA[0],colB[0]);
             if(eval()<k){
                 col=i;
             }
             num[fc][fl]=7;
             converture();
         }
      }
      i++;
      converture();
     }
  
    }
void mi(int x,int y){
    int k=0,l=firstLine();
   for(int i=col;i>0;i--){
     num[l][i]=8;
     classer(x,y);
     tt(x,y);
     ttAg();
     k=eval();
     if(eval()<k-8){
         col=i+1;
     }
     converture();
 } 
}
    
void valeur(){
    int s;
    for(int i=0;i<8;i++){
        classer(colA[i],colB[i]);
        tt(colA[i],colB[i]);
        mi(colA[i],colB[i]);
        ttAg();
        s=eval();
        for(int j=i+1;j<8;j++){
            classer(colA[j],colB[j]);
            tt(colA[j],colB[j]);
            mi(colA[j],colB[j]);
            ttAg();
            num[firstLine()][col]=colA[j];
            num[firstLine()-1][col]=colB[j];
            if(s>eval){
              futur[i]= col;
            }
        }
        
    }
}
 
 
 void recherche(){
     
     for(int i=0;i<8;i++){
        
        for(int j=i+1;j<8;j++){
            if(colA[i]==colB[i] && colA[j]==colB[j] && colA[i]==colB[j] ){
             classer(colA[i],colB[i]);
             tt(colA[i],colA[i]);
             mi(colA[i],colA[i]);
             ttAg();
             futur[i]=col;
             futur[j]=col;
            }
        }
     }
 }
int main()
{

   int x=0,y=0,k=0,init=0,a,b,d;
    // game loop
    while (1) {
        for (int i = 0; i < 8; i++) {
            int colorA; // color of the first block
            int colorB; // color of the attached block
            scanf("%d%d", &colorA, &colorB);
            if(i==0){x= colorA;y=colorB;}
            colA[i]=colorA;
            colB[i]=colorB;
        }
        for (int i = 0; i < 12; i++) {
            char row[7];
            scanf("%s", row);
            for(int j=0;j<6;j++){t[i][j]=row[j];}
           // fprintf(stderr, "%s\n",t[i]);
        }
        for (int i = 0; i < 12; i++) {
            char row[7]; // One line of the map ('.' = empty, '0' = skull block, '1' to '5' = colored block)
            scanf("%s", row);
        }
          if(k%8==0){
              k=0;
          }
     //     recherche();
     
      /*   if(futur[k]!=0){
            printf("%d %d Brexe the swag  \n",futur[k],3);  
            futur[k]=0;
         }else{*/
             classer(x,y);
             tt(x,y);
             mi(x,y);
             ttAg();
            printf("%d %d Brexe the swag  \n",col,rot);   
       //  }
          k++;
    }

    return 0;
}
