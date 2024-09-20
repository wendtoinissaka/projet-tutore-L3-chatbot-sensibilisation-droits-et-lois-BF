import React, { useEffect, useState } from 'react';
import axios from 'axios';

const LegalInfo = () => {
  const [legalData, setLegalData] = useState([]);

  useEffect(() => {
    const fetchLegalInfo = async () => {
      try {
        const res = await axios.get('http://localhost:5000/api/legal');
        setLegalData(res.data);
      } catch (error) {
        console.error("Error fetching legal data:", error);
      }
    };

    fetchLegalInfo();
  }, []);

  return (
    <div>
      <h2>Legal Information</h2>
      <ul>
        {legalData.map((item) => (
          <li key={item.id}>{item.title}: {item.description}</li>
        ))}
      </ul>
    </div>
  );
};

export default LegalInfo;
