import React, { useState } from "react";


export default function ChatBox({ chatMessages, setChatMessages, loading }) {
    const [chatInput, setChatInput] = useState("");


    const sendChat = async () => {
        if (!chatInput.trim()) return;
        const text = chatInput.trim();
        setChatMessages((m) => [...m, { from: "user", text }]);
        setChatInput("");


        try {
            const res = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text }),
            });
            const json = await res.json();
                setChatMessages((m) => [...m, { from: "assistant", text: json.reply || "I couldn't produce a reply." }]);
        } catch (err) {
            setChatMessages((m) => [...m, { from: "assistant", text: `Chat error: ${err.message}` }]);
        }
    };


    return (
        <div className="col-span-1 lg:col-span-2 bg-white shadow rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3 text-pink-600">Data Assistant Chat</h2>


            <div className="h-80 overflow-auto border rounded p-3 bg-gray-50">
                {chatMessages.map((m, i) => (
                <div key={i} className={`mb-3 ${m.from === "assistant" ? "text-left" : "text-right"}`}>
                <div
                className={`inline-block px-3 py-2 rounded-lg ${m.from === "assistant" ? "bg-white border" : "bg-pink-500 text-white"}`}
                style={{ maxWidth: "85%" }}
                >
                {m.text}
                </div>
                </div>
                ))}
            </div>


            <div className="mt-3 flex">
                <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendChat()}
                placeholder="Ask about the data, e.g. 'show summary of column X'"
                className="flex-1 px-3 py-2 rounded-l border"
                />
                <button onClick={sendChat} className="px-4 rounded-r bg-pink-500 text-white">Send</button>
            </div>
            {loading && <div className="mt-2 text-sm">Processing...</div>}
        </div>
    );
}