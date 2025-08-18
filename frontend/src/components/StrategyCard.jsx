import React from 'react';

const StrategyCard = ({ strategy }) => {
  const getFormatIcon = (format) => {
    const icons = {
      'Reel': '🎥',
      'Short': '📱',
      'Post': '📝',
      'Story': '📸',
      'Carousel': '🎠',
      'Thread': '🧵'
    };
    return icons[format] || '📄';
  };

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200 hover:shadow-lg transition-all">
      <div className="flex justify-between items-start mb-4">
        <h3 className="font-bold text-lg text-gray-800 flex-1">
          {strategy.title}
        </h3>
        <span className="text-2xl ml-2">
          {getFormatIcon(strategy.format)}
        </span>
      </div>
      
      <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
        <div className="bg-white rounded p-2">
          <span className="text-gray-500 font-medium">Format:</span>
          <span className="ml-2 text-blue-600 font-semibold">{strategy.format}</span>
        </div>
        <div className="bg-white rounded p-2">
          <span className="text-gray-500 font-medium">Platform:</span>
          <span className="ml-2 text-green-600 font-semibold">{strategy.platform}</span>
        </div>
        <div className="bg-white rounded p-2">
          <span className="text-gray-500 font-medium">Best Time:</span>
          <span className="ml-2 text-purple-600 font-semibold">{strategy.best_time}</span>
        </div>
        <div className="bg-white rounded p-2">
          <span className="text-gray-500 font-medium">Hook:</span>
          <span className="ml-2 text-orange-600 font-semibold">{strategy.hook}</span>
        </div>
      </div>
      
      <div className="bg-white rounded p-3">
        <p className="text-gray-700 text-sm leading-relaxed">
          {strategy.description}
        </p>
      </div>
    </div>
  );
};

export default StrategyCard;
