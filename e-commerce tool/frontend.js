import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { BarChart, PieChart } from "recharts";
import { Button } from "@/components/ui/button";

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/dashboard")
      .then((res) => res.json())
      .then((data) => setDashboardData(data));
  }, []);

  if (!dashboardData) return <div>Loading...</div>;

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      <motion.h1
        className="text-3xl font-bold mb-6"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        E-commerce Automation Dashboard
      </motion.h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Object.entries(dashboardData.overview).map(([key, value]) => (
          <Card key={key} className="bg-gray-800">
            <CardContent className="p-4">
              <motion.h2
                className="text-xl font-semibold"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                {key.replace("_", " ").toUpperCase()}
              </motion.h2>
              <motion.p
                className="text-lg mt-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
              >
                {value}
              </motion.p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-gray-800 p-4">
          <h2 className="text-xl font-semibold">Sales by Channel</h2>
          <BarChart data={dashboardData.analytics.sales_by_channel_chart} />
        </Card>

        <Card className="bg-gray-800 p-4">
          <h2 className="text-xl font-semibold">Customer Segments</h2>
          <PieChart data={dashboardData.customer_management.customer_segments_chart} />
        </Card>
      </div>

      <div className="mt-8 flex gap-4">
        <Button className="bg-blue-600 hover:bg-blue-700">Run Automation</Button>
        <Button className="bg-red-600 hover:bg-red-700">Manage Inventory</Button>
      </div>
    </div>
  );
}
