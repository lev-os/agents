#!/usr/bin/env node

import { Command } from 'commander';
import { ValyuClient } from 'valyu-js';
import chalk from 'chalk';
import ora from 'ora';
import { config } from 'dotenv';
import { recursiveResearch } from './research.js';
import { writeFileSync } from 'fs';
import { join } from 'path';

// Load .env from ~/.valyu/.env
config({ path: join(process.env.HOME!, '.valyu', '.env') });

const program = new Command();

// Initialize client
const getClient = () => {
  const apiKey = process.env.VALYU_API_KEY;
  if (!apiKey) {
    console.error(chalk.red('Error: VALYU_API_KEY not found'));
    console.error(chalk.yellow('Set it in ~/.valyu/.env or export VALYU_API_KEY=your-key'));
    process.exit(1);
  }
  return new ValyuClient({ apiKey });
};

program
  .name('valyu')
  .description('Valyu AI Search CLI - Real-time search for AI agents')
  .version('1.0.0');

// Search command
program
  .command('search <query>')
  .description('Search web, news, and proprietary sources')
  .option('-n, --num <number>', 'Number of results', '10')
  .option('-t, --type <type>', 'Search type: all|web|proprietary|news', 'all')
  .option('-f, --fast', 'Fast mode (reduced latency)')
  .option('--start <date>', 'Start date (YYYY-MM-DD)')
  .option('--end <date>', 'End date (YYYY-MM-DD)')
  .option('-o, --output <file>', 'Save results to file')
  .action(async (query, options) => {
    const spinner = ora('Searching...').start();
    const client = getClient();

    try {
      const results = await client.search({
        query,
        max_num_results: parseInt(options.num),
        search_type: options.type,
        fast_mode: options.fast || false,
        start_date: options.start,
        end_date: options.end,
      });

      spinner.succeed('Search complete');

      console.log(chalk.bold(`\n📊 Found ${results.results.length} results`));
      console.log(chalk.gray(`Cost: $${results.total_deduction_dollars.toFixed(4)}`));

      results.results.forEach((result, i) => {
        console.log(chalk.bold.cyan(`\n[${i + 1}] ${result.title}`));
        console.log(chalk.gray(result.url));
        console.log(result.content.slice(0, 200) + '...');
        if (result.source_type !== 'general') {
          console.log(chalk.yellow(`Type: ${result.source_type}`));
        }
      });

      if (options.output) {
        writeFileSync(options.output, JSON.stringify(results, null, 2));
        console.log(chalk.green(`\n✓ Saved to ${options.output}`));
      }
    } catch (error: any) {
      spinner.fail('Search failed');
      console.error(chalk.red(error.message));
      process.exit(1);
    }
  });

// Answer command
program
  .command('answer <query>')
  .description('Get AI-generated answer grounded in search results')
  .option('-t, --type <type>', 'Search type: all|web|proprietary|news', 'all')
  .option('-i, --instructions <text>', 'System instructions for AI')
  .option('--stream', 'Enable streaming mode')
  .option('-o, --output <file>', 'Save answer to file')
  .action(async (query, options) => {
    const spinner = ora('Generating answer...').start();
    const client = getClient();

    try {
      const result = await client.answer({
        query,
        search_type: options.type,
        system_instructions: options.instructions,
        streaming: options.stream || false,
      });

      spinner.succeed('Answer generated');

      console.log(chalk.bold.green('\n💡 Answer:\n'));
      console.log(result.contents);

      console.log(chalk.bold.cyan('\n📚 Sources:'));
      result.search_results.slice(0, 5).forEach((source: any, i: number) => {
        console.log(chalk.gray(`[${i + 1}] ${source.title}`));
        console.log(chalk.gray(`    ${source.url}`));
      });

      console.log(chalk.gray(`\nCost: $${result.cost.total_dollars.toFixed(4)}`));
      console.log(chalk.gray(`Tokens: ${result.ai_usage.input_tokens + result.ai_usage.output_tokens}`));

      if (options.output) {
        writeFileSync(options.output, JSON.stringify(result, null, 2));
        console.log(chalk.green(`\n✓ Saved to ${options.output}`));
      }
    } catch (error: any) {
      spinner.fail('Answer generation failed');
      console.error(chalk.red(error.message));
      process.exit(1);
    }
  });

// Contents command
program
  .command('contents <urls...>')
  .description('Extract content from URLs')
  .option('-l, --length <size>', 'Response length: short|medium|large|max', 'short')
  .option('-e, --effort <level>', 'Extract effort: normal|high|auto', 'normal')
  .option('-s, --summary <instructions>', 'AI summary instructions')
  .option('--screenshot', 'Include screenshots')
  .option('-o, --output <file>', 'Save results to file')
  .action(async (urls, options) => {
    const spinner = ora(`Extracting content from ${urls.length} URL(s)...`).start();
    const client = getClient();

    try {
      const results = await client.contents({
        urls,
        response_length: options.length,
        extract_effort: options.effort,
        summary: options.summary || false,
        screenshot: options.screenshot || false,
      });

      spinner.succeed('Content extracted');

      console.log(chalk.bold(`\n📄 Processed ${results.urls_processed}/${results.urls_requested} URLs`));
      console.log(chalk.gray(`Cost: $${results.total_cost_dollars.toFixed(4)}`));

      results.results.forEach((result: any, i: number) => {
        console.log(chalk.bold.cyan(`\n[${i + 1}] ${result.title}`));
        console.log(chalk.gray(result.url));
        console.log(result.content.slice(0, 300) + '...');
        if (result.screenshot_url) {
          console.log(chalk.yellow(`Screenshot: ${result.screenshot_url}`));
        }
      });

      if (options.output) {
        writeFileSync(options.output, JSON.stringify(results, null, 2));
        console.log(chalk.green(`\n✓ Saved to ${options.output}`));
      }
    } catch (error: any) {
      spinner.fail('Content extraction failed');
      console.error(chalk.red(error.message));
      process.exit(1);
    }
  });

// Recursive Research command
program
  .command('research <query>')
  .description('Recursive deep research with turn-based refinement')
  .option('-n, --turns <number>', 'Number of research turns (1-10)', '5')
  .option('-t, --threshold <number>', 'Confidence threshold to stop (0.0-1.0)', '0.85')
  .option('-o, --output <dir>', 'Output directory for results', './valyu-research')
  .option('--strategy <type>', 'Research strategy: breadth|depth|balanced', 'balanced')
  .action(async (query, options) => {
    const turns = Math.min(Math.max(parseInt(options.turns), 1), 10);
    const threshold = parseFloat(options.threshold);

    console.log(chalk.bold.blue('\n🔬 Starting Recursive Deep Research\n'));
    console.log(chalk.gray(`Query: ${query}`));
    console.log(chalk.gray(`Turns: ${turns} (max)`));
    console.log(chalk.gray(`Threshold: ${threshold}`));
    console.log(chalk.gray(`Strategy: ${options.strategy}\n`));

    const client = getClient();

    try {
      const result = await recursiveResearch(client, {
        query,
        maxTurns: turns,
        confidenceThreshold: threshold,
        strategy: options.strategy,
        outputDir: options.output,
      });

      console.log(chalk.bold.green('\n✓ Research Complete\n'));
      console.log(chalk.bold('📊 Summary:'));
      console.log(chalk.gray(`Total turns: ${result.totalTurns}`));
      console.log(chalk.gray(`Final confidence: ${(result.finalConfidence * 100).toFixed(1)}%`));
      console.log(chalk.gray(`Total cost: $${result.totalCost.toFixed(4)}`));
      console.log(chalk.gray(`Results saved: ${options.output}/`));

      console.log(chalk.bold.cyan('\n💡 Final Synthesis:\n'));
      console.log(result.synthesis);

      console.log(chalk.bold.yellow('\n📚 Key Sources:'));
      result.keySources.slice(0, 10).forEach((source, i) => {
        console.log(chalk.gray(`[${i + 1}] ${source.title}`));
        console.log(chalk.gray(`    ${source.url} (cited ${source.citations}x)`));
      });
    } catch (error: any) {
      console.error(chalk.red('\n✗ Research failed:'), error.message);
      process.exit(1);
    }
  });

program.parse();
