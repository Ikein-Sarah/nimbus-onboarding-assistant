import { ChatIcon } from './Icons'

export default function ChatButton({ onClick }) {
  return (
    <button className="fab" aria-label="Ask Nimbus" onClick={onClick}>
      <ChatIcon />
    </button>
  )
}
