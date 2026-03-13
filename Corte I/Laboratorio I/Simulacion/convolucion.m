%% Convolución: numérica (conv) vs Laplace (tf/lsim)
clear; clc; close all;

%% ====== PARAMETROS ======
tau = 0.5;              % Constante de tiempo 
dt  = 1e-3;             % Paso de tiempo
t_end = 10*tau;         % Simular 0..10*tau
t = 0:dt:t_end;

%% ====== ENTRADA x(t) ======
% Ejemplo: escalón de amplitud A0 (puedes cambiarlo por tu tren de pulsos, etc.)
A0 = 1;
x = A0*(t >= 0);

%% ====== RESPUESTA AL IMPULSO h(t) del sistema RC ======
h = (1/tau)*exp(-t/tau);   % h(t) = (1/tau) e^{-t/tau} u(t)

%% ============================
% Convolución numérica (aprox. integral)
y_conv_full = dt*conv(x,h);
t_full = 0:dt:(length(y_conv_full)-1)*dt;
y_conv = y_conv_full(1:length(t)); % recorte a 0..10tau

%% ============================
% Método por Laplace usando tf/lsim (equivalente a resolver el sistema)
s = tf('s');
H = 1/(tau*s+1);
y_lsim = lsim(H, x, t);

%% ====== GRAFICAS ======
figure
plot(t, x, 'LineWidth', 1.5); grid on
xlabel('t (s)'); ylabel('x(t)')
title('Entrada x(t)')

figure
plot(t, h, 'LineWidth', 1.5); grid on
xlabel('t (s)'); ylabel('h(t)')
title('Respuesta al impulso h(t)')

figure
plot(t, y_conv, 'LineWidth', 1.8); hold on; grid on
plot(t, y_lsim, '--', 'LineWidth', 1.8);
xlabel('t (s)'); ylabel('y(t)')
title('Salida: Convolución numérica vs tf/lsim')
legend('y\_conv (dt*conv)', 'y\_{lsim} (tf/lsim)', 'Location', 'best')
