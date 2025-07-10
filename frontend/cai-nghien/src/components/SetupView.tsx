import { useState } from 'react';

// Define the props this component accepts using a TypeScript interface.
interface SetupViewProps {
    onSave: (date: string) => void;
}

export function SetupView({ onSave }: SetupViewProps) {
    const [selectedDate, setSelectedDate] = useState<string>('');

    const handleSave = () => {
        if (selectedDate) {
            onSave(selectedDate);
        }
    };

    return (
        <div className="view">
            <h1>Welcome!</h1>
            <p>When did you start your journey?</p>
            <input 
                type="date" 
                id="start-date-input"
                onChange={(e) => setSelectedDate(e.target.value)}
            />
            <button id="save-btn" onClick={handleSave}>Save and Begin</button>
        </div>
    );
}