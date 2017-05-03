import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Set;


enum Action{ LEFT,RIGHT,UP,DOWN}
class Jeu{
	int players;
	int h,w;
	Integer[][] board;
	public Jeu(){}
	public Jeu(int h,int w,int players){
		this.h=h;
		this.w=w;
		this.players=players;
		this.board=new Integer[w][h];
	}
	public Jeu(Integer[][] board){
		this.board=board.clone();
	}
	Action toAction(int nx,int ny,int sx,int sy){
		if(sx<nx)return Action.RIGHT;
		if (sy<ny)return Action.RIGHT;
		if(sx>nx)return Action.LEFT;
		if(sy>ny)return Action.UP;
	}

	void applly(int tx,int ty,int player){board[tx][yt]=player;}
	int getScore(int player){
		s=0
		for(Integer[] tmp :board){
			for(int p:tmp){
				if(p==player)s+=1;
			}
		}
		return s;
	}

}
class IA{
	Action actionChoisie=null;
	public IA() {
		h_max=8;
	}
 
	private static int h_max=0;
	public int getUtilite(Jeu jeu){
		int score=0;
		for(Joueur j:jeu.getJoueurs()){
			if(j.equals(this)){
				score+=j.getScore()+j.getTroll().getBouclier()+j.getTroll().getMagie();
			}else{
				score-=(j.getScore()+j.getTroll().getBouclier()+j.getTroll().getMagie());
			}
		}
		return score;
	}
	public int qualite(Action a,Jeu jeu){
			
		int tmp=0;
		
		
		return tmp;
	}
	
	public int alphaBeta(Jeu etatInit,int a,int b,int h, int n){	

		if (etatInit.estTermine() || h == n){
			
			return getUtilite(etatInit);
		}else{

			int q=0;
			if (etatInit.getJoueurCourant().equals(this)) {

				for(int i=0;i<actions.size() && a<b ;i++){
				
					tmp=(Jeu)etatInit.clone();		
					//q=qualite(actions.get(i),tmp);
					if(tableTrans.contains(tmp)){
						a=Math.max(a,tableTrans.get(tmp));
					}else{
						actions.get(i).appliquer(tmp);
						tmp.finirTour();
						a = Math.max(a,alphaBeta(tmp,a,b,h,n));	
					}
				}
				if(tableTrans.contains(tmp)){
					tableTrans.put(tmp, a+(int)Math.pow(2, h_max-h));
				}
				else{
					tableTrans.put(tmp, a);
				}
				return a;
			} else {

				for(int i=0;i<actions.size() && a<b ;i++){	
					tmp=(Jeu)etatInit.clone();
					//q=qualite(actions.get(i),tmp);
					if(tableTrans.contains(tmp)){
						b=Math.min(b,tableTrans.get(tmp));
					}else{
						actions.get(i).appliquer(tmp);
						tmp.finirTour();
						b= Math.min(b,alphaBeta(tmp,a,b,h,n));
					}
				}
				
			}
			if(tableTrans.contains(tmp)){
				tableTrans.put(tmp, a+(int)Math.pow(2, h_max-h));
			}else{
					tableTrans.put(tmp, a);
			}
			return b;
		}
	}
	
	

	public List<Action> trieAction(Jeu j){

		List<Action> tmp=new ArrayList<Action>();
		
		List<Action> actions=j.listerActionsPossibles();
		actions.remove(0);
		for(Action a:actions){
			if( a instanceof DeplacerTroll && contientCristal((DeplacerTroll)a)  && this.getTroll().getMagie()<2 ){			
				tmp.add(a);	
			}
		}
		
		for(Action a:actions){
			if( a instanceof ReveillerDeplacerDragon  && j.getDragons().get(0).peutAtteindre(getAdv(j).getTroll().getPosition(), j)){			
				tmp.add(a);	
			}
		}
		
		for(Action a:actions){
			if( a instanceof DeplacerTroll && contientBourse((DeplacerTroll)a)){			
				tmp.add(a);	
			}
		}
		
		for(Action a:actions){
			if(a instanceof DeplacerTroll && contientPiece((DeplacerTroll)a)){	
				tmp.add(a);	
			}
		}
		
		
		for(Action a:actions){
			if( a instanceof DeplacerTroll && contientCoeur((DeplacerTroll)a) && this.getTroll().getVies()<2 ){			
				tmp.add(a);	
			}
		}

		for(Action a:actions){
			if( a instanceof DeplacerTroll && contientBouclier((DeplacerTroll)a) ){			
				tmp.add(a);	
			}
		}
		
		
		if(tmp.isEmpty()){
			
			return actions;
		}

		return tmp;
	}
	
	int h(Action a,Jeu j){
		Jeu tmp=(Jeu)j.clone();					
		a.appliquer(tmp);
		tmp.finirTour();
		return getUtilite(tmp);
	}
	void racine(int profondeur,Jeu j,int x,int y){
		
		int t;
		
		List<Action> actions=trieAction(j);
		/*List<Action> actions=j.listerActionsPossibles();
		Collections.sort(actions, new Comparator<Action>() {

			@Override
			public int compare(Action o1, Action o2) {
				if(h(o1,j)<h(o2,j)){
					return 0;
				}
				return 1;
			}
		});*/
		
		for(int i=0;i<actions.size() ;i++){
		
			Jeu tmp=(Jeu)j.clone();					
			actions.get(i).appliquer(tmp);
			tmp.finirTour();
			if(!(tmp.estTermine())){
				if(tableTrans.contains(tmp)){
					t=tableTrans.get(tmp);
				}else{
					t=alphaBeta(tmp, x, y, 0,profondeur-1 );
				}
				if(x<t ){
					x=t;
					tableTrans.put(tmp, t+(int)Math.pow(2, h_max-profondeur+1));
					this.memoriserAction(actions.get(i));
					actionChoisie=actions.get(i);
				}	
			}else{
				this.memoriserAction(actions.get(i));
				actionChoisie=actions.get(i);
			}
		}
	}		
	void ID(int profondeur, Jeu j){
		int score = j.scoreMax;
		int d=1;
		
		while(d<=profondeur){
			
			racine(d,j,Integer.MIN_VALUE, Integer.MAX_VALUE);
			d++;
			System.out.println("************************** "+d);
		}
	}
		
	public Action choisirAction(Jeu j) {
		
		
		Jeu clone =(Jeu)j.clone();
		//System.out.println(visitees);
		ID (h_max,clone);
		return  actionChoisie;	

	}


	public double distance(Case A,Case B){
		return Math.sqrt(Math.pow(B.getAbscisse()-A.getAbscisse(),2)+Math.pow(B.getOrdonnee()-A.getOrdonnee(),2));
	}
}
