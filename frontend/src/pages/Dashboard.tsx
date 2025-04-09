import { useEffect, useState } from "react";
import { api } from "../library/axios";
import EnergyChart from "../components/charts/EnergyChart/EnergyChart";
import SectorBarChart from "../components/charts/SourceBarChart/SourceBarChart";
import PieChart from "../components/charts/PieChart/PieChart";

export default function Dashboard() {
    const [consumptionData, setConsumptionData] = useState<any[]>([]);
    const [generationData, setGenerationData] = useState<any[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [consRes, genRes] = await Promise.all([
                    api.get("/energy/consumption"),
                    api.get("/energy/generation"),
                ]);
                setConsumptionData(consRes.data);
                setGenerationData(genRes.data);
            } catch (err) {
                console.error("❌ Error fetching dashboard data", err);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="max-w-7xl mx-auto p-4 space-y-4">
            <EnergyChart
                consumptionData={consumptionData}
                generationData={generationData}
            />
            <div className="flex flex-col md:flex-row gap-4">
                <div className="w-full md:w-1/2">
                    <SectorBarChart generationData={generationData} />
                </div>
                <div className="w-full md:w-1/2">
                    <PieChart consumptionData={consumptionData} />
                </div>
            </div>
        </div>
    );
}
