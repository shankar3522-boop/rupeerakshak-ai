import { useState, useRef, useEffect } from 'react'
import MessageList from './MessageList'
import InputBox from './InputBox'

const ChatWidget = ({ language }) => {
  const [messages, setMessages] = useState([
    {
      id: '1',
      content: 'Welcome to Rupee Rakshak AI! How can I help you today?',
      role: 'assistant',
      timestamp: new Date()
    }
  ])
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (content) => {
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date()
    }])
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, language })
      })
      const data = await response.json()
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        content: data.content || 'Sorry, I could not process your request.',
        role: 'assistant',
        timestamp: new Date()
      }])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className='flex items-center justify-center min-h-screen p-4'>
      <div className='bg-white rounded-lg shadow-lg w-full max-w-2xl h-96 flex flex-col'>
        <div className='bg-blue-600 text-white p-4 rounded-t-lg'>
          <h2 className='text-xl font-bold'>Rupee Rakshak AI</h2>
          <p className='text-sm'>Your Wealth Advisor</p>
        </div>
        <MessageList messages={messages} />
        <InputBox onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  )
}

export default ChatWidget