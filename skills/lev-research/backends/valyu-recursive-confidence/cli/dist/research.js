import chalk from 'chalk';
import ora from 'ora';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
export async function recursiveResearch(client, options) {
    const { query, maxTurns, confidenceThreshold, strategy, outputDir } = options;
    // Create output directory
    mkdirSync(outputDir, { recursive: true });
    const turns = [];
    const allSources = new Map();
    let currentQuery = query;
    let totalCost = 0;
    let currentConfidence = 0;
    // Turn-based research loop
    for (let turn = 1; turn <= maxTurns; turn++) {
        const spinner = ora(`Turn ${turn}/${maxTurns}: ${currentQuery.slice(0, 60)}...`).start();
        try {
            // Execute search + answer for this turn
            const searchResult = await client.search(currentQuery, {
                maxNumResults: strategy === 'breadth' ? 20 : strategy === 'depth' ? 10 : 15,
                searchType: 'all',
            });
            const answerResponse = await client.answer(currentQuery, {
                systemInstructions: `You are conducting turn ${turn} of ${maxTurns} in a recursive research process.

Previous context: ${turns.length > 0 ? turns[turns.length - 1].findings : 'None'}

Provide:
1. Key findings from current search
2. Confidence level (0.0-1.0) in answer completeness
3. Suggested next research direction (if confidence < ${confidenceThreshold})

Format:
FINDINGS: [detailed findings]
CONFIDENCE: [0.0-1.0]
NEXT_QUERY: [refined query for next turn, or "COMPLETE" if done]`,
            });
            // Handle response type
            if (!('success' in answerResponse) || !answerResponse.success) {
                const errorMsg = 'error' in answerResponse ? answerResponse.error : 'Unknown answer error';
                throw new Error(errorMsg);
            }
            const answerResult = answerResponse;
            totalCost += searchResult.total_deduction_dollars;
            totalCost += answerResult.cost.total_deduction_dollars;
            // Track sources
            searchResult.results.forEach((source) => {
                const key = source.url;
                if (allSources.has(key)) {
                    allSources.get(key).count++;
                }
                else {
                    allSources.set(key, {
                        title: source.title,
                        url: source.url,
                        count: 1,
                    });
                }
            });
            // Parse AI response for confidence and next steps
            const response = answerResult.contents;
            const confidenceMatch = response.match(/CONFIDENCE:\s*([\d.]+)/);
            const nextQueryMatch = response.match(/NEXT_QUERY:\s*(.+?)(?:\n|$)/);
            const findingsMatch = response.match(/FINDINGS:\s*(.+?)(?=CONFIDENCE:|$)/s);
            currentConfidence = confidenceMatch ? parseFloat(confidenceMatch[1]) : 0.7;
            const findings = findingsMatch ? findingsMatch[1].trim() : response;
            const nextQuery = nextQueryMatch ? nextQueryMatch[1].trim() : null;
            // Save turn results
            const turnResult = {
                turn,
                query: currentQuery,
                confidence: currentConfidence,
                findings,
                sources: searchResult.results.length,
                cost: searchResult.total_deduction_dollars + answerResult.cost.total_deduction_dollars,
                refinementReason: nextQuery && nextQuery !== 'COMPLETE' ? `Confidence ${(currentConfidence * 100).toFixed(0)}% < ${(confidenceThreshold * 100).toFixed(0)}%` : undefined,
            };
            turns.push(turnResult);
            // Write turn results to file
            writeFileSync(join(outputDir, `turn-${turn}.json`), JSON.stringify({ turnResult, searchResult, answerResult }, null, 2));
            writeFileSync(join(outputDir, `turn-${turn}.md`), `# Turn ${turn}: ${currentQuery}\n\n` +
                `**Confidence:** ${(currentConfidence * 100).toFixed(1)}%\n` +
                `**Sources:** ${searchResult.results.length}\n` +
                `**Cost:** $${turnResult.cost.toFixed(4)}\n\n` +
                `## Findings\n\n${findings}\n\n` +
                `## Sources\n\n${searchResult.results.map((s, i) => `${i + 1}. [${s.title}](${s.url})`).join('\n')}\n`);
            spinner.succeed(`Turn ${turn} complete: ${(currentConfidence * 100).toFixed(0)}% confidence, ${searchResult.results.length} sources, $${turnResult.cost.toFixed(4)}`);
            // Check stopping conditions
            if (currentConfidence >= confidenceThreshold) {
                console.log(chalk.green(`\n✓ Confidence threshold reached (${(currentConfidence * 100).toFixed(0)}% >= ${(confidenceThreshold * 100).toFixed(0)}%)`));
                break;
            }
            if (turn === maxTurns) {
                console.log(chalk.yellow(`\n⚠ Max turns reached (${maxTurns})`));
                break;
            }
            if (!nextQuery || nextQuery === 'COMPLETE') {
                console.log(chalk.green('\n✓ Research marked complete by AI'));
                break;
            }
            // Refine query for next turn
            currentQuery = nextQuery;
            console.log(chalk.blue(`\n→ Next turn: ${currentQuery.slice(0, 80)}...\n`));
        }
        catch (error) {
            spinner.fail(`Turn ${turn} failed: ${error.message}`);
            throw error;
        }
    }
    // Generate final synthesis
    const synthesisSpinner = ora('Generating final synthesis...').start();
    const synthesisQuery = `Based on ${turns.length} research turns on "${query}", provide a comprehensive final synthesis.

Turn summaries:
${turns.map((t, i) => `Turn ${i + 1} (${(t.confidence * 100).toFixed(0)}% confidence): ${t.findings.slice(0, 200)}...`).join('\n\n')}

Provide:
1. Comprehensive answer to original query
2. Key insights discovered
3. Confidence in answer completeness
4. Areas requiring further research (if any)`;
    const synthesisResponse = await client.answer(synthesisQuery, {
        systemInstructions: 'You are synthesizing multi-turn recursive research. Be comprehensive, cite sources, and indicate certainty levels.',
    });
    // Handle response type
    if (!('success' in synthesisResponse) || !synthesisResponse.success) {
        const errorMsg = 'error' in synthesisResponse ? synthesisResponse.error : 'Unknown synthesis error';
        throw new Error(errorMsg);
    }
    const synthesisResult = synthesisResponse;
    totalCost += synthesisResult.cost.total_deduction_dollars;
    synthesisSpinner.succeed('Synthesis complete');
    // Sort sources by citation count
    const keySources = Array.from(allSources.values())
        .sort((a, b) => b.count - a.count)
        .map(s => ({ title: s.title, url: s.url, citations: s.count }));
    const result = {
        totalTurns: turns.length,
        finalConfidence: currentConfidence,
        totalCost,
        synthesis: synthesisResult.contents,
        keySources,
        turns,
    };
    // Write final report
    const report = `# Recursive Research Report: ${query}

**Generated:** ${new Date().toISOString()}
**Total Turns:** ${turns.length}
**Final Confidence:** ${(currentConfidence * 100).toFixed(1)}%
**Total Cost:** $${totalCost.toFixed(4)}
**Total Sources:** ${keySources.length}

---

## Final Synthesis

${synthesisResult.contents}

---

## Research Timeline

${turns.map(t => `### Turn ${t.turn}: ${t.query}

**Confidence:** ${(t.confidence * 100).toFixed(1)}%
**Sources:** ${t.sources}
**Cost:** $${t.cost.toFixed(4)}

${t.findings}

${t.refinementReason ? `**Refinement reason:** ${t.refinementReason}` : ''}

---`).join('\n\n')}

## Top Sources (by citations)

${keySources.slice(0, 20).map((s, i) => `${i + 1}. [${s.title}](${s.url}) (cited ${s.citations}x)`).join('\n')}

---

## Cost Breakdown

| Turn | Query | Cost | Sources |
|------|-------|------|---------|
${turns.map(t => `| ${t.turn} | ${t.query.slice(0, 40)}... | $${t.cost.toFixed(4)} | ${t.sources} |`).join('\n')}
| **Synthesis** | Final synthesis | $${synthesisResult.cost.total_deduction_dollars.toFixed(4)} | - |
| **Total** | - | **$${totalCost.toFixed(4)}** | **${keySources.length}** |
`;
    writeFileSync(join(outputDir, 'REPORT.md'), report);
    writeFileSync(join(outputDir, 'results.json'), JSON.stringify(result, null, 2));
    return result;
}
