import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Loader } from 'lucide-react';

const API_BASE = 'http://localhost:5000/api';

const QUICK_QUERIES = [
  'What are my highest cost services?',
  'How can I optimize my EC2 spending?',
  'What unused resources do I have?',
  'What are the top cost optimization opportunities?',
  'Show me cost trends for the last 30 days',
  'Which regions have the highest costs?'
];

function ChatInterface({ onStatsUpdate }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: '👋 Welcome to FinOps AI! I can help you optimize your AWS costs. Ask me anything about your spending, resources, or optimization opportunities.',
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId] = useState('conv_' + Date.now());
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (query = null) => {
    const messageText = query || input.trim();
    if (!messageText) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: messageText,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/chat`, {
        message: messageText,
        conversation_id: conversationId
      });

      if (response.data.status === 'success') {
        const botMessage = {
          id: messages.length + 2,
          text: response.data.bot_response,
          sender: 'bot',
          timestamp: new Date(),
          data: response.data.relevant_data
        };
        setMessages(prev => [...prev, botMessage]);
        onStatsUpdate();
      }
    } catch (error) {
      const errorMessage = {
        id: messages.length + 2,
        text: '❌ Error: Unable to process your request. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-8 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-slide-in`}
          >
            <div
              className={`max-w-md lg:max-w-2xl px-6 py-4 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-purple-600 text-white rounded-br-none'
                  : 'bg-white text-gray-800 rounded-bl-none shadow-md'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.text}</p>
              {message.data && (
                <div className="mt-4 pt-4 border-t border-gray-300">
                  {message.data.costs && message.data.costs.length > 0 && (
                    <div className="mb-3">
                      <p className="font-semibold text-xs mb-2">Related Costs:</p>
                      {message.data.costs.slice(0, 2).map((cost, idx) => {
                        const costText = typeof cost === 'string' 
                          ? cost 
                          : `${cost.service || 'Unknown'}: ${cost.cost || 0}`;
                        return <p key={idx} className="text-xs opacity-75">{costText}</p>;
                      })}
                    </div>
                  )}
                  {message.data.optimizations && message.data.optimizations.length > 0 && (
                    <div>
                      <p className="font-semibold text-xs mb-2">Optimizations:</p>
                      {message.data.optimizations.slice(0, 2).map((opt, idx) => {
                        const optText = typeof opt === 'string' 
                          ? opt 
                          : `${opt.title || 'Optimization'}: ${opt.savings || opt.potential_savings || 0}`;
                        return <p key={idx} className="text-xs opacity-75">{optText}</p>;
                      })}
                    </div>
                  )}
                </div>
              )}
              <p className="text-xs opacity-50 mt-2">
                {message.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white text-gray-800 px-6 py-4 rounded-lg rounded-bl-none shadow-md">
              <div className="flex items-center gap-2">
                <Loader className="animate-spin" size={16} />
                <span className="text-sm">Thinking...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Queries */}
      {messages.length === 1 && (
        <div className="px-8 py-4 bg-white border-t border-gray-200">
          <p className="text-sm font-semibold text-gray-700 mb-3">Quick Queries:</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
            {QUICK_QUERIES.map((query, idx) => (
              <button
                key={idx}
                onClick={() => sendMessage(query)}
                className="text-left px-4 py-2 bg-gray-100 hover:bg-purple-100 text-gray-700 hover:text-purple-700 rounded-lg text-sm transition"
              >
                {query}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-6">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about your AWS costs..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600 resize-none"
            rows="2"
            disabled={loading}
          />
          <button
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
            className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg transition flex items-center gap-2 font-semibold"
          >
            {loading ? <Loader className="animate-spin" size={20} /> : <Send size={20} />}
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatInterface;
