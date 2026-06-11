import { useState, useRef, useCallback } from 'react';
import { uploadPaper } from '../services/paper';
import { Upload, FileText, CheckCircle, AlertCircle, X } from 'lucide-react';
import toast from 'react-hot-toast';
import './UploadBox.css';

export default function UploadBox({ onUploadComplete }) {
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('idle'); // idle | uploading | processing | done | error
  const inputRef = useRef(null);

  const handleFile = useCallback((f) => {
    if (!f || !f.name.endsWith('.pdf')) {
      toast.error('Only PDF files are supported');
      return;
    }
    if (f.size > 20 * 1024 * 1024) {
      toast.error('File size must be under 20 MB');
      return;
    }
    setFile(f);
    setStatus('idle');
  }, []);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    handleFile(f);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setUploading(true);
    setStatus('uploading');
    setProgress(0);

    try {
      const result = await uploadPaper(file, (evt) => {
        const pct = Math.round((evt.loaded * 100) / evt.total);
        setProgress(pct);
        if (pct === 100) setStatus('processing');
      });

      setStatus('done');
      toast.success(`"${result.title}" processed successfully!`);
      onUploadComplete?.(result);
      setTimeout(() => {
        setFile(null);
        setStatus('idle');
        setProgress(0);
      }, 2000);
    } catch (err) {
      setStatus('error');
      toast.error(err?.response?.data?.detail || 'Upload failed. Try again.');
    } finally {
      setUploading(false);
    }
  };

  const statusMessages = {
    uploading: `Uploading… ${progress}%`,
    processing: 'AI agents processing your paper…',
    done: 'Done! Report ready.',
    error: 'Something went wrong.',
  };

  return (
    <div className="upload-section">
      <div
        className={`upload-box ${dragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => !file && inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          className="upload-input-hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />

        {!file ? (
          <div className="upload-idle">
            <div className="upload-icon-wrap">
              <Upload size={28} />
            </div>
            <p className="upload-title">Drop your PDF here</p>
            <p className="upload-hint">or click to browse · max 20 MB</p>
          </div>
        ) : (
          <div className="upload-file-info">
            <div className="upload-file-icon">
              {status === 'done' ? <CheckCircle size={24} color="var(--success)" /> :
               status === 'error' ? <AlertCircle size={24} color="var(--error)" /> :
               <FileText size={24} color="var(--accent-bright)" />}
            </div>
            <div className="upload-file-meta">
              <span className="upload-filename">{file.name}</span>
              <span className="upload-filesize">
                {status !== 'idle' ? statusMessages[status] : `${(file.size / 1024 / 1024).toFixed(2)} MB`}
              </span>
            </div>
            {!uploading && status === 'idle' && (
              <button
                className="btn btn-icon btn-ghost upload-remove"
                onClick={(e) => { e.stopPropagation(); setFile(null); }}
              >
                <X size={16} />
              </button>
            )}
          </div>
        )}
      </div>

      {(status === 'uploading' || status === 'processing') && (
        <div className="upload-progress-bar">
          <div
            className="upload-progress-fill"
            style={{ width: `${status === 'processing' ? 100 : progress}%` }}
          />
        </div>
      )}

      {file && status === 'idle' && (
        <button className="btn btn-primary btn-lg upload-submit" onClick={handleSubmit}>
          <Upload size={18} />
          Analyze Paper
        </button>
      )}
    </div>
  );
}
