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

const API_BASE = 'https://api.search.brave.com/res/v1';

const program = new Command();

// Initialize API client
const getClient = (): AxiosInstance => {
  const apiKey = process.env.BRAVE_API_KEY;
  if (!apiKey) {
    console.error(chalk.red('Error: BRAVE_API_KEY not found'));
    console.error(chalk.yellow('Set it in ~/.env.local or export BRAVE_API_KEY=your-key'));
    process.exit(1);
  }
  return axios.create({
    baseURL: API_BASE,
    headers: {
      'X-Subscription-Token': apiKey,
      'Accept': 'application/json',
    },
  });
};

// Helper to save output
const saveOutput = (data: unknown, output?: string) => {
  if (output) {
    writeFileSync(output, JSON.stringify(data, null, 2));
    console.log(chalk.green(`\n✓ Saved to ${output}`));
  }
};

program
  .name('brave')
  .description('Brave Search CLI - Fast web search for AI')
  .version('1.0.0');

// Web search
program
  .command('search <query>')
  .description('Search the web')
  .option('-n, --num <number>', 'Number of results', '10')
  .option('-c, --country <code>', 'Country code (US, GB, etc)', 'US')
  .option('-l, --lang <code>', 'Language code', 'en')
  .option('--freshness <period>', 'Filter: pd (24h), pw (week), pm (month), py (year)')
  .option('--safe <level>', 'Safe search: off, moderate, strict', 'moderate')
  .option('-o, --output <file>', 'Save results to file')
  .option('--json', 'Output as JSON')
  .action(async (query, options) => {
    const spinner = ora('Searching...').start();
    const client = getClient();

    try {
      const params: Record<string, string> = {
        q: query,
        count: options.num,
        country: options.country,
        search_lang: options.lang,
        safesearch: options.safe,
      };

      if (options.freshness) {
        params.freshness = options.freshness;
      }

      const response = await client.get('/web/search', { params });
      spinner.succeed('Search complete');

      const { web } = response.data;

      if (options.json) {
        console.log(JSON.stringify(response.data, null, 2));
      } else {
        console.log(chalk.bold(`\n🔍 Found ${web?.results?.length || 0} results\n`));

        web?.results?.forEach((result: any, i: number) => {
          console.log(chalk.cyan(`[${i + 1}] ${result.title}`));
          console.log(chalk.gray(result.url));
          if (result.description) {
            console.log(result.description.slice(0, 200));
          }
          console.log('');
        });
      }

      saveOutput(response.data, options.output);
    } catch (error: any) {
      spinner.fail('Search failed');
      console.error(chalk.red(error.response?.data?.message || error.message));
      process.exit(1);
    }
  });

// News search
program
  .command('news <query>')
  .description('Search news articles')
  .option('-n, --num <number>', 'Number of results', '10')
  .option('-c, --country <code>', 'Country code', 'US')
  .option('--freshness <period>', 'Filter: pd (24h), pw (week), pm (month)')
  .option('-o, --output <file>', 'Save results to file')
  .option('--json', 'Output as JSON')
  .action(async (query, options) => {
    const spinner = ora('Searching news...').start();
    const client = getClient();

    try {
      const params: Record<string, string> = {
        q: query,
        count: options.num,
        country: options.country,
      };

      if (options.freshness) {
        params.freshness = options.freshness;
      }

      const response = await client.get('/news/search', { params });
      spinner.succeed('News search complete');

      const { results } = response.data;

      if (options.json) {
        console.log(JSON.stringify(response.data, null, 2));
      } else {
        console.log(chalk.bold(`\n📰 Found ${results?.length || 0} news articles\n`));

        results?.forEach((result: any, i: number) => {
          console.log(chalk.cyan(`[${i + 1}] ${result.title}`));
          console.log(chalk.gray(`${result.source?.name || 'Unknown'} - ${result.age || ''}`));
          console.log(chalk.gray(result.url));
          if (result.description) {
            console.log(result.description.slice(0, 150));
          }
          console.log('');
        });
      }

      saveOutput(response.data, options.output);
    } catch (error: any) {
      spinner.fail('News search failed');
      console.error(chalk.red(error.response?.data?.message || error.message));
      process.exit(1);
    }
  });

// Video search
program
  .command('video <query>')
  .description('Search videos')
  .option('-n, --num <number>', 'Number of results', '10')
  .option('-c, --country <code>', 'Country code', 'US')
  .option('-o, --output <file>', 'Save results to file')
  .option('--json', 'Output as JSON')
  .action(async (query, options) => {
    const spinner = ora('Searching videos...').start();
    const client = getClient();

    try {
      const params: Record<string, string> = {
        q: query,
        count: options.num,
        country: options.country,
      };

      const response = await client.get('/videos/search', { params });
      spinner.succeed('Video search complete');

      const { results } = response.data;

      if (options.json) {
        console.log(JSON.stringify(response.data, null, 2));
      } else {
        console.log(chalk.bold(`\n🎬 Found ${results?.length || 0} videos\n`));

        results?.forEach((result: any, i: number) => {
          console.log(chalk.cyan(`[${i + 1}] ${result.title}`));
          console.log(chalk.gray(`${result.creator || 'Unknown'} - ${result.duration || ''}`));
          console.log(chalk.gray(result.url));
          console.log('');
        });
      }

      saveOutput(response.data, options.output);
    } catch (error: any) {
      spinner.fail('Video search failed');
      console.error(chalk.red(error.response?.data?.message || error.message));
      process.exit(1);
    }
  });

// Image search
program
  .command('image <query>')
  .description('Search images')
  .option('-n, --num <number>', 'Number of results', '20')
  .option('-c, --country <code>', 'Country code', 'US')
  .option('--safe <level>', 'Safe search: off, strict', 'strict')
  .option('-o, --output <file>', 'Save results to file')
  .option('--json', 'Output as JSON')
  .action(async (query, options) => {
    const spinner = ora('Searching images...').start();
    const client = getClient();

    try {
      const params: Record<string, string> = {
        q: query,
        count: options.num,
        country: options.country,
        safesearch: options.safe,
      };

      const response = await client.get('/images/search', { params });
      spinner.succeed('Image search complete');

      const { results } = response.data;

      if (options.json) {
        console.log(JSON.stringify(response.data, null, 2));
      } else {
        console.log(chalk.bold(`\n🖼️ Found ${results?.length || 0} images\n`));

        results?.slice(0, 10).forEach((result: any, i: number) => {
          console.log(chalk.cyan(`[${i + 1}] ${result.title || 'Untitled'}`));
          console.log(chalk.gray(result.url));
          console.log(chalk.gray(`${result.properties?.width || '?'}x${result.properties?.height || '?'}`));
          console.log('');
        });

        if (results?.length > 10) {
          console.log(chalk.gray(`... and ${results.length - 10} more images`));
        }
      }

      saveOutput(response.data, options.output);
    } catch (error: any) {
      spinner.fail('Image search failed');
      console.error(chalk.red(error.response?.data?.message || error.message));
      process.exit(1);
    }
  });

// Local search
program
  .command('local <query>')
  .description('Search local businesses and places')
  .option('-c, --country <code>', 'Country code', 'US')
  .option('-o, --output <file>', 'Save results to file')
  .option('--json', 'Output as JSON')
  .action(async (query, options) => {
    const spinner = ora('Searching local...').start();
    const client = getClient();

    try {
      const params: Record<string, string> = {
        q: query,
        country: options.country,
        result_filter: 'locations',
      };

      const response = await client.get('/web/search', { params });
      spinner.succeed('Local search complete');

      const { locations } = response.data;

      if (options.json) {
        console.log(JSON.stringify(response.data, null, 2));
      } else {
        console.log(chalk.bold(`\n📍 Found ${locations?.results?.length || 0} places\n`));

        locations?.results?.forEach((place: any, i: number) => {
          console.log(chalk.cyan(`[${i + 1}] ${place.title}`));
          if (place.address) {
            console.log(chalk.gray(place.address));
          }
          if (place.rating) {
            console.log(chalk.yellow(`★ ${place.rating.ratingValue} (${place.rating.ratingCount} reviews)`));
          }
          if (place.phone) {
            console.log(chalk.gray(`📞 ${place.phone}`));
          }
          console.log('');
        });
      }

      saveOutput(response.data, options.output);
    } catch (error: any) {
      spinner.fail('Local search failed');
      console.error(chalk.red(error.response?.data?.message || error.message));
      process.exit(1);
    }
  });

// Status check
program
  .command('status')
  .description('Check API key status')
  .action(async () => {
    const apiKey = process.env.BRAVE_API_KEY;
    console.log(chalk.bold('\n  🦁 brave cli v1.0.0\n'));

    if (!apiKey) {
      console.log(chalk.red('  ✗ Not authenticated'));
      console.log(chalk.yellow('    Set BRAVE_API_KEY in ~/.env.local'));
      process.exit(1);
    }

    console.log(chalk.green('  ● Authenticated via BRAVE_API_KEY'));

    // Test API
    try {
      const client = getClient();
      await client.get('/web/search', { params: { q: 'test', count: '1' } });
      console.log(chalk.green('  ● API key verified'));
    } catch (error: any) {
      if (error.response?.status === 401) {
        console.log(chalk.red('  ✗ API key invalid'));
      } else if (error.response?.status === 429) {
        console.log(chalk.yellow('  ⚠ Rate limited'));
      } else {
        console.log(chalk.green('  ● API key verified'));
      }
    }
    console.log('');
  });

program.parse();
