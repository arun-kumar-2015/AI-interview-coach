import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  const features = [
    {
      icon: '📄',
      title: 'Resume Upload',
      description: 'Upload your PDF resume and let AI analyze your experience',
      link: '/upload',
      color: 'bg-blue-500'
    },
    {
      icon: '🎯',
      title: 'Mock Interview',
      description: 'Practice with personalized technical questions based on your resume',
      link: '/interview',
      color: 'bg-green-500'
    },
    {
      icon: '👔',
      title: 'HR Questions',
      description: 'Prepare for behavioral and leadership questions',
      link: '/hr-questions',
      color: 'bg-purple-500'
    },
    {
      icon: '📝',
      title: 'Resume Improvement',
      description: 'Get ATS optimization and content improvement suggestions',
      link: '/improve',
      color: 'bg-orange-500'
    }
  ];

  const benefits = [
    { icon: '🧠', title: 'AI-Powered', description: 'Uses advanced AI to generate personalized questions' },
    { icon: '📚', title: 'RAG Technology', description: 'Retrieval-Augmented Generation for relevant content' },
    { icon: '⭐', title: 'Scored Answers', description: 'Get detailed scoring and feedback on your answers' },
    { icon: '🔒', title: 'Secure', description: 'Your data is processed securely and not stored' }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="gradient-bg text-white py-20">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-5xl font-bold mb-6 animate-fade-in">
              Smart AI Interview & Resume Coach
            </h1>
            <p className="text-xl mb-8 opacity-90">
              Master your next interview with personalized questions, real-time feedback, 
              and AI-powered resume improvements using Generative AI.
            </p>
            <div className="flex justify-center space-x-4">
              <Link
                to="/upload"
                className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-all duration-300 transform hover:scale-105"
              >
                Get Started 🚀
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
            Everything You Need to Ace Your Interview
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Link
                key={index}
                to={feature.link}
                className="bg-gray-50 p-6 rounded-xl hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 card-hover"
              >
                <div className={`w-14 h-14 ${feature.color} rounded-lg flex items-center justify-center text-2xl mb-4`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2 text-gray-800">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
            Why Use AI Interview Coach?
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {benefits.map((benefit, index) => (
              <div key={index} className="bg-white p-6 rounded-xl shadow-md">
                <div className="text-4xl mb-4">{benefit.icon}</div>
                <h3 className="text-lg font-semibold mb-2 text-gray-800">
                  {benefit.title}
                </h3>
                <p className="text-gray-600 text-sm">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
            How It Works
          </h2>
          
          <div className="max-w-4xl mx-auto">
            <div className="flex flex-col md:flex-row items-center justify-between space-y-8 md:space-y-0">
              {[
                { step: '1', title: 'Upload Resume', desc: 'Upload your PDF resume' },
                { step: '2', title: 'AI Analysis', desc: 'We analyze your experience' },
                { step: '3', title: 'Practice Questions', desc: 'Get personalized questions' },
                { step: '4', title: 'Get Feedback', desc: 'Receive scores and tips' }
              ].map((item, index) => (
                <div key={index} className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4">
                    {item.step}
                  </div>
                  <h3 className="font-semibold text-gray-800 mb-1">{item.title}</h3>
                  <p className="text-gray-500 text-sm">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-gradient-to-r from-primary-600 to-purple-600">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Land Your Dream Job?
          </h2>
          <p className="text-white/80 mb-8 max-w-2xl mx-auto">
            Start practicing now and boost your confidence for your next interview.
          </p>
          <Link
            to="/upload"
            className="inline-block bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-all duration-300"
          >
            Start Now 🎯
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8">
        <div className="container mx-auto px-4 text-center">
          <p>© 2024 AI Interview Coach. Built with ❤️ using Generative AI.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
