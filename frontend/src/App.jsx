import React, { useState, useRef } from "react";
import FileUploadPreview from "./components/FileUploadPreview";
import ChatBox from "./components/ChatBox";
import Dashboard from "./components/Dashboard";


export default function App() {
  const [chatMessages, setChatMessages] = useState([
      { from: "assistant", text: "Hello — upload a CSV or Excel file to get started." },
  ]);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);


  return (
    <div className="min-h-screen bg-white text-gray-800 p-6 font-sans">
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        <FileUploadPreview
          setChatMessages={setChatMessages}
          setLoading={setLoading}
          setDashboardData={setDashboardData}
        />
        <ChatBox
          chatMessages={chatMessages}
          setChatMessages={setChatMessages}
          loading={loading}
        />
        <Dashboard data={dashboardData} loading={loading} />
      </div>
    </div>
  );
}