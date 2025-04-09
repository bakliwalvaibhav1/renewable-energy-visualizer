import { Range } from "react-range";

type FiltersProps = {
    showConsumption: boolean;
    setShowConsumption: (val: boolean) => void;
    showGeneration: boolean;
    setShowGeneration: (val: boolean) => void;
    dateList: string[];
    dateRange: number[];
    setDateRange: React.Dispatch<React.SetStateAction<[number, number]>>;
    minDate: number;
    maxDate: number;
    consumptionLocations: string[];
    selectedConsumptionLocations: string[];
    setSelectedConsumptionLocations: (val: string[]) => void;
    generationLocations: string[];
    selectedGenerationLocations: string[];
    setSelectedGenerationLocations: (val: string[]) => void;
};

export default function Filters({
    showConsumption,
    setShowConsumption,
    showGeneration,
    setShowGeneration,
    dateList,
    dateRange,
    setDateRange,
    minDate,
    maxDate,
    consumptionLocations,
    selectedConsumptionLocations,
    setSelectedConsumptionLocations,
    generationLocations,
    selectedGenerationLocations,
    setSelectedGenerationLocations,
}: FiltersProps) {
    const toggleAll = (
        current: string[],
        selected: string[],
        setSelected: (val: string[]) => void
    ) => {
        if (selected.length === current.length) {
            setSelected([]);
        } else {
            setSelected([...current]);
        }
    };

    const toggleSingle = (
        location: string,
        selected: string[],
        setSelected: (val: string[]) => void
    ) => {
        if (selected.includes(location)) {
            setSelected(selected.filter((loc) => loc !== location));
        } else {
            setSelected([...selected, location]);
        }
    };

    return (
        <div className="flex flex-wrap p-4 bg-white gap-2">
            {/* Energy Filter */}
            <div className="p-4 bg-white rounded shadow">
                <p className="font-semibold mb-2">Energy</p>
                <div className="flex flex-col gap-2 mb-4">
                    <label className="inline-flex items-center">
                        <input
                            type="checkbox"
                            className="form-checkbox mr-2"
                            checked={showConsumption}
                            onChange={() => setShowConsumption(!showConsumption)}
                        />
                        Energy Consumption
                    </label>
                    <label className="inline-flex items-center">
                        <input
                            type="checkbox"
                            className="form-checkbox mr-2"
                            checked={showGeneration}
                            onChange={() => setShowGeneration(!showGeneration)}
                        />
                        Energy Generation
                    </label>
                </div>
            </div>

            {/* Date Filter */}
            <div className="p-4 bg-white rounded shadow">
                <p className="font-semibold mb-2">Date Range</p>
                <div className="flex flex-col gap-2">
                    <Range
                        values={dateRange}
                        step={1}
                        min={minDate}
                        max={maxDate}
                        onChange={(values) =>
                            setDateRange(values as [number, number])
                        }
                        renderTrack={({ props, children }) => (
                            <div
                                {...props}
                                className="h-2 bg-gray-200 rounded-full"
                                style={{ ...props.style }}
                            >
                                {children}
                            </div>
                        )}
                        renderThumb={({ props, index }) => {
                            const { key, ...rest } = props;
                            return (
                                <div
                                    key={key ?? index}
                                    {...rest}
                                    className="w-4 h-4 bg-blue-500 rounded-full shadow"
                                />
                            );
                        }}
                    />
                    <div className="flex justify-between text-sm mt-2 text-gray-600">
                        <span>{dateList?.[dateRange[0]] ?? "Start"}</span>
                        <span>{dateList?.[dateRange[1]] ?? "End"}</span>
                    </div>
                </div>
            </div>

            {/* Consumption Locations */}
            <div className="p-4 bg-white rounded shadow">
                <p className="font-semibold mb-2">Consumption Locations</p>
                <div className="flex flex-col gap-2">
                    <label className="inline-flex items-center">
                        <input
                            type="checkbox"
                            className="form-checkbox mr-2"
                            checked={selectedConsumptionLocations.length === consumptionLocations.length}
                            onChange={() =>
                                toggleAll(
                                    consumptionLocations,
                                    selectedConsumptionLocations,
                                    setSelectedConsumptionLocations
                                )
                            }
                        />
                        Select All
                    </label>
                    {consumptionLocations.map((loc) => (
                        <label key={loc} className="inline-flex items-center">
                            <input
                                type="checkbox"
                                className="form-checkbox mr-2"
                                checked={selectedConsumptionLocations.includes(loc)}
                                onChange={() =>
                                    toggleSingle(loc, selectedConsumptionLocations, setSelectedConsumptionLocations)
                                }
                            />
                            {loc}
                        </label>
                    ))}
                </div>
            </div>

            {/* Generation Locations */}
            <div className="p-4 bg-white rounded shadow">
                <p className="font-semibold mb-2">Generation Locations</p>
                <div className="flex flex-col gap-2">
                    <label className="inline-flex items-center">
                        <input
                            type="checkbox"
                            className="form-checkbox mr-2"
                            checked={selectedGenerationLocations.length === generationLocations.length}
                            onChange={() =>
                                toggleAll(
                                    generationLocations,
                                    selectedGenerationLocations,
                                    setSelectedGenerationLocations
                                )
                            }
                        />
                        Select All
                    </label>
                    {generationLocations.map((loc) => (
                        <label key={loc} className="inline-flex items-center">
                            <input
                                type="checkbox"
                                className="form-checkbox mr-2"
                                checked={selectedGenerationLocations.includes(loc)}
                                onChange={() =>
                                    toggleSingle(loc, selectedGenerationLocations, setSelectedGenerationLocations)
                                }
                            />
                            {loc}
                        </label>
                    ))}
                </div>
            </div>
        </div>
    );
}
