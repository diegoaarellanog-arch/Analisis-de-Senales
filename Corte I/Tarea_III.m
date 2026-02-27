clc
clear
close all


f = 100 % frecuencia
T = 1/f % periodo


Ts = T/10 % unidad de tiempo
t = -20*T:Ts:20*T; % tiempo
y = abs(t); % funcion


figure(1)
subplot(3, 1, 1)
plot(t, y, 'g')
title("Señal Continua x_{(t)}")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on

%% 

n = -2:8;               % Rango de muestras
x_n = (n >= 0 & n <= 5) .* n; % Lógica: n si 0 <= n <= 5, de lo contrario 0

figure(1)
subplot(3, 1, 2)
stem(n, x_n, 'g')
title('Señal Discreta x_{(n)}');
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on

%%
f = 100 % frecuencia
T = 1/f % periodo


Ts = T/10 % unidad de tiempo
t = -40*T:Ts:400*T; % tiempo
y = (t >= 1) .*exp(-2*(t-1)); % funcion


figure(1)
subplot(3, 1, 3)
plot(t, y, 'g')
title("Señal Continua x_{(t)}")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on