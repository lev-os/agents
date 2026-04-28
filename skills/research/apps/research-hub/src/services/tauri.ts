import { invoke } from '@tauri-apps/api/core';
import { listen, UnlistenFn } from '@tauri-apps/api/event';

// Types matching Rust backend
export interface Source {
  id: string;
  url: string;
  title: string;
  type: 'web' | 'academic' | 'social' | 'news';
  relevance: number;
  snippet?: string;
  discoveredAt: Date;
}

export interface Turn {
  number: number;
  query: string;
  confidence: number;
  sourcesCount: number;
  cost: number;
  duration: number;
  completedAt: Date;
}

export interface Session {
  id: string;
  query: string;
  mode: 'quick' | 'deep' | 'full';
  status: 'idle' | 'searching' | 'extracting' | 'synthesizing' | 'complete' | 'paused' | 'error';
  createdAt: Date;
  pausedAt?: Date;
  completedAt?: Date;
  turns: Turn[];
  sources: Source[];
  cost: number;
  confidence: number;
}

export interface ProgressPayload {
  sessionId: string;
  turn: number;
  maxTurns: number;
  confidence: number;
  sources: number;
  cost: number;
  duration: number;
  status: string;
}

export interface SourcePayload {
  sessionId: string;
  source: Source;
}

export interface ResultPayload {
  sessionId: string;
  session: Session;
}

// Tauri Commands
export async function searchStart(query: string, mode: 'quick' | 'deep'): Promise<string> {
  return await invoke<string>('search_start', { query, mode });
}

export async function searchPause(sessionId: string): Promise<void> {
  await invoke('search_pause', { sessionId });
}

export async function searchResume(sessionId: string): Promise<void> {
  await invoke('search_resume', { sessionId });
}

export async function sessionList(): Promise<Session[]> {
  return await invoke<Session[]>('session_list');
}

export async function sessionGet(sessionId: string): Promise<Session> {
  return await invoke<Session>('session_get', { sessionId });
}

// Event Listeners
export function listenToProgress(
  callback: (payload: ProgressPayload) => void
): Promise<UnlistenFn> {
  return listen<ProgressPayload>('research:progress', (event) => {
    callback(event.payload);
  });
}

export function listenToSourceFound(
  callback: (payload: SourcePayload) => void
): Promise<UnlistenFn> {
  return listen<SourcePayload>('research:source_found', (event) => {
    callback(event.payload);
  });
}

export function listenToComplete(
  callback: (payload: ResultPayload) => void
): Promise<UnlistenFn> {
  return listen<ResultPayload>('research:complete', (event) => {
    callback(event.payload);
  });
}
