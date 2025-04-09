import { useEffect, useState, useMemo } from "react";
import { Line } from "react-chartjs-2";
import { api } from "../../../library/axios";
import Filters from "./Filters";
import dayjs from "dayjs";

import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
    Legend,
    ChartOptions,
} from "chart.js";

ChartJS.register(
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
    Legend
);

export default function EnergyChart() {
    const dateList = useMemo(() => {
        const dates = [];
        let current = dayjs("2023-01-01");
        const end = dayjs("2025-04-08");
        while (current.isBefore(end) || current.isSame(end)) {
            dates.push(current.format("YYYY-MM-DD"));
            current = current.add(1, "day");
        }
        return dates;
    }, []);

    const [dateRange, setDateRange] = useState<[number, number]>([0, 0]);
    const [showConsumption, setShowConsumption] = useState(true);
    const [showGeneration, setShowGeneration] = useState(true);
    const [consumptionData, setConsumptionData] = useState<any[]>([]);
    const [generationData, setGenerationData] = useState<any[]>([]);

    // const [allLocations, setAllLocations] = useState<string[]>([]);
    const [consumptionLocations, setConsumptionLocations] = useState<string[]>([]);
    const [generationLocations, setGenerationLocations] = useState<string[]>([]);
    const [selectedConsumptionLocations, setSelectedConsumptionLocations] = useState<string[]>([]);
    const [selectedGenerationLocations, setSelectedGenerationLocations] = useState<string[]>([]);

    useEffect(() => {
        const fetchConsumption = async () => {
            try {
                const res = await api.get("/energy/consumption");
                setConsumptionData(res.data);
            } catch (err) {
                console.error("Failed to fetch consumption data", err);
            }
        };
        const fetchGeneration = async () => {
            try {
                const res = await api.get("/energy/generation");
                setGenerationData(res.data);
            } catch (err) {
                console.error("Failed to fetch generation data", err);
            }
        };

        fetchConsumption();
        fetchGeneration();
    }, []);

    useEffect(() => {
        if (dateList.length > 0) {
            const defaultStart = dayjs("2025-01-01");
            const defaultEnd = dayjs("2025-04-08");

            const startIndex = dateList.findIndex((d) => dayjs(d).isSame(defaultStart, "day"));
            const endIndex = dateList.findIndex((d) => dayjs(d).isSame(defaultEnd, "day"));

            if (startIndex !== -1 && endIndex !== -1) {
                setDateRange([startIndex, endIndex]);
            } else {
                setDateRange([0, dateList.length - 1]);
            }
        }
    }, [dateList]);

    useEffect(() => {
        const consumptionLocs = new Set(consumptionData.map((item) => item.location));
        const generationLocs = new Set(generationData.map((item) => item.location));

        setConsumptionLocations(Array.from(consumptionLocs));
        setGenerationLocations(Array.from(generationLocs));
        setSelectedConsumptionLocations(Array.from(consumptionLocs));
        setSelectedGenerationLocations(Array.from(generationLocs));
    }, [consumptionData, generationData]);

    const startDate = dayjs(dateList[dateRange[0]]);
    const endDate = dayjs(dateList[dateRange[1]]);

    const filteredConsumption = consumptionData.filter((entry) => {
        const entryDate = dayjs(entry.timestamp);
        return (
            selectedConsumptionLocations.includes(entry.location) &&
            entryDate.isAfter(startDate.subtract(1, "day")) &&
            entryDate.isBefore(endDate.add(1, "day"))
        );
    });

    const filteredGeneration = generationData.filter((entry) => {
        const entryDate = dayjs(entry.timestamp);
        return (
            selectedGenerationLocations.includes(entry.location) &&
            entryDate.isAfter(startDate.subtract(1, "day")) &&
            entryDate.isBefore(endDate.add(1, "day"))
        );
    });

    const groupByDate = (data: any[]) => {
        const totals: Record<string, number> = {};
        data.forEach(({ timestamp, energy_kwh }) => {
            const date = timestamp.split("T")[0];
            totals[date] = (totals[date] || 0) + energy_kwh;
        });
        return totals;
    };

    const consumptionTotals = groupByDate(filteredConsumption);
    const generationTotals = groupByDate(filteredGeneration);

    const allDates = Array.from(
        new Set([...Object.keys(consumptionTotals), ...Object.keys(generationTotals)])
    ).sort();

    const labels = allDates;
    const consumption = allDates.map((date) => consumptionTotals[date] ?? 0);
    const generation = allDates.map((date) => generationTotals[date] ?? 0);

    const datasets = [];

    if (showConsumption) {
        datasets.push({
            label: "Energy Consumption (kWh)",
            data: consumption,
            fill: false,
            borderColor: "rgb(75, 192, 192)",
            tension: 0.3,
            pointRadius: 3,
        });
    }

    if (showGeneration) {
        datasets.push({
            label: "Energy Generation (kWh)",
            data: generation,
            fill: false,
            borderColor: "rgb(255, 99, 132)",
            tension: 0.3,
            pointRadius: 3,
        });
    }

    const data = { labels, datasets };

    const options: ChartOptions<"line"> = {
        responsive: true,
        plugins: { legend: { display: true } },
        scales: {
            x: {
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 10,
                    callback: function (_tickValue, index) {
                        const label = labels[index];
                        if (typeof label === "string") {
                            const date = new Date(label);
                            return new Intl.DateTimeFormat("en-US", {
                                month: "short",
                                day: "2-digit",
                                year: "2-digit",
                            }).format(date);
                        }
                        return label;
                    },
                },
                grid: { display: true },
            },
            y: {
                min: 0,
                max: 2100,
                ticks: { stepSize: 300 },
                grid: { display: true },
            },
        },
    };

    return (
        <div className="bg-white rounded shadow p-2 max-w-full overflow-x-auto">
            <Filters
                showConsumption={showConsumption}
                setShowConsumption={setShowConsumption}
                showGeneration={showGeneration}
                setShowGeneration={setShowGeneration}
                dateRange={dateRange}
                setDateRange={setDateRange}
                dateList={dateList}
                minDate={0}
                maxDate={dateList.length - 1}
                consumptionLocations={consumptionLocations}
                selectedConsumptionLocations={selectedConsumptionLocations}
                setSelectedConsumptionLocations={setSelectedConsumptionLocations}
                generationLocations={generationLocations}
                selectedGenerationLocations={selectedGenerationLocations}
                setSelectedGenerationLocations={setSelectedGenerationLocations}
            />
            <div className="w-full min-w-[600px]">
                <Line data={data} options={options} />
            </div>
        </div>
    );
}
