clear; clc; close all;
%% ******************** PARAMETROS ******************** %%
% Fisicos
R = 4467;                       % Resistencia en ohmios
C = 100e-6;                     % Capacitancia en faradios
tau = R*C;                      % Constante de tiempo
V_0 = 2;                        % Amplitud de la señal
T = 3;                          % Duracion del pulso
f = 1;
omega = 2*pi*f;

% Simulacion
dt = 1e-3;                      % Diferencial de tiempo
t_end = 100*tau;               % Paso final 
t = 0:dt:t_end;                 % Valores de tiempo

%% ******************** ENTRADAS ******************** %%
% Auxiliares
u_t = 1*(t > 0);                % u(t)
u_T = 1*(t > T);                % u(t - T)

% Principales
x_A = V_0*(u_t - u_T);          % x_A(t) = V_0[u(t) - u(t - T)]
x_C = V_0*sind(omega*t).*u_t;   % x_C(t) = V_0*sind(omega*t)*u(t) 

%% ******************** RESPUESTA AL IMPULSO h(t) del sistema RC ******************** %%
h = 1/(tau) * exp(-t/(tau));    % h(t) = (1/tau) e^{-t/tau} u(t)

% Convolución numérica (aprox. integral)
y_A_conv_full = dt*conv(x_A,h);
y_C_conv_full = dt*conv(x_C,h);

t_full = 0:dt:(length(y_A_conv_full)-1)*dt;
y_A_conv = y_A_conv_full(1:length(t)); % recorte a 0..10tau
y_C_conv = y_C_conv_full(1:length(t)); % recorte a 0..10tau

figure
hold on
plot(t,x_A)
plot(t,u_t)
plot(t,u_T)
plot(t,x_C)
plot(t,h)
figure
hold on
plot(t,y_A_conv)
plot(t,y_C_conv)