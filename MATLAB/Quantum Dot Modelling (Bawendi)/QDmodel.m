%% 5.38 URIECA Module 10
% Massachusetts Institute of Technology
% Department of Chemistry
% Dylan Arias and Gautham Nair
% 22 October 2008
%
% Modified 19 January 2011
% Thomas Bischof
%
% This program models the Schrödinger equation for an infinite stepped
% radial well, mimicking the band structure of a core-shell quantum dot
% composed of two semiconducting layers. In this model, the reference 
% energy is the center of the bandgap of the core material, and the system
% is treated as an anisotropic ideal sphere. Thus, the potential energy
% has a step at the interface if the two band gaps are not the same.
%
% Given the approrpriate parameters, this program returns:
% Ee, Eh: ground state of the electron/hole wavefunction (eV)
% ewavefunction, hwavefunction: parameters for the electron/hole 
%                wavefunction (see parameters.m)
% epsi, hpsi: amplitude of the electron/hole wavefunction at various 
%             values of r
% Eexc: exciton energy (eV)
% lambda: exciton wavelength (nm)
% r: values of the radius for which the wavefunction was calculated
%
% The input parameters are:
% Gapin, Gapout: band gap in the core and shell, respectively (eV)
% Offset: (eV)
% mein, mhout: effective mass of the electron in the core and the shell,
%       respectively (free electron masses)
% mhin, mhout: effective mass of the hole in the core and the shell,
%       respectively (free electron masses)
% D: radius of the core (nm)
% R: thickness of the shell (nm)
%
% Once the appropriate parameters are determined, the potential energy,
% wavefunction, and exciton energy and wavelength are plotted. 
function [Ee, ewavefunction, epsi, ...
          Eh, hwavefunction, hpsi, Eexc, lambda, r] ...
    = QDmodel(Gapin, Gapout, Offset, mein, meout, mhin, mhout, D, R)

R = D + R;

%% Solve for electron parameters, wavefunctions, and energies
Ve1 = Gapin/2;
Ve2 = Gapout/2 + Offset;
[Ee, ewavefunction, epsi, rrange] = ...
    infstepwell(Ve1, Ve2, mein, meout, D, R);

%% Solve for hole parameters, wavefunctions, and energies
Vh1 = -Gapin/2;
Vh2 = -Gapout/2 + Offset;
[Eh, hwavefunction, hpsi] = infstepwell(-Vh1, -Vh2, mhin, mhout, D, R);
Eh = -Eh;

%% Exciton energy and transition wavelength
Eexc = (Ee-Eh);
lambda = constants.eV_to_nm/Eexc;

%% Plot the band diagram
eBand = [Ve1 Ve1 Ve2 Ve2]; 
elevel=[Ee Ee Ee Ee];

hBand=[Vh1 Vh1 Vh2 Vh2];
hlevel=[Eh Eh Eh Eh];

Bandrange=[0 D D R]; 
reflevel=[0 0 0 0];

figure(1)
subplot(2,1,1)
plot(Bandrange, eBand, 'b', ...
     Bandrange, hBand, 'b', ...
     Bandrange, elevel, '--r', ...
     Bandrange, hlevel, '--r', ...
     Bandrange,reflevel,'--k')
title('Band diagram with electron and hole energy levels')

xlabel('r/nm')
ylabel('E/eV')
text(D/4, -Gapin/5, ['Exciton energy = ', num2str(Eexc), 'eV'])
text(D/4, -Gapin/3, ['\lambda = ', num2str(lambda), 'nm'])

%% Plot the wavefunctions
lim = max([abs(epsi).^2 abs(hpsi).^2]);

r = rrange ./ constants.nm;

figure(1), subplot(2,1,2)
plot(r, abs(epsi).^2, 'r', ...
     r, abs(hpsi).^2, 'b', ...
     [D D], [0 lim], '--k')
ylim([0 lim])
title('Wavefunctions   electron - red   hole - blue')
xlabel('r/nm')
