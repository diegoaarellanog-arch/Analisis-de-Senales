clear; clc; close all;
%% ******************** PARAMETROS ******************** %%
% Montaje 
R = 4467;                                   % Resistencia en ohmios
C = 100e-6;                                 % Capacitancia en faradios
tau = R*C;                                  % Constante de tiempo Tau

% Señasl A: Pulso rectangular causal
V_0_A = 3.5;                                % Amplitud de la señal
T = 3;                                      % Duracion del pulso

% Señal C: Senoidal causal
V_0_C = 3.5/2;                              % Amplitud de la señal
T_C = 10;                                   % Periodo de la señal
f = 1/T_C;                                  % Frecuencia lineal
omega = 2*pi*f;                             % Frecuencia anguloar

% Simulacion
dt = tau/200;                               % Diferencial de tiempo
t_end_A = 10*tau;                           % Paso final señal A
t_A = 0:dt:t_end_A;                         % Valores de tiempo señal A
t_end_C = 30*tau;                           % Paso final señal C
t_C = 0:dt:t_end_C;                         % Valores de tiempo señal C

%% ******************** ENTRADAS ******************** %%
% Auxiliares para señal A
u_t_A = 1*(t_A > 0);                        % u(t)
u_T_A = 1*(t_A > T);                        % u(t - T)

% Auxiliares para señal C
u_t_C = 1*(t_C > 0);                        % u(t)
u_T_C = 1*(t_C > T);                        % u(t - T)

% Principales
x_A = V_0_A*(u_t_A - u_T_A);                % x_A(t) = V_0[u(t) - u(t - T)]
x_C = V_0_C*sin(omega*t_C).*u_t_C;         % x_C(t) = V_0*sind(omega*t)*u(t) 

%% ******************** RESPUESTA AL IMPULSO h(t) del sistema RC ******************** %%
% Para señal A
h_A = 1/(tau) * exp(-t_A/(tau));            % h(t) = (1/tau) e^{-t/tau} u(t)

% Para señal C
h_C = 1/(tau) * exp(-t_C/(tau));            % h(t) = (1/tau) e^{-t/tau} u(t)

% Convolución numérica (aprox. integral)
y_A_conv_full = dt*conv(x_A,h_A);
y_C_conv_full = dt*conv(x_C,h_C);

t_full = 0:dt:(length(y_A_conv_full)-1)*dt;
y_A_conv = y_A_conv_full(1:length(t_A));    % recorte a 0..10tau
y_C_conv = y_C_conv_full(1:length(t_C));    % recorte a 0..200tau

% Método por Laplace usando tf/lsim (equivalente a resolver el sistema)
s = tf('s');
H = 1/(tau*s + 1);
y_A_1sim = lsim(H, x_A, t_A);
y_C_1sim = lsim(H, x_C, t_C);

%% ******************** GRAFICAS ******************** %%
figure
plot(t_A, x_A, 'LineWidth', 5); grid on
xlabel('t(s)'); ylabel('x(t)')
%title('Entrada x_A(t)')
set(gca, 'FontSize', 50)
xlim([0 3.5]); ylim([0 4]);

figure
plot(t_A, h_A, 'LineWidth', 5); grid on
xlabel('t(s)'); ylabel('h(t)')
%title('Respuesta al impulso h(t)')
set(gca, 'FontSize', 50)
xlim([0 3.5]); ylim([0 2.5]);

figure
plot(t_A, y_A_conv, 'LineWidth', 5); hold on; grid on
plot(t_A, y_A_1sim, '--', 'LineWidth', 5);
xlabel('t (s)'); ylabel('y(t)')
%title('Salida: Convolución numérica vs tf/lsim')
set(gca, 'FontSize', 50)
legend('y\_conv (dt*conv)', 'y\_{lsim} (tf/lsim)', 'Location', 'best')
xlim([0 4.5]); ylim([0 4]);

figure
plot(t_C, x_C, 'LineWidth', 5); grid on
xlabel('t(s)'); ylabel('x(t)')
%title('Entrada x_C(t)')
set(gca, 'FontSize', 50)
xlim([0 12]); ylim([-2 2]);

figure
plot(t_C, y_C_conv, 'LineWidth', 5); hold on; grid on
plot(t_C, y_C_1sim, '--', 'LineWidth', 5);
xlabel('t (s)'); ylabel('y(t)')
%title('Salida: Convolución numérica vs tf/lsim')
set(gca, 'FontSize', 50)
legend('y\_conv (dt*conv)', 'y\_{lsim} (tf/lsim)', 'Location', 'best')
xlim([0 12]); ylim([-2 2]);

%% ******************** VALIDACION CUANTITATIVA ******************** %%
% Vectores columna para el error por señal
error_A_t = y_A_conv(:) - y_A_1sim(:);
error_C_t = y_C_conv(:) - y_C_1sim(:);

% Error maximo
e_A_max = max(abs(error_A_t));
e_C_max = max(abs(error_C_t));

% Error RMS
T_total = t_A(end); 
e_A_rms = sqrt( (1/T_total) * sum(error_A_t.^2) * dt);
T_total = t_C(end); 
e_C_rms = sqrt( (1/T_total) * sum(error_C_t.^2) * dt);

fprintf('Error Máximo Señal Pulso: %.4f\n', e_A_max);
fprintf('Error RMS Señal Pulso: %.4f\n', e_A_rms);
fprintf('Error Máximo Señal Senoidal: %.4f\n', e_C_max);
fprintf('Error RMS Señal Senoidal: %.4f\n', e_C_rms);