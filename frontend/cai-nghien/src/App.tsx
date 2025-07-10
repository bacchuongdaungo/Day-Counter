import { useState, useEffect } from 'react';
import { SetupView } from './components/SetupView';
import { MainView } from './components/MainView';

function App() {
    const [startDate, setStartDate] = useState<string | null>(null);

    // On initial app load, check localStorage for a saved date.
    useEffect(() => {
        const savedDate = localStorage.getItem('userStartDate');
        if (savedDate) {
            setStartDate(savedDate);
        }
    }, []);

    const handleSaveDate = (date: string) => {
        localStorage.setItem('userStartDate', date);
        setStartDate(date);
    };

    return (
        <div className="container">
            {startDate ? <MainView startDate={startDate} /> : <SetupView onSave={handleSaveDate} />}
        </div>
    );
}

export default App;