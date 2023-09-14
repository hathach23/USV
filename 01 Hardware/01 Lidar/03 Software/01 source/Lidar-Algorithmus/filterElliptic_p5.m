function Hd = filterElliptic_p5
%FILTERELLIPTIC_P5 Returns a discrete-time filter object.

% MATLAB Code
% Generated by MATLAB(R) 9.14 and Signal Processing Toolbox 9.2.
% Generated on: 11-Sep-2023 16:36:52

% Elliptic Lowpass filter designed using FDESIGN.LOWPASS.

% All frequency values are normalized to 1.

N     = 3;             % Order
Fpass = 0.5;           % Passband Frequency
Apass = 3.0102999566;  % Passband Ripple (dB)
Astop = 30;            % Stopband Attenuation (dB)

% Construct an FDESIGN object and call its ELLIP method.
h  = fdesign.lowpass('N,Fp,Ap,Ast', N, Fpass, Apass, Astop);
Hd = design(h, 'ellip');

% [EOF]
