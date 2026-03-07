import { Valyu } from 'valyu-js';
interface ResearchOptions {
    query: string;
    maxTurns: number;
    confidenceThreshold: number;
    strategy: 'breadth' | 'depth' | 'balanced';
    outputDir: string;
}
interface ResearchResult {
    totalTurns: number;
    finalConfidence: number;
    totalCost: number;
    synthesis: string;
    keySources: Array<{
        title: string;
        url: string;
        citations: number;
    }>;
    turns: Array<TurnResult>;
}
interface TurnResult {
    turn: number;
    query: string;
    confidence: number;
    findings: string;
    sources: number;
    cost: number;
    refinementReason?: string;
}
export declare function recursiveResearch(client: Valyu, options: ResearchOptions): Promise<ResearchResult>;
export {};
