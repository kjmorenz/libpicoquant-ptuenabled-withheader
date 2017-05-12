classdef constants
    % Quick listing of some useful constants for the scripts.
    
    properties (Constant)
        h = 6.63e-34; % Planck's constant
        hbar = constants.h/(2*pi);
        eV_to_J = 1.602e-19;
        e_mass = 9.109e-31; % kg
        nm = 1e-9; % m
        c = 3e8; % speed of light
        eV_to_nm = constants.h*constants.c / ...
            (constants.eV_to_J*constants.nm);
            % divide eV_to_nm by E to get nm units
    end   
end

