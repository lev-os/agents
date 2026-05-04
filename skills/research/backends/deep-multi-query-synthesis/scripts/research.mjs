#!/usr/bin/env bun

import { readFileSync, existsSync } from "fs";
import { homedir } from "os";
import { join } from "path";

// ============================================================================
// Configuration
// ============================================================================

function usage() {
  console.error(`
Deep Research - Multi-mode research agent using Tavily

Usage: research.mjs "query" [options]

Modes:
  --quick       Single query, fast results (default if no mode specified)
  --expand      Iterative query expansion with follow-ups
  --deep        Multi-query synthesis with comprehensive analysis

Options:
  --max-iter <n>     Maximum iterations (default: 5)
  --confidence <n>   Confidence threshold 0-100 (default: 85)
  --results <n>      Results per query (default: 5, max: 20)
  --topic <t>        Search topic: general (default) or news
  --days <n>         For news topic, limit to last n days
  --json             Output raw JSON instead of markdown
  -h, --help         Show this help

Examples:
  research.mjs "What is quantum computing?" --quick
  research.mjs "CRISPR gene editing applications" --expand
  research.mjs "Kubernetes autoscaling best practices" --deep
`);
  process.exit(2);
}

// ============================================================================
// API Key Loading
// ============================================================================

function getApiKey() {
  // 1. Environment variable
  const envKey = (process.env.TAVILY_API_KEY ?? "").trim();
  if (envKey) return envKey;

  // 2. Clawdbot config
  const configPath = join(homedir(), ".clawdbot", "clawdbot.json");
  if (existsSync(configPath)) {
    try {
      const config = JSON.parse(readFileSync(configPath, "utf-8"));
      const skillKey = config?.skills?.entries?.["tavily-search"]?.apiKey;
      if (skillKey) return skillKey.trim();
    } catch {
      // Ignore parse errors
    }
  }

  return null;
}

// ============================================================================
// Tavily API
// ============================================================================

async function tavilySearch(apiKey, query, options = {}) {
  const {
    maxResults = 5,
    searchDepth = "advanced",
    topic = "general",
    days = null,
  } = options;

  const body = {
    api_key: apiKey,
    query,
    search_depth: searchDepth,
    topic,
    max_results: Math.max(1, Math.min(maxResults, 20)),
    include_answer: true,
    include_raw_content: false,
  };

  if (topic === "news" && days) {
    body.days = days;
  }

  const resp = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Tavily Search failed (${resp.status}): ${text}`);
  }

  return resp.json();
}

// ============================================================================
// Research Modes
// ============================================================================

/**
 * Quick mode - single query
 */
async function quickResearch(apiKey, query, options) {
  const trace = [{ iteration: 1, query, type: "initial" }];
  
  const result = await tavilySearch(apiKey, query, {
    maxResults: options.results,
    searchDepth: "basic", // Quick mode uses basic depth
    topic: options.topic,
    days: options.days,
  });

  trace[0].resultsCount = result.results?.length ?? 0;

  return {
    query,
    mode: "quick",
    summary: result.answer || "No summary available",
    confidence: 70, // Quick mode = moderate confidence
    findings: extractFindings(result.results || []),
    sources: deduplicateSources(result.results || []),
    trace,
    iterations: 1,
  };
}

/**
 * Expand mode - iterative query refinement
 */
async function expandResearch(apiKey, query, options) {
  const trace = [];
  const allSources = [];
  const seenUrls = new Set();
  let currentQuery = query;
  let confidence = 0;
  let lastNewCount = 0;

  for (let i = 1; i <= options.maxIter; i++) {
    trace.push({ iteration: i, query: currentQuery, type: i === 1 ? "initial" : "expansion" });

    const result = await tavilySearch(apiKey, currentQuery, {
      maxResults: options.results,
      searchDepth: "advanced",
      topic: options.topic,
      days: options.days,
    });

    // Track new sources
    const newSources = (result.results || []).filter(r => {
      const url = r.url?.trim();
      if (!url || seenUrls.has(url)) return false;
      seenUrls.add(url);
      return true;
    });

    allSources.push(...newSources);
    trace[i - 1].resultsCount = result.results?.length ?? 0;
    trace[i - 1].newResultsCount = newSources.length;

    // Calculate confidence based on answer quality and source agreement
    confidence = calculateConfidence(result.answer, allSources, i, options.maxIter);
    trace[i - 1].confidence = confidence;

    // Smart stopping conditions
    if (confidence >= options.confidence) {
      trace[i - 1].stopReason = "confidence_threshold";
      break;
    }

    if (i > 1 && newSources.length === 0) {
      trace[i - 1].stopReason = "no_new_info";
      break;
    }

    if (i > 2 && newSources.length <= lastNewCount * 0.3) {
      trace[i - 1].stopReason = "diminishing_returns";
      break;
    }

    lastNewCount = newSources.length;

    // Generate follow-up query for next iteration
    if (i < options.maxIter) {
      currentQuery = generateFollowUpQuery(query, allSources, i);
    }
  }

  return {
    query,
    mode: "expand",
    summary: synthesizeSummary(query, allSources),
    confidence,
    findings: extractFindings(allSources),
    sources: deduplicateSources(allSources),
    trace,
    iterations: trace.length,
  };
}

/**
 * Deep mode - multi-query parallel synthesis
 */
async function deepResearch(apiKey, query, options) {
  const trace = [];
  const allSources = [];
  const seenUrls = new Set();
  let confidence = 0;

  // Generate multiple angle queries
  const queries = generateMultipleQueries(query);
  
  for (let i = 1; i <= options.maxIter; i++) {
    const iterationQueries = i === 1 ? queries : [generateDeepFollowUp(query, allSources, i)];
    
    trace.push({
      iteration: i,
      queries: iterationQueries,
      type: i === 1 ? "parallel_initial" : "synthesis_followup",
    });

    // Run queries in parallel
    const results = await Promise.all(
      iterationQueries.map(q =>
        tavilySearch(apiKey, q, {
          maxResults: options.results,
          searchDepth: "advanced",
          topic: options.topic,
          days: options.days,
        })
      )
    );

    // Aggregate new sources
    let totalNew = 0;
    for (const result of results) {
      const newSources = (result.results || []).filter(r => {
        const url = r.url?.trim();
        if (!url || seenUrls.has(url)) return false;
        seenUrls.add(url);
        return true;
      });
      allSources.push(...newSources);
      totalNew += newSources.length;
    }

    trace[i - 1].resultsCount = results.reduce((sum, r) => sum + (r.results?.length ?? 0), 0);
    trace[i - 1].newResultsCount = totalNew;

    // Calculate confidence
    confidence = calculateConfidence(null, allSources, i, options.maxIter, true);
    trace[i - 1].confidence = confidence;

    // Smart stopping
    if (confidence >= options.confidence) {
      trace[i - 1].stopReason = "confidence_threshold";
      break;
    }

    if (i > 1 && totalNew === 0) {
      trace[i - 1].stopReason = "no_new_info";
      break;
    }

    if (i >= options.maxIter) {
      trace[i - 1].stopReason = "max_iterations";
    }
  }

  return {
    query,
    mode: "deep",
    summary: synthesizeSummary(query, allSources, true),
    confidence,
    findings: extractFindings(allSources, true),
    sources: deduplicateSources(allSources),
    trace,
    iterations: trace.length,
  };
}

// ============================================================================
// Helper Functions
// ============================================================================

function calculateConfidence(answer, sources, iteration, maxIter, isDeep = false) {
  let confidence = 40; // Base confidence

  // More sources = higher confidence (up to +25)
  const sourceBonus = Math.min(sources.length * 2.5, 25);
  confidence += sourceBonus;

  // High relevance scores boost confidence (up to +20)
  const avgRelevance = sources.reduce((sum, s) => sum + (s.score || 0.5), 0) / Math.max(sources.length, 1);
  confidence += avgRelevance * 20;

  // Answer presence boosts confidence
  if (answer && answer.length > 100) {
    confidence += 10;
  }

  // Deep mode gets slight boost for thoroughness
  if (isDeep) {
    confidence += 5;
  }

  // Later iterations suggest thorough research
  if (iteration > 1) {
    confidence += iteration * 2;
  }

  return Math.min(Math.round(confidence), 98);
}

function generateFollowUpQuery(originalQuery, sources, iteration) {
  // Extract key terms from sources to refine search
  const terms = new Set();
  for (const s of sources.slice(0, 5)) {
    const content = s.content || "";
    // Extract capitalized terms (likely proper nouns/concepts)
    const matches = content.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || [];
    matches.slice(0, 3).forEach(m => terms.add(m));
  }

  const termArray = [...terms].slice(0, 3);
  const refinement = termArray.length > 0 ? termArray.join(" ") : "";

  // Add depth modifiers based on iteration
  const depthModifiers = ["detailed", "comprehensive", "in-depth", "technical"];
  const modifier = depthModifiers[Math.min(iteration - 1, depthModifiers.length - 1)];

  return `${modifier} ${originalQuery} ${refinement}`.trim();
}

function generateMultipleQueries(query) {
  // Generate queries from different angles
  return [
    query, // Original
    `${query} explained`, // Explanation angle
    `${query} examples use cases`, // Practical angle
    `${query} best practices recommendations`, // Advisory angle
  ];
}

function generateDeepFollowUp(originalQuery, sources, iteration) {
  // For deep mode, generate synthesis-oriented follow-ups
  const angles = [
    "comparison analysis",
    "challenges limitations",
    "future trends predictions",
    "expert opinions",
  ];
  const angle = angles[Math.min(iteration - 2, angles.length - 1)] || "overview";
  return `${originalQuery} ${angle}`;
}

function extractFindings(sources, isDeep = false) {
  const findings = [];
  const seen = new Set();

  // Extract key sentences from source content
  for (const s of sources.slice(0, isDeep ? 15 : 8)) {
    const content = s.content || "";
    // Get first substantive sentence
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 30);
    for (const sentence of sentences.slice(0, 2)) {
      const trimmed = sentence.trim();
      const normalized = trimmed.toLowerCase().slice(0, 50);
      if (!seen.has(normalized) && trimmed.length > 30) {
        seen.add(normalized);
        findings.push(trimmed);
        if (findings.length >= (isDeep ? 8 : 5)) break;
      }
    }
    if (findings.length >= (isDeep ? 8 : 5)) break;
  }

  return findings;
}

function deduplicateSources(sources) {
  const seen = new Set();
  return sources
    .filter(s => {
      const url = s.url?.trim();
      if (!url || seen.has(url)) return false;
      seen.add(url);
      return true;
    })
    .sort((a, b) => (b.score || 0) - (a.score || 0))
    .slice(0, 15)
    .map(s => ({
      title: s.title?.trim() || "Untitled",
      url: s.url?.trim(),
      relevance: Math.round((s.score || 0.5) * 100),
      snippet: (s.content || "").slice(0, 200),
    }));
}

function synthesizeSummary(query, sources, isDeep = false) {
  if (sources.length === 0) {
    return "No information found for this query.";
  }

  // Build summary from top sources
  const topSources = sources.slice(0, isDeep ? 8 : 4);
  const snippets = topSources
    .map(s => s.content || "")
    .filter(c => c.length > 50)
    .slice(0, 3);

  if (snippets.length === 0) {
    return `Found ${sources.length} sources related to "${query}".`;
  }

  // Combine key information
  const combined = snippets.join(" ").slice(0, 800);
  return combined + (combined.length >= 800 ? "..." : "");
}

// ============================================================================
// Output Formatting
// ============================================================================

function formatMarkdown(result) {
  const lines = [];

  lines.push(`# Research: ${result.query}\n`);
  lines.push(`**Mode:** ${result.mode} | **Confidence:** ${result.confidence}% | **Iterations:** ${result.iterations}\n`);

  lines.push("## Summary\n");
  lines.push(result.summary);
  lines.push("");

  if (result.findings.length > 0) {
    lines.push("## Key Findings\n");
    for (const f of result.findings) {
      lines.push(`- ${f}`);
    }
    lines.push("");
  }

  lines.push("## Sources\n");
  for (const s of result.sources) {
    lines.push(`- **[${s.title}](${s.url})** (${s.relevance}%)`);
    if (s.snippet) {
      lines.push(`  ${s.snippet.slice(0, 150)}...`);
    }
  }
  lines.push("");

  lines.push("## Research Trace\n");
  for (const t of result.trace) {
    const queries = t.queries ? t.queries.join(", ") : t.query;
    const newInfo = t.newResultsCount !== undefined ? `, ${t.newResultsCount} new` : "";
    const stop = t.stopReason ? ` [${t.stopReason}]` : "";
    const conf = t.confidence ? ` (confidence: ${t.confidence}%)` : "";
    lines.push(`- **Iteration ${t.iteration}** (${t.type}): "${queries}" → ${t.resultsCount} results${newInfo}${conf}${stop}`);
  }

  return lines.join("\n");
}

// ============================================================================
// Main
// ============================================================================

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === "-h" || args[0] === "--help") {
    usage();
  }

  // Parse arguments
  const query = args[0];
  const options = {
    mode: "expand", // Default mode
    maxIter: 5,
    confidence: 85,
    results: 5,
    topic: "general",
    days: null,
    json: false,
  };

  for (let i = 1; i < args.length; i++) {
    const a = args[i];
    switch (a) {
      case "--quick":
        options.mode = "quick";
        break;
      case "--expand":
        options.mode = "expand";
        break;
      case "--deep":
        options.mode = "deep";
        break;
      case "--max-iter":
        options.maxIter = parseInt(args[++i] || "5", 10);
        break;
      case "--confidence":
        options.confidence = parseInt(args[++i] || "85", 10);
        break;
      case "--results":
        options.results = parseInt(args[++i] || "5", 10);
        break;
      case "--topic":
        options.topic = args[++i] || "general";
        break;
      case "--days":
        options.days = parseInt(args[++i] || "7", 10);
        break;
      case "--json":
        options.json = true;
        break;
      default:
        if (a.startsWith("-")) {
          console.error(`Unknown option: ${a}`);
          usage();
        }
    }
  }

  // Get API key
  const apiKey = getApiKey();
  if (!apiKey) {
    console.error("Error: No Tavily API key found.");
    console.error("Set TAVILY_API_KEY or configure in ~/.clawdbot/clawdbot.json");
    process.exit(1);
  }

  // Run research
  let result;
  try {
    switch (options.mode) {
      case "quick":
        result = await quickResearch(apiKey, query, options);
        break;
      case "expand":
        result = await expandResearch(apiKey, query, options);
        break;
      case "deep":
        result = await deepResearch(apiKey, query, options);
        break;
    }
  } catch (err) {
    console.error(`Research failed: ${err.message}`);
    process.exit(1);
  }

  // Output
  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(formatMarkdown(result));
  }
}

main();
