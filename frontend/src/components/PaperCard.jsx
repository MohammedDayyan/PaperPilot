import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { deletePaper } from '../services/paper';
import { downloadReport } from '../services/report';
import { FileText, ExternalLink, Download, Trash2, Calendar } from 'lucide-react';
import toast from 'react-hot-toast';
import './PaperCard.css';

export default function PaperCard({ paper, onDeleted }) {
  const navigate = useNavigate();
  const [deleting, setDeleting] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await deletePaper(paper.id);
      toast.success('Paper deleted');
      onDeleted?.(paper.id);
    } catch {
      toast.error('Delete failed');
      setDeleting(false);
    }
    setShowConfirm(false);
  };

  const handleDownload = async (e) => {
    e.stopPropagation();
    setDownloading(true);
    try {
      await downloadReport(paper.id, paper.title);
      toast.success('Report downloaded');
    } catch {
      toast.error('Download failed');
    } finally {
      setDownloading(false);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric',
    });
  };

  return (
    <div className={`paper-card glass-card fade-up ${deleting ? 'paper-card-deleting' : ''}`}>
      {/* Icon + Title */}
      <div className="paper-card-header">
        <div className="paper-card-icon">
          <FileText size={20} />
        </div>
        <div className="paper-card-title-wrap">
          <h3 className="paper-card-title">{paper.title}</h3>
          {paper.uploaded_at && (
            <span className="paper-card-date">
              <Calendar size={11} />
              {formatDate(paper.uploaded_at)}
            </span>
          )}
        </div>
      </div>

      <div className="paper-card-divider" />

      {/* Actions */}
      {!showConfirm ? (
        <div className="paper-card-actions">
          <button
            className="btn btn-primary btn-sm paper-card-open"
            onClick={() => navigate(`/paper/${paper.id}`)}
          >
            <ExternalLink size={14} />
            Open
          </button>

          <button
            className="btn btn-ghost btn-sm"
            onClick={handleDownload}
            disabled={downloading}
          >
            {downloading ? <span className="spinner" style={{width:14,height:14}} /> : <Download size={14} />}
            Report
          </button>

          <button
            className="btn btn-danger btn-sm"
            onClick={(e) => { e.stopPropagation(); setShowConfirm(true); }}
          >
            <Trash2 size={14} />
            Delete
          </button>
        </div>
      ) : (
        <div className="paper-card-confirm">
          <p className="paper-card-confirm-text">Delete this paper and all its data?</p>
          <div className="paper-card-confirm-btns">
            <button
              className="btn btn-danger btn-sm"
              onClick={handleDelete}
              disabled={deleting}
            >
              {deleting ? <span className="spinner" style={{width:14,height:14}} /> : <Trash2 size={14} />}
              Yes, delete
            </button>
            <button
              className="btn btn-ghost btn-sm"
              onClick={() => setShowConfirm(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
