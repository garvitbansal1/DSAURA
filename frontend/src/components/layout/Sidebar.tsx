import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Link2, Network, Brain, BookOpen,
  Sparkles, ClipboardCheck, AlertTriangle, RotateCcw,
  TrendingUp, Settings, ChevronLeft, ChevronRight, LogOut,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { useUIStore } from '../../store/uiStore';
import { cn } from '../../utils/cn';

const NAV_ITEMS = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Overview' },
  { to: '/profiles', icon: Link2, label: 'My Profiles' },
  { to: '/knowledge-map', icon: Network, label: 'Knowledge Map' },
  { to: '/topics', icon: Brain, label: 'Topic Intelligence' },
  { to: '/patterns', icon: BookOpen, label: 'Pattern Library' },
  { to: '/recommendations', icon: Sparkles, label: 'Recommendations' },
  { to: '/assessment', icon: ClipboardCheck, label: 'Assessment' },
  { to: '/reality-check', icon: AlertTriangle, label: 'Reality Check' },
  { to: '/revision', icon: RotateCcw, label: 'Revision Center' },
  { to: '/journey', icon: TrendingUp, label: 'Journey History' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export function Sidebar() {
  const collapsed = useUIStore((s) => s.sidebarCollapsed);
  const toggleSidebar = useUIStore((s) => s.toggleSidebar);
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const user = useAuthStore((s) => s.user);
  const navigate = useNavigate();

  const handleLogout = () => {
    clearAuth();
    navigate('/');
  };

  return (
    <aside
      className={cn(
        'flex flex-col bg-[#0d0d1f] border-r border-[#2a2a4a] transition-all duration-300 relative',
        collapsed ? 'w-16' : 'w-60'
      )}
    >
      {/* Logo */}
      <div className={cn('flex items-center gap-3 px-4 py-5 border-b border-[#2a2a4a]', collapsed && 'justify-center')}>
        <div className="w-8 h-8 bg-gradient-to-br from-[#6272f1] to-[#4044cb] rounded-lg flex items-center justify-center flex-shrink-0">
          <span className="text-white font-bold text-sm">D</span>
        </div>
        {!collapsed && (
          <div>
            <div className="text-white font-bold text-lg leading-none">DSAURA</div>
            <div className="text-[#6272f1] text-[10px] font-medium tracking-wider mt-0.5">DSA INTELLIGENCE</div>
          </div>
        )}
      </div>

      {/* Nav Links */}
      <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-0.5">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all',
                isActive
                  ? 'text-white bg-[#6272f1]/20 border border-[#6272f1]/30'
                  : 'text-gray-400 hover:text-white hover:bg-[#1a1a2e]',
                collapsed && 'justify-center'
              )
            }
            title={collapsed ? label : undefined}
          >
            <Icon className="w-4 h-4 flex-shrink-0" />
            {!collapsed && <span>{label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* User + Logout */}
      {!collapsed && (
        <div className="p-3 border-t border-[#2a2a4a]">
          <div className="flex items-center gap-2 px-2 py-2 mb-1">
            <div className="w-7 h-7 rounded-full bg-[#6272f1]/30 flex items-center justify-center text-xs font-bold text-[#6272f1] flex-shrink-0">
              {user?.name?.[0]?.toUpperCase() || 'U'}
            </div>
            <div className="min-w-0">
              <div className="text-white text-xs font-medium truncate">{user?.name || 'User'}</div>
              <div className="text-gray-500 text-[10px] truncate">{user?.email}</div>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/5 text-xs font-medium transition-colors"
          >
            <LogOut className="w-3.5 h-3.5" />
            Sign out
          </button>
        </div>
      )}

      {/* Collapse toggle */}
      <button
        onClick={toggleSidebar}
        className="absolute -right-3 top-20 w-6 h-6 bg-[#1a1a2e] border border-[#2a2a4a] rounded-full flex items-center justify-center hover:bg-[#252540] transition-colors z-10"
      >
        {collapsed ? <ChevronRight className="w-3 h-3 text-gray-400" /> : <ChevronLeft className="w-3 h-3 text-gray-400" />}
      </button>
    </aside>
  );
}
