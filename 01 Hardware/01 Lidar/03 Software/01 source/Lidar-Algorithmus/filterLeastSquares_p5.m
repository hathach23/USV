function Hd = filterLeastSquares_p5
%FILTERLEASTSQUARES_P5 Returns a discrete-time filter object.

% MATLAB Code
% Generated by MATLAB(R) 9.14 and Signal Processing Toolbox 9.2.
% Generated on: 12-Sep-2023 12:21:28

% FIR least-squares Lowpass filter designed using the FIRLS function.

% All frequency values are normalized to 1.

N     = 3;      % Order
Fpass = 0.4;    % Passband Frequency
Fstop = 0.5;    % Stopband Frequency
Wpass = 0.005;  % Passband Weight
Wstop = 0.955;  % Stopband Weight

% Calculate the coefficients using the FIRLS function.
b  = firls(N, [0 Fpass Fstop 1], [1 1 0 0], [Wpass Wstop]);
Hd = dfilt.dffir(b);

% [EOF]
