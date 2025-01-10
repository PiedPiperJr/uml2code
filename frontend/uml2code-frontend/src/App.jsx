import React from 'react';
import AppNavbar from './components/AppNavbar';
import UploadStepper from './components/stepper/UploadStepper';

const App = () => {
    return (
        <div className="min-h-screen bg-gray-50">
            <AppNavbar />
            <UploadStepper />
            {/* Other components go here */}
        </div>
    );
};

export default App;