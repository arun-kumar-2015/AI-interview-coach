import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import UploadResume from './pages/UploadResume';
import Interview from './pages/Interview';
import HRQuestions from './pages/HRQuestions';
import ResumeImprovement from './pages/ResumeImprovement';
import VideoInterviewPage from './pages/VideoInterviewPage';
import Loading from './components/Loading';
import Error from './components/Error';
import InstallPrompt from './components/InstallPrompt';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check for existing session in localStorage
    const savedSession = localStorage.getItem('interview_session_id');
    if (savedSession) {
      setSessionId(savedSession);
    }
    setLoading(false);
  }, []);

  const handleSessionCreated = (newSessionId) => {
    setSessionId(newSessionId);
    localStorage.setItem('interview_session_id', newSessionId);
  };

  const handleSessionClear = () => {
    setSessionId(null);
    localStorage.removeItem('interview_session_id');
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <Navbar sessionId={sessionId} onSessionClear={handleSessionClear} />

        <main className="container mx-auto px-4 py-6">
          <Routes>
            <Route
              path="/"
              element={
                sessionId ? (
                  <Navigate to="/interview" replace />
                ) : (
                  <Home />
                )
              }
            />
            <Route
              path="/upload"
              element={
                <UploadResume
                  sessionId={sessionId}
                  onSessionCreated={handleSessionCreated}
                />
              }
            />
            <Route
              path="/interview"
              element={
                sessionId ? (
                  <Interview sessionId={sessionId} />
                ) : (
                  <Navigate to="/upload" replace />
                )
              }
            />
            <Route
              path="/video-interview"
              element={
                sessionId ? (
                  <VideoInterviewPage sessionId={sessionId} />
                ) : (
                  <Navigate to="/upload" replace />
                )
              }
            />
            <Route
              path="/hr-questions"
              element={
                sessionId ? (
                  <HRQuestions sessionId={sessionId} />
                ) : (
                  <Navigate to="/upload" replace />
                )
              }
            />
            <Route
              path="/improve"
              element={
                sessionId ? (
                  <ResumeImprovement sessionId={sessionId} />
                ) : (
                  <Navigate to="/upload" replace />
                )
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* Error Toast */}
        {error && (
          <Error
            message={error}
            onClose={() => setError(null)}
          />
        )}

        {/* PWA Install Prompt */}
        <InstallPrompt />
      </div>
    </Router>
  );
}

export default App;
