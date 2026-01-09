
import React, { useState, useEffect, useCallback } from 'react';
import HangmanVisual from './components/HangmanVisual';

const MAX_WRONG_GUESSES = 6;
const RANGE_MAX = 100;

function App() {
  const [targetNumber, setTargetNumber] = useState<number>(0);
  const [currentGuess, setCurrentGuess] = useState<string>('');
  const [wrongGuesses, setWrongGuesses] = useState<number>(0);
  const [message, setMessage] = useState<string>('Determine the secret value between 1 and 100');
  const [gameStatus, setGameStatus] = useState<'playing' | 'won' | 'lost'>('playing');
  const [history, setHistory] = useState<{guess: number, type: 'low' | 'high'}[]>([]);

  const startNewGame = useCallback(() => {
    setTargetNumber(Math.floor(Math.random() * RANGE_MAX) + 1);
    setWrongGuesses(0);
    setGameStatus('playing');
    setMessage('Determine the secret value between 1 and 100');
    setHistory([]);
    setCurrentGuess('');
  }, []);

  useEffect(() => {
    startNewGame();
  }, [startNewGame]);

  const handleGuess = (e: React.FormEvent) => {
    e.preventDefault();
    if (gameStatus !== 'playing') return;

    const numGuess = parseInt(currentGuess);
    if (isNaN(numGuess) || numGuess < 1 || numGuess > RANGE_MAX) {
      setMessage(`Range: 1 to ${RANGE_MAX}`);
      return;
    }

    if (numGuess === targetNumber) {
      setGameStatus('won');
      setMessage(`Exceptional. ${targetNumber} is correct.`);
    } else {
      const isLow = numGuess < targetNumber;
      const type = isLow ? 'low' : 'high';
      
      setWrongGuesses(prev => {
        const next = prev + 1;
        if (next >= MAX_WRONG_GUESSES) {
          setGameStatus('lost');
          setMessage(`Riddle Concluded. Secret was ${targetNumber}.`);
        } else {
          setMessage(`${numGuess} is too ${type}.`);
        }
        return next;
      });

      setHistory(prev => [{ guess: numGuess, type }, ...prev]);
      setCurrentGuess('');
    }
  };

  const bearPosition = (wrongGuesses / MAX_WRONG_GUESSES) * 100;

  return (
    <div className="min-h-screen flex flex-col items-center selection:bg-rosepink selection:text-white">
      {/* Top Navbar */}
      <nav className="w-full h-16 border-b border-rosepink/10 flex items-center justify-between px-6 md:px-12 bg-white/50 backdrop-blur-sm z-50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-darkpink flex items-center justify-center">
            <i className="fas fa-leaf text-white text-xs"></i>
          </div>
          <span className="font-bold tracking-[0.2em] uppercase text-sm">Rosebud</span>
        </div>
        <div className="flex gap-6 items-center text-[10px] font-bold uppercase tracking-widest text-rosepink/60">
          <button onClick={startNewGame} className="hover:text-darkpink transition-colors">Reset Game</button>
          <span className="w-1 h-1 rounded-full bg-rosepink/20"></span>
          <span>v1.2.5</span>
        </div>
      </nav>

      {/* Hero Header */}
      <header className="mt-16 mb-12 text-center px-4">
        <h1 className="text-5xl md:text-6xl font-light text-darkpink tracking-tighter mb-4">
          Rosebud <span className="font-bold">Riddle</span>
        </h1>
        <div className="h-1 w-24 bg-rosepink/30 mx-auto rounded-full"></div>
      </header>

      <main className="w-full max-w-5xl px-4 grid grid-cols-1 lg:grid-cols-12 gap-8 mb-20 flex-grow">
        
        {/* Left Aspect: The Visuals & Bear Runner */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <div className="glass-card rounded-[2rem] p-10 flex flex-col items-center relative overflow-hidden shadow-sm">
            
            {/* Integrated Bear Track */}
            <div className="w-full mb-12 px-4">
              <div className="flex justify-between items-end mb-4">
                <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-rosepink">Bear's Progress</span>
                <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-rosepink/40">Attempt {wrongGuesses}/{MAX_WRONG_GUESSES}</span>
              </div>
              <div className="relative h-px w-full bg-rosepink/20">
                <div 
                  className="absolute top-1/2 -translate-y-1/2 transition-all duration-1000 ease-out flex flex-col items-center"
                  style={{ left: `calc(${bearPosition}% - 12px)` }}
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" className="text-darkpink mb-1 animate-bounce">
                    <path d="M12,2C15.31,2 18,4.69 18,8C18,9.15 17.67,10.23 17.1,11.15L21,19H19L17.5,16H6.5L5,19H3L6.9,11.15C6.33,10.23 6,9.15 6,8C6,4.69 8.69,2 12,2M12,4A4,4 0 0,0 8,8A4,4 0 0,0 12,12A4,4 0 0,0 16,8A4,4 0 0,0 12,4" />
                  </svg>
                </div>
                <div className="absolute right-0 top-1/2 -translate-y-1/2 text-rosepink/30">
                  <i className="fas fa-flag-checkered text-xs"></i>
                </div>
              </div>
            </div>

            <div className={`${gameStatus === 'playing' ? 'float-animation' : ''} h-52 flex items-center`}>
              <HangmanVisual wrongGuesses={wrongGuesses} />
            </div>

            <div className="w-full mt-10">
              <div className="text-center mb-8">
                <p className={`text-xl font-medium tracking-tight transition-all duration-500 ${gameStatus === 'lost' ? 'text-rosepink' : 'text-darkpink'}`}>
                  {message}
                </p>
              </div>

              {gameStatus === 'playing' ? (
                <form onSubmit={handleGuess} className="flex flex-col md:flex-row gap-4 max-w-md mx-auto">
                  <input
                    type="number"
                    value={currentGuess}
                    onChange={(e) => setCurrentGuess(e.target.value)}
                    className="flex-1 p-5 text-2xl text-center rounded-2xl border border-rosepink/20 focus:outline-none focus:border-darkpink/40 bg-white shadow-inner font-light"
                    autoFocus
                  />
                  <button
                    type="submit"
                    className="px-10 py-5 bg-darkpink text-white font-bold rounded-2xl transition-all shadow-lg hover:shadow-rosepink/20 active:scale-95 text-xs uppercase tracking-[0.3em]"
                  >
                    Submit
                  </button>
                </form>
              ) : (
                <button
                  onClick={startNewGame}
                  className="block mx-auto px-12 py-5 border-2 border-darkpink text-darkpink font-bold rounded-2xl transition-all hover:bg-darkpink hover:text-white text-xs uppercase tracking-[0.3em]"
                >
                  Restart Experience
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Right Aspect: Insights & Meta */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="glass-card rounded-[2rem] p-8 flex flex-col h-full shadow-sm">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-xs font-bold uppercase tracking-[0.3em]">History</h2>
              <i className="fas fa-fingerprint text-rosepink/30 text-lg"></i>
            </div>
            
            <div className="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2 min-h-[200px]">
              {history.length === 0 ? (
                <div className="h-full flex items-center justify-center opacity-20 flex-col gap-2">
                  <i className="fas fa-inbox text-2xl"></i>
                  <span className="text-[10px] uppercase tracking-widest font-bold">No Data</span>
                </div>
              ) : (
                history.map((h, i) => (
                  <div key={i} className="flex justify-between items-center p-4 rounded-2xl bg-white border border-rosepink/5 group hover:border-rosepink/20 transition-all">
                    <span className="text-lg font-light text-darkpink">{h.guess}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-[9px] font-bold uppercase tracking-widest opacity-40">{h.type}</span>
                      <div className={`w-1.5 h-1.5 rounded-full ${h.type === 'low' ? 'bg-rosepink' : 'bg-darkpink'}`}></div>
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="mt-8 pt-6 border-t border-rosepink/10 text-center">
              <p className="text-[9px] uppercase tracking-[0.3em] font-bold opacity-40 mb-1">Produced By</p>
              <p className="text-xs font-bold tracking-widest text-darkpink">Creative Design Studio</p>
            </div>
          </div>
        </div>
      </main>

      {/* Dark Pink Professional Footer - Refined and Corrected */}
      <footer className="w-full py-10 px-12 bg-darkpink flex flex-col md:flex-row justify-between items-center gap-6 text-[10px] font-bold uppercase tracking-[0.4em]">
        <div className="flex gap-10 text-white/90">
          <span className="tracking-[0.5em]">Premium Experience</span>
        </div>
        <div className="text-center md:text-right text-white/60">
          Rosebud Riddle &copy; 2025. All Rights Reserved.
        </div>
      </footer>
    </div>
  );
}

export default App;
