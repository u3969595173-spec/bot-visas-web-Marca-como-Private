import React, { useState, useRef, useEffect } from 'react';
import './ChatbotIA.css';

const ChatbotIA = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        {
            sender: 'bot',
            text: '¡Hola! Soy tu Asistente Empresarial de Capital Iberia. Conozco todas las operativas (con techo hasta el 300%) y normativas internas. ¿En qué te ayudo?'
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);

    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const handleSend = async () => {
        if (!inputValue.trim()) return;

        const currentInput = inputValue;
        const userMsg = { sender: 'user', text: currentInput };
        setMessages((prev) => [...prev, userMsg]);
        setInputValue('');
        setIsTyping(true);

        try {
            const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: currentInput })
            });
            const data = await response.json();

            const botMsg = { sender: 'bot', text: data.response };
            setMessages((prev) => [...prev, botMsg]);
        } catch (error) {
            setMessages((prev) => [...prev, { sender: 'bot', text: 'Mis núcleos de procesamiento están inactivos. Verifica la conexión a Internet o los puertos del servidor.' }]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    };

    return (
        <div className="chatbot-wrapper">
            {!isOpen && (
                <button onClick={toggleChat} className="chatbot-trigger" aria-label="Abrir Chatbot">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.38-.445 1.543-1.42 2.72-2.18 3.32-.195.155-.38.293-.559.407a1.05 1.05 0 0 0 .474 1.832 9.079 9.079 0 0 0 4.67-.707A8.736 8.736 0 0 0 12 20.25Z" />
                    </svg>
                    <span className="chatbot-notification-dot"></span>
                </button>
            )}

            {isOpen && (
                <div className="chatbot-window">
                    {/* Header */}
                    <div className="chatbot-header">
                        <div className="chatbot-header-info">
                            <div className="chatbot-avatar">CI</div>
                            <div className="chatbot-header-text">
                                <h3>Asistente IA</h3>
                                <span>En línea</span>
                            </div>
                        </div>
                        <button onClick={toggleChat} className="chatbot-close-btn" aria-label="Cerrar Chatbot">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    {/* Messages Area */}
                    <div className="chatbot-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`chat-message ${msg.sender}`}>
                                {msg.text}
                            </div>
                        ))}

                        {isTyping && (
                            <div className="chat-loading">
                                <div className="dot"></div>
                                <div className="dot"></div>
                                <div className="dot"></div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="chatbot-input-area">
                        <input
                            type="text"
                            placeholder="Escribe tu consulta aquí..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={handleKeyPress}
                        />
                        <button
                            className="chatbot-send-btn"
                            onClick={handleSend}
                            disabled={!inputValue.trim()}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                            </svg>
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatbotIA;
