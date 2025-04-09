import { useMemo } from "react";
import { Pie } from "react-chartjs-2";
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

type PieChartProps = {
    consumptionData: any[];
};

export default function PieChart({ consumptionData }: PieChartProps) {
    const sectorTotals = useMemo(() => {
        const totals: Record<string, number> = {};
        consumptionData.forEach((entry) => {
            const sector = entry.sector;
            totals[sector] = (totals[sector] || 0) + entry.energy_kwh;
        });
        return totals;
    }, [consumptionData]);

    const labels = Object.keys(sectorTotals);
    const values = Object.values(sectorTotals);

    const data = {
        labels,
        datasets: [
            {
                label: "Energy Consumption (kWh)",
                data: values,
                backgroundColor: [
                    "rgb(255, 99, 132)",
                    "rgb(54, 162, 235)",
                    "rgb(255, 205, 86)",
                ],
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className="bg-white rounded shadow p-4 w-full">
            <h2 className="text-lg font-semibold mb-4">Sector-wise Energy Consumption</h2>
            <Pie data={data} />
        </div>
    );
}
