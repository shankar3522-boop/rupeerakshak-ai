const MessageList = ({ messages }) => {
  return (
    <div className='flex-1 overflow-y-auto p-4'>
      {messages.map((msg) => (
        <div key={msg.id} className='mb-4'>
          <div className={msg.role === 'user' ? 'bg-blue-500 text-white rounded-lg p-3 ml-auto max-w-xs' : 'bg-gray-200 text-gray-900 rounded-lg p-3 mr-auto max-w-xs'}>
            <p className='text-sm'>{msg.content}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

export default MessageList