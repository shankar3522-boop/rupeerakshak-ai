const LanguageSelector = ({ language, setLanguage }) => {
  const languages = [
    { code: 'english', label: 'English' },
    { code: 'hindi', label: 'हिंदी' },
    { code: 'kannada', label: 'ಕನ್ನಡ' },
  ]

  return (
    <select
      value={language}
      onChange={(e) => setLanguage(e.target.value)}
      className='px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
    >
      {languages.map((lang) => (
        <option key={lang.code} value={lang.code}>
          {lang.label}
        </option>
      ))}
    </select>
  )
}

export default LanguageSelector