import React from 'react';

interface AnimatedTextProps {
    text: string;
}

const AnimatedText: React.FC<AnimatedTextProps> = ({ text }) => {
    const words: string[] = text.split(' ');

    
    return (
        <div className="flex flex-wrap">
            {words.map((word, index) => (
                <span
                    key={index}
                    className={`inline-block mr-1 opacity-0 animate-word-appear`}
                    style={{ animationDelay: `${index * 0.5}s` }}
                >
                    {word}
                </span>
            ))}
        </div>
    );
};

export default AnimatedText;
