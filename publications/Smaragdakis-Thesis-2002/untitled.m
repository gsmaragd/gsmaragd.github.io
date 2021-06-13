l1_1=[0,3,0];
l1_2=[1.5,0,0];
l1_3=[3,0,0];
syms x y z  
normal=cross(l1_1-l1_2,l1_1-l1_3)
P=[x,y,z] 
planefunction=dot(normal,P-l1_1)  