function Hd = filterWindowGauss_p3
%FILTERWINDOWGAUSS_P3 Returns a discrete-time filter object.

% MATLAB Code
% Generated by MATLAB(R) 9.14 and DSP System Toolbox 9.16.
% Generated on: 12-Sep-2023 12:37:46

% FIR Window Lowpass filter designed using the FIR1 function.

% All frequency values are normalized to 1.

N     = 3;          % Order
Fc    = 0.3;        % Cutoff Frequency
flag  = 'noscale';  % Sampling Flag
Alpha = 4.5;        % Window Parameter

% Create the window vector for the design algorithm.
win = gausswin(N+1, Alpha);

% Calculate the coefficients using the FIR1 function.
b  = fir1(N, Fc, 'low', win, flag);
Hd = dfilt.dffir(b);

% [EOF]
