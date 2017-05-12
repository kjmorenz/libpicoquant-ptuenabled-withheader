%% 5.38 URIECA Module 10
% 13 January 2011
% Evaluates the ground state wavefunction at various point in space, given:
% r: 1xN vector containing the spatial coordinates
% wavefunction: wavefunction parameters as created by parameters.m
function psi = wavefunctions(r, wavefunction)

psi = (sin(wavefunction.k1 * r)./(r*(sin(wavefunction.k1 * wavefunction.D))).* ...
          (1 - heaviside(r - wavefunction.D))) ...
      + sin(wavefunction.k2 *(wavefunction.R - r)) ./ (r*sin(wavefunction.k2 *(wavefunction.R-wavefunction.D))).* ...
          heaviside(r - wavefunction.D);
   
psi = psi/sqrt(psi * psi'); % Normalization