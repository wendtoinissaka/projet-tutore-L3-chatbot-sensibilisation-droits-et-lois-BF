import { useState } from 'react';
import axios from 'axios';

function ChatBox() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/ask', { question });
            setAnswer(response.data.answer);
        } catch (error) {
            console.error("There was an error sending the question!", error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Posez votre question ici"
                />
                <button type="submit">Envoyer</button>
            </form>
            {answer && <p>Réponse : {answer}</p>}
        </div>
    );
}
export default ChatBox;
