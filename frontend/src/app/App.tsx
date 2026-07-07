import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import DashboardPage from '../pages/dashboard/ui/DashboardPage';
import NotFoundPage from '../pages/not-found/ui/NotFoundPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;
