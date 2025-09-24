import React from "react";
import {
    LineChart,
    Line,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    BarChart,
    Bar,
} from "recharts";


export default function Dashboard({ data, loading }) {
    return (
        <div className="col-span-1 lg:col-span-3 bg-white shadow rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3 text-pink-600">Dashboard</h2>
            {loading && <div className="text-sm mb-2">Loading...</div>}
            
            
            {!data || data.length === 0 ? (
                <div className="text-sm text-gray-500">No dashboard data yet. Click "Dashboard Agent" to generate charts.</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="h-64 bg-white p-2 border rounded">
                        <h4 className="text-sm font-medium mb-1">Line Chart</h4>
                        <ResponsiveContainer width="100%" height={220}>
                        <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="label" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="value" stroke="#ff33aa" strokeWidth={2} />
                        </LineChart>
                        </ResponsiveContainer>
                    </div>
                    
                    
                    <div className="h-64 bg-white p-2 border rounded">
                        <h4 className="text-sm font-medium mb-1">Bar Chart</h4>
                        <ResponsiveContainer width="100%" height={220}>
                        <BarChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="label" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="value" fill="#ff33aa" />
                        </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            )}
        </div>
    );
}