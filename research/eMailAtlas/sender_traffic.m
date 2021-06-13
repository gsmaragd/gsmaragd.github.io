%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                               %
% Georgios Smaragdakis                                          %
% gsmaragd@cs.bu.edu                                            %
% WING Friday Lunch, Dec 03 2004                                %
%                                                               %
% Sending Gravity                                               %
%                                                               %
% Inspired by CAIDA Internet Topology Visualization project:    %
% http://www.caida.org/analysis/topology/as_core_network        %
%                                                               % 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear;
MAX_NODES=1672; %Maximum distinct nodes
R=load('maillog.cs.sender_order');
max(R);
maximum=ans(2);
radius=1-log((R(:,2)+1)/maximum);

zeroRadius=1.25*(max(radius))
for i=1:1:MAX_NODES+1 
    theta(i)=(2*pi)*(1-rand);
    xc(i)=zeroRadius*cos(theta(i));
    yc(i)=zeroRadius*sin(theta(i));
    send(i)=0;
end

figure(1)
for i=1:1:length(radius)-1
    theta(i)=(2*pi)*(1-rand);
    x(i)=radius(i)*cos(theta(i));
    y(i)=radius(i)*sin(theta(i));
    if (i==1)
      plot(x(i),y(i),'-ro');
    end
    if (i>1 & i<=11)
      plot(x(i),y(i),'-o');
    end
    if (i>11)
      plot(x(i),y(i),'-go');
    end
    hold on;
    xc(R(i)+1)=x(i);
    yc(R(i)+1)=y(i);
    send(R(i)+1)=1;
end

for i=1:1:MAX_NODES+1
    if(send(i)==0)
      plot(xc(i),yc(i),'yo');
      hold on;
    end
end
    
    
%pause();


C=load('maillog.cs.order');

hold on;
for i=1:1:length(C)-1
  plot([xc(C(i,1)+1),xc(C(i,2)+1)],[yc(C(i,1)+1),yc(C(i,2)+1)],'k-');
hold on;
end
  


for i=1:1:length(radius)-1
    if (i==1)
      plot(x(i),y(i),'-ro');
    end
    if (i>1 & i<=11)
      plot(x(i),y(i),'-o');
    end
     if (i>11)
      plot(x(i),y(i),'-go');
    end
    hold on;
end

