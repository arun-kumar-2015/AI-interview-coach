import React, { useState, useEffect, useRef, useCallback } from 'react';
import Timer from './Timer';
import InterviewFeedback from './InterviewFeedback';

// A mock list of questions for the demo. In a real app, these could be fetched from the backend.
const MOCK_QUESTIONS = {
    'Software Developer': [
        "Could you walk me through your experience building full-stack web applications?",
        "How do you handle writing unit tests and ensuring code quality?",
        "Describe a time you had to optimize a slow-performing database query or API endpoint."
    ],
    'Data Analyst': [
        "What is your process for cleaning and preparing messy datasets?",
        "Can you explain the difference between correlation and causation with an example?",
        "How do you communicate complex data findings to non-technical stakeholders?"
    ],
    'HR': [
        "How do you handle conflicts between two team members?",
        "What strategies do you use to improve employee retention?",
        "Describe your experience with modern ATS systems and recruiting."
    ],
    'Marketing Manager': [
        "How do you measure the success of a digital marketing campaign?",
        "Describe a time a campaign failed and what you learned from it.",
        "What is your approach to managing a marketing budget?"
    ]
};

const VideoInterview = () => {
    const [role, setRole] = useState('Software Developer');
    const [isInterviewStarted, setIsInterviewStarted] = useState(false);
    const [isInterviewFinished, setIsInterviewFinished] = useState(false);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

    const [isRecording, setIsRecording] = useState(false);
    const [transcript, setTranscript] = useState('');

    const [isLoadingFeedback, setIsLoadingFeedback] = useState(false);
    const [currentFeedback, setCurrentFeedback] = useState(null);
    const [allFeedbacks, setAllFeedbacks] = useState([]);
    const [isSpeaking, setIsSpeaking] = useState(false);

    const videoRef = useRef(null);
    const streamRef = useRef(null);
    const recognitionRef = useRef(null);

    // Initialize Speech Recognition
    useEffect(() => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = true;
            recognitionRef.current.interimResults = true;

            recognitionRef.current.onresult = (event) => {
                let currentTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    currentTranscript += event.results[i][0].transcript;
                }
                setTranscript((prev) => prev + " " + currentTranscript);
            };

            recognitionRef.current.onerror = (event) => {
                console.error("Speech recognition error", event.error);
                setIsRecording(false);
            };
        } else {
            console.warn("Speech Recognition API is not supported in this browser.");
        }

        return () => {
            stopMediaTracks();
            if (recognitionRef.current) {
                recognitionRef.current.stop();
            }
            if (window.speechSynthesis) {
                window.speechSynthesis.cancel();
            }
        };
    }, []);

    // Speak the question text whenever a new question is displayed
    useEffect(() => {
        if (isInterviewStarted && !currentFeedback && !isInterviewFinished) {
            speakQuestion(MOCK_QUESTIONS[role][currentQuestionIndex]);
        }
    }, [isInterviewStarted, currentQuestionIndex, currentFeedback, isInterviewFinished, role]);

    const speakQuestion = (text) => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel(); // Stop any currently speaking audio
            const utterance = new SpeechSynthesisUtterance(text);

            // Configure voice settings to sound professional
            utterance.rate = 0.95; // Slightly slower
            utterance.pitch = 1.0;

            utterance.onstart = () => setIsSpeaking(true);
            utterance.onend = () => setIsSpeaking(false);
            utterance.onerror = () => setIsSpeaking(false);

            window.speechSynthesis.speak(utterance);
        }
    };

    const stopMediaTracks = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
        }
    };

    const startInterview = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
            streamRef.current = stream;
            setIsInterviewStarted(true);
            setCurrentQuestionIndex(0);
            setTranscript('');
            setAllFeedbacks([]);
            setCurrentFeedback(null);
            setIsInterviewFinished(false);
        } catch (err) {
            console.error("Error accessing media devices.", err);
            alert("Please allow camera and microphone access to start the interview.");
        }
    };

    const toggleRecording = () => {
        if (isRecording) {
            recognitionRef.current?.stop();
            setIsRecording(false);
        } else {
            setTranscript('');
            recognitionRef.current?.start();
            setIsRecording(true);
        }
    };

    const submitAnswer = async () => {
        if (isRecording) {
            toggleRecording(); // Stop recording if active
        }
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel(); // Stop speaking when user submits answer
        }

        setIsLoadingFeedback(true);
        const question = MOCK_QUESTIONS[role][currentQuestionIndex];

        const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        try {
            const response = await fetch(`${API_BASE_URL}/api/video-interview`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    role: role,
                    question: question,
                    answer: transcript || "No answer provided visually or audibly."
                })
            });

            if (!response.ok) throw new Error("API failed");

            const feedback = await response.json();
            setCurrentFeedback(feedback);
            setAllFeedbacks(prev => [...prev, feedback]);

        } catch (error) {
            console.error("Error fetching feedback:", error);
            // Fallback dummy feedback for resilience
            setCurrentFeedback({
                confidence: 5, clarity: 5, technical_accuracy: 5,
                feedback: "We couldn't process your answer at this time due to a network error.",
                improvement_tips: "Please try answering the next question."
            });
        } finally {
            setIsLoadingFeedback(false);
            setTranscript('');
        }
    };

    const nextQuestion = () => {
        if (currentQuestionIndex < MOCK_QUESTIONS[role].length - 1) {
            setCurrentQuestionIndex(prev => prev + 1);
            setCurrentFeedback(null);
            setTranscript('');
        } else {
            finishInterview();
        }
    };

    const handleTimeUp = () => {
        if (!currentFeedback && !isLoadingFeedback && isInterviewStarted) {
            submitAnswer();
        }
    };

    const finishInterview = () => {
        stopMediaTracks();
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
        setIsInterviewStarted(false);
        setIsInterviewFinished(true);
    };

    const calculateTotalScore = () => {
        if (allFeedbacks.length === 0) return 0;
        const total = allFeedbacks.reduce((acc, curr) =>
            acc + curr.confidence + curr.clarity + curr.technical_accuracy, 0);
        const maxScore = allFeedbacks.length * 30; // 3 attributes * 10
        return Math.round((total / maxScore) * 100);
    };

    if (isInterviewFinished) {
        return (
            <div className="max-w-4xl mx-auto p-8 bg-gray-900 rounded-2xl shadow-2xl text-white mt-10 border border-gray-800">
                <h2 className="text-3xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
                    Interview Completed! 🎉
                </h2>

                <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 mb-8 border border-white/20">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xl font-semibold">Total Performance Score</h3>
                        <div className={`text-4xl font-bold ${calculateTotalScore() >= 70 ? 'text-green-400' : 'text-yellow-400'}`}>
                            {calculateTotalScore()}%
                        </div>
                    </div>
                    <p className="text-gray-300">Great job completing the simulation! Review your feedback below to see where you can improve.</p>
                </div>

                <div className="space-y-6">
                    <h3 className="text-2xl font-semibold mb-4 border-b border-gray-700 pb-2">Feedback Summary</h3>
                    {allFeedbacks.map((fb, idx) => (
                        <div key={idx} className="bg-gray-800 rounded-lg p-5 border border-gray-700">
                            <h4 className="font-bold text-gray-200 mb-2">Q{idx + 1}: {MOCK_QUESTIONS[role][idx]}</h4>
                            <div className="flex space-x-4 mb-3 text-sm">
                                <span className="bg-gray-900 px-3 py-1 rounded-full text-blue-300">Confidence: {fb.confidence}/10</span>
                                <span className="bg-gray-900 px-3 py-1 rounded-full text-green-300">Clarity: {fb.clarity}/10</span>
                                <span className="bg-gray-900 px-3 py-1 rounded-full text-purple-300">Tech: {fb.technical_accuracy}/10</span>
                            </div>
                            <p className="text-gray-400 text-sm italic mb-2">"{fb.feedback}"</p>
                            <p className="text-blue-400 text-sm font-medium">💡 Tip: {fb.improvement_tips}</p>
                        </div>
                    ))}
                </div>

                <div className="mt-8 flex justify-center">
                    <button
                        onClick={() => window.print()}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-8 rounded-full transition-all shadow-lg hover:shadow-indigo-500/30 flex items-center"
                    >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                        Download Report PDF
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-[85vh] flex flex-col pt-4">
            {/* Header */}
            <div className="bg-gray-900 text-white rounded-t-2xl p-6 shadow-xl border-b border-gray-800 flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400">
                        Live AI Interview Simulation
                    </h1>
                    <p className="text-blue-200/60 mt-1 font-medium tracking-wide">Powered by AI Employer Engine</p>
                </div>

                {!isInterviewStarted && (
                    <div className="flex space-x-4">
                        <select
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                            className="bg-gray-800 border border-gray-700 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
                        >
                            {Object.keys(MOCK_QUESTIONS).map(r => <option key={r} value={r}>{r}</option>)}
                        </select>
                        <button
                            onClick={startInterview}
                            className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-6 py-2.5 rounded-lg font-bold shadow-lg shadow-green-500/30 transition-all transform hover:scale-105"
                        >
                            Start Interview
                        </button>
                    </div>
                )}
            </div>

            {/* Main Content Area */}
            <div className="flex-1 bg-gray-950 p-6 rounded-b-2xl shadow-2xl flex space-x-6 overflow-hidden relative border border-t-0 border-gray-800">

                {!isInterviewStarted ? (
                    <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-gray-900/80 backdrop-blur-sm rounded-b-2xl">
                        <div className="text-6xl mb-4 animate-bounce">🎥</div>
                        <h2 className="text-2xl text-white font-bold mb-2">Ready for your interview?</h2>
                        <p className="text-gray-400 text-center max-w-md">Select your role and click start. Make sure your camera and microphone are connected and allowed.</p>
                    </div>
                ) : null}

                {/* Left Side: Video Panels & Controls */}
                <div className="flex-1 flex flex-col space-y-4">

                    {/* Active Question Box */}
                    <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl p-5 shadow-lg relative overflow-hidden group">
                        <div className="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
                        <div className="flex justify-between items-start mb-2">
                            <span className="text-blue-300 font-bold text-sm tracking-wider uppercase">Question {currentQuestionIndex + 1} of {MOCK_QUESTIONS[role].length}</span>
                            <Timer initialSeconds={60} isActive={isInterviewStarted && !currentFeedback && !isLoadingFeedback} onTimeUp={handleTimeUp} />
                        </div>
                        <h3 className="text-2xl font-medium text-white leading-relaxed animate-[fadeIn_0.5s_ease-out]">
                            "{MOCK_QUESTIONS[role][currentQuestionIndex]}"
                        </h3>
                    </div>

                    {/* Video Grid */}
                    <div className="flex-1 grid grid-cols-2 gap-4 min-h-[300px]">
                        {/* AI Avatar Panel */}
                        <div className="bg-gray-900 rounded-xl border border-gray-800 relative overflow-hidden shadow-inner flex flex-col items-center justify-center group">
                            <div className="absolute top-4 left-4 bg-black/50 text-xs text-white px-2 py-1 rounded backdrop-blur-md z-10 flex items-center">
                                <span className="w-2 h-2 rounded-full bg-blue-500 mr-2 animate-pulse"></span>
                                AI Employer
                            </div>
                            {/* Styling a CSS-based AI Avatar pulsing head */}
                            <div className="relative">
                                <div className={`w-32 h-32 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(99,102,241,0.5)] z-10 relative transition-transform duration-300 ${isSpeaking ? 'scale-110 shadow-[0_0_50px_rgba(99,102,241,0.8)]' : 'scale-100'}`}>
                                    <span className="text-5xl">{isSpeaking ? '🗣️' : '🤖'}</span>
                                </div>
                                {/* Animated rings */}
                                <div className={`absolute top-0 left-0 w-32 h-32 border-4 border-indigo-500 rounded-full ${isSpeaking ? 'animate-[ping_1s_cubic-bezier(0,0,0.2,1)_infinite] opacity-100' : 'animate-[ping_2s_cubic-bezier(0,0,0.2,1)_infinite] opacity-0'} ${(isLoadingFeedback && !isSpeaking) ? 'opacity-100' : ''}`}></div>
                            </div>
                            {isLoadingFeedback && !isSpeaking && <p className="mt-6 text-indigo-300 animate-pulse font-medium">Processing your response...</p>}
                            {isSpeaking && <p className="mt-6 text-blue-300 animate-pulse font-medium">Asking question...</p>}
                        </div>

                        {/* User Webcam Panel */}
                        <div className="bg-gray-900 rounded-xl border border-gray-800 relative overflow-hidden shadow-inner">
                            <div className="absolute top-4 left-4 bg-black/50 text-xs text-white px-2 py-1 rounded backdrop-blur-md z-10 flex items-center">
                                <span className="w-2 h-2 rounded-full bg-red-500 mr-2 animate-pulse"></span>
                                You
                            </div>
                            <video
                                ref={videoRef}
                                autoPlay
                                playsInline
                                muted
                                className="w-full h-full object-cover transform scale-x-[-1]"
                            ></video>
                        </div>
                    </div>

                    {/* Controls & Transcript Area */}
                    <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50 backdrop-blur-sm flex items-start space-x-4">

                        <button
                            onClick={toggleRecording}
                            disabled={!!currentFeedback || isLoadingFeedback}
                            className={`p-4 rounded-full flex-shrink-0 transition-all ${isRecording
                                ? 'bg-red-500 hover:bg-red-600 shadow-[0_0_20px_rgba(239,68,68,0.5)] animate-pulse'
                                : 'bg-gray-700 hover:bg-gray-600 text-white'
                                } ${(!!currentFeedback || isLoadingFeedback) ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
                        </button>

                        <div className="flex-1 bg-black/30 rounded-lg p-3 min-h-[60px] max-h-[120px] overflow-y-auto border border-gray-800">
                            {transcript ? (
                                <p className="text-gray-300 text-sm leading-relaxed">{transcript}</p>
                            ) : (
                                <p className="text-gray-600 text-sm italic mt-2">
                                    {isRecording ? "Listening... Speak now." : "Click the microphone to start answering..."}
                                </p>
                            )}
                        </div>

                        <div className="flex flex-col space-y-2 flex-shrink-0 w-32">
                            {!currentFeedback ? (
                                <button
                                    onClick={submitAnswer}
                                    disabled={isLoadingFeedback || transcript.length < 5}
                                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:text-gray-500 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                                >
                                    Submit Answer
                                </button>
                            ) : (
                                <button
                                    onClick={nextQuestion}
                                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors shadow-[0_0_15px_rgba(22,163,74,0.4)]"
                                >
                                    {currentQuestionIndex < MOCK_QUESTIONS[role].length - 1 ? 'Next Question' : 'Finish'}
                                </button>
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Side: Dynamic Feedback Panel */}
                <InterviewFeedback feedbackData={currentFeedback} isLoading={isLoadingFeedback} />
            </div>
        </div>
    );
};

export default VideoInterview;
