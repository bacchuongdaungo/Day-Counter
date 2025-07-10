// The base URL for our deployed Google Cloud Function.
const API_BASE_URL = "https://us-central1-cainghien.cloudfunctions.net/get-motivational-phrase";

// TypeScript types for our API responses. This gives us type safety.
export interface DayCountResponse {
    day_count: number;
}

export interface PhraseResponse {
    phrase: string;
}

export async function fetchDayCount(startDate: string): Promise<DayCountResponse> {
    const response = await fetch(`${API_BASE_URL}/get-day-count?startDate=${startDate}`);
    if (!response.ok) {
        throw new Error('Failed to fetch day count');
    }
    return response.json();
}

export async function fetchPhrase(): Promise<PhraseResponse> {
    const response = await fetch(`${API_BASE_URL}/get-phrase`);
    if (!response.ok) {
        throw new Error('Failed to fetch phrase');
    }
    return response.json();
}