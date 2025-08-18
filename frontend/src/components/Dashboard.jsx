import React, { useState } from 'react';
import { trendService } from '../services/api';
import TrendCard from './TrendCard';
import LoadingSpinner from './LoadingSpinner';

const Dashboard = () => {
  const [strategy, setStrategy] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [targetAudience, setTargetAudience] = useState('Gen Z');
  const [niche, setNiche] = useState('General');

  const generateStrategy = async () => {
    setLoading(true);
    setError(null);
    setStrategy(null);

    try {
      // Generate content strategy (use GET to match backend route definition)
      const strategyUrl = `http://localhost:8000/api/v1/strategy?target_audience=${encodeURIComponent(targetAudience)}&niche=${encodeURIComponent(niche)}`;
      const strategyResponse = await fetch(strategyUrl);

      if (!strategyResponse.ok) {
        throw new Error(`HTTP error! status: ${strategyResponse.status}`);
      }

      const strategyData = await strategyResponse.json();
      console.log('✅ Strategy data received:', strategyData);
      setStrategy(strategyData);

    } catch (err) {
      console.error('❌ Error generating strategy:', err);
      setError(`Failed to generate strategy: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const downloadStrategy = async (format = 'json') => {
    if (!strategy) {
      alert('No strategy data available to download');
      return;
    }

    if (format === 'pdf') {
      try {
        console.log('📄 Starting PDF generation...');
        console.log('Strategy data:', strategy);

        // First install jsPDF if not already installed
        // npm install jspdf
        const { jsPDF } = await import('jspdf');
        console.log('✅ jsPDF imported successfully');
        
        const pdf = new jsPDF();
        let yPosition = 20;
        const lineHeight = 8;
        const pageHeight = pdf.internal.pageSize.height;
        const pageWidth = pdf.internal.pageSize.width;
        const margin = 20;
        const maxWidth = pageWidth - (margin * 2);

        // Helper function for page breaks
        const checkPageBreak = (requiredSpace = 20) => {
          if (yPosition + requiredSpace > pageHeight - 20) {
            pdf.addPage();
            yPosition = 20;
            return true;
          }
          return false;
        };

        // Helper function for safe text addition
        const addText = (text, fontSize = 12, fontWeight = 'normal', indent = 0) => {
          if (!text || text === 'undefined' || text === 'null') {
            text = 'N/A';
          }
          
          pdf.setFontSize(fontSize);
          pdf.setFont('helvetica', fontWeight);
          
          const textLines = pdf.splitTextToSize(String(text), maxWidth - indent);
          textLines.forEach(line => {
            checkPageBreak(lineHeight);
            pdf.text(line, margin + indent, yPosition);
            yPosition += lineHeight;
          });
        };

        // Title
        pdf.setFontSize(20);
        pdf.setFont('helvetica', 'bold');
        pdf.text('AI Content Strategy Report', margin, yPosition);
        yPosition += 15;

        // Metadata
        addText(`Generated on: ${new Date().toLocaleDateString()}`, 12);
        addText(`Target Audience: ${targetAudience}`, 12);
        addText(`Niche: ${niche}`, 12);
        yPosition += 10;

        // Analysis Summary
        if (strategy.analysis_summary) {
          console.log('📋 Adding analysis summary...');
          checkPageBreak(30);
          
          pdf.setFontSize(16);
          pdf.setFont('helvetica', 'bold');
          pdf.text('Analysis Summary', margin, yPosition);
          yPosition += 10;
          
          addText(strategy.analysis_summary, 11, 'normal');
          yPosition += 10;
        }

        // Top Trends
        if (strategy.top_trends && Array.isArray(strategy.top_trends) && strategy.top_trends.length > 0) {
          console.log('🔥 Adding top trends...');
          checkPageBreak(40);
          
          pdf.setFontSize(16);
          pdf.setFont('helvetica', 'bold');
          pdf.text('Top Trending Topics', margin, yPosition);
          yPosition += 10;

          strategy.top_trends.forEach((trend, index) => {
            checkPageBreak(25);
            
            // Trend title
            const title = trend.title || `Trend ${index + 1}`;
            addText(`${index + 1}. ${title}`, 12, 'bold');
            
            // Trend details
            const platform = trend.platform || 'Unknown';
            const score = trend.engagement_score || 'N/A';
            addText(`Platform: ${platform} | Score: ${score}`, 10, 'normal', 5);
            
            // Analysis if available
            if (trend.metadata && trend.metadata.analysis) {
              addText(`Analysis: ${trend.metadata.analysis}`, 10, 'italic', 5);
            }
            
            yPosition += 5;
          });
          yPosition += 10;
        }

        // Content Strategy
        if (strategy.content_strategy && Array.isArray(strategy.content_strategy) && strategy.content_strategy.length > 0) {
          console.log('🚀 Adding content strategy...');
          checkPageBreak(40);
          
          pdf.setFontSize(16);
          pdf.setFont('helvetica', 'bold');
          pdf.text('Content Strategy Recommendations', margin, yPosition);
          yPosition += 10;

          strategy.content_strategy.forEach((item, index) => {
            checkPageBreak(35);
            
            // Strategy title
            const title = item.title || `Strategy ${index + 1}`;
            addText(`${index + 1}. ${title}`, 14, 'bold');
            
            // Strategy details
            const format = item.format || 'Not specified';
            const platform = item.platform || 'Not specified';
            const bestTime = item.best_time || 'Not specified';
            const hook = item.hook || 'Not specified';
            
            addText(`Format: ${format}`, 11, 'normal', 5);
            addText(`Platform: ${platform}`, 11, 'normal', 5);
            addText(`Best Time: ${bestTime}`, 11, 'normal', 5);
            addText(`Hook: ${hook}`, 11, 'normal', 5);
            
            // Description
            if (item.description) {
              addText('Description:', 11, 'bold', 5);
              addText(item.description, 10, 'normal', 10);
            }
            
            yPosition += 10;
          });
        }

        // Footer
        const totalPages = pdf.internal.getNumberOfPages();
        for (let i = 1; i <= totalPages; i++) {
          pdf.setPage(i);
          pdf.setFontSize(8);
          pdf.setFont('helvetica', 'normal');
          pdf.text(
            `Page ${i} of ${totalPages} - Generated by AI Content Strategy Engine`, 
            margin, 
            pageHeight - 10
          );
        }

        console.log('✅ PDF generated successfully');
        pdf.save(`ai-content-strategy-${Date.now()}.pdf`);
        console.log('✅ PDF download initiated');

      } catch (error) {
        console.error('❌ PDF Generation Error:', error);
        console.error('Error details:', error.message);
        console.error('Error stack:', error.stack);
        
        // More specific error messages
        if (error.message.includes('jsPDF')) {
          alert('PDF library not found. Please run: npm install jspdf');
        } else if (error.message.includes('splitTextToSize')) {
          alert('PDF text formatting error. Please check your data.');
        } else {
          alert(`PDF Generation Failed: ${error.message}\n\nCheck the browser console for more details.`);
        }
      }
    } else {
      // JSON download
      try {
        const dataStr = JSON.stringify(strategy, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
        
        const exportFileDefaultName = `content-strategy-${Date.now()}.json`;
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
        
        console.log('✅ JSON download successful');
      } catch (error) {
        console.error('❌ JSON download failed:', error);
        alert('JSON download failed. Please try again.');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🚀 AI Content Strategy Engine
          </h1>
          <p className="text-gray-600 text-lg">
            Real-time trending analysis & AI-powered content strategies
          </p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience
              </label>
              <select
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Gen Z">Gen Z</option>
                <option value="Millennials">Millennials</option>
                <option value="Gen X">Gen X</option>
                <option value="Boomers">Boomers</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Niche
              </label>
              <select
                value={niche}
                onChange={(e) => setNiche(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="General">General</option>
                <option value="Tech">Technology</option>
                <option value="Fashion">Fashion</option>
                <option value="Fitness">Fitness</option>
                <option value="Food">Food</option>
                <option value="Travel">Travel</option>
                <option value="Business">Business</option>
              </select>
            </div>
            
            <button
              onClick={generateStrategy}
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {loading ? '🔄 Generating...' : '✨ Generate Strategy'}
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-8">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <LoadingSpinner message="Analyzing trends and generating AI strategy..." />
        )}

        {/* Results */}
        {strategy && !loading && (
          <div className="space-y-8">
            {/* Header with Download */}
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">📊 AI Strategy Results</h2>
              <div className="flex space-x-2">
                <button
                  onClick={() => downloadStrategy('json')}
                  className="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium text-sm"
                >
                  📄 JSON
                </button>
                <button
                  onClick={() => downloadStrategy('pdf')}
                  className="px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 font-medium text-sm"
                >
                  📋 PDF
                </button>
              </div>
            </div>
            
            {/* Analysis Summary */}
            {strategy.analysis_summary && (
              <div className="bg-blue-50 border-l-4 border-blue-500 p-6 mb-6">
                <h3 className="font-semibold text-blue-900 mb-3 text-lg">📋 AI Analysis Summary</h3>
                <p className="text-blue-800 whitespace-pre-wrap">{strategy.analysis_summary}</p>
              </div>
            )}
            
            {/* Top Trends */}
            {strategy.top_trends && strategy.top_trends.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h3 className="text-xl font-semibold mb-4 text-gray-800">🔥 Top Trending Topics</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {strategy.top_trends.map((trend, index) => (
                    <TrendCard key={index} trend={trend} />
                  ))}
                </div>
              </div>
            )}
            
            {/* Content Strategy */}
            {strategy.content_strategy && strategy.content_strategy.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold mb-4 text-gray-800">🚀 Content Strategy Recommendations</h3>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {strategy.content_strategy.map((item, index) => (
                    <div key={index} className="bg-gradient-to-br from-purple-600 to-blue-600 text-white rounded-lg p-6">
                      <div className="flex justify-between items-start mb-4">
                        <h4 className="font-bold text-lg">{item.title}</h4>
                        <span className="text-2xl">
                          {item.format === 'Reel' ? '🎥' : 
                           item.format === 'Carousel' ? '🎠' : 
                           item.format === 'Story' ? '📸' : 
                           item.format === 'Short' ? '📱' : '📝'}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
                        <div className="bg-white bg-opacity-20 rounded p-2">
                          <strong>Format:</strong> {item.format}
                        </div>
                        <div className="bg-white bg-opacity-20 rounded p-2">
                          <strong>Platform:</strong> {item.platform}
                        </div>
                        <div className="bg-white bg-opacity-20 rounded p-2">
                          <strong>Best Time:</strong> {item.best_time}
                        </div>
                        <div className="bg-white bg-opacity-20 rounded p-2">
                          <strong>Hook:</strong> {item.hook}
                        </div>
                      </div>
                      
                      <div className="bg-white bg-opacity-20 rounded p-3">
                        <p className="text-sm leading-relaxed">{item.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Debug Info (Remove in production) */}
            <div className="bg-gray-100 border rounded p-4 text-sm">
              <h4 className="font-semibold mb-2">Debug Info:</h4>
              <p>Strategy keys: {Object.keys(strategy).join(', ')}</p>
              <p>Top trends count: {strategy.top_trends ? strategy.top_trends.length : 0}</p>
              <p>Content strategy count: {strategy.content_strategy ? strategy.content_strategy.length : 0}</p>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!strategy && !loading && !error && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              Ready to Generate AI Content Strategy
            </h3>
            <p className="text-gray-600">
              Click "Generate Strategy" to analyze current trends and get AI-powered content recommendations.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
