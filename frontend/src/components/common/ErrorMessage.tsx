interface ErrorMessageProps {
  message?: string
}

const ErrorMessage = ({ message = 'Произошла ошибка' }: ErrorMessageProps) => {
  return (
    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      {message}
    </div>
  )
}

export default ErrorMessage
