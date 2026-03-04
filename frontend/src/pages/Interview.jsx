import React, { useState, useEffect } from 'react';
import { generateTechnicalQuestions, evaluateAnswer, generateFollowUp } from '../services/api';

const Interview = ({ sessionId }) => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('practice'); // 'practice' or 'feedback'
  const [followUpQuestion, setFollowUpQuestion] = useState(null);

  useEffect(() => {
    loadQuestions();
  }, [sessionId]);

  const loadQuestions = async () => {
    setLoadingQuestions(true);
    setError(null);
    try {
      const response = await generateTechnicalQuestions(sessionId, 'Software Engineer', 10);
      setQuestions(response.questions);
    } catch (err) {
      console.error('Error loading questions:', err);
      setError('Failed to generate questions. Please try again.');
    } finally {
      setLoadingQuestions(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) return;
    
    setLoading(true);
    setError(null);
    setMode('feedback');

    try {
      const currentQuestion = questions[currentQuestionIndex];
      const response = await evaluateAnswer(
        sessionId,
        currentQuestion.question,
        answer,
        currentQuestion.category
      );
      setEvaluation(response);
    } catch (err) {
      console.error('Error evaluating answer:', err);
      setError('Failed to evaluate answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFollowUp = async () => {
    setLoading(true);
    try {
      const currentQuestion = questions[currentQuestionIndex];
      const response = await generateFollowUp(
        sessionId,
        currentQuestion.question,
        answer,
        currentQuestion.category
      );
      setFollowUpQuestion(response);
    } catch (err) {
      console.error('Error generating follow-up:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNextQuestion = () => {
    setAnswer('');
    setEvaluation(null);
    setFollowUpQuestion(null);
    setMode('practice');
    
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      // Loop back to first question or generate new ones
      setCurrentQuestionIndex(0);
      loadQuestions();
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
      setAnswer('');
      setEvaluation(null);
      setFollowUpQuestion(null);
      setMode('practice');
    }
  };

  const getScoreColor = (score) => {
    if (score >= 8) return 'bg-green-500';
    if (score >= 6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loadingQuestions) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="text-6xl mb-6">🤔</div>
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">Generating Interview Questions</h2>
        <p className="text-gray-600 mb-6">Analyzing your resume to create personalized questions...</p>
        <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">😕</div>
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">No Questions Available</h2>
        <p className="text-gray-600 mb-6">{error || 'Please upload a resume first.'}</p>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">🎯 Mock Interview</h1>
            <p className="text-gray-600">Practice with personalized technical questions</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-500">Question</p>
            <p className="text-2xl font-bold text-primary-600">
              {currentQuestionIndex + 1} <span className="text-gray-400">/ {questions.length}</span>
            </p>
          </div>
        </div>
        
        {/* Progress Bar */}
        <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-primary-500 to-purple-500 transition-all duration-500"
            style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white rounded-2xl shadow-lg overflow-hidden mb-6">
        <div className="gradient-bg p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <span className={`badge ${getDifficultyColor(currentQuestion.difficulty)}`}>
              {currentQuestion.difficulty}
            </span>
            <span className="bg-white/20 px-3 py-1 rounded-full text-sm">
              {currentQuestion.category}
            </span>
          </div>
          <h2 className="text-xl font-semibold">{currentQuestion.question}</h2>
          <p className="text-sm opacity-80 mt-2">Focus: {currentQuestion.focus}</p>
        </div>

        <div className="p-6">
          {/* Answer Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Answer
            </label>
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer here... (Use STAR method for behavioral questions)"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 h-40 resize-none"
              disabled={mode === 'feedback'}
            ></textarea>
            <p className="text-sm text-gray-500 mt-1">
              {answer.length} characters
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            {mode === 'practice' ? (
              <button
                onClick={handleSubmitAnswer}
                disabled={!answer.trim() || loading}
                className={`flex-1 py-3 rounded-lg font-semibold transition-all duration-300
                  ${!answer.trim() || loading 
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-primary-600 to-purple-600 text-white hover:shadow-lg'
                  }`}
              >
                {loading ? 'Evaluating...' : 'Submit Answer'}
              </button>
            ) : (
              <div className="flex gap-4 flex-1">
                <button
                  onClick={handleFollowUp}
                  disabled={loading}
                  className="flex-1 py-3 rounded-lg font-semibold border-2 border-primary-600 text-primary-600 hover:bg-primary-50 transition-colors"
                >
                  {loading ? 'Loading...' : 'Get Follow-up'}
                </button>
                <button
                  onClick={handleNextQuestion}
                  className="flex-1 py-3 rounded-lg font-semibold bg-gradient-to-r from-green-600 to-emerald-600 text-white hover:shadow-lg transition-all"
                >
                  Next Question →
                </button>
              </div>
            )}
          </div>

          {/* Navigation */}
          <div className="flex justify-between mt-4">
            <button
              onClick={handlePreviousQuestion}
              disabled={currentQuestionIndex === 0}
              className="text-gray-600 hover:text-gray-800 disabled:opacity-50"
            >
              ← Previous
            </button>
            <button
              onClick={loadQuestions}
              className="text-primary-600 hover:text-primary-700 text-sm"
            >
              Generate New Questions
            </button>
          </div>
        </div>
      </div>

      {/* Evaluation Results */}
      {evaluation && mode === 'feedback' && (
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden animate-fade-in">
          <div className="p-6 border-b border-gray-100">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-gray-800">📊 Answer Evaluation</h3>
              <div className={`score-circle ${getScoreColor(evaluation.score)} text-white`}>
                {evaluation.score}/10
              </div>
            </div>
          </div>

          <div className="p-6">
            {/* Score Breakdown */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
              {[
                { label: 'Relevance', score: evaluation.breakdown.relevance, max: 2 },
                { label: 'Technical', score: evaluation.breakdown.technical_accuracy, max: 3 },
                { label: 'Depth', score: evaluation.breakdown.depth, max: 2 },
                { label: 'Communication', score: evaluation.breakdown.communication, max: 2 },
                { label: 'STAR', score: evaluation.breakdown.star_format, max: 1 },
              ].map((item, index) => (
                <div key={index} className="text-center p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">{item.label}</p>
                  <p className="text-xl font-bold text-gray-800">{item.score}/{item.max}</p>
                </div>
              ))}
            </div>

            {/* Strengths */}
            <div className="mb-6">
              <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
                <span className="text-green-500 mr-2">✓</span> Strengths
              </h4>
              <ul className="space-y-2">
                {evaluation.strengths.map((strength, index) => (
                  <li key={index} className="flex items-start text-gray-600">
                    <span className="text-green-500 mr-2">•</span>
                    {strength}
                  </li>
                ))}
              </ul>
            </div>

            {/* Improvements */}
            <div className="mb-6">
              <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
                <span className="text-yellow-500 mr-2">⚠</span> Areas for Improvement
              </h4>
              <ul className="space-y-2">
                {evaluation.improvements.map((improvement, index) => (
                  <li key={index} className="flex items-start text-gray-600">
                    <span className="text-yellow-500 mr-2">•</span>
                    {improvement}
                  </li>
                ))}
              </ul>
            </div>

            {/* Suggested Answer */}
            <div className="bg-blue-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-800 mb-2">💡 Suggested Approach</h4>
              <p className="text-gray-700">{evaluation.suggested_answer}</p>
            </div>

            {/* Overall Feedback */}
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h4 className="font-semibold text-gray-800 mb-2">📝 Overall Feedback</h4>
              <p className="text-gray-700">{evaluation.overall_feedback}</p>
            </div>
          </div>
        </div>
      )}

      {/* Follow-up Question */}
      {followUpQuestion && (
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden mt-6 animate-fade-in">
          <div className="gradient-bg p-6 text-white">
            <h3 className="text-lg font-semibold">🔄 Follow-up Question</h3>
          </div>
          <div className="p-6">
            <p className="text-gray-800 font-medium mb-4">{followUpQuestion.follow_up_question}</p>
            <p className="text-gray-600 text-sm">{followUpQuestion.reason}</p>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg mt-6">
          {error}
        </div>
      )}
    </div>
  );
};

export default Interview;
