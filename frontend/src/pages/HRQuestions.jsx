import React, { useState, useEffect } from 'react';
import { generateHRQuestions, generateLeadershipQuestions, getBehavioralTips } from '../services/api';

const HRQuestions = ({ sessionId }) => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [questionType, setQuestionType] = useState('behavioral'); // 'behavioral' or 'leadership'
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [tips, setTips] = useState(null);
  const [showTips, setShowTips] = useState(false);

  useEffect(() => {
    loadQuestions();
    loadTips();
  }, [sessionId, questionType]);

  const loadQuestions = async () => {
    setLoading(true);
    setError(null);
    setSelectedQuestion(null);
    setAnswer('');
    setEvaluation(null);
    
    try {
      let response;
      if (questionType === 'behavioral') {
        response = await generateHRQuestions(sessionId, 10);
      } else {
        response = await generateLeadershipQuestions(sessionId, 5);
      }
      setQuestions(response.questions);
    } catch (err) {
      console.error('Error loading questions:', err);
      setError('Failed to generate questions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadTips = async () => {
    try {
      const response = await getBehavioralTips();
      setTips(response);
    } catch (err) {
      console.error('Error loading tips:', err);
    }
  };

  const handleSelectQuestion = (question) => {
    setSelectedQuestion(question);
    setAnswer('');
    setEvaluation(null);
  };

  const handleAnswerSubmit = async () => {
    if (!answer.trim() || !selectedQuestion) return;
    
    setLoading(true);
    try {
      const { evaluateAnswer } = await import('../services/api');
      const response = await evaluateAnswer(
        sessionId,
        selectedQuestion.question,
        answer,
        'Behavioral'
      );
      setEvaluation(response);
    } catch (err) {
      console.error('Error evaluating answer:', err);
      setError('Failed to evaluate answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Leadership': 'bg-purple-100 text-purple-800',
      'Teamwork': 'bg-blue-100 text-blue-800',
      'Communication': 'bg-green-100 text-green-800',
      'Problem Solving': 'bg-yellow-100 text-yellow-800',
      'Adaptability': 'bg-red-100 text-red-800',
      'Conflict Resolution': 'bg-orange-100 text-orange-800',
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const getScoreColor = (score) => {
    if (score >= 8) return 'bg-green-500';
    if (score >= 6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">👔 HR & Behavioral Questions</h1>
            <p className="text-gray-600">Practice behavioral interviews with STAR method</p>
          </div>
          <div className="flex gap-4">
            <button
              onClick={() => setShowTips(!showTips)}
              className="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              {showTips ? 'Hide Tips' : 'Show Tips 📝'}
            </button>
          </div>
        </div>

        {/* Question Type Selection */}
        <div className="flex gap-4 mt-4">
          <button
            onClick={() => setQuestionType('behavioral')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              questionType === 'behavioral'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Behavioral Questions
          </button>
          <button
            onClick={() => setQuestionType('leadership')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              questionType === 'leadership'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Leadership Focus
          </button>
        </div>
      </div>

      {/* Tips Section */}
      {showTips && tips && (
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 animate-fade-in">
          <h2 className="text-xl font-bold text-gray-800 mb-4">📝 STAR Method Tips</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">What is STAR?</h3>
              <ul className="space-y-2 text-gray-600">
                <li><span className="font-medium text-primary-600">S</span>ituation - Describe the context</li>
                <li><span className="font-medium text-primary-600">T</span>ask - Explain your responsibility</li>
                <li><span className="font-medium text-primary-600">A</span>ction - Detail what you did</li>
                <li><span className="font-medium text-primary-600">R</span>esult - Share the outcome</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Common Themes</h3>
              <div className="flex flex-wrap gap-2">
                {tips.common_themes.map((theme, index) => (
                  <span key={index} className="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700">
                    {theme}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {loading && !selectedQuestion ? (
        <div className="flex flex-col items-center justify-center min-h-[40vh]">
          <div className="text-5xl mb-4">🤔</div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Generating Questions</h2>
          <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
          {/* Questions List */}
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            <div className="p-4 border-b border-gray-100">
              <h2 className="font-semibold text-gray-800">
                {questionType === 'behavioral' ? 'Behavioral Questions' : 'Leadership Questions'}
              </h2>
            </div>
            <div className="divide-y divide-gray-100 max-h-[60vh] overflow-y-auto">
              {questions.map((q, index) => (
                <button
                  key={index}
                  onClick={() => handleSelectQuestion(q)}
                  className={`w-full text-left p-4 hover:bg-gray-50 transition-colors ${
                    selectedQuestion?.question === q.question ? 'bg-primary-50' : ''
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="text-sm text-gray-500">Q{index + 1}</span>
                    <span className={`badge text-xs ${getCategoryColor(q.category)}`}>
                      {q.category}
                    </span>
                  </div>
                  <p className="text-gray-800 font-medium line-clamp-2">{q.question}</p>
                  <p className="text-xs text-gray-500 mt-1">{q.what_it_tests}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Question Detail & Answer */}
          <div className="space-y-6">
            {selectedQuestion ? (
              <>
                <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
                  <div className="gradient-bg p-6 text-white">
                    <div className="flex items-center justify-between mb-3">
                      <span className={`badge ${getCategoryColor(selectedQuestion.category)}`}>
                        {selectedQuestion.category}
                      </span>
                      <span className="text-sm opacity-80">{selectedQuestion.experience_level}</span>
                    </div>
                    <h3 className="text-lg font-semibold">{selectedQuestion.question}</h3>
                    <p className="text-sm opacity-80 mt-2">Tests: {selectedQuestion.what_it_tests}</p>
                    <div className="mt-3 p-3 bg-white/10 rounded-lg">
                      <p className="text-sm"><span className="font-medium">STAR Structure:</span> {selectedQuestion.sample_structure}</p>
                    </div>
                  </div>

                  <div className="p-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Your Answer (using STAR method)
                    </label>
                    <textarea
                      value={answer}
                      onChange={(e) => setAnswer(e.target.value)}
                      placeholder="Situation: ... Task: ... Action: ... Result: ..."
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 h-40 resize-none"
                      disabled={evaluation !== null}
                    ></textarea>
                    
                    {!evaluation ? (
                      <button
                        onClick={handleAnswerSubmit}
                        disabled={!answer.trim() || loading}
                        className={`w-full mt-4 py-3 rounded-lg font-semibold transition-all ${
                          !answer.trim() || loading
                            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                            : 'bg-gradient-to-r from-primary-600 to-purple-600 text-white hover:shadow-lg'
                        }`}
                      >
                        {loading ? 'Evaluating...' : 'Submit Answer'}
                      </button>
                    ) : (
                      <button
                        onClick={() => {
                          setAnswer('');
                          setEvaluation(null);
                        }}
                        className="w-full mt-4 py-3 rounded-lg font-semibold border-2 border-primary-600 text-primary-600 hover:bg-primary-50"
                      >
                        Try Another Answer
                      </button>
                    )}
                  </div>
                </div>

                {/* Evaluation Results */}
                {evaluation && (
                  <div className="bg-white rounded-2xl shadow-lg overflow-hidden animate-fade-in">
                    <div className="p-4 border-b border-gray-100 flex items-center justify-between">
                      <h3 className="font-semibold text-gray-800">📊 Evaluation</h3>
                      <div className={`score-circle ${getScoreColor(evaluation.score)} text-white text-sm`}>
                        {evaluation.score}/10
                      </div>
                    </div>
                    <div className="p-4 space-y-4">
                      <div>
                        <h4 className="font-medium text-gray-800 mb-2 flex items-center">
                          <span className="text-green-500 mr-2">✓</span> Strengths
                        </h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {evaluation.strengths.map((s, i) => (
                            <li key={i}>• {s}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-800 mb-2 flex items-center">
                          <span className="text-yellow-500 mr-2">⚠</span> Improvements
                        </h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {evaluation.improvements.map((i, idx) => (
                            <li key={idx}>• {i}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <h4 className="font-medium text-gray-800 mb-1">💡 Feedback</h4>
                        <p className="text-sm text-gray-700">{evaluation.overall_feedback}</p>
                      </div>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="bg-white rounded-2xl shadow-lg p-12 text-center">
                <div className="text-5xl mb-4">👈</div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Select a Question</h3>
                <p className="text-gray-600">Choose a question from the list to practice your answer</p>
              </div>
            )}
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

export default HRQuestions;
