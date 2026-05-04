import { assign, setup } from 'xstate';

/**
 * Research Hub Session Management State Machine
 * XState v5 implementation for managing research session lifecycle
 * Supports multi-turn research with concurrent source discovery and synthesis
 */

// ============================================================================
// TYPES
// ============================================================================

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
}

export interface ResearchContext {
  session: Session | null;
  turns: Turn[];
  sources: Source[];
  cost: number;
  confidence: number;
  error: string | null;
  startTime?: Date;
}

// ============================================================================
// EVENTS
// ============================================================================

export type ResearchEvent =
  | { type: 'START'; query: string; mode: 'quick' | 'deep' | 'full' }
  | { type: 'SOURCE_FOUND'; source: Source }
  | { type: 'TURN_COMPLETE'; turn: Omit<Turn, 'completedAt'> }
  | { type: 'PAUSE' }
  | { type: 'RESUME' }
  | { type: 'CANCEL' }
  | { type: 'ERROR'; message: string }
  | { type: 'RETRY' }
  | { type: 'COMPLETE' };

// ============================================================================
// STATE MACHINE DEFINITION (XState v5)
// ============================================================================

const initialContext: ResearchContext = {
  session: null,
  turns: [],
  sources: [],
  cost: 0,
  confidence: 0,
  error: null,
  startTime: undefined,
};

export const researchMachine = setup({
  types: {
    context: {} as ResearchContext,
    events: {} as ResearchEvent,
  },
  actions: {
    initializeSession: assign({
      session: ({ event }) => {
        if (event.type !== 'START') return null;
        return {
          id: crypto.randomUUID(),
          query: event.query,
          mode: event.mode,
          status: 'searching' as const,
          createdAt: new Date(),
        };
      },
      turns: () => [],
      sources: () => [],
      cost: () => 0,
      confidence: () => 0,
      error: () => null,
      startTime: () => new Date(),
    }),
    resetSession: assign({
      session: ({ event }) => {
        if (event.type !== 'START') return null;
        return {
          id: crypto.randomUUID(),
          query: event.query,
          mode: event.mode,
          status: 'searching' as const,
          createdAt: new Date(),
        };
      },
      turns: () => [],
      sources: () => [],
      cost: () => 0,
      confidence: () => 0,
      error: () => null,
      startTime: () => new Date(),
    }),
    addSource: assign({
      sources: ({ context, event }) => {
        if (event.type !== 'SOURCE_FOUND') return context.sources;
        const exists = context.sources.some(s => s.id === event.source.id);
        return exists ? context.sources : [...context.sources, event.source];
      },
    }),
    completeTurn: assign({
      turns: ({ context, event }) => {
        if (event.type !== 'TURN_COMPLETE') return context.turns;
        return [
          ...context.turns,
          {
            ...event.turn,
            completedAt: new Date(),
          },
        ];
      },
      cost: ({ context, event }) => {
        if (event.type !== 'TURN_COMPLETE') return context.cost;
        return context.cost + event.turn.cost;
      },
      confidence: ({ event }) => {
        if (event.type !== 'TURN_COMPLETE') return 0;
        return event.turn.confidence;
      },
    }),
    setError: assign({
      error: ({ event }) => {
        if (event.type !== 'ERROR') return null;
        return event.message;
      },
    }),
    clearError: assign({
      error: () => null,
    }),
    pauseSession: assign({
      session: ({ context }) => {
        if (!context.session) return null;
        return {
          ...context.session,
          status: 'paused' as const,
          pausedAt: new Date(),
        };
      },
    }),
    resumeSession: assign({
      session: ({ context }) => {
        if (!context.session) return null;
        return {
          ...context.session,
          status: 'searching' as const,
          pausedAt: undefined,
        };
      },
    }),
    completeSession: assign({
      session: ({ context }) => {
        if (!context.session) return null;
        return {
          ...context.session,
          status: 'complete' as const,
          completedAt: new Date(),
        };
      },
    }),
  },
}).createMachine({
  id: 'research',
  initial: 'idle',
  context: initialContext,
  states: {
    idle: {
      description: 'Waiting for user to initiate a research session',
      on: {
        START: {
          target: 'searching',
          actions: 'initializeSession',
        },
      },
    },

    searching: {
      description: 'Running distributed search across multiple sources (Brave, Firecrawl, Valyu)',
      on: {
        SOURCE_FOUND: {
          actions: 'addSource',
        },
        TURN_COMPLETE: {
          target: 'extracting',
          actions: 'completeTurn',
        },
        PAUSE: {
          target: 'paused',
          actions: 'pauseSession',
        },
        CANCEL: {
          target: 'idle',
        },
        ERROR: {
          target: 'error',
          actions: 'setError',
        },
      },
    },

    extracting: {
      description: 'Scraping and extracting content from discovered sources',
      on: {
        SOURCE_FOUND: {
          actions: 'addSource',
        },
        TURN_COMPLETE: {
          target: 'synthesizing',
          actions: 'completeTurn',
        },
        PAUSE: {
          target: 'paused',
          actions: 'pauseSession',
        },
        CANCEL: {
          target: 'idle',
        },
        ERROR: {
          target: 'error',
          actions: 'setError',
        },
      },
    },

    synthesizing: {
      description: 'AI synthesis and analysis of extracted content',
      on: {
        TURN_COMPLETE: {
          actions: 'completeTurn',
        },
        COMPLETE: {
          target: 'complete',
          actions: 'completeSession',
        },
        PAUSE: {
          target: 'paused',
          actions: 'pauseSession',
        },
        CANCEL: {
          target: 'idle',
        },
        ERROR: {
          target: 'error',
          actions: 'setError',
        },
      },
    },

    paused: {
      description: 'Session paused pending user intervention',
      on: {
        RESUME: {
          target: 'searching',
          actions: 'resumeSession',
        },
        CANCEL: {
          target: 'idle',
        },
      },
    },

    complete: {
      description: 'Research session completed with results ready',
      on: {
        START: {
          target: 'searching',
          actions: 'resetSession',
        },
      },
    },

    error: {
      description: 'Recoverable error occurred during research',
      on: {
        RETRY: {
          target: 'searching',
          actions: 'clearError',
        },
        START: {
          target: 'searching',
          actions: 'resetSession',
        },
        CANCEL: {
          target: 'idle',
        },
      },
    },
  },
});

// ============================================================================
// TYPE EXPORTS FOR XSTATE INTEGRATION
// ============================================================================

export type ResearchMachine = typeof researchMachine;

/**
 * Type-safe event sender for use in Solid.js components
 * Example: send({ type: 'START', query: 'AI agents', mode: 'deep' })
 */
export type ResearchSend = (event: ResearchEvent) => void;

/**
 * Type-safe snapshot for use in Solid.js components with Solid.js actor integration
 * Example: snapshot().value = 'searching', snapshot().context.cost = 0.42
 */
export interface ResearchSnapshot {
  value: 'idle' | 'searching' | 'extracting' | 'synthesizing' | 'paused' | 'complete' | 'error';
  context: ResearchContext;
  matches: (state: string) => boolean;
}
