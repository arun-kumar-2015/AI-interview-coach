import axios from 'axios';

// API Base URL - Configure this to match your backend URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds timeout
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`📤 ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`📥 Response from ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ Response error:', error);
    return Promise.reject(error);
  }
);

// ==================== Resume Upload API ====================

export const uploadResume = async (file, jobRole = 'Software Engineer') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_role', jobRole);

  const response = await api.post('/api/upload_resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getSessionInfo = async (sessionId) => {
  const response = await api.get(`/api/session/${sessionId}`);
  return response.data;
};

export const deleteSession = async (sessionId) => {
  const response = await api.delete(`/api/session/${sessionId}`);
  return response.data;
};

// ==================== Technical Questions API ====================

export const generateTechnicalQuestions = async (sessionId, jobRole, numQuestions = 10) => {
  const response = await api.post('/api/generate_questions', {
    session_id: sessionId,
    job_role: jobRole,
    num_questions: numQuestions,
  });
  return response.data;
};

export const analyzeResume = async (sessionId) => {
  const response = await api.post('/api/analyze_resume', null, {
    params: { session_id: sessionId },
  });
  return response.data;
};

export const getSkillQuestions = async (sessionId, skill, numQuestions = 3) => {
  const response = await api.get(`/api/skill_questions/${sessionId}`, {
    params: { skill, num_questions: numQuestions },
  });
  return response.data;
};

// ==================== Answer Evaluation API ====================

export const evaluateAnswer = async (sessionId, question, answer, category = 'Technical') => {
  const response = await api.post('/api/evaluate_answer', {
    session_id: sessionId,
    question,
    answer,
    category,
  });
  return response.data;
};

export const generateFollowUp = async (sessionId, question, answer, category = 'Technical') => {
  const response = await api.post('/api/generate_followup', {
    session_id: sessionId,
    question,
    answer,
    category,
  });
  return response.data;
};

export const getAnswerTips = async (category) => {
  const response = await api.get(`/api/answer_tips/${category}`);
  return response.data;
};

// ==================== HR Questions API ====================

export const generateHRQuestions = async (sessionId, numQuestions = 10, focusAreas = '') => {
  const response = await api.post('/api/generate_hr_questions', {
    session_id: sessionId,
    num_questions: numQuestions,
    focus_areas: focusAreas,
  });
  return response.data;
};

export const generateLeadershipQuestions = async (sessionId, numQuestions = 5) => {
  const response = await api.post('/api/generate_leadership_questions', null, {
    params: { session_id: sessionId, num_questions: numQuestions },
  });
  return response.data;
};

export const getBehavioralTips = async () => {
  const response = await api.get('/api/behavioral_tips');
  return response.data;
};

// ==================== Resume Improvement API ====================

export const improveResume = async (sessionId, targetRole = 'Software Engineer', industry = 'Technology') => {
  const response = await api.post('/api/improve_resume', {
    session_id: sessionId,
    target_role: targetRole,
    industry,
  });
  return response.data;
};

export const checkATS = async (sessionId) => {
  const response = await api.post('/api/check_ats', null, {
    params: { session_id: sessionId },
  });
  return response.data;
};

export const getATSTips = async () => {
  const response = await api.get('/api/ats_tips');
  return response.data;
};

// ==================== Health Check ====================

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
