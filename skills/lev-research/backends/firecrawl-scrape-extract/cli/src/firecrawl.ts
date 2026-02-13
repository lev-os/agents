#!/usr/bin/env node

import { Command } from 'commander';
import axios, { AxiosInstance } from 'axios';
import chalk from 'chalk';
import ora from 'ora';
import { config } from 'dotenv';
import { writeFileSync } from 'fs';
import { join } from 'path';

// Load .env from ~/.env.local
config({ path: join(process.env.HOME!, '.env.local') });

const API_BASE = 'https://api.firecrawl.dev/v1';

const program = new Command();

// Initialize API client
const getClient = (): AxiosInstance => {
  const apiKey = process.env.FIRECRAWL_API_KEY;
  if (!apiKey) {
    console.error(chalk.red('Error: FIRECRAWL_API_KEY not found'));
    console.error(chalk.yellow('Set it in ~/.env.local or export FIRECRAWL_API_KEY=your-key'));
    process.exit(1);
  }
  return axios.create({
    baseURL: API_BASE,
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });
};

// Helper to save output
const saveOutput = (data: unknown, output?: string, format: 'json' | 'text' = 'json') => {
  if (output) {
    const content = format === 'json' ? JSON.stringify(data, null, 2) : String(data);
    writeFileSync(output, content);
    console.log(chalk.green(`\n✓ Saved to ${output}`));
  }
};

// Poll for job completion
const pollJob = async (
  client: AxiosInstance,
  endpoint: string,
  jobId: string,
  spinner: ReturnType<typeof ora>
): Promise<unknown> => {
  const maxAttempts = 120; // 10 minutes with 5s intervals
  let attempts = 0;

  while (attempts < maxAttempts) {
    const response = await client.get(`${endpoint}/${jobId}`);
    const { status, data, total, completed } = response.data;

    if (status === 'completed') {
      return response.data;
    }

    if (status === 'failed') {
      throw new Error('Job failed');
    }

    spinner.text = `Processing... ${completed || 0}/${total || '?'} pages`;
    attempts++;
    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  throw new Error('Job timed out after 10 minutes');
};

program
  .name('firecrawl')
  .description('Firecrawl CLI - Web scraping and crawling for AI')
  .version('1.0.0');

// Check for --status flag before parsing
const checkStatus = async (): Promise<boolean> => {
  if (process.argv.includes('--status')) {
    const apiKey = process.env.FIRECRAWL_API_KEY;
    console.log(chalk.bold('\n  🔥 firecrawl cli v1.0.0\n'));

    if (!apiKey) {
      console.log(chalk.red('  ✗ Not authenticated'));
      console.log(chalk.yellow('    Set FIRECRAWL_API_KEY in ~/.env.local'));
      process.exit(1);
    }

    console.log(chalk.green('  ● Authenticated via FIRECRAWL_API_KEY'));

    // Try to verify API key works
    try {
      const client = axios.create({
        baseURL: API_BASE,
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });
      await client.post('/scrape', { url: 'https://example.com', formats: ['markdown'] });
      console.log(chalk.green('  ● API key verified'));
    } catch (error: unknown) {
      const err = error as { response?: { status?: number } };
      if (err.response?.status === 401) {
        console.log(chalk.red('  ✗ API key invalid'));
      } else if (err.response?.status === 402) {
        console.log(chalk.yellow('  ⚠ Payment required - check credits'));
      } else {
        console.log(chalk.green('  ● API key verified'));
      }
    }
    console.log('');
    process.exit(0);
  }
  return false;
};

// Scrape command - single URL
program
  .command('scrape <url>')
  .description('Scrape content from a single URL')
  .option('-f, --format <formats>', 'Output formats: markdown,html,links,screenshot', 'markdown')
  .option('--only-main-content', 'Extract main content only', true)
  .option('--wait-for <ms>', 'Wait before scraping (for JS content)', '0')
  .option('--include-tags <tags>', 'Only include specific HTML tags')
  .option('--exclude-tags <tags>', 'Exclude specific HTML tags')
  .option('--timeout <ms>', 'Request timeout in milliseconds', '30000')
  .option('-o, --output <file>', 'Save results to file')
  .option('--json', 'Force JSON output')
  .action(async (url, options) => {
    const spinner = ora('Scraping URL...').start();
    const client = getClient();

    try {
      const formats = options.format.split(',').map((f: string) => f.trim());

      const payload: Record<string, unknown> = {
        url,
        formats,
        onlyMainContent: options.onlyMainContent,
        waitFor: parseInt(options.waitFor),
        timeout: parseInt(options.timeout),
      };

      if (options.includeTags) {
        payload.includeTags = options.includeTags.split(',').map((t: string) => t.trim());
      }
      if (options.excludeTags) {
        payload.excludeTags = options.excludeTags.split(',').map((t: string) => t.trim());
      }

      const response = await client.post('/scrape', payload);
      spinner.succeed('Scrape complete');

      const { data } = response.data;

      if (options.json || formats.length > 1) {
        // JSON output for multiple formats
        console.log(chalk.bold(`\n📄 Scraped: ${data.metadata?.title || url}`));
        console.log(chalk.gray(`Source: ${data.metadata?.sourceURL || url}`));

        if (data.markdown) {
          console.log(chalk.cyan('\n--- Markdown Preview ---'));
          console.log(data.markdown.slice(0, 500) + (data.markdown.length > 500 ? '...' : ''));
        }
        if (data.links?.length) {
          console.log(chalk.cyan(`\n--- ${data.links.length} Links Found ---`));
        }

        saveOutput(response.data, options.output, 'json');
      } else {
        // Raw markdown output for single format
        console.log(chalk.bold(`\n📄 ${data.metadata?.title || url}\n`));
        console.log(data.markdown || data.html || JSON.stringify(data, null, 2));

        if (options.output) {
          const content = data.markdown || data.html || JSON.stringify(data, null, 2);
          writeFileSync(options.output, content);
          console.log(chalk.green(`\n✓ Saved to ${options.output}`));
        }
      }
    } catch (error: unknown) {
      spinner.fail('Scrape failed');
      const err = error as { response?: { data?: { error?: string } }; message?: string };
      console.error(chalk.red(err.response?.data?.error || err.message || 'Unknown error'));
      process.exit(1);
    }
  });

// Crawl command - entire site
program
  .command('crawl <url>')
  .description('Crawl an entire website')
  .option('-l, --limit <number>', 'Maximum pages to crawl', '100')
  .option('-d, --max-depth <number>', 'Maximum crawl depth')
  .option('--include-paths <patterns>', 'URL patterns to include (regex, comma-separated)')
  .option('--exclude-paths <patterns>', 'URL patterns to exclude (regex, comma-separated)')
  .option('--allow-subdomains', 'Follow subdomain links', false)
  .option('--allow-external', 'Follow external links', false)
  .option('-o, --output <file>', 'Save results to file')
  .option('--no-wait', 'Return immediately without waiting for completion')
  .action(async (url, options) => {
    const spinner = ora('Starting crawl...').start();
    const client = getClient();

    try {
      const payload: Record<string, unknown> = {
        url,
        limit: parseInt(options.limit),
        scrapeOptions: {
          formats: ['markdown'],
          onlyMainContent: true,
        },
      };

      if (options.maxDepth) {
        payload.maxDiscoveryDepth = parseInt(options.maxDepth);
      }
      if (options.includePaths) {
        payload.includePaths = options.includePaths.split(',').map((p: string) => p.trim());
      }
      if (options.excludePaths) {
        payload.excludePaths = options.excludePaths.split(',').map((p: string) => p.trim());
      }
      if (options.allowSubdomains) {
        payload.allowSubdomains = true;
      }
      if (options.allowExternal) {
        payload.allowExternalLinks = true;
      }

      const response = await client.post('/crawl', payload);
      const { id } = response.data;

      if (options.wait === false) {
        spinner.succeed(`Crawl started: ${id}`);
        console.log(chalk.gray(`Check status: firecrawl status crawl ${id}`));
        return;
      }

      spinner.text = 'Crawling...';
      const result = await pollJob(client, '/crawl', id, spinner);
      spinner.succeed('Crawl complete');

      const crawlResult = result as { data?: unknown[]; total?: number; creditsUsed?: number };
      console.log(chalk.bold(`\n🕷️ Crawled ${crawlResult.data?.length || 0} pages`));
      console.log(chalk.gray(`Credits used: ${crawlResult.creditsUsed || 'N/A'}`));

      if (crawlResult.data && Array.isArray(crawlResult.data)) {
        crawlResult.data.slice(0, 5).forEach((page: unknown, i: number) => {
          const p = page as { metadata?: { title?: string; sourceURL?: string } };
          console.log(chalk.cyan(`\n[${i + 1}] ${p.metadata?.title || 'Untitled'}`));
          console.log(chalk.gray(p.metadata?.sourceURL || ''));
        });
        if (crawlResult.data.length > 5) {
          console.log(chalk.gray(`\n... and ${crawlResult.data.length - 5} more pages`));
        }
      }

      saveOutput(result, options.output);
    } catch (error: unknown) {
      spinner.fail('Crawl failed');
      const err = error as { response?: { data?: { error?: string } }; message?: string };
      console.error(chalk.red(err.response?.data?.error || err.message || 'Unknown error'));
      process.exit(1);
    }
  });

// Map command - discover URLs
program
  .command('map <url>')
  .description('Get a complete list of URLs from a website')
  .option('-l, --limit <number>', 'Maximum URLs to return', '5000')
  .option('-s, --search <query>', 'Filter URLs by search query')
  .option('--include-subdomains', 'Include subdomains', true)
  .option('-o, --output <file>', 'Save results to file')
  .option('--json', 'Output as JSON')
  .action(async (url, options) => {
    const spinner = ora('Mapping site...').start();
    const client = getClient();

    try {
      const payload: Record<string, unknown> = {
        url,
      };

      if (options.search) {
        payload.search = options.search;
      }
      if (options.includeSubdomains !== undefined) {
        payload.includeSubdomains = options.includeSubdomains;
      }

      const response = await client.post('/map', payload);
      spinner.succeed('Map complete');

      const { links } = response.data;
      console.log(chalk.bold(`\n🗺️ Found ${links.length} URLs`));

      if (options.json) {
        console.log(JSON.stringify(response.data, null, 2));
        saveOutput(response.data, options.output);
      } else {
        links.slice(0, 20).forEach((link: { url: string; title?: string }) => {
          if (typeof link === 'string') {
            console.log(link);
          } else {
            console.log(chalk.cyan(link.url));
            if (link.title) {
              console.log(chalk.gray(`  ${link.title}`));
            }
          }
        });
        if (links.length > 20) {
          console.log(chalk.gray(`\n... and ${links.length - 20} more URLs`));
        }

        if (options.output) {
          const content = links.map((l: string | { url: string }) =>
            typeof l === 'string' ? l : l.url
          ).join('\n');
          writeFileSync(options.output, content);
          console.log(chalk.green(`\n✓ Saved to ${options.output}`));
        }
      }
    } catch (error: unknown) {
      spinner.fail('Map failed');
      const err = error as { response?: { data?: { error?: string } }; message?: string };
      console.error(chalk.red(err.response?.data?.error || err.message || 'Unknown error'));
      process.exit(1);
    }
  });

// Extract command - structured data extraction
program
  .command('extract <urls...>')
  .description('Extract structured data from URLs using AI')
  .option('-p, --prompt <text>', 'Extraction prompt/instructions')
  .option('--schema <json>', 'JSON Schema for structured output')
  .option('--show-sources', 'Include sources in response', false)
  .option('--enable-web-search', 'Enable web search augmentation', false)
  .option('-o, --output <file>', 'Save results to file')
  .option('--no-wait', 'Return immediately without waiting for completion')
  .action(async (urls, options) => {
    const spinner = ora('Starting extraction...').start();
    const client = getClient();

    try {
      const payload: Record<string, unknown> = {
        urls,
        showSources: options.showSources,
        enableWebSearch: options.enableWebSearch,
      };

      if (options.prompt) {
        payload.prompt = options.prompt;
      }
      if (options.schema) {
        try {
          payload.schema = JSON.parse(options.schema);
        } catch {
          console.error(chalk.red('Invalid JSON schema'));
          process.exit(1);
        }
      }

      const response = await client.post('/extract', payload);
      const { id } = response.data;

      if (options.wait === false) {
        spinner.succeed(`Extraction started: ${id}`);
        console.log(chalk.gray(`Check status: firecrawl status extract ${id}`));
        return;
      }

      spinner.text = 'Extracting...';
      const result = await pollJob(client, '/extract', id, spinner);
      spinner.succeed('Extraction complete');

      const extractResult = result as { data?: unknown };
      console.log(chalk.bold('\n📊 Extracted Data:\n'));
      console.log(JSON.stringify(extractResult.data, null, 2));

      saveOutput(result, options.output);
    } catch (error: unknown) {
      spinner.fail('Extraction failed');
      const err = error as { response?: { data?: { error?: string } }; message?: string };
      console.error(chalk.red(err.response?.data?.error || err.message || 'Unknown error'));
      process.exit(1);
    }
  });

// Batch command - batch scrape multiple URLs
program
  .command('batch <urls...>')
  .description('Batch scrape multiple URLs')
  .option('-f, --format <formats>', 'Output formats: markdown,html,links,screenshot', 'markdown')
  .option('--only-main-content', 'Extract main content only', true)
  .option('--max-concurrency <number>', 'Maximum concurrent scrapes')
  .option('-o, --output <file>', 'Save results to file')
  .option('--no-wait', 'Return immediately without waiting for completion')
  .action(async (urls, options) => {
    const spinner = ora(`Starting batch scrape of ${urls.length} URLs...`).start();
    const client = getClient();

    try {
      const formats = options.format.split(',').map((f: string) => f.trim());

      const payload: Record<string, unknown> = {
        urls,
        formats,
        onlyMainContent: options.onlyMainContent,
        ignoreInvalidURLs: true,
      };

      if (options.maxConcurrency) {
        payload.maxConcurrency = parseInt(options.maxConcurrency);
      }

      const response = await client.post('/batch/scrape', payload);
      const { id, invalidURLs } = response.data;

      if (invalidURLs?.length) {
        console.log(chalk.yellow(`\n⚠️ ${invalidURLs.length} invalid URLs skipped`));
      }

      if (options.wait === false) {
        spinner.succeed(`Batch scrape started: ${id}`);
        console.log(chalk.gray(`Check status: firecrawl status batch ${id}`));
        return;
      }

      spinner.text = 'Processing batch...';
      const result = await pollJob(client, '/batch/scrape', id, spinner);
      spinner.succeed('Batch scrape complete');

      const batchResult = result as { data?: unknown[]; creditsUsed?: number };
      console.log(chalk.bold(`\n📦 Scraped ${batchResult.data?.length || 0} pages`));
      console.log(chalk.gray(`Credits used: ${batchResult.creditsUsed || 'N/A'}`));

      if (batchResult.data && Array.isArray(batchResult.data)) {
        batchResult.data.slice(0, 5).forEach((page: unknown, i: number) => {
          const p = page as { metadata?: { title?: string; sourceURL?: string } };
          console.log(chalk.cyan(`\n[${i + 1}] ${p.metadata?.title || 'Untitled'}`));
          console.log(chalk.gray(p.metadata?.sourceURL || ''));
        });
        if (batchResult.data.length > 5) {
          console.log(chalk.gray(`\n... and ${batchResult.data.length - 5} more pages`));
        }
      }

      saveOutput(result, options.output);
    } catch (error: unknown) {
      spinner.fail('Batch scrape failed');
      const err = error as { response?: { data?: { error?: string } }; message?: string };
      console.error(chalk.red(err.response?.data?.error || err.message || 'Unknown error'));
      process.exit(1);
    }
  });

// Status command - check job status
program
  .command('status <type> <id>')
  .description('Check status of a crawl, extract, or batch job')
  .option('-o, --output <file>', 'Save results to file')
  .action(async (type, id, options) => {
    const spinner = ora('Checking status...').start();
    const client = getClient();

    try {
      const endpoints: Record<string, string> = {
        crawl: '/crawl',
        extract: '/extract',
        batch: '/batch/scrape',
      };

      const endpoint = endpoints[type];
      if (!endpoint) {
        throw new Error(`Invalid type: ${type}. Use: crawl, extract, or batch`);
      }

      const response = await client.get(`${endpoint}/${id}`);
      spinner.succeed('Status retrieved');

      const { status, total, completed, data, creditsUsed } = response.data;

      console.log(chalk.bold(`\n📊 Job Status: ${status}`));
      if (total !== undefined) {
        console.log(chalk.gray(`Progress: ${completed || 0}/${total} pages`));
      }
      if (creditsUsed !== undefined) {
        console.log(chalk.gray(`Credits used: ${creditsUsed}`));
      }
      if (data?.length) {
        console.log(chalk.gray(`Results: ${data.length} items`));
      }

      saveOutput(response.data, options.output);
    } catch (error: unknown) {
      spinner.fail('Status check failed');
      const err = error as { response?: { data?: { error?: string } }; message?: string };
      console.error(chalk.red(err.response?.data?.error || err.message || 'Unknown error'));
      process.exit(1);
    }
  });

// Search command - web search with optional scraping
program
  .command('search <query>')
  .description('Search the web and optionally scrape results')
  .option('-l, --limit <number>', 'Maximum results', '5')
  .option('--scrape', 'Scrape content from search results', false)
  .option('--scrape-formats <formats>', 'Formats when scraping: markdown,html,links', 'markdown')
  .option('--tbs <value>', 'Time filter: qdr:h, qdr:d, qdr:w, qdr:m, qdr:y')
  .option('--location <location>', 'Geographic location')
  .option('--country <code>', 'ISO country code', 'US')
  .option('-o, --output <file>', 'Save results to file')
  .option('--json', 'Output as JSON')
  .action(async (query, options) => {
    const spinner = ora('Searching...').start();
    const client = getClient();

    try {
      const payload: Record<string, unknown> = {
        query,
        limit: parseInt(options.limit),
      };

      if (options.scrape) {
        payload.scrapeOptions = {
          formats: options.scrapeFormats.split(',').map((f: string) => f.trim()),
        };
      }
      if (options.tbs) {
        payload.tbs = options.tbs;
      }
      if (options.location) {
        payload.location = options.location;
      }
      if (options.country) {
        payload.country = options.country;
      }

      const response = await client.post('/search', payload);
      spinner.succeed('Search complete');

      const { data } = response.data;
      console.log(chalk.bold(`\n🔍 Found ${data?.length || 0} results`));

      if (options.json) {
        console.log(JSON.stringify(response.data, null, 2));
      } else if (data && Array.isArray(data)) {
        data.forEach((result: { title?: string; url?: string; description?: string; markdown?: string }, i: number) => {
          console.log(chalk.cyan(`\n[${i + 1}] ${result.title || 'Untitled'}`));
          console.log(chalk.gray(result.url || ''));
          if (result.description) {
            console.log(result.description.slice(0, 200));
          }
          if (result.markdown && options.scrape) {
            console.log(chalk.yellow('\n--- Content Preview ---'));
            console.log(result.markdown.slice(0, 300) + '...');
          }
        });
      }

      saveOutput(response.data, options.output);
    } catch (error: unknown) {
      spinner.fail('Search failed');
      const err = error as { response?: { data?: { error?: string } }; message?: string };
      console.error(chalk.red(err.response?.data?.error || err.message || 'Unknown error'));
      process.exit(1);
    }
  });

// Main execution
const main = async () => {
  await checkStatus();
  program.parse();
};

main();
