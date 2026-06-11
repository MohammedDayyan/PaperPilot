import { Link, useNavigate, useLocation } from 'react-router-dom';
import { logout, getStoredUser } from '../services/auth';
import { BookOpen, LogOut, LayoutDashboard } from 'lucide-react';
import './Navbar.css';

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const user = getStoredUser();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/dashboard" className="navbar-brand">
          <div className="brand-icon">
            <BookOpen size={18} />
          </div>
          <span className="brand-name">PaperPilot<span className="brand-ai"> AI</span></span>
        </Link>

        <div className="navbar-right">
          {user && (
            <span className="navbar-email">{user.email}</span>
          )}
          <Link
            to="/dashboard"
            className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}
          >
            <LayoutDashboard size={16} />
            Dashboard
          </Link>
          <button className="btn btn-ghost btn-sm" onClick={handleLogout}>
            <LogOut size={15} />
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
