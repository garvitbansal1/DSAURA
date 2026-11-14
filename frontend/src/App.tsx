import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import { AppShell } from './components/layout/AppShell';
import { Landing } from './pages/Landing';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Profiles } from './pages/Profiles';
import { KnowledgeMap } from './pages/KnowledgeMap';
import { TopicIntelligence } from './pages/TopicIntelligence';
import { PatternLibrary } from './pages/PatternLibrary';
import { Recommendations } from './pages/Recommendations';
import { Assessment } from './pages/Assessment';
import { RealityCheck } from './pages/RealityCheck';
import { RevisionCenter } from './pages/RevisionCenter';
import { Journey } from './pages/Journey';
import { Settings } from './pages/Settings';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected routes inside AppShell */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <AppShell>
              <Dashboard />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/profiles"
        element={
          <ProtectedRoute>
            <AppShell>
              <Profiles />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/knowledge-map"
        element={
          <ProtectedRoute>
            <AppShell>
              <KnowledgeMap />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/topics"
        element={
          <ProtectedRoute>
            <AppShell>
              <TopicIntelligence />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/patterns"
        element={
          <ProtectedRoute>
            <AppShell>
              <PatternLibrary />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/recommendations"
        element={
          <ProtectedRoute>
            <AppShell>
              <Recommendations />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assessment"
        element={
          <ProtectedRoute>
            <AppShell>
              <Assessment />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/reality-check"
        element={
          <ProtectedRoute>
            <AppShell>
              <RealityCheck />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/revision"
        element={
          <ProtectedRoute>
            <AppShell>
              <RevisionCenter />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/journey"
        element={
          <ProtectedRoute>
            <AppShell>
              <Journey />
            </AppShell>
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <AppShell>
              <Settings />
            </AppShell>
          </ProtectedRoute>
        }
      />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
