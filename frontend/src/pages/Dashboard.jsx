import { useState, useEffect } from 'react';
import { listPapers } from '../services/paper';
import Navbar from '../components/Navbar';
import UploadBox from '../components/UploadBox';
import PaperCard from '../components/PaperCard';
import { FileText, Sparkles, Search, X } from 'lucide-react';
import './Dashboard.css';

export default function Dashboard() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchPapers = async () => {
    setLoading(true);
    try {
      const data = await listPapers();
      setPapers(data || []);
    } catch {
      setPapers([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPapers();
  }, []);

  const handleUploadComplete = () => {
    fetchPapers();
  };

  const handleDeleted = (paperId) => {
    setPapers((prev) => prev.filter((p) => p.id !== paperId));
  };

  return (
    <div className="app-layout">
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <Navbar />

      <main className="page-content">
        {/* Hero */}
        <div className="dashboard-hero fade-up">
          <div className="dashboard-hero-badge badge badge-accent">
            <Sparkles size={12} />
            Multi-Agent AI
          </div>
          <h1 className="dashboard-hero-title">
            Research Intelligence,<br />
            <span className="gradient-text">Instantly Unlocked</span>
          </h1>
          <p className="dashboard-hero-subtitle">
            Upload any academic PDF and get a professional report, quiz, flashcards, and AI tutor — in seconds.
          </p>
        </div>

        {/* Upload */}
        <section className="dashboard-upload glass-card">
          <div className="dashboard-section-label">
            <FileText size={15} />
            New Paper
          </div>
          <UploadBox onUploadComplete={handleUploadComplete} />
        </section>

        {/* Papers grid */}
        <section className="dashboard-papers">
          {(() => {
            const filteredPapers = papers.filter((paper) =>
              (paper.title || '').toLowerCase().includes(searchQuery.toLowerCase())
            );
            return (
              <>
                <div className="dashboard-papers-header">
                  <div>
                    <h2 className="section-title">Your Papers</h2>
                    <p className="section-subtitle">
                      {searchQuery
                        ? `${filteredPapers.length} of ${papers.length} paper${papers.length !== 1 ? 's' : ''} found`
                        : `${papers.length} paper${papers.length !== 1 ? 's' : ''} analyzed`}
                    </p>
                  </div>
                  {papers.length > 0 && (
                    <div className="dashboard-search-container">
                      <Search size={16} className="search-icon" />
                      <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search papers by title..."
                        className="dashboard-search-input"
                      />
                      {searchQuery && (
                        <button className="search-clear-btn" onClick={() => setSearchQuery('')}>
                          <X size={14} />
                        </button>
                      )}
                    </div>
                  )}
                </div>

                {loading ? (
                  <div className="grid-auto">
                    {[1, 2, 3].map((i) => (
                      <div key={i} className="paper-skeleton glass-card">
                        <div className="skeleton" style={{ height: 44, width: 44, borderRadius: 8 }} />
                        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 8 }}>
                          <div className="skeleton" style={{ height: 14, width: '70%' }} />
                          <div className="skeleton" style={{ height: 12, width: '40%' }} />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : papers.length === 0 ? (
                  <div className="empty-state glass-card">
                    <div className="empty-state-icon">
                      <FileText size={28} color="var(--text-muted)" />
                    </div>
                    <h3 style={{ fontSize: 16, fontWeight: 600, color: 'var(--text-primary)' }}>
                      No papers yet
                    </h3>
                    <p style={{ fontSize: 14 }}>Upload your first PDF above to get started</p>
                  </div>
                ) : filteredPapers.length === 0 ? (
                  <div className="empty-state glass-card">
                    <div className="empty-state-icon">
                      <Search size={28} color="var(--text-muted)" />
                    </div>
                    <h3 style={{ fontSize: 16, fontWeight: 600, color: 'var(--text-primary)' }}>
                      No results found
                    </h3>
                    <p style={{ fontSize: 14 }}>Try adjusting your search query</p>
                  </div>
                ) : (
                  <div className="grid-auto">
                    {filteredPapers.map((paper) => (
                      <PaperCard
                        key={paper.id}
                        paper={paper}
                        onDeleted={handleDeleted}
                      />
                    ))}
                  </div>
                )}
              </>
            );
          })()}
        </section>
      </main>
    </div>
  );
}
