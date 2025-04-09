import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    BarElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

type SourceBarChartProps = {
    generationData: any[];
};

export default function SourceBarChart({ generationData }: SourceBarChartProps) {

    // Group data by source and sum energy
    const sourceTotals: Record<string, number> = {};
    generationData.forEach((entry) => {
        const source = entry.source;
        sourceTotals[source] = (sourceTotals[source] || 0) + entry.energy_kwh;
    });

    const labels = Object.keys(sourceTotals);
    const values = labels.map((source) => sourceTotals[source]);

    const data = {
        labels,
        datasets: [
            {
                label: "Total Consumption (kWh)",
                data: values,
                backgroundColor: ["#22c55e", "#3b82f6", "#f97316"],
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
                    stepSize: 100000,
                },
            },
        },
    };

    return (
        <div className="bg-white rounded shadow p-4">
            <h2 className="text-lg font-semibold mb-4">Energy Generation by Sector</h2>
            <div className="w-full min-w-[500px]">
                <Bar data={data} options={options} />
            </div>
        </div>
    );
}
