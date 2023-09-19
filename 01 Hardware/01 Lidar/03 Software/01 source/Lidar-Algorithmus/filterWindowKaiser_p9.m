function Hd = filterWindowKaiser_p9
%FILTERWINDOWKAISER_P9 Returns a discrete-time filter object.

% MATLAB Code
% Generated by MATLAB(R) 9.14 and Signal Processing Toolbox 9.2.
% Generated on: 12-Sep-2023 12:10:30

% FIR Window Lowpass filter designed using the FIR1 function.

% All frequency values are normalized to 1.

N    = 3;        % Order
Fc   = 0.01;     % Cutoff Frequency
flag = 'scale';  % Sampling Flag
Beta = 1;        % Window Parameter

% Create the window vector for the design algorithm.
win = kaiser(N+1, Beta);

% Calculate the coefficients using the FIR1 function.
b  = fir1(N, Fc, 'low', win, flag);
Hd = dfilt.dffir(b);

% [EOF]