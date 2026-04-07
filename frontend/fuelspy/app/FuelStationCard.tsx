import Link from "next/link";

interface fuelCardProps {
    id: number;
    name: string;
    address: string;
    brand: string;
    prices: Array<{fuel_type: {name: string}, price_cents: number}>;
}

const fuelTypeColors: Record<string, string> = {
    E10: "bg-green-100 text-green-700",
    U91: "bg-blue-100 text-blue-700",
    U95: "bg-purple-100 text-purple-700",
    U98: "bg-orange-100 text-orange-700",
    Diesel: "bg-gray-200 text-gray-700",
}

export function fuelCard({id, name, address, brand, prices}: fuelCardProps) {
    return (
    <Link href={`/stations/${id}`}>
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition cursor-pointer">
        <div className="flex items-center justify-between mb-3">
          <div>
            <p className="font-semibold text-gray-900">{name}</p>
            <p className="text-gray-400 text-sm">{address}</p>
            <p className="text-gray-400 text-xs">{brand}</p>
          </div>
        </div>
        
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
          {prices.map(price => (
            <div key={price.fuel_type.name} className="text-center">
              <p className={`text-xs font-medium px-2 py-1 rounded-full ${fuelTypeColors[price.fuel_type.name] ?? "bg-gray-100"}`}>
                {price.fuel_type.name}
              </p>
              <p className="text-lg font-bold text-gray-900 mt-1">{(price.price_cents / 100).toFixed(1)}</p>
              <p className="text-gray-400 text-xs">c/L</p>
            </div>
          ))}
        </div>
      </div>
    </Link>
  );
}