import React, { useState } from 'react';
import Navbar from './components/Navbar';
import AdminDashboard from './components/AdminDashboard';

export default function App() {
  const [lang, setLang] = useState('en');

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col selection:bg-emerald-500 selection:text-white">
      <div className="no-print">
        <Navbar
          lang={lang}
          setLang={setLang}
          onOpenChat={() => {}}
          onResetHome={() => {}}
          currentView="admin"
          onToggleView={() => {}}
        />
      </div>

      <main className="flex-1">
        <AdminDashboard onBackToFarmerView={() => {}} />
      </main>
    </div>
  );
}
