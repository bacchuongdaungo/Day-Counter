import { useState, useEffect } from 'react';
import { fetchDayCount, fetchPhrase } from '../api';

interface MainViewProps {
    startDate: string;
}

export function MainView({ startDate }: MainViewProps) {
    const [dayCount, setDayCount] = useState<number>(0);
    const [phrase, setPhrase] = useState<string>("Tap the button to get a phrase!");
    const [isLoading, setIsLoading] = useState<boolean>(false);

    // This useEffect hook runs when the component first loads
    // to fetch the initial day count.
    useEffect(() => {
        fetchDayCount(startDate)
            .then(data => setDayCount(data.day_count))
            .catch(err => console.error(err));
    }, [startDate]); // It re-runs if the startDate ever changes.

    const handleNewPhrase = async () => {
        setIsLoading(true);
        try {
            const data = await fetchPhrase();
            setPhrase(data.phrase);
        } catch (error) {
            console.error(error);
            setPhrase('Could not fetch a phrase. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="view" style={{ width: '400px', height: '500px', overflow: 'hidden' }}>
            <div className="day-counter">
            <p>Day</p>
            <h1 id="day-count">{dayCount}</h1>
            </div>
            {/* The style attribute helps maintain a consistent size for the phrase container,
            preventing layout shifts when the phrase content changes. */}
            <div className="phrase-container" style={{ minHeight: '10em', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <p id="phrase-text" style={{ textAlign: 'center' }}>{phrase}</p>
            </div>
            <button id="new-phrase-btn" onClick={handleNewPhrase} disabled={isLoading}>
            {isLoading ? <div className="spinner"></div> : 'New Phrase'}
            </button>
        </div>
    );
}