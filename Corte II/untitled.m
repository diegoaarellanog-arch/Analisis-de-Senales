clc
clear
close all

A = 4;
w0=2*pi;
t=0:0.01:2;
y = 0;
a0 = A/2;

for n = 1:10
    k = 2*n - 1
    y = y + ((2*A) / (k*pi))*sin(k*w0*t);
    plot(t,y)
    hold off
    grid on 
    pause(0.5)
end