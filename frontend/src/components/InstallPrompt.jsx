import React, { useState, useEffect } from 'react';

const InstallPrompt = () => {
    const [deferredPrompt, setDeferredPrompt] = useState(null);
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const handler = (e) => {
            // Prevent the mini-infobar from appearing on mobile
            e.preventDefault();
            // Stash the event so it can be triggered later.
            setDeferredPrompt(e);
            // Update UI notify the user they can install the PWA
            setIsVisible(true);
        };

        window.addEventListener('beforeinstallprompt', handler);

        return () => window.removeEventListener('beforeinstallprompt', handler);
    }, []);

    const handleInstallClick = async () => {
        if (!deferredPrompt) return;

        // Show the install prompt
        deferredPrompt.prompt();

        // Wait for the user to respond to the prompt
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`User response to the install prompt: ${outcome}`);

        // We've used the prompt, and can't use it again, throw it away
        setDeferredPrompt(null);
        setIsVisible(false);
    };

    if (!isVisible) return null;

    return (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] animate-bounce">
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-1 rounded-2xl shadow-2xl">
                <div className="bg-gray-900 px-6 py-4 rounded-[14px] flex items-center space-x-6">
                    <div className="flex-shrink-0">
                        <span className="text-3xl">📱</span>
                    </div>
                    <div>
                        <h4 className="text-white font-bold text-lg leading-tight">Install AI Coach</h4>
                        <p className="text-gray-400 text-sm">Add to home screen for the full app experience</p>
                    </div>
                    <div className="flex space-x-3">
                        <button
                            onClick={() => setIsVisible(false)}
                            className="text-gray-500 hover:text-white transition-colors"
                        >
                            Later
                        </button>
                        <button
                            onClick={handleInstallClick}
                            className="bg-indigo-500 hover:bg-indigo-400 text-white font-bold px-4 py-2 rounded-lg transition-all"
                        >
                            Install Now
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default InstallPrompt;
