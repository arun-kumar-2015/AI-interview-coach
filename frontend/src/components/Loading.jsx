import React from 'react';

const Loading = ({ message = 'Loading...' }) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="text-center">
        {/* Animated Robot Icon */}
        <div className="mb-8">
          <div className="relative inline-block">
            <span className="text-6xl animate-bounce">🤖</span>
            <div className="absolute -top-2 -right-2 w-4 h-4 bg-green-500 rounded-full animate-ping"></div>
          </div>
        </div>
        
        {/* Loading Spinner */}
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        </div>
        
        {/* Message */}
        <h2 className="text-xl font-semibold text-gray-700 mb-2">{message}</h2>
        <p className="text-gray-500">Please wait while we prepare your interview experience...</p>
        
        {/* Progress Dots */}
        <div className="flex justify-center mt-6 space-x-2">
          <div className="w-3 h-3 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-3 h-3 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-3 h-3 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  );
};

export default Loading;
