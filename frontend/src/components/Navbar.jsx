import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = ({ sessionId, onSessionClear }) => {
  const location = useLocation();

  const navLinks = [
    { path: '/', label: 'Home', icon: '🏠' },
    { path: '/upload', label: 'Upload Resume', icon: '📄' },
    { path: '/interview', label: 'Interview', icon: '🎯' },
    { path: '/video-interview', label: 'Live Video Interview', icon: '🎥' },
    { path: '/hr-questions', label: 'HR Questions', icon: '👔' },
    { path: '/improve', label: 'Improve Resume', icon: '📝' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl">🤖</span>
            <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
              AI Interview Coach
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 
                  ${isActive(link.path)
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
              >
                <span className="mr-1">{link.icon}</span>
                {link.label}
              </Link>
            ))}
          </div>

          {/* Session Status */}
          <div className="flex items-center space-x-3">
            {sessionId && (
              <div className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <span className="text-sm text-gray-600">Session Active</span>
                <button
                  onClick={onSessionClear}
                  className="text-sm text-red-600 hover:text-red-700 font-medium"
                >
                  Clear
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden border-t border-gray-100">
        <div className="flex items-center justify-around py-2">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`flex flex-col items-center px-3 py-1 text-xs 
                ${isActive(link.path)
                  ? 'text-primary-600'
                  : 'text-gray-500'
                }`}
            >
              <span className="text-lg mb-1">{link.icon}</span>
              {link.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
