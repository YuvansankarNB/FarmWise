import React from 'react';
import { Sprout } from 'lucide-react';
import { translations } from '../utils/translations';

export default function Navbar({ lang, setLang, onOpenChat, onResetHome }) {
  const t = translations[lang] || translations.en;

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-emerald-100 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div 
            onClick={onResetHome}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-700 to-green-500 flex items-center justify-center shadow-md shadow-emerald-700/20 group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold tracking-tight text-slate-900 group-hover:text-emerald-700 transition-colors">
                  Farmwise<span className="text-emerald-600">AI</span>
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">
                {lang === 'ta' ? 'பல்-மாதிரி வேளாண்மை நுண்ணறிவு தளம்' : 'Multi-Model Agricultural Intelligence Platform'}
              </p>
            </div>
          </div>

          {/* Right actions: Language toggle */}
          <div className="flex items-center gap-3">
            {/* Language Selector */}
            <div className="flex items-center bg-slate-100 rounded-lg p-0.5 border border-slate-200 text-xs font-medium">
              <button
                onClick={() => setLang('en')}
                className={`px-2.5 py-1 rounded-md transition-all ${
                  lang === 'en' ? 'bg-white text-emerald-700 font-bold shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                EN
              </button>
              <button
                onClick={() => setLang('ta')}
                className={`px-2.5 py-1 rounded-md transition-all ${
                  lang === 'ta' ? 'bg-white text-emerald-700 font-bold shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                தமிழ்
              </button>
              <button
                onClick={() => setLang('hi')}
                className={`px-2.5 py-1 rounded-md transition-all ${
                  lang === 'hi' ? 'bg-white text-emerald-700 font-bold shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                हिंदी
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
