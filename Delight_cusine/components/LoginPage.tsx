
import React, { useState } from 'react';
import { User, UserRole } from '../types';
import { db } from '../db';

interface LoginPageProps {
  onLogin: (user: User) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [role, setRole] = useState<UserRole>(UserRole.CUSTOMER);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (isRegistering) {
      if (role === UserRole.ADMIN) {
        setError('Administrators cannot be registered through this portal.');
        return;
      }
      if (db.findUserByEmail(email)) {
        setError('An account with this email already exists.');
        return;
      }
      const newUser: User = {
        id: Math.random().toString(36).substr(2, 9),
        email,
        password,
        role: UserRole.CUSTOMER
      };
      db.saveUser(newUser);
      alert('Registration successful! Please login.');
      setIsRegistering(false);
    } else {
      const user = db.findUserByEmail(email);
      if (user && user.password === password && user.role === role) {
        onLogin(user);
      } else {
        setError('Invalid credentials or role selection.');
      }
    }
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
            onClick={() => { setIsRegistering(true); setRole(UserRole.CUSTOMER); setError(''); }}
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

          {/* Role Selection */}
          <div className="space-y-3">
            <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] ml-1">Select Identity</label>
            <div className="grid grid-cols-2 gap-3">
              <button 
                type="button"
                onClick={() => setRole(UserRole.CUSTOMER)}
                className={`py-3 rounded-xl border text-[10px] font-black transition-all ${role === UserRole.CUSTOMER ? 'border-amber-500 honey-text bg-amber-500/5' : 'border-white/5 bg-white/5 text-white/30'}`}
              >
                CUSTOMER
              </button>
              <button 
                type="button"
                onClick={() => {
                  if(isRegistering) {
                    setError('Admins cannot register.');
                  } else {
                    setRole(UserRole.ADMIN);
                  }
                }}
                className={`py-3 rounded-xl border text-[10px] font-black transition-all ${role === UserRole.ADMIN ? 'border-amber-500 honey-text bg-amber-500/5' : 'border-white/5 bg-white/5 text-white/30'} ${isRegistering ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                ADMIN
              </button>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] ml-1">Email Address</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={role === UserRole.ADMIN ? "admin123@gmail.com" : "your@email.com"}
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
            className="w-full honey-gradient py-5 rounded-2xl text-black font-black text-sm shadow-xl shadow-amber-500/20 active:scale-95 transition-all uppercase tracking-widest mt-4"
          >
            {isRegistering ? 'CREATE ACCOUNT' : 'SECURE SIGN IN'}
          </button>
        </form>

        <p className="text-center text-[10px] text-white/20 font-bold uppercase tracking-widest">
          {role === UserRole.ADMIN ? 'Restricted Access for Staff' : 'Encryption Active • Delight OS v2.0'}
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
