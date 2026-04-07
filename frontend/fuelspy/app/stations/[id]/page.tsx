'use client';

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { fetchStationDetail, fetchPriceHistory, Station, PriceHistory } from '@/app/lib/api';

export default function StationDetail() {
  const params = useParams();
  const id = parseInt(params.id as string);
  
  const [station, setStation] = useState<Station | null>(null);
  const [history, setHistory] = useState<PriceHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const stationData = await fetchStationDetail(id);
        const historyData = await fetchPriceHistory(id, 7);
        setStation(stationData);
        setHistory(historyData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load station');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  if (error) return <div className="min-h-screen flex items-center justify-center text-red-500">Error: {error}</div>;
  if (!station) return <div className="min-h-screen flex items-center justify-center">Station not found</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto">
        <Link href="/" className="text-blue-500 hover:underline mb-4 inline-block">← Back</Link>
        
        <div className="bg-white rounded-xl p-6 shadow-md mb-6">
          <h1 className="text-3xl font-bold text-gray-900">{station.name}</h1>
          <p className="text-gray-500 text-lg">{station.address}</p>
          <p className="text-gray-400 text-sm">ID: {station.id}</p>
          <p className="text-gray-400 text-sm">Brand: {station.brand}</p>

          <div className="mt-6">
            <h2 className="text-xl font-bold text-gray-900 mb-3">Current Prices</h2>
            <div className="grid grid-cols-2 gap-4">
              {station.prices.map(price => (
                <div key={price.id} className="bg-gray-100 p-4 rounded-lg">
                  <p className="text-gray-600">{price.fuel_type.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{(price.price_cents / 100).toFixed(2)}c</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-md">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Price History (Last 7 Days)</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <div className="bg-white rounded-xl p-6 shadow-md">
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Price History (Last 7 Days)</h2>
                    {history.length === 0 ? (
                        <p className="text-gray-500">No price history available</p>
                    ) : (
                        <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead className="bg-gray-100 border-b">
                            <tr>
                                <th className="p-3 text-left font-semibold text-gray-900">Date</th>
                                <th className="p-3 text-left font-semibold text-gray-900">Fuel Type</th>
                                <th className="p-3 text-right font-semibold text-gray-900">Price</th>
                            </tr>
                            </thead>
                            <tbody>
                            {history.map(h => (
                                <tr key={h.id} className="border-b hover:bg-gray-50 transition">
                                <td className="p-3 text-gray-900">{new Date(h.fetched_at).toLocaleDateString()}</td>
                                <td className="p-3 text-gray-900">{h.fuel_type.name}</td>
                                <td className="p-3 text-right text-gray-900 font-semibold">{(h.price_cents / 100).toFixed(2)}c</td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                        </div>
                    )}
            </div>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}