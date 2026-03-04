import React, { useState, useEffect } from 'react';

const Timer = ({ initialSeconds, onTimeUp, isActive }) => {
    const [seconds, setSeconds] = useState(initialSeconds);

    useEffect(() => {
        let interval = null;

        // Reset timer when it becomes active again (e.g., new question)
        if (isActive && seconds === 0) {
            setSeconds(initialSeconds);
        }

        if (isActive && seconds > 0) {
            interval = setInterval(() => {
                setSeconds((seconds) => seconds - 1);
            }, 1000);
        } else if (seconds === 0 && isActive) {
            clearInterval(interval);
            if (onTimeUp) {
                onTimeUp();
            }
        }
        return () => clearInterval(interval);
    }, [isActive, seconds, onTimeUp, initialSeconds]);

    // Format time as MM:SS
    const formatTime = (timeInSeconds) => {
        const minutes = Math.floor(timeInSeconds / 60)
            .toString()
            .padStart(2, '0');
        const remainingSeconds = (timeInSeconds % 60).toString().padStart(2, '0');
        return `${minutes}:${remainingSeconds}`;
    };

    return (
        <div className={`flex items-center space-x-2 font-mono text-xl font-bold p-3 rounded-lg shadow-sm border ${seconds <= 10 ? 'bg-red-50 border-red-200 text-red-600 animate-pulse' : 'bg-white border-gray-200 text-gray-700'}`}>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{formatTime(seconds)}</span>
        </div>
    );
};

export default Timer;
