import React from 'react';
import VideoInterview from '../components/VideoInterview';

const VideoInterviewPage = ({ sessionId }) => {
    return (
        <div className="animate-fade-in">
            <VideoInterview sessionId={sessionId} />
        </div>
    );
};

export default VideoInterviewPage;
