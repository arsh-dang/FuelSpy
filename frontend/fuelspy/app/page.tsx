"use client"
import { fuelCard as FuelCard } from "./FuelStationCard";
import { useState, useEffect } from "react";
import { useStations } from "./context/StationContext";
import { Station } from "./lib/api";


export default function Home(){
    const {stations, loading, error, fetchStationsData} = useStations();
    const [search, setSearch] = useState("");
    const fuelTypes = ["All","E10","U91","U95","U98","Diesel"];
    const [preferredFuelType, setFuelType] = useState(fuelTypes[0]);
    const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");


    const sortedStations = stations.filter((station) => {
        if(preferredFuelType === "All"){
          return true;
        }
        return station.prices.some(p => p.fuel_type.name === preferredFuelType);
      }).filter(s => s.name.toLowerCase().includes(search.toLowerCase())).sort((a, b) => {
        const getPrice = (station: Station) => {
          if(preferredFuelType === "All"){
            return Math.min(...station.prices.map(p => p.price_cents));
          }
          const price = station.prices.find(p => p.fuel_type.name === preferredFuelType);
          return price?.price_cents ?? Infinity;
        };

        const priceA = getPrice(a);
        const priceB = getPrice(b);

        return sortDirection === "asc" ? priceA - priceB : priceB - priceA;
      })

    useEffect(() => {
      fetchStationsData();
    }, [fetchStationsData]);

    useEffect(() => {
      if(preferredFuelType !== "All"){
        fetchStationsData(preferredFuelType, sortDirection === "asc" ? "price_asc" : "price_desc");
      } else {
        fetchStationsData(undefined, sortDirection === "asc" ? "price_asc" : "price_desc");
      }
    }, [preferredFuelType, sortDirection, fetchStationsData])


    if (loading) return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950">
        <p className="text-white text-lg">Loading...</p>
      </div>
    );

    if (error) return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950">
        <p className="text-red-400 text-lg">Error: {error}</p>
      </div>
    );

    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-2xl mx-auto">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search station name..."
            className="w-full px-4 py-2.5 rounded-xl bg-white border border-gray-200 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent mb-4"
          />

          <div className="flex gap-3 mb-6">
            <select
              value={preferredFuelType}
              onChange={(e) => setFuelType(e.target.value)}
              className="px-4 py-2 rounded-xl bg-white border border-gray-200 text-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              {fuelTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>

            <button
              onClick={() => setSortDirection(sortDirection === "asc" ? "desc" : "asc")}
              className="px-4 py-2 rounded-xl bg-white border border-gray-200 text-gray-700 text-sm hover:bg-gray-50 transition"
            >
              Price: {sortDirection === "asc" ? "Low \u2192 High" : "High \u2192 Low"}
            </button>
          </div>

          <div className="flex flex-col gap-3">
            {sortedStations.map(p => (
                <FuelCard key={p.id}{...p} />
              ))}
          </div>
        </div>
      </div>
    );
    
}
    
    
