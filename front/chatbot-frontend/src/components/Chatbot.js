import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAskQuestion = async () => {
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/api/chatbot/ask', {
        question: question,
      });
      setResponse(res.data.response);
    } catch (error) {
      console.error("Error asking question:", error);
      setResponse("Sorry, there was an error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h1>Ask the Legal Chatbot</h1>
      <div className="form-group mt-3">
        <input
          type="text"
          className="form-control"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question"
        />
      </div>
      <button className="btn btn-primary mt-3" onClick={handleAskQuestion}>
        Ask
      </button>
      {loading && <p>Loading...</p>}
      {response && <p>Bot Response: {response}</p>}
    </div>
  );
};

export default Chatbot;
