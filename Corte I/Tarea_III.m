clc
clear
close all


f = 100 % frecuencia
T = 1/f % periodo


Ts = T/10 % unidad de tiempo
t = -2*T:Ts:2*T; % tiempo
n = 1; % Define a condition for the if statement
y = abs(t); % funcion


figure(1)
subplot(1, 2, 1)
plot(t, y, 'g')
title("Señal Continua x_{(t)} = |t|")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on

%% 

n = -2:8;               % Rango de muestras
x_n = (n >= 0 & n <= 5) .* n; % Lógica: n si 0 <= n <= 5, de lo contrario 0

figure(1)
subplot(1, 2, 2)
plot(n, x_n, 'g')
title('Señal Discreta x_{(n)}');
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on
