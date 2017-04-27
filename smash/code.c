
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
 char l[7];
 char t[12][6];
 int num[12][6];
 int lig,col=0,rot=0,fc,fl;
 int g[12][7],cg[12][7], color[8];
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
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

void tt(int x,int y){
    
    int l=0,k=0,n,m;

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
    converture();
   }
}

 void ttag(){
     int i=0;
    
    if(l[col]!='.'){
        for(i=0;i<6;i++){
             if(l[i]=='.'){
                 col=i;
                 
                 i=6;
             }
        }
    }
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

void  getFirst(){
    
    
    for(int i=11;i>=0;i--){ 
     for(int j=0;j<6;j++){
         if(num[i][j]==0){
           fc=j;fl=i;  
            i=-1;j=6;
        }
    }
    } 
 }
 void classer(int x,int y){
    
    
    int v=eval(),tmp=0,n,m;
    bool c=false;
    int l=firstLine(),la=lastLine();
    
    if(col<5 && col>0)rot=col%3;
    else if(col==0)rot=1;
    else rot=3;
    converture();
    getFirst();
    col=fc;
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
          rot=3;
          if(fc==0 && fl==0 && col<6)col++;
         }
         
       }
         j++;
     }
     i++;
    }
}
void mi(int x,int y){
    int k=0,l=firstLine();
   for(int i=col;i>0;i--){
     num[l][i]=8;
     classer(x,y);
     tt(x,y);
     ttag();
     k=eval();
     if(eval()<k-8){
         col=i+1;
     }
     converture();
 } 
}
int main()
{

    // game loop
    while (1) {
        for (int i = 0; i < 8; i++) {
            int colorA; // color of the first block
            int colorB; // color of the attached block
            scanf("%d%d", &colorA, &colorB);
            if(i==0){
                color[0]=colorA;
                color[1]=colorB;
            }
            
        }
        int score1;
        scanf("%d", &score1);
        for (int i = 0; i < 12; i++) {
            char row[7];
            scanf("%s", row);
            if(i==1){
                strcpy(l,row);
            }
            for(int j=0;j<6;j++){t[i][j]=row[j];}
        }
        int score2;
        scanf("%d", &score2);
        for (int i = 0; i < 12; i++) {
            char row[7]; // One line of the map ('.' = empty, '0' = skull block, '1' to '5' = colored block)
            scanf("%s", row);
        }
        
        // Write an action using printf(). DON'T FORGET THE TRAILING \n
        // To debug: fprintf(stderr, "Debug messages...\n");
       
       converture();
       classer( color[0], color[1]);
       tt(color[0], color[1]);
       ttag();
       if(rot==0 && col==5){rot=2;}
       if(rot==2 && col==0){rot=0;}
       fprintf(stderr, "Debug messages... %d  %d\n",col,rot);
       printf("%d %d\n",col,rot); // "x": the column in which to drop your blocks
       
    }

    return 0;
}
