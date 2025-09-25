import { useState } from "react";

export default function ChatBox({ messages, onSend }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input) return;
    onSend(input);
    setInput("");
  };

  return (
    <div>
      <div style={{ maxHeight: "400px", overflowY: "scroll", border: "1px solid gray", padding: "10px" }}>
        {messages.map((m, i) => (
          <div key={i}><b>{m.sender}:</b> {m.text}</div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="メッセージを入力" />
        <button type="submit">送信</button>
      </form>
    </div>
  );
}
