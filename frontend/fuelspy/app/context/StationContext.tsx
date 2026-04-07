"use client"

import React, {createContext, useContext, useState, useCallback} from 'react';
import {Station, fetchStations} from '@/app/lib/api'

interface StationContextType{
    stations: Station[];
    loading: boolean;
    error: string | null;
    fetchStationsData: (fuel_type?: string, sort?: 'price_asc' | 'price_desc', 
        latitude?: number, longitude?: number) => Promise<void>
}

const StationContext = createContext<StationContextType |undefined>(undefined);

export function StationProvider({children}: {children: React.ReactNode}){
    const [stations, setStations] = useState<Station[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchStationsData = useCallback(async (
        fuel_type?: string, 
        sort?: 'price_asc' | 'price_desc',
        latitude?: number, 
        longitude?: number
    ) => {
        setLoading(true);
        setError(null);
        try{
            const data = await fetchStations(fuel_type, sort, latitude, longitude);
            setStations(data);
        } catch(err) {
            setError(err instanceof Error ? err.message: 'An error occured');
        } finally {
            setLoading(false);
        }
    }, []);

    return (
        <StationContext.Provider value = {{stations, loading, error, fetchStationsData}}>
            {children}
        </StationContext.Provider>
    );
}

export function useStations() {
    const context = useContext(StationContext);
    if(!context) throw new Error('useStations must be used inside StationProvider');
    return context;
}