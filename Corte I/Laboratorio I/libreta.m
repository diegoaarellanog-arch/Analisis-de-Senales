clear
clc
close all

V0 = 5;      % Amplitud
T = 2;       % Duración del pulso
t = -1:0.01:3;       % Tiempo desde -1 hasta 3 segundos

% Generamos el pulso rectangular
xB = V0 * ( (t >= 0) - (t >= T) );

plot(t, xB, 'LineWidth', 3);
ylim([-1, V0 + 1]);
grid on; hold on;
title('Pulso Rectangular x_B(t)');
xlabel('Tiempo (t)'); ylabel('Voltaje (V_0)');

%%  
f = 2;               % Frecuencia en Hz
w = 2*pi*f;          % Frecuencia angular

% Creamos la señal: (t>=0) actúa como el escalón unitario u(t)
xD = V0 * sin(w*t) .* (t >= 0);

plot(t, xD, 'b', 'LineWidth', 2);
grid on;
plot(t, zeros(size(t)), 'k--'); % Línea de referencia en cero
title('Señal Sinusoide Causal x_D(t) = V_0 sin(\omega t) u(t)');
xlabel('Tiempo (t)'); ylabel('Amplitud');

