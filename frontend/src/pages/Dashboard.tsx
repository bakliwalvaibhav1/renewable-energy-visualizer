import EnergyChart from "../components/charts/EnergyChart/EnergyChart";
import SectorBarChart from "../components/charts/SectorBarChart/SectorBarChart";

export default function Dashboard() {
    return (
        <div className="max-w-7xl mx-auto p-4">
            <EnergyChart />
            <SectorBarChart />
        </div>
    );
}
