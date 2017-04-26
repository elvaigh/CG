import java.util.*;
import java.math.*;
import java.util.*;
class Solution{public static void main(String[] args){
    Scanner in=new Scanner(System.in);
    int i=0,o=0,n=in.nextInt(),k=n;in.nextLine();
    while(i<n){o=Math.abs(in.nextInt());i++;if(o<k)k=o;}
    System.out.println(k);}
}
