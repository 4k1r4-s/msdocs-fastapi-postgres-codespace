import { useState } from "react";
import ChatBox from "./components/ChatBox";

function App() {
  const [messages, setMessages] = useState([]);

  const sendMessage = async (text) => {
    setMessages([...messages, { sender: "You", text }]);
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    setMessages((prev) => [...prev, { sender: "Bot", text: data.reply }]);
  };

  return (
    <div className="App">
      <h1>コースティックとチャット</h1>
      <ChatBox messages={messages} onSend={sendMessage} />
    </div>
  );
}

export default App;
