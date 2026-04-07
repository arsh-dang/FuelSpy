const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export interface Price{
    id: number;
    fuel_type_id: number;
    fuel_type: FuelType;
    price_cents: number;
    fetched_at: string;
}

export interface FuelType {id: number, name: string}

export interface Station {
    id: number;
    name: string;
    address: string;
    latitude: number;
    longitude: number;
    brand: string;
    prices: Price[];
}

export interface PriceHistory {
    id: number
    station_id: number;
    fuel_type_id: number;
    fuel_type: FuelType;
    price_cents: number;
    fetched_at: string;
}

export async function fetchStations(
    fuel_type?: string,
    sort?: 'price_asc' | 'price_desc',
    latitude?: number, 
    longitude?: number
): Promise<Station[]> {
    const params = new URLSearchParams();
    if(fuel_type) params.append('fuel_type', fuel_type)
    if(sort) params.append('sort', sort)
    // Commented to use in further implementation
    // if(latitude) params.append('latitude', latitude.toString())
    // if(longitude) params.append('longitude', longitude.toString())
    const response = await fetch(`${API_BASE_URL}/api/stations/?${params}`)
    if(!response.ok) throw new Error('Station not found');
    return response.json();
}

export async function fetchStationDetail(id: number): Promise<Station>{
    const response = await fetch(`${API_BASE_URL}/api/stations/${id}`)
    if(!response.ok) throw new Error('Station not found');
    return response.json()
}

export async function fetchPriceHistory(id: number, days: number = 7){
    const response = await fetch(`${API_BASE_URL}/api/stations/${id}/history?days=${days}`)
    if(!response.ok) throw new Error('Failed to fetch price history');
    return response.json()
}