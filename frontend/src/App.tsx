import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import LandingPage from './pages/LandingPage';
import GoalInputPage from './pages/GoalInputPage';
import HollandTestPage from './pages/HollandTestPage';
import MbtiTestPage from './pages/MbtiTestPage';
import AdditionalInfoPage from './pages/AdditionalInfoPage';
import ResultDashboard from './pages/ResultDashboard';
import { StudentProfile } from './types';

function App() {
  const [profile, setProfile] = useState<Partial<StudentProfile>>({});

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route
          path="/assessment/goal"
          element={<GoalInputPage profile={profile} setProfile={setProfile} />}
        />
        <Route
          path="/assessment/holland"
          element={<HollandTestPage profile={profile} setProfile={setProfile} />}
        />
        <Route
          path="/assessment/mbti"
          element={<MbtiTestPage profile={profile} setProfile={setProfile} />}
        />
        <Route
          path="/assessment/info"
          element={<AdditionalInfoPage profile={profile} setProfile={setProfile} />}
        />
        <Route
          path="/result"
          element={<ResultDashboard profile={profile as StudentProfile} />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
