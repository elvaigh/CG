o=gets
m=99
gets.split.each{|j|k=j.to_i;i=k.abs;m,o=i,k if i==m&&k>0||i<m}
puts o
