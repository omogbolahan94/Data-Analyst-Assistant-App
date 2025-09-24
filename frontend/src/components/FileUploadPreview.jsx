import React, { useState, useRef } from "react";
import { parseCSV, parseExcel } from "../utils/fileParser";


export default function FileUploadPreview({ setChatMessages, setLoading, setDashboardData }) {
    const [fileName, setFileName] = useState(null);
    const [previewRows, setPreviewRows] = useState([]);
    const [columns, setColumns] = useState([]);
    const fileRef = useRef(null);
    
    
    const handleFileLocalPreview = async (file) => {
        setFileName(file.name);
        const name = file.name.toLowerCase();
        if (name.endsWith(".csv")) {
            const { fields, data } = await parseCSV(file);
            setColumns(fields);
            setPreviewRows(data);
        } else if (name.endsWith(".xls") || name.endsWith(".xlsx")) {
            const { fields, data } = await parseExcel(file);
            setColumns(fields);
            setPreviewRows(data);
        }
    };

    const handleFileUpload = async (file) => {
        setLoading(true);
        try {
            const fd = new FormData();
            fd.append("file", file);
            const res = await fetch("/api/upload", { method: "POST", body: fd });
            const json = await res.json();
            setChatMessages((m) => [...m, { from: "assistant", text: json.message || "File uploaded." }]);
        } catch (err) {
            setChatMessages((m) => [...m, { from: "assistant", text: `Upload error: ${err.message}` }]);
        } finally {
            setLoading(false);
        }
    };

    const onFileChange = async (e) => {
        const f = e.target.files && e.target.files[0];
        if (!f) return;
        await handleFileLocalPreview(f);
        await handleFileUpload(f);
        };
        
        
    const callDashboardAgent = async () => {
        setLoading(true);
        try {
            const res = await fetch("/api/dashboard");
            const json = await res.json();
            setDashboardData(json.data || []);
            setChatMessages((m) => [...m, { from: "assistant", text: json.message || "Dashboard generated." }]);
        } catch (err) {
            setChatMessages((m) => [...m, { from: "assistant", text: `Dashboard error: ${err.message}` }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="col-span-1 bg-white shadow rounded-lg p-4 border border-pink-500">
            <h2 className="text-lg font-semibold mb-2 text-pink-600">File Upload & Preview</h2>
            <input ref={fileRef} type="file" accept=".csv,.xls,.xlsx" onChange={onFileChange} />
            <div className="mt-3 text-sm text-gray-600">Uploaded: {fileName || "none"}</div>

            <div className="mt-4 overflow-auto max-h-48 border rounded">
                <table className="w-full text-sm">
                    <thead className="bg-gray-50">
                        <tr>
                            {columns.map((c, i) => (
                                <th key={i} className="px-2 py-1 text-left border-b">{c}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {previewRows.map((row, ri) => (
                        <tr key={ri} className={ri % 2 ? "bg-white" : "bg-gray-50"}>
                            {columns.map((c, ci) => (
                            <td key={ci} className="px-2 py-1 border-b text-xs">{String(row[c] || "")}</td>
                            ))}
                        </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-4">
                <button
                    onClick={() => fileRef.current && fileRef.current.click()}
                    className="px-3 py-2 rounded shadow-sm border text-white bg-pink-500 hover:bg-pink-600"
                    >
                    Choose File
                </button>
                <button
                    onClick={callDashboardAgent}
                    className="ml-2 px-3 py-2 rounded shadow-sm border text-pink-600 border-pink-600 bg-white hover:bg-pink-50"
                    >
                    Dashboard Agent
                </button>
            </div>
        </div>
    );
}