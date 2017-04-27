import java.util.*;
import java.io.*;
import java.math.*;
import java.util.ArrayList;
import java.util.List;
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
 
class Solution {

    public static void conversion(int c){
        if(c==0){
            System.out.print("00");
        }else{
          System.out.print('0');
        }
    }
    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);
        String MESSAGE = in.nextLine();

        // Write an action using System.out.println()
        // To debug: System.err.println("Debug messages...");
        byte[] bytes = MESSAGE.getBytes();
        StringBuilder binary = new StringBuilder();
        List<String> list = new ArrayList<String>();
    
         for (byte b : bytes)
          {
             int val = b;
             for (int i = 0; i < 8; i++)
             {
                binary.append((val & 128) == 0 ? 0 : 1);
                val <<= 1;
             }
             binary.append(' ');
          }
          char[] t=binary.toString().toCharArray(),s=new char[t.length];
          int b=1,a=0,h=0;
          while(b<t.length){
              if(t[b]==' ' && b<t.length-1){
    
                  s[a]=t[b+2];
                  a+=1;
                  b+=3;
                  h+=2;
              }else{
                  s[a]=t[b];
                  a++;
                  b++;
              }
          }
         
       int l=s.length-h,j=0;
        //System.out.println(l+" "+h);
        for(int i=0;i<l-1;i++){
            if(s[i]=='1' ){;
                System.out.print("0 ");
                j=i;
                while(s[j]=='1'){
                    System.out.print("0");

                    j++;
                }
                i=j-1;
                if(j<l-2){
                  System.out.print(" ");
                }
                
            }else if(s[i]=='0'){
                 if(j<l-2)
                 System.out.print("00 ");
                 j=i;
                while(s[j]=='0'){
                    System.out.print("0");
                    j++;
                }
                i=j-1;
                if(j<l-2){
                  System.out.print(" ");
                }
            }
            
        }
         
    }
}
