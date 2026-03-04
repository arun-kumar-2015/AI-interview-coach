import React, { useEffect } from 'react';

const Error = ({ message, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 5000);

    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className="fixed bottom-4 right-4 z-50 animate-slide-up">
      <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg shadow-lg max-w-md">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <span className="text-2xl">⚠️</span>
          </div>
          <div className="ml-3 flex-1">
            <p className="text-sm text-red-700 font-medium">Error</p>
            <p className="text-sm text-red-600 mt-1">{message}</p>
          </div>
          <button
            onClick={onClose}
            className="ml-3 text-red-400 hover:text-red-600"
          >
            <span className="text-xl">×</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Error;
