from services.supabase_service import get_client

PAPERS_BUCKET = "papers"
REPORTS_BUCKET = "reports"


def upload_file(
    bucket: str,
    path: str,
    file_bytes: bytes,
    content_type: str = "application/pdf",
) -> str:
    """Upload bytes to a Supabase Storage bucket. Returns the public URL."""
    client = get_client()
    client.storage.from_(bucket).upload(
        path,
        file_bytes,
        file_options={"content-type": content_type, "upsert": "true"},
    )
    return client.storage.from_(bucket).get_public_url(path)


def download_file(bucket: str, path: str) -> bytes:
    """Download a file from Supabase Storage and return its bytes."""
    client = get_client()
    return client.storage.from_(bucket).download(path)


def delete_file(bucket: str, path: str) -> None:
    """Remove a file from Supabase Storage. Silently ignores missing files."""
    try:
        get_client().storage.from_(bucket).remove([path])
    except Exception:
        pass
