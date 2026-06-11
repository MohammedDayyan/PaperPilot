-- =============================================================================
-- PaperPilot-AI — Supabase Schema Setup
-- Run this in your Supabase project's SQL Editor (once)
-- =============================================================================

-- ── Profiles ──────────────────────────────────────────────────────────────────
create table if not exists profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text unique,
  created_at timestamp with time zone default now()
);

-- Auto-populate profile on new user signup
create or replace function handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email)
  values (new.id, new.email)
  on conflict (id) do nothing;
  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function handle_new_user();

-- ── Papers ────────────────────────────────────────────────────────────────────
create table if not exists papers (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade,
  title text not null,
  file_url text,
  uploaded_at timestamp with time zone default now()
);

-- ── Reports ───────────────────────────────────────────────────────────────────
create table if not exists reports (
  id uuid primary key default gen_random_uuid(),
  paper_id uuid references papers(id) on delete cascade,
  report_text text,
  pdf_url text
);

-- ── Quizzes (Phase 2) ─────────────────────────────────────────────────────────
create table if not exists quizzes (
  id uuid primary key default gen_random_uuid(),
  paper_id uuid references papers(id) on delete cascade,
  quiz jsonb
);

-- ── Flashcards (Phase 2) ──────────────────────────────────────────────────────
create table if not exists flashcards (
  id uuid primary key default gen_random_uuid(),
  paper_id uuid references papers(id) on delete cascade,
  cards jsonb
);

-- ── Study Advice (Phase 2) ────────────────────────────────────────────────────
create table if not exists study_advice (
  id uuid primary key default gen_random_uuid(),
  paper_id uuid references papers(id) on delete cascade,
  advice text
);

-- ── Chat History (Phase 3) ────────────────────────────────────────────────────
create table if not exists chat_history (
  id uuid primary key default gen_random_uuid(),
  paper_id uuid references papers(id) on delete cascade,
  question text,
  answer text,
  created_at timestamp with time zone default now()
);

-- ── Row Level Security ────────────────────────────────────────────────────────
-- Enable RLS on all tables
alter table profiles enable row level security;
alter table papers enable row level security;
alter table reports enable row level security;
alter table quizzes enable row level security;
alter table flashcards enable row level security;
alter table study_advice enable row level security;
alter table chat_history enable row level security;

-- Policies: users can only see their own data
drop policy if exists "Users can view own profile" on profiles;
create policy "Users can view own profile"
  on profiles for select using (auth.uid() = id);

drop policy if exists "Users can manage own papers" on papers;
create policy "Users can manage own papers"
  on papers for all using (auth.uid() = user_id);

drop policy if exists "Users can view reports for own papers" on reports;
create policy "Users can view reports for own papers"
  on reports for all using (
    exists (select 1 from papers where papers.id = reports.paper_id and papers.user_id = auth.uid())
  );

drop policy if exists "Users can view quizzes for own papers" on quizzes;
create policy "Users can view quizzes for own papers"
  on quizzes for all using (
    exists (select 1 from papers where papers.id = quizzes.paper_id and papers.user_id = auth.uid())
  );

drop policy if exists "Users can view flashcards for own papers" on flashcards;
create policy "Users can view flashcards for own papers"
  on flashcards for all using (
    exists (select 1 from papers where papers.id = flashcards.paper_id and papers.user_id = auth.uid())
  );

drop policy if exists "Users can view study_advice for own papers" on study_advice;
create policy "Users can view study_advice for own papers"
  on study_advice for all using (
    exists (select 1 from papers where papers.id = study_advice.paper_id and papers.user_id = auth.uid())
  );

drop policy if exists "Users can view chat_history for own papers" on chat_history;
create policy "Users can view chat_history for own papers"
  on chat_history for all using (
    exists (select 1 from papers where papers.id = chat_history.paper_id and papers.user_id = auth.uid())
  );

-- ── Storage Buckets ───────────────────────────────────────────────────────────
-- Run these separately if buckets don't exist:
-- insert into storage.buckets (id, name, public) values ('papers', 'papers', true);
-- insert into storage.buckets (id, name, public) values ('reports', 'reports', true);
