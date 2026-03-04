import React from 'react';

const InterviewFeedback = ({ feedbackData, isLoading }) => {

    if (isLoading) {
        return (
            <div className="h-full bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 flex flex-col items-center justify-center space-y-4 animate-pulse shrink-0 w-80">
                <div className="w-12 h-12 border-4 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-blue-100 font-medium text-center">AI Employer Engine is evaluating your response...</p>
            </div>
        );
    }

    if (!feedbackData) {
        return (
            <div className="h-full bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 flex flex-col items-center justify-center shrink-0 w-80">
                <div className="text-6xl mb-4 opacity-50">🤖</div>
                <p className="text-gray-400 text-center font-medium">Your real-time AI feedback will appear here after you answer.</p>
            </div>
        );
    }

    const { confidence, clarity, technical_accuracy, feedback, improvement_tips } = feedbackData;

    const getScoreColor = (score) => {
        if (score >= 8) return 'text-green-400';
        if (score >= 5) return 'text-yellow-400';
        return 'text-red-400';
    };

    const getScoreBg = (score) => {
        if (score >= 8) return 'bg-green-400';
        if (score >= 5) return 'bg-yellow-400';
        return 'bg-red-400';
    }

    return (
        <div className="h-full bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 flex flex-col space-y-6 shrink-0 w-80 text-white shadow-2xl transition-all duration-500 transform translate-x-0">
            <h3 className="text-xl font-bold border-b border-white/20 pb-3 flex items-center">
                <span className="mr-2">📊</span> Evaluation Results
            </h3>

            {/* Scores */}
            <div className="space-y-4">
                {[{ label: 'Confidence', score: confidence }, { label: 'Clarity', score: clarity }, { label: 'Technical', score: technical_accuracy }].map((item, idx) => (
                    <div key={idx} className="space-y-1">
                        <div className="flex justify-between text-sm font-medium">
                            <span className="text-gray-300">{item.label}</span>
                            <span className={`font-bold ${getScoreColor(item.score)}`}>{item.score}/10</span>
                        </div>
                        <div className="w-full bg-white/10 rounded-full h-2">
                            <div className={`h-2 rounded-full ${getScoreBg(item.score)} transition-all duration-1000 ease-out`} style={{ width: `${(item.score / 10) * 100}%` }}></div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Feedback text */}
            <div className="flex-grow space-y-4 overflow-y-auto pr-2 custom-scrollbar">
                <div className="bg-blue-900/30 border border-blue-500/30 rounded-xl p-4">
                    <h4 className="text-blue-300 text-xs font-bold uppercase tracking-wider mb-2">Detailed Feedback</h4>
                    <p className="text-sm text-gray-200 leading-relaxed">{feedback}</p>
                </div>

                <div className="bg-purple-900/30 border border-purple-500/30 rounded-xl p-4">
                    <h4 className="text-purple-300 text-xs font-bold uppercase tracking-wider mb-2">Improvement Tips</h4>
                    <p className="text-sm text-gray-200 leading-relaxed">{improvement_tips}</p>
                </div>
            </div>
        </div>
    );
};

export default InterviewFeedback;
