import React, { useState } from 'react';
import { db } from '../db';

interface LoginPageProps {
  onLogin: (username: string, password: string) => Promise<void>;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isRegistering) {
        // Register new customer
        const user = await db.register(username, email, password, 'customer');

        if (!user) {
          setError('Registration failed. Please try again.');
          setLoading(false);
          return;
        }

        alert('Registration successful! Please login.');
        setIsRegistering(false);
        setUsername('');
        setEmail('');
        setPassword('');
      } else {
        // Login - backend determines role
        const user = await db.login(email || username, password);

        if (!user) {
          setError('Invalid credentials. Please check your email and password.');
          setLoading(false);
          return;
        }

        // Call onLogin which will redirect based on role
        await onLogin(email || username, password);
      }
    } catch (err) {
      setError('Connection error. Please try again.');
      console.error('Auth error:', err);
    }

    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto py-12 px-4">
      <div className="glass-panel rounded-[2.5rem] p-10 space-y-8 shadow-2xl border border-white/10 relative overflow-hidden">
        {/* Background glow */}
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-amber-500/10 blur-[80px] rounded-full"></div>

        <div className="text-center relative z-10">
          <h2 className="text-4xl font-black tracking-tighter honey-text">
            {isRegistering ? 'JOIN THE CLUB' : 'WELCOME BACK'}
          </h2>
          <p className="text-white/40 text-sm mt-2 font-medium">
            {isRegistering ? 'Create your Delight Cuisine account' : 'Access your gourmet dashboard'}
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-white/5 p-1 rounded-2xl relative z-10">
          <button
            onClick={() => { setIsRegistering(false); setError(''); }}
            className={`flex-1 py-3 rounded-xl text-xs font-black transition-all ${!isRegistering ? 'bg-amber-500 text-black shadow-lg' : 'text-white/40 hover:text-white'}`}
          >
            LOGIN
          </button>
          <button
            onClick={() => { setIsRegistering(true); setError(''); }}
            className={`flex-1 py-3 rounded-xl text-xs font-black transition-all ${isRegistering ? 'bg-amber-500 text-black shadow-lg' : 'text-white/40 hover:text-white'}`}
          >
            REGISTER
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 relative z-10">
          {error && (
            <div className="bg-red-500/10 border border-red-500/50 text-red-500 text-[10px] font-black p-3 rounded-xl text-center uppercase tracking-widest">
              {error}
            </div>
          )}

          {/* Username field (only for registration) */}
          {isRegistering && (
            <div className="space-y-2">
              <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] ml-1">Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="johndoe"
                className="w-full bg-white/5 border border-white/10 rounded-2xl px-5 py-4 outline-none focus:border-amber-500 transition-all text-sm placeholder:text-white/10"
                required={isRegistering}
              />
            </div>
          )}

          <div className="space-y-2">
            <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] ml-1">
              {isRegistering ? 'Email Address' : 'Email'}
            </label>
            <input
              type={isRegistering ? "email" : "text"}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={isRegistering ? "your@email.com" : "your@email.com"}
              className="w-full bg-white/5 border border-white/10 rounded-2xl px-5 py-4 outline-none focus:border-amber-500 transition-all text-sm placeholder:text-white/10"
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] ml-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-white/5 border border-white/10 rounded-2xl px-5 py-4 outline-none focus:border-amber-500 transition-all text-sm placeholder:text-white/10"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full honey-gradient py-5 rounded-2xl text-black font-black text-sm shadow-xl shadow-amber-500/20 active:scale-95 transition-all uppercase tracking-widest mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'PROCESSING...' : (isRegistering ? 'CREATE ACCOUNT' : 'SECURE SIGN IN')}
          </button>
        </form>

        <p className="text-center text-[10px] text-white/20 font-bold uppercase tracking-widest">
          Encryption Active • Delight OS v2.0
        </p>
      </div>
    </div>
  );
};

export default LoginPage;