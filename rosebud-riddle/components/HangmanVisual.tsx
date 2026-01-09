
import React from 'react';

interface HangmanVisualProps {
  wrongGuesses: number;
}

const HangmanVisual: React.FC<HangmanVisualProps> = ({ wrongGuesses }) => {
  // Use only the requested palette colors
  const darkPink = "#AD1457";
  const rosePink = "#F06292";
  const strokeWidth = 5;

  return (
    <div className="w-full max-w-[220px] aspect-square flex items-center justify-center">
      <svg viewBox="0 0 100 120" className="w-full h-full drop-shadow-md">
        {/* Gallows - strictly darkpink */}
        <line x1="10" y1="110" x2="90" y2="110" stroke={darkPink} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="30" y1="110" x2="30" y2="10" stroke={darkPink} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="30" y1="10" x2="75" y2="10" stroke={darkPink} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="75" y1="10" x2="75" y2="25" stroke={darkPink} strokeWidth={strokeWidth} strokeLinecap="round" />

        {/* The Man - using rosepink for a softer cute look */}
        {/* Head */}
        {wrongGuesses >= 1 && (
          <circle cx="75" cy="35" r="10" stroke={rosePink} strokeWidth={strokeWidth} fill="none" />
        )}
        
        {/* Body */}
        {wrongGuesses >= 2 && (
          <line x1="75" y1="45" x2="75" y2="75" stroke={rosePink} strokeWidth={strokeWidth} strokeLinecap="round" />
        )}

        {/* Left Arm */}
        {wrongGuesses >= 3 && (
          <line x1="75" y1="55" x2="60" y2="65" stroke={rosePink} strokeWidth={strokeWidth} strokeLinecap="round" />
        )}

        {/* Right Arm */}
        {wrongGuesses >= 4 && (
          <line x1="75" y1="55" x2="90" y2="65" stroke={rosePink} strokeWidth={strokeWidth} strokeLinecap="round" />
        )}

        {/* Left Leg */}
        {wrongGuesses >= 5 && (
          <line x1="75" y1="75" x2="60" y2="95" stroke={rosePink} strokeWidth={strokeWidth} strokeLinecap="round" />
        )}

        {/* Right Leg */}
        {wrongGuesses >= 6 && (
          <line x1="75" y1="75" x2="90" y2="95" stroke={rosePink} strokeWidth={strokeWidth} strokeLinecap="round" />
        )}
      </svg>
    </div>
  );
};

export default HangmanVisual;
