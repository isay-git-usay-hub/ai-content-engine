import React from 'react';

const TrendCard = ({ trend, platform }) => {
  // Safety check for trend object
  if (!trend) {
    return null;
  }

  // Use platform prop or extract from trend object
  const trendPlatform = platform || trend.platform || 'unknown';

  const getPlatformColor = (platform) => {
    const colors = {
      google_trends: 'bg-red-100 text-red-800',
      reddit: 'bg-orange-100 text-orange-800',
      youtube: 'bg-red-100 text-red-800',
      twitter: 'bg-blue-100 text-blue-800'
    };
    return colors[platform] || 'bg-gray-100 text-gray-800';
  };

  const getPlatformIcon = (platform) => {
    const icons = {
      google_trends: '🔍',
      reddit: '📰',
      youtube: '📺',
      twitter: '🐦'
    };
    return icons[platform] || '📊';
  };

  // Safe platform display function
  const formatPlatformName = (platform) => {
    if (!platform || platform === 'unknown') return 'UNKNOWN';
    return platform.replace(/_/g, ' ').toUpperCase();
  };

  // Extract trend data safely
  const trendTitle = typeof trend === 'string' ? trend : (trend.title || 'No title available');
  const engagementScore = trend.engagement_score;
  const metadata = trend.metadata;

  return (
    <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-blue-500 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPlatformColor(trendPlatform)}`}>
          {getPlatformIcon(trendPlatform)} {formatPlatformName(trendPlatform)}
        </span>
        {engagementScore && (
          <span className="text-sm text-gray-500">
            {engagementScore.toLocaleString()} engagements
          </span>
        )}
      </div>
      
      <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2">
        {trendTitle}
      </h3>
      
      {/* Reddit-specific metadata */}
      {metadata && (
        <div className="text-xs text-gray-500 space-y-1">
          {metadata.subreddit && (
            <span className="inline-block bg-gray-100 px-2 py-1 rounded">
              r/{metadata.subreddit}
            </span>
          )}
          {metadata.comments && (
            <span className="ml-2">💬 {metadata.comments} comments</span>
          )}
          {metadata.analysis && (
            <p className="text-xs text-gray-600 mt-2 italic">
              💡 {metadata.analysis}
            </p>
          )}
        </div>
      )}

      {/* Add URL link if available */}
      {trend.url && (
        <div className="mt-3">
          <a 
            href={trend.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 text-xs font-medium"
          >
            View Source →
          </a>
        </div>
      )}
    </div>
  );
};

export default TrendCard;
