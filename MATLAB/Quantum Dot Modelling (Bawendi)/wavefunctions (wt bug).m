%% 5.38 URIECA Module 10
% 13 January 2011
% Evaluates the ground state wavefunction at various point in space, given:
% r: 1xN vector containing the spatial coordinates
% wavefunction: wavefunction parameters as created by parameters.m
function psi = wavefunctions(r, wavefunction)

psi = ( wavefunction.A1 * sin(wavefunction.k1 * r) .* ...
          (1 - heaviside(r - wavefunction.D)) ...
      + wavefunction.A2 * sin(wavefunction.k1 * r) .* ...
          heaviside(r - wavefunction.D) ) ./ r;
psi = psi/sqrt(psi * psi'); % Normalization