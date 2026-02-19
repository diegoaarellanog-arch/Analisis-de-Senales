clc
clear
close all

% Señales en el dominio del tiempo
A = 10
f = 100
T = 1/f
% Tiempo/frecuencia de muestreo
Ts = T/10
t = -2*T:Ts:2*T;
y = A*sin(f*t);
% Grafica continua
figure(1)
grid on
subplot(1, 2, 1)
plot(t, y, 'g')
title("Señal Continua")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on
%Grafica discreta
subplot(1, 2, 2)
stem(t, y)
title("Señal Discreta")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc
clear
close all
% Señales en el dominio del tiempo
A = 10;
f = 1;
T = 1/f;
% Tiempo/frecuencia de muestreo
Ts = T/100;
t = -2*T:Ts:2*T;
y = A*sin(f*t*2*pi);
% Grafica continua
figure(1)
grid on
subplot(1, 2, 1)
plot(t, y, 'g')
title("Señal Continua")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on
% Grafica discreta
subplot(1, 2, 2)
stem(t, y)
title("Señal Discreta")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc
clear
close all
% Señales en el dominio del tiempo
A = 10;
f = 1;
T = 1/f;
% Tiempo/frecuencia de muestreo
Ts = T/100;
t = 0*T:Ts:2*T;
y = A*sin(f*t*2*pi).*exp(-t); % Producto vectorial (sen amortiguado)
% Grafica continua
figure (1)
subplot(5, 1, 1)
plot(t,y,'b')
title("Señal Continua")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on
% Grafica discreta
subplot(5, 1, 2)
stem(t, y)
title("Señal Discreta")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on
% Transformación de la variable independiente
% Inversión de la señal
y_inv = fliplr(y);
subplot(5, 1, 3)
plot(t, y_inv)
title("Señal Invertida")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on
% Escalamiento
k = 0.5;
t_k = k*t;
% Interpolación, predecir el dato que se encuentra en medio
y_k = interp1(t, y, t_k, 'linear', 0);
subplot(5, 1, 4)
plot(t_k, y_k)
title("Señal Escalada")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on
% Desplazamiento
t0 = -0.5;
y_shilft = interp1(t, y, t-t0, 'linear', 0);
subplot(5, 1, 5)
plot(t, y_shilft)
title("Señal Desplazada")
xlabel("Tiempo (s)")
ylabel("Amplitud")
grid on