%% 5.38 Module 10
% Massachusetts Institute of Technology
% Dylan Arias
% 19 January 2009
%
% Thomas Bischof
% 18 February 2011
% 
% Given spectra for a reference sample and a sample with unknown quantum
% yield, this routine determines the quantum yield of the unknown sample.
%
% All spectra here refer to text files containing those spectra.
% reference_fluorescence: emission spectrum for the reference sample 
% reference_absorbance: absorbance spectrum for the reference sample
% reference_QY: the quantum yield of the reference sample 
% sample_fluorescence: emission spectrum for the unknown sample
% sample_absorbance: absorbance spectrum for the unknown sample
% laser_wavelength: wavelength (in nanometers) of the laser used to excite
%                   the sample.
%
% The spectra are expected to come from the Ocean Optics SpectraSuite
% software as tab-delimited files with headers, so there are 17 lines of
% header we want to skip. After this, the file is a normal tab-delimited
% file with: <wavelength/nm>\t<intensity>\n At the end of the file there is
% a line with ">>>>>End Processed Spectra Data<<<<<". This is followed by a
% blank row.
%
% Alternately, we can just take in the tab-delimited spectrum part; the
% read_ocean_optics routine can tell the difference and take both.
%
function [yield] = QY(reference_fluorescence, reference_absorbance, ...
    reference_QY, sample_fluorescence, sample_absorbance, laser_wavelength)
% Find the absorbance of each sample at the excitation wavelength.
reference_A = read_ocean_optics(reference_absorbance);
reference_Aexcitation = reference_A(nearest_index(reference_A, ...
                                                  laser_wavelength), 2);
sample_A = read_ocean_optics(sample_absorbance);
sample_Aexcitation = sample_A(nearest_index(sample_A, ...
                                            laser_wavelength), 2);
                            
% Plot the absorbance data to make sure things are going well.
figure();
subplot(2,2,1);
plot(reference_A(:,1), reference_A(:,2));
title('Reference absorbance spectrum');
xlabel('\lambda/nm');
% the excitation is at 532nm, so anything bluer than that is probably just
% noise. Also, the spectrometer is currently calibrated out to ~650nm.
xlim([450 650]); 

subplot(2,2,3);
plot(sample_A(:,1), sample_A(:,2));
title('Sample absorbance spectrum')
xlabel('\lambda/nm')
xlim([450 650])

% Load the emission data
sample_emission = read_ocean_optics(sample_fluorescence);
reference_emission = read_ocean_optics(reference_fluorescence);

% If needed, this is where we would subtract the background spectra. For
% this experiment, there is not really any backround spectrum to worry
% about.

% Now, plot the raw emission data so we can see what we are up against.
%emission_figure = figure();
subplot(2,2,2);
plot(reference_emission(:,1), reference_emission(:,2));
title('Reference emission spectrum');
xlabel('\lambda/nm');
% the excitation is at 532nm, so anything bluer than that is probably just
% noise. Also, the spectrometer is currently calibrated out to ~650nm.
xlim([500 650]); 

subplot(2,2,4);
plot(sample_emission(:,1), sample_emission(:,2));
title('Sample emission spectrum')
xlabel('\lambda/nm')
xlim([500 650])

% Having made some plots, we need to select what portion of the spectrum is
% actually the signal we want to examine. For example, in this experiment
% we excite with a 532nm laser, some of which scatters to the detector.
% This is something we do not want to include in our calculation, so we
% allow the user to remove it before proceeding. This could be automated to
% a certain extent, but sometimes the laser and sample spectra overlap a
% little too well. 
disp('Choose the left and right limits for the emission spectra')
g = ginput(2);
lambda1 = g(1);
lambda2 = g(2);

reference_limits = nearest_index(reference_emission(:,1), lambda1): ...
                   nearest_index(reference_emission(:,1), lambda2);
sample_limits = nearest_index(sample_emission(:,1), lambda1): ...
                nearest_index(sample_emission(:,1), lambda2);

% So, now we have the left and right limits for the spectra, which means we
% can integrate the intensity of the spectra and compare these values with
% the absorption values. This tells us the overall number of photons
% observed from each sample relative to the number of photons absorbed by
% each sample, giving us a way to determine the relative ability of each
% sample to absorb and emit photons. Once we have this proportionality, we
% can use the established value for the reference quantum yield to find the
% quantum yield of the sample.
%
% Some things to consider:
% - we have assumed the response of the detector is uniform across the
% spectrum. That is, we assume that a unit of intensity for two different
% wavelengths corresponds to the same number of photons.
% - we have assumed that the samples are sufficiently dilute that they do
% not undergo appreciable Rayleigh scattering of the emitted photons. In a
% concentrated solution, beam penetration is too shallow to allow for the
% escape of all photons.
% - we have assumed that the cuvettes and solvents are created equal, such
% that the same solid angle of scattering is emitted to the detector.
% - because we are exciting at just one wavelength, we may or may not be
% determining the full extent of this emission efficiency; there may be
% some frequency dependence.
%
% As you perform your analysis, think about how you might improve any of
% these assumptions, and see if you can modify this script to make your
% results more accurate. 

reference_emission_intensity = sum(reference_emission(reference_limits,2));
sample_emission_intensity = sum(sample_emission(sample_limits, 2));

% Now, we just calculate a ratio of values to get the quantum yield.
yield = reference_QY * ...
    (1-10^(-reference_Aexcitation))/(1-10^(-sample_Aexcitation)) ...
        * (sample_emission_intensity/reference_emission_intensity);
