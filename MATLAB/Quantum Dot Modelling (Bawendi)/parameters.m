%% 5.38 URIECA Module 10
% 13 January 2011
% Given the following parameters, creates an object wavefunction which 
% contains the appropriate wavefunction parameters, and determines the
% ground-state energy for the wavefunction.
% V1 - core potential
% V2 - shell potential
% m1 - mass of the particle in the core
% m2 - mass of the particle in the shell
% D - radius of the core
% R - total radius of the quantum dot

function [Eground, wavefunction] = parameters(V1, V2, m1, m2, D, R)
% Assuming E = hbar^2*k^2/(2*m) + V, determine the magnitude of the
% wavevector.
wavevector = @(m, V, E) sqrt(2*m*(E-V)/constants.hbar^2);

% Energy condition
E1star = constants.hbar^2/(2*m1)*(pi/D)^2 + V1; 
E2star = constants.hbar^2/(2*m2)*(pi/(R-D))^2 + V2;

Eshift = 1.602e-28; % Shift of 1 nano eV away from endpoints .. Why?

F = @(E) wavevector(m1, V1, E)/m1 .* cot(wavevector(m1, V1, E) * D) ...
       + wavevector(m2, V2, E)/m2 .* cot(wavevector(m2, V2, E) * (R-D));

Eground = fzero(F, [min(V1, V2) + Eshift ... 
                    min(E1star, E2star) - Eshift],  ...
                optimset('TolX', 1e-28));

wavefunction.k1 = wavevector(m1, V1, Eground);
wavefunction.k2 = wavevector(m2, V2, Eground);
wavefunction.A1 = 1;
wavefunction.A2 = sin(wavefunction.k1 * D) / sin(wavefunction.k2 * (R-D));
wavefunction.D = D;
wavefunction.R = R;

Eground = Eground/constants.eV_to_J; % convert from J to eV
