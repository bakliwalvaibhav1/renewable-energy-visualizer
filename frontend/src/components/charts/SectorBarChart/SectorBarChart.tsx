// components/charts/SectorBarChart.tsx
import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import { api } from "../../../library/axios";
import {
    Chart as ChartJS,
    BarElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend,
} from "chart.js";
import dayjs from "dayjs";

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

export default function SectorBarChart() {
    const [consumptionData, setConsumptionData] = useState<any[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await api.get("/energy/consumption");
                setConsumptionData(res.data);
            } catch (err) {
                console.error("Failed to fetch consumption data", err);
            }
        };

        fetchData();
    }, []);

    // Group data by sector and sum energy
    const sectorTotals: Record<string, number> = {};
    consumptionData.forEach((entry) => {
        const sector = entry.sector;
        sectorTotals[sector] = (sectorTotals[sector] || 0) + entry.energy_kwh;
    });

    const labels = Object.keys(sectorTotals);
    const values = labels.map((sector) => sectorTotals[sector]);

    const data = {
        labels,
        datasets: [
            {
                label: "Total Consumption (kWh)",
                data: values,
                backgroundColor: ["#22c55e", "#3b82f6", "#f97316"], // Tailwind green-500, blue-500, orange-500
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { display: true },
            tooltip: {
                callbacks: {
                    label: function (context: any) {
                        return `${context.dataset.label}: ${context.parsed.y.toFixed(2)} kWh`;
                    },
                },
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1000,
                },
            },
        },
    };

    return (
        <div className="bg-white rounded shadow p-4 mt-4">
            <h2 className="text-lg font-semibold mb-4">Energy Consumption by Sector</h2>
            <div className="w-full min-w-[500px]">
                <Bar data={data} options={options} />
            </div>
        </div>
    );
}
