import { useState } from 'react'
import ChatWidget from './components/ChatWidget'
import LanguageSelector from './components/LanguageSelector'

function App() {
  const [language, setLanguage] = useState('english')

  return (
    <div className='min-h-screen bg-gradient-to-b from-blue-50 to-white'>
      <div className='fixed top-4 right-4'>
        <LanguageSelector language={language} setLanguage={setLanguage} />
      </div>
      <ChatWidget language={language} />
    </div>
  )
}

export default App