#!/usr/bin/env node

import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const usage = () => {
  console.error('Usage: valyu-research.mjs --query "<query>" [--turns 5] [--threshold 0.85] [--output ./valyu-research] [--strategy breadth|depth|balanced]');
  process.exit(2);
};

const args = process.argv.slice(2);
const options = {
  query: '',
  turns: 5,
  threshold: 0.85,
  output: './valyu-research',
  strategy: 'balanced',
};

for (let index = 0; index < args.length; index += 1) {
  const arg = args[index];
  switch (arg) {
    case '--query':
      options.query = args[++index] ?? '';
      break;
    case '--turns':
      options.turns = Number.parseInt(args[++index] ?? '5', 10);
      break;
    case '--threshold':
      options.threshold = Number.parseFloat(args[++index] ?? '0.85');
      break;
    case '--output':
      options.output = args[++index] ?? './valyu-research';
      break;
    case '--strategy':
      options.strategy = args[++index] ?? 'balanced';
      break;
    default:
      usage();
  }
}

if (!options.query) {
  usage();
}

if (!process.env.VALYU_API_KEY) {
  console.error('Error: VALYU_API_KEY not set');
  process.exit(1);
}

const apiPost = async (endpoint, body) => {
  const response = await fetch(`https://api.valyu.ai/v1/${endpoint}`, {
    method: 'POST',
    headers: {
      'x-api-key': process.env.VALYU_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const message = await response.text().catch(() => '');
    throw new Error(`Valyu ${endpoint} failed (${response.status}): ${message}`);
  }

  return response.json();
};

const search = async (query) => {
  const maxNumResults =
    options.strategy === 'breadth' ? 20 :
      options.strategy === 'depth' ? 10 : 15;

  return apiPost('search', {
    query,
    max_num_results: maxNumResults,
    search_type: 'all',
  });
};

const answer = async (query, systemInstructions) => apiPost('answer', {
  query,
  system_instructions: systemInstructions,
  streaming: false,
});

const parseTurnResponse = (text, fallback) => {
  const confidenceMatch = text.match(/CONFIDENCE:\s*([\d.]+)/);
  const nextQueryMatch = text.match(/NEXT_QUERY:\s*(.+?)(?:\n|$)/);
  const findingsMatch = text.match(/FINDINGS:\s*(.+?)(?=CONFIDENCE:|$)/s);

  return {
    confidence: confidenceMatch ? Number.parseFloat(confidenceMatch[1]) : 0.7,
    nextQuery: nextQueryMatch ? nextQueryMatch[1].trim() : null,
    findings: findingsMatch ? findingsMatch[1].trim() : fallback,
  };
};

mkdirSync(options.output, { recursive: true });

let currentQuery = options.query;
let totalCost = 0;
let currentConfidence = 0;
const turns = [];
const allSources = new Map();

for (let turn = 1; turn <= options.turns; turn += 1) {
  const searchResult = await search(currentQuery);
  const answerResult = await answer(
    currentQuery,
    `You are conducting turn ${turn} of ${options.turns} in a recursive research process.

Previous context: ${turns.length > 0 ? turns[turns.length - 1].findings : 'None'}

Provide:
1. Key findings from current search
2. Confidence level (0.0-1.0) in answer completeness
3. Suggested next research direction (if confidence < ${options.threshold})

Format:
FINDINGS: [detailed findings]
CONFIDENCE: [0.0-1.0]
NEXT_QUERY: [refined query for next turn, or "COMPLETE" if done]`
  );

  const answerText = typeof answerResult.contents === 'string' ?
    answerResult.contents :
    JSON.stringify(answerResult.contents, null, 2);

  const parsed = parseTurnResponse(answerText, answerText);
  currentConfidence = parsed.confidence;
  totalCost += Number(searchResult.total_deduction_dollars ?? 0);
  totalCost += Number(answerResult.cost?.total_deduction_dollars ?? 0);

  for (const source of searchResult.results ?? []) {
    if (!source.url) {
      continue;
    }
    const count = allSources.get(source.url)?.count ?? 0;
    allSources.set(source.url, {
      title: source.title,
      url: source.url,
      count: count + 1,
    });
  }

  const turnResult = {
    turn,
    query: currentQuery,
    confidence: currentConfidence,
    findings: parsed.findings,
    sources: (searchResult.results ?? []).length,
    cost:
      Number(searchResult.total_deduction_dollars ?? 0) +
      Number(answerResult.cost?.total_deduction_dollars ?? 0),
    refinementReason:
      parsed.nextQuery && parsed.nextQuery !== 'COMPLETE' ?
        `Confidence ${(currentConfidence * 100).toFixed(0)}% < ${(options.threshold * 100).toFixed(0)}%` :
        undefined,
  };

  turns.push(turnResult);
  writeFileSync(join(options.output, `turn-${turn}.json`), JSON.stringify({
    turnResult,
    searchResult,
    answerResult,
  }, null, 2));

  if (currentConfidence >= options.threshold || !parsed.nextQuery || parsed.nextQuery === 'COMPLETE') {
    break;
  }

  currentQuery = parsed.nextQuery;
}

const synthesisPrompt = `Based on ${turns.length} research turns on "${options.query}", provide a comprehensive final synthesis.

Turn summaries:
${turns.map((turn) => `Turn ${turn.turn} (${(turn.confidence * 100).toFixed(0)}% confidence): ${turn.findings.slice(0, 200)}...`).join('\n\n')}

Provide:
1. Comprehensive answer to original query
2. Key insights discovered
3. Confidence in answer completeness
4. Areas requiring further research (if any)`;

const synthesisResult = await answer(
  synthesisPrompt,
  'You are synthesizing multi-turn recursive research. Be comprehensive, cite sources, and indicate certainty levels.'
);

const synthesisText = typeof synthesisResult.contents === 'string' ?
  synthesisResult.contents :
  JSON.stringify(synthesisResult.contents, null, 2);

totalCost += Number(synthesisResult.cost?.total_deduction_dollars ?? 0);

const keySources = [...allSources.values()].sort((left, right) => right.count - left.count);
const finalResult = {
  totalTurns: turns.length,
  finalConfidence: currentConfidence,
  totalCost,
  synthesis: synthesisText,
  keySources,
  turns,
};

writeFileSync(join(options.output, 'report.json'), JSON.stringify(finalResult, null, 2));
console.log(JSON.stringify(finalResult, null, 2));
