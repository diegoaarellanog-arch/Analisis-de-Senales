clear; clc; close all;
%%
% Parametros de simulacion
dt  = 1e-3;
t_end = 10;
t = 0:dt:t_end;

%% ******************** EJERCICIO 1 ******************** %%
T = 0;
x = 1*(t > T) - 1*(t > T + 2);
T = 1;
xi = 1*(t > T) - 1*(t > T + 2); 

figure
plot(t, x, 'LineWidth', 1.5); grid on; hold on
plot(t, xi, 'LineWidth', 1.5);
xlabel('t (s)'); ylabel('x(t)')
title('Entrada x(t)')
legend('x(t)', 'x_i(t)')

%% ******************** EJERCICIO 2 ******************** %%

syms t u(t)          % Esto |define 't' como variable y 'u' como función de 't'
x = u(t) - u(t-2)    % Define x(t) de forma pura
xi = subs(x, t, t-1) % Define xi(t) como x(t-1) desplazada