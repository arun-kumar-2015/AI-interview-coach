import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadResume } from '../services/api';

const UploadResume = ({ sessionId, onSessionCreated }) => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  
  const [file, setFile] = useState(null);
  const [jobRole, setJobRole] = useState('Software Engineer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const jobRoles = [
    'Software Engineer',
    'Data Scientist',
    'Frontend Developer',
    'Backend Developer',
    'Full Stack Developer',
    'DevOps Engineer',
    'Machine Learning Engineer',
    'Product Manager',
    'UX Designer',
    'Other'
  ];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile);
        setError(null);
      } else {
        setError('Please upload a PDF file');
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type === 'application/pdf') {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Please upload a PDF file');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await uploadResume(file, jobRole);
      onSessionCreated(response.session_id);
      navigate('/interview');
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.response?.data?.detail || 'Failed to upload resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
        {/* Header */}
        <div className="gradient-bg p-8 text-white">
          <h1 className="text-3xl font-bold mb-2">📄 Upload Your Resume</h1>
          <p className="opacity-90">
            Upload your PDF resume to get personalized interview questions
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-8">
          {/* Drop Zone */}
          <div
            className={`border-2 border-dashed rounded-xl p-8 text-center mb-6 transition-all duration-200 
              ${dragActive 
                ? 'border-primary-500 bg-primary-50' 
                : file 
                  ? 'border-green-500 bg-green-50' 
                  : 'border-gray-300 hover:border-primary-400'
              }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
            />

            {file ? (
              <div className="flex flex-col items-center">
                <span className="text-5xl mb-3">📄</span>
                <p className="font-semibold text-gray-800 mb-1">{file.name}</p>
                <p className="text-sm text-gray-500 mb-3">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
                <button
                  type="button"
                  onClick={() => {
                    setFile(null);
                    if (fileInputRef.current) fileInputRef.current.value = '';
                  }}
                  className="text-sm text-red-600 hover:text-red-700"
                >
                  Remove file
                </button>
              </div>
            ) : (
              <div className="flex flex-col items-center">
                <span className="text-5xl mb-3">📁</span>
                <p className="text-gray-700 font-medium mb-1">
                  Drag and drop your PDF here
                </p>
                <p className="text-gray-500 text-sm mb-3">or</p>
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Browse Files
                </button>
              </div>
            )}
          </div>

          {/* Job Role Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Job Role
            </label>
            <select
              value={jobRole}
              onChange={(e) => setJobRole(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              {jobRoles.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
            <p className="text-sm text-gray-500 mt-1">
              This helps us generate relevant interview questions
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!file || loading}
            className={`w-full py-4 rounded-lg font-semibold text-lg transition-all duration-300 
              ${!file || loading 
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                : 'bg-gradient-to-r from-primary-600 to-purple-600 text-white hover:shadow-lg transform hover:scale-[1.02]'
              }`}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing Resume...
              </span>
            ) : (
              '🚀 Generate Interview Questions'
            )}
          </button>

          {/* Info */}
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium text-gray-800 mb-2">🔒 Privacy Note</h3>
            <p className="text-sm text-gray-600">
              Your resume is processed securely and is not stored on our servers. 
              The AI uses your resume content only to generate personalized interview questions.
            </p>
          </div>
        </form>
      </div>

      {/* Tips Section */}
      <div className="mt-8 bg-white rounded-xl shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">📝 Tips for Better Results</h2>
        <ul className="space-y-2 text-gray-600">
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            Use a clean, well-formatted PDF resume
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            Include specific technologies and projects
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            Quantify your achievements where possible
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            Keep the job role selection accurate
          </li>
        </ul>
      </div>
    </div>
  );
};

export default UploadResume;
