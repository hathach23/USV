function Hd = filterChebyshevI_p2
%FILTERCHEBYSHEVI_P2 Returns a discrete-time filter object.

% MATLAB Code
% Generated by MATLAB(R) 9.14 and Signal Processing Toolbox 9.2.
% Generated on: 07-Sep-2023 17:00:05

% Chebyshev Type I Lowpass filter designed using FDESIGN.LOWPASS.

% All frequency values are normalized to 1.

N     = 3;             % Order
Fpass = 0.5;           % Passband Frequency
Apass = 3.0102999566;  % Passband Ripple (dB)

% Construct an FDESIGN object and call its CHEBY1 method.
h  = fdesign.lowpass('N,Fp,Ap', N, Fpass, Apass);
Hd = design(h, 'cheby1');

% [EOF]