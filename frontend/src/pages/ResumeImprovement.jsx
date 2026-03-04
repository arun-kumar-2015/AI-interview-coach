import React, { useState, useEffect } from 'react';
import { improveResume, checkATS, getATSTips } from '../services/api';

const ResumeImprovement = ({ sessionId }) => {
  const [loading, setLoading] = useState(true);
  const [improvements, setImprovements] = useState(null);
  const [atsCheck, setAtsCheck] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('improvements');
  const [tips, setTips] = useState(null);
  const [targetRole, setTargetRole] = useState('Software Engineer');
  const [industry, setIndustry] = useState('Technology');

  useEffect(() => {
    loadData();
  }, [sessionId]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [improvementsData, atsData, tipsData] = await Promise.all([
        improveResume(sessionId, targetRole, industry),
        checkATS(sessionId),
        getATSTips()
      ]);
      
      setImprovements(improvementsData);
      setAtsCheck(atsData);
      setTips(tipsData);
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 8) return 'bg-green-100';
    if (score >= 6) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="text-6xl mb-6">📝</div>
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">Analyzing Your Resume</h2>
        <p className="text-gray-600 mb-6">Generating improvement suggestions and ATS analysis...</p>
        <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">📝 Resume Improvement</h1>
            <p className="text-gray-600">Get AI-powered suggestions to improve your resume</p>
          </div>
          <div className="flex gap-4">
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            >
              <option value="Software Engineer">Software Engineer</option>
              <option value="Data Scientist">Data Scientist</option>
              <option value="Product Manager">Product Manager</option>
              <option value="DevOps Engineer">DevOps Engineer</option>
              <option value="Frontend Developer">Frontend Developer</option>
            </select>
            <button
              onClick={loadData}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Regenerate Analysis
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mt-4">
          <button
            onClick={() => setActiveTab('improvements')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              activeTab === 'improvements'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Improvements
          </button>
          <button
            onClick={() => setActiveTab('ats')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              activeTab === 'ats'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            ATS Analysis
          </button>
          <button
            onClick={() => setActiveTab('tips')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              activeTab === 'tips'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            ATS Tips
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Improvements Tab */}
      {activeTab === 'improvements' && improvements && (
        <div className="space-y-6 animate-fade-in">
          {/* Overall Score */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-800">Overall Resume Score</h2>
                <p className="text-gray-600">Based on content, formatting, and ATS optimization</p>
              </div>
              <div className={`text-5xl font-bold ${getScoreColor(improvements.overall_score)}`}>
                {improvements.overall_score}/10
              </div>
            </div>
          </div>

          {/* Priority Actions */}
          {improvements.priority_actions && improvements.priority_actions.length > 0 && (
            <div className="bg-gradient-to-r from-primary-600 to-purple-600 rounded-2xl shadow-lg p-6 text-white">
              <h2 className="text-xl font-bold mb-4">🎯 Priority Actions</h2>
              <ul className="space-y-2">
                {improvements.priority_actions.map((action, index) => (
                  <li key={index} className="flex items-start">
                    <span className="mr-2">{index + 1}.</span>
                    {action}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* ATS Analysis Summary */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 ATS Analysis</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-600">ATS Score</span>
                  <span className={`font-bold ${getScoreColor(improvements.ats_analysis.score)}`}>
                    {improvements.ats_analysis.score}/10
                  </span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full">
                  <div 
                    className={`h-full rounded-full ${getScoreBg(improvements.ats_analysis.score)}`}
                    style={{ width: `${improvements.ats_analysis.score * 10}%` }}
                  ></div>
                </div>
              </div>
              <div>
                <h3 className="font-medium text-gray-800 mb-2">Keywords Found</h3>
                <div className="flex flex-wrap gap-1">
                  {improvements.ats_analysis.keywords_found.slice(0, 10).map((kw, i) => (
                    <span key={i} className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            
            {improvements.ats_analysis.keywords_missing.length > 0 && (
              <div className="mt-4">
                <h3 className="font-medium text-gray-800 mb-2">Keywords to Add</h3>
                <div className="flex flex-wrap gap-1">
                  {improvements.ats_analysis.keywords_missing.slice(0, 10).map((kw, i) => (
                    <span key={i} className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs">
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Quantification Suggestions */}
          {improvements.quantification_suggestions && improvements.quantification_suggestions.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">📈 Quantification Suggestions</h2>
              <div className="space-y-4">
                {improvements.quantification_suggestions.map((item, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="mb-2">
                      <span className="text-sm text-gray-500">Original:</span>
                      <p className="text-gray-700">{item.original}</p>
                    </div>
                    <div className="mb-2">
                      <span className="text-sm text-green-600 font-medium">Improved:</span>
                      <p className="text-gray-800 font-medium">{item.improved}</p>
                    </div>
                    <div className="text-sm text-gray-600">
                      <span className="font-medium">Why:</span> {item.impact}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Content Improvements */}
          {improvements.content_improvements && improvements.content_improvements.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">✍️ Content Improvements</h2>
              <div className="space-y-4">
                {improvements.content_improvements.map((item, index) => (
                  <div key={index} className="border-l-4 border-primary-500 pl-4">
                    <h3 className="font-medium text-gray-800">{item.section}</h3>
                    <p className="text-sm text-gray-600 mt-1">{item.issue}</p>
                    <p className="text-primary-600 mt-2 font-medium">{item.suggestion}</p>
                    {item.example && (
                      <div className="mt-2 p-3 bg-gray-50 rounded-lg">
                        <p className="text-sm text-gray-700">{item.example}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Overall Feedback */}
          {improvements.overall_feedback && (
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">💡 Overall Feedback</h2>
              <p className="text-gray-700">{improvements.overall_feedback}</p>
            </div>
          )}
        </div>
      )}

      {/* ATS Analysis Tab */}
      {activeTab === 'ats' && atsCheck && (
        <div className="space-y-6 animate-fade-in">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-800">🔍 ATS Compatibility Check</h2>
              <div className={`text-4xl font-bold ${getScoreColor(atsCheck.ats_score)}`}>
                {atsCheck.ats_score}%
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Parseability */}
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-3">📖 Parseability</h3>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-600">Score</span>
                  <span className={`font-bold ${getScoreColor(atsCheck.parseability.score)}`}>
                    {atsCheck.parseability.score}/10
                  </span>
                </div>
                {atsCheck.parseability.issues.length > 0 && (
                  <div className="mt-2">
                    <p className="text-sm text-gray-600 mb-1">Issues:</p>
                    <ul className="text-sm text-red-600">
                      {atsCheck.parseability.issues.map((issue, i) => (
                        <li key={i}>• {issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Keyword Analysis */}
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-3">🔑 Keyword Analysis</h3>
                <div className="mb-2">
                  <span className="text-gray-600">Density: </span>
                  <span className="font-medium capitalize">{atsCheck.keyword_analysis.keyword_density}</span>
                </div>
                {atsCheck.keyword_analysis.missing_keywords.length > 0 && (
                  <div className="mt-2">
                    <p className="text-sm text-gray-600 mb-1">Missing Keywords:</p>
                    <div className="flex flex-wrap gap-1">
                      {atsCheck.keyword_analysis.missing_keywords.map((kw, i) => (
                        <span key={i} className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs">
                          {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Format Compliance */}
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-3">📐 Format Compliance</h3>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-600">Score</span>
                  <span className={`font-bold ${getScoreColor(atsCheck.format_compliance.score)}`}>
                    {atsCheck.format_compliance.score}/10
                  </span>
                </div>
                {atsCheck.format_compliance.issues.length > 0 && (
                  <div className="mt-2">
                    <p className="text-sm text-gray-600 mb-1">Issues:</p>
                    <ul className="text-sm text-red-600">
                      {atsCheck.format_compliance.issues.map((issue, i) => (
                        <li key={i}>• {issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Section Analysis */}
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-3">📋 Section Analysis</h3>
                <div className="mb-2">
                  <span className="text-gray-600">Order: </span>
                  <span className="font-medium capitalize">{atsCheck.section_analysis.section_order}</span>
                </div>
                <div className="flex flex-wrap gap-1 mt-2">
                  {atsCheck.section_analysis.sections_found.map((section, i) => (
                    <span key={i} className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                      {section}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Recommendations */}
            {atsCheck.specific_recommendations.length > 0 && (
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-3">💡 Recommendations</h3>
                <ul className="space-y-2">
                  {atsCheck.specific_recommendations.map((rec, i) => (
                    <li key={i} className="flex items-start text-gray-700">
                      <span className="text-blue-500 mr-2">•</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tips Tab */}
      {activeTab === 'tips' && tips && (
        <div className="space-y-6 animate-fade-in">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-6">📝 ATS-Friendly Resume Tips</h2>
            
            {/* General Tips */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">General Tips</h3>
              <ul className="space-y-2">
                {tips.general_tips.map((tip, i) => (
                  <li key={i} className="flex items-start text-gray-700">
                    <span className="text-green-500 mr-2">✓</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>

            {/* Keyword Strategies */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Keyword Strategies</h3>
              <ul className="space-y-2">
                {tips.keyword_strategies.map((tip, i) => (
                  <li key={i} className="flex items-start text-gray-700">
                    <span className="text-blue-500 mr-2">✓</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>

            {/* Formatting Tips */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Formatting Tips</h3>
              <ul className="space-y-2">
                {tips.formatting_tips.map((tip, i) => (
                  <li key={i} className="flex items-start text-gray-700">
                    <span className="text-purple-500 mr-2">✓</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>

            {/* Common Mistakes */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Common Mistakes to Avoid</h3>
              <ul className="space-y-2">
                {tips.common_mistakes.map((mistake, i) => (
                  <li key={i} className="flex items-start text-gray-700">
                    <span className="text-red-500 mr-2">✗</span>
                    {mistake}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeImprovement;
