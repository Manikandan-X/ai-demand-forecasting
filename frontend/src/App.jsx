import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Login             from "./pages/Login";
import Register          from "./pages/Register";
import Dashboard         from "./pages/Dashboard";
import UploadDataset     from "./pages/UploadDataset";
import Forecast          from "./pages/Forecast";
import Reports           from "./pages/Reports";
import ForecastHistory   from "./pages/ForecastHistory";
import AdminDashboard    from "./pages/AdminDashboard";

// ── New pages (Phase 1D + Enterprise) ─────
import EnterpriseIntegrations from "./pages/EnterpriseIntegrations";
import AIInsightsPage         from "./pages/AIInsights";
import ForecastIntelligence from "./pages/ForecastIntelligence";

import ProtectedRoute    from "./routes/ProtectedRoute";
import ThemeProvider     from "./context/ThemeProvider";
import { ToastProvider } from "./components/ui/Toast";

function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <BrowserRouter>
          <Routes>

            <Route path="/"        element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route path="/dashboard" element={
              <ProtectedRoute><Dashboard /></ProtectedRoute>
            } />

            <Route path="/upload" element={
              <ProtectedRoute><UploadDataset /></ProtectedRoute>
            } />

            <Route path="/forecast" element={
              <ProtectedRoute><Forecast /></ProtectedRoute>
            } />

            <Route path="/forecast-history" element={
              <ProtectedRoute><ForecastHistory /></ProtectedRoute>
            } />

            <Route path="/reports" element={
              <ProtectedRoute><Reports /></ProtectedRoute>
            } />

            <Route path="/admin" element={
              <ProtectedRoute adminOnly={true}>
                <AdminDashboard />
              </ProtectedRoute>
            } />

            {/* ── New routes ──────────────── */}
            <Route path="/enterprise-integrations" element={
              <ProtectedRoute adminOnly={true}>
                <EnterpriseIntegrations />
              </ProtectedRoute>
            } />

            <Route path="/ai-insights" element={
              <ProtectedRoute>
                <AIInsightsPage />
              </ProtectedRoute>
            } />

            <Route path="/forecast-intelligence" element={
              <ProtectedRoute>
                <ForecastIntelligence />
                </ProtectedRoute>
            } />

          </Routes>
        </BrowserRouter>
      </ToastProvider>
    </ThemeProvider>
  );
}

export default App;
