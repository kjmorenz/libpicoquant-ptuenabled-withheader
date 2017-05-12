%% 5.38 URIECA Module 10
% 13 January 2011
% Function that solves for ground state in the quantum dot model, giving: 
% Eground: ground state energy (eV)
% wavefunction: wavefunction parameters
% psi: wavefunction value in space
% rrange: spatial coordinates for psi.
%
% Requires as input:
% V1: core potential (eV)
% V2: shell potential (eV)
% m1: mass in the core (electron masses)
% m2: mass in the shell (electron masses)
% D: radius of the core (nm)
% R: total radius of the particle, core and shell (nm)

function [Eground, wavefunction, psi, rrange] ...
    = infstepwell(V1, V2, m1, m2, D, R)

% Convert the values to meter/kilogram/second units.
V1 = V1 * constants.eV_to_J; 
V2 = V2 * constants.eV_to_J;
m1 = m1 * constants.e_mass; 
m2 = m2 * constants.e_mass;
R = R * constants.nm;
D = D * constants.nm;

% Solve for the wavefunction and its ground-state energy.
[Eground, wavefunction] = parameters(V1, V2, m1, m2, D, R);

% Produce the values of the wavefunction in space
rrange = linspace(eps, wavefunction.R, 1000);

psi = wavefunctions(rrange, wavefunction);