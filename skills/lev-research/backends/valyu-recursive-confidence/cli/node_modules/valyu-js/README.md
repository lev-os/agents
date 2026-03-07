# Valyu SDK

**Search for AIs**

Valyu's Deepsearch API gives AI the context it needs. Integrate trusted, high-quality public and proprietary sources, with full-text multimodal retrieval.

Get **$10 free credits** for the Valyu API when you sign up at [Valyu](https://platform.valyu.ai)!

_No credit card required._

## How does it work?

We do all the heavy lifting for you - one unified API for all data:

- **Academic & Research Content** - Access millions of scholarly papers and textbooks
- **Real-time Web Search** - Get the latest information from across the internet
- **Structured Financial Data** - Stock prices, market data, and financial metrics
- **Intelligent Reranking** - Results across all sources are automatically sorted by relevance
- **Transparent Pricing** - Pay only for what you use with clear CPM pricing

## Installation

Install the Valyu SDK using npm:

```bash
npm install valyu-js
```

## Quick Start

Here's what it looks like, make your first query in just 4 lines of code:

```javascript
const { Valyu } = require("valyu-js");

const valyu = new Valyu("your-api-key-here");

const response = await valyu.search(
  "Implementation details of agentic search-enhanced large reasoning models",
  {
    maxNumResults: 5, // Limit to top 5 results
    maxPrice: 10, // Maximum price per thousand queries (CPM)
  }
);

console.log(response);

// Feed the results to your AI agent as you would with other search APIs
```

## API Reference

### DeepResearch Method

The `deepresearch` namespace provides access to Valyu's AI-powered research agent that conducts comprehensive, multi-step research with citations and cost tracking.

```javascript
// Create a research task
const task = await valyu.deepresearch.create({
  query: "What are the latest developments in quantum computing?",
  model: "fast", // "fast" (Haiku) or "heavy" (thorough, Sonnet)
  outputFormats: ["markdown", "pdf"], // Output formats
});

// Wait for completion with progress updates
const result = await valyu.deepresearch.wait(task.deepresearch_id, {
  onProgress: (status) => {
    if (status.progress) {
      console.log(
        `Step ${status.progress.current_step}/${status.progress.total_steps}`
      );
    }
  },
});

console.log(result.output); // Markdown report
console.log(result.pdf_url); // PDF download URL
```

#### DeepResearch Methods

| Method                           | Description                               |
| -------------------------------- | ----------------------------------------- |
| `create(options)`                | Create a new research task                |
| `status(taskId)`                 | Get current status of a task              |
| `wait(taskId, options?)`         | Wait for task completion with polling     |
| `stream(taskId, callbacks)`      | Stream real-time updates                  |
| `list(options)`                  | List all your research tasks              |
| `update(taskId, instruction)`    | Add follow-up instruction to running task |
| `cancel(taskId)`                 | Cancel a running task                     |
| `delete(taskId)`                 | Delete a task                             |
| `togglePublic(taskId, isPublic)` | Make task publicly accessible             |

#### DeepResearch Create Options

| Parameter         | Type                      | Default        | Description                                   |
| ----------------- | ------------------------- | -------------- | --------------------------------------------- |
| `input`           | `string`                  | _required_     | Research query or task description            |
| `model`           | `"fast" \| "heavy"`       | `"fast"`       | Research model - fast or heavy (thorough)     |
| `outputFormats`   | `("markdown" \| "pdf")[]` | `["markdown"]` | Output formats for the report                 |
| `strategy`        | `string`                  | -              | Natural language research strategy            |
| `search`          | `object`                  | -              | Search configuration (type, sources)          |
| `urls`            | `string[]`                | -              | URLs to extract and analyze                   |
| `files`           | `FileAttachment[]`        | -              | PDF/image files to analyze                    |
| `mcpServers`      | `MCPServerConfig[]`       | -              | MCP tool server configurations                |
| `codeExecution`   | `boolean`                 | `true`         | Enable/disable code execution                 |
| `previousReports` | `string[]`                | -              | Previous report IDs for context (max 3)       |
| `webhookUrl`      | `string`                  | -              | HTTPS webhook URL for completion notification |
| `metadata`        | `Record<string, any>`     | -              | Custom metadata key-value pairs               |

#### DeepResearch Examples

**Basic Research:**

```javascript
const task = await valyu.deepresearch.create({
  query: "Summarize recent AI safety research",
  model: "fast",
});

const result = await valyu.deepresearch.wait(task.deepresearch_id);
console.log(result.output);
```

**With Custom Sources:**

```javascript
const task = await valyu.deepresearch.create({
  query: "Latest transformer architecture improvements",
  search: {
    searchType: "proprietary",
    includedSources: ["valyu/valyu-arxiv"],
  },
  model: "heavy",
  outputFormats: ["markdown", "pdf"],
});
```

**Streaming Updates:**

```javascript
await valyu.deepresearch.stream(task.deepresearch_id, {
  onProgress: (current, total) => {
    console.log(`Progress: ${current}/${total}`);
  },
  onMessage: (message) => {
    console.log("Agent:", message);
  },
  onComplete: (result) => {
    console.log("Complete! Cost:", result.usage.total_cost);
  },
});
```

**With File Analysis:**

```javascript
const task = await valyu.deepresearch.create({
  query: "Analyze these research papers and provide key insights",
  files: [
    {
      data: "data:application/pdf;base64,...",
      filename: "paper.pdf",
      mediaType: "application/pdf",
    },
  ],
  urls: ["https://arxiv.org/abs/2103.14030"],
});
```

### Batch API

The `batch` namespace allows you to process multiple DeepResearch tasks efficiently. Perfect for running large-scale research operations.

```javascript
// Create a batch
const batch = await valyu.batch.create({
  name: "Q4 Research Batch",
  mode: "fast", // "fast", "standard", or "heavy"
  outputFormats: ["markdown"],
});

// Add tasks to the batch
await valyu.batch.addTasks(batch.batch_id, {
  tasks: [
    { query: "What are the latest AI developments?" },
    { query: "Analyze climate change trends" },
    { query: "Review quantum computing progress" },
  ],
});

// Wait for completion
const result = await valyu.batch.waitForCompletion(batch.batch_id, {
  pollInterval: 10000, // Check every 10 seconds
  onProgress: (batch) => {
    console.log(`Progress: ${batch.counts.completed}/${batch.counts.total}`);
  },
});

console.log("Total cost:", result.cost);
```

#### Batch Methods

| Method                                 | Description                            |
| -------------------------------------- | -------------------------------------- |
| `create(options?)`                     | Create a new batch                     |
| `status(batchId)`                      | Get batch status and task counts       |
| `addTasks(batchId, options)`           | Add tasks to a batch                   |
| `listTasks(batchId)`                   | List all tasks in a batch              |
| `list()`                               | List all batches                       |
| `cancel(batchId)`                      | Cancel a batch and all pending tasks   |
| `waitForCompletion(batchId, options?)` | Wait for batch completion with polling |

#### Batch Create Options

| Parameter       | Type                              | Default        | Description                        |
| --------------- | --------------------------------- | -------------- | ---------------------------------- |
| `name`          | `string`                          | -              | Optional batch name                |
| `mode`          | `"fast" \| "standard" \| "heavy"` | `"standard"`   | DeepResearch mode for all tasks    |
| `outputFormats` | `("markdown" \| "pdf")[]`         | `["markdown"]` | Output formats                     |
| `search`        | `object`                          | -              | Search configuration for all tasks |
| `webhookUrl`    | `string`                          | -              | HTTPS URL for completion webhook   |
| `metadata`      | `object`                          | -              | Custom metadata key-value pairs    |

#### Batch Status Response

```javascript
{
  success: true,
  batch: {
    batch_id: "batch_xxx",
    status: "processing",  // "open", "processing", "completed", "cancelled"
    mode: "standard",  // "fast", "standard", or "heavy"
    name: "My Batch",
    counts: {
      total: 10,
      queued: 3,
      running: 2,
      completed: 4,
      failed: 1,
      cancelled: 0
    },
    cost: 0.20,  // Total cost (replaces usage object)
    created_at: "2025-01-10T12:00:00Z",  // ISO 8601 date-time string
    completed_at: "2025-01-10T12:30:00Z"  // ISO 8601 date-time string (when completed)
  }
}
```

### Search Method

The `search()` method is the core of the Valyu SDK. It accepts a query string as the first parameter, followed by optional configuration parameters.

```javascript
valyu.search(
  query, // Your search query
  {
    searchType: "all", // "all", "web", or "proprietary"
    maxNumResults: 10, // Maximum results to return (1-20)
    isToolCall: true, // Whether this is an AI tool call
    relevanceThreshold: 0.5, // Minimum relevance score (0-1)
    maxPrice: 30, // Maximum price per thousand queries (CPM)
    includedSources: [], // Specific sources to search
    excludeSources: [], // Sources/domains to exclude
    category: null, // Category filter
    startDate: null, // Start date (YYYY-MM-DD)
    endDate: null, // End date (YYYY-MM-DD)
    countryCode: null, // Country code filter
    responseLength: null, // Response length control
  }
);
```

### Parameters

| Parameter            | Type               | Default    | Description                                                            |
| -------------------- | ------------------ | ---------- | ---------------------------------------------------------------------- |
| `query`              | `string`           | _required_ | The search query string                                                |
| `searchType`         | `string`           | `"all"`    | Search scope: `"all"`, `"web"`, or `"proprietary"`                     |
| `maxNumResults`      | `number`           | `10`       | Maximum number of results to return (1-20)                             |
| `isToolCall`         | `boolean`          | `true`     | Whether this is an AI tool call (affects processing)                   |
| `relevanceThreshold` | `number`           | `0.5`      | Minimum relevance score for results (0.0-1.0)                          |
| `maxPrice`           | `number`           | `30`       | Maximum price per thousand queries in CPM                              |
| `includedSources`    | `string[]`         | `[]`       | Specific data sources or URLs to search                                |
| `excludeSources`     | `string[]`         | `[]`       | Data sources or URLs to exclude from search                            |
| `category`           | `string`           | `null`     | Category filter for results                                            |
| `startDate`          | `string`           | `null`     | Start date filter in YYYY-MM-DD format                                 |
| `endDate`            | `string`           | `null`     | End date filter in YYYY-MM-DD format                                   |
| `countryCode`        | `string`           | `null`     | Country code filter (e.g., "US", "GB", "JP", "ALL")                    |
| `responseLength`     | `string \| number` | `null`     | Response length: "short", "medium", "large", "max", or character count |

### Response Format

The search method returns a `SearchResponse` object with the following structure:

```javascript
{
    success: boolean,                           // Whether the search was successful
    error: string | null,                       // Error message if any
    tx_id: string,                             // Transaction ID for feedback
    query: string,                             // The original query
    results: SearchResult[],                   // List of search results
    results_by_source: {                       // Count of results by source type
        web: number,
        proprietary: number
    },
    total_deduction_pcm: number,               // Cost in CPM
    total_deduction_dollars: number,           // Cost in dollars
    total_characters: number                   // Total characters returned
}
```

Each `SearchResult` contains:

```javascript
{
    title: string,                             // Result title
    url: string,                              // Source URL
    content: string,                          // Full content
    description?: string,                     // Brief description
    source: string,                           // Source identifier
    price: number,                            // Cost for this result
    length: number,                           // Content length in characters
    relevance_score?: number,                 // Relevance score (0-1), not available in fast_mode or url_only
    data_type?: string,                       // "structured" or "unstructured"
    source_type?: string,                     // Source type identifier
    publication_date?: string,                // Publication date (YYYY-MM-DD)
    id?: string,                              // Unique result identifier
    image_url?: Record<string, string>        // Associated images
}
```

### Contents Method

The `contents()` method extracts clean, structured content from web pages with optional AI-powered data extraction and summarization. It accepts an array of URLs as the first parameter, followed by optional configuration parameters.

```javascript
valyu.contents(
  urls, // Array of URLs to process (max 10)
  {
    summary: false, // AI processing: false, true, string, or JSON schema
    extractEffort: "normal", // Extraction effort: "normal" or "high"
    responseLength: "short", // Content length control
    maxPriceDollars: null, // Maximum cost limit in USD
  }
);
```

### Parameters

| Parameter         | Type                          | Default    | Description                                                                                                                                  |
| ----------------- | ----------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `urls`            | `string[]`                    | _required_ | Array of URLs to process (maximum 10 URLs per request)                                                                                       |
| `summary`         | `boolean \| string \| object` | `false`    | AI summary configuration: `false` (raw content), `true` (auto summary), string (custom instructions), or JSON schema (structured extraction) |
| `extractEffort`   | `string`                      | `"normal"` | Extraction thoroughness: `"normal"` (fast) or `"high"` (more thorough but slower)                                                            |
| `responseLength`  | `string \| number`            | `"short"`  | Content length per URL: `"short"` (25k chars), `"medium"` (50k), `"large"` (100k), `"max"` (no limit), or custom number                      |
| `maxPriceDollars` | `number`                      | `null`     | Maximum cost limit in USD                                                                                                                    |

### Contents Response Format

The contents method returns a `ContentsResponse` object with the following structure:

```javascript
{
    success: boolean,                           // Request success status
    error: string | null,                       // Error message if any
    tx_id: string,                              // Transaction ID for tracking
    urls_requested: number,                     // Total URLs requested
    urls_processed: number,                     // Successfully processed URLs
    urls_failed: number,                        // Failed URL count
    results: ContentResult[],                   // Array of processed results
    total_cost_dollars: number,                 // Actual cost charged
    total_characters: number                    // Total characters extracted
}
```

Each `ContentResult` contains:

```javascript
{
    url: string,                                // Source URL
    title: string,                              // Page/document title
    content: string | number,                   // Extracted content
    length: number,                             // Content length in characters
    source: string,                             // Data source identifier
    summary?: string | object,                  // AI-generated summary (if enabled)
    summary_success?: boolean,                  // Whether summary generation succeeded
    data_type?: string,                         // Type of data extracted
    image_url?: Record<string, string>,         // Extracted images
    citation?: string                           // APA-style citation
}
```

## Examples

### Basic Search

```javascript
const { Valyu } = require("valyu-js");

const valyu = new Valyu("your-api-key");

// Simple search across all sources
const response = await valyu.search("What is machine learning?");
console.log(`Found ${response.results.length} results`);
```

### Academic Research

```javascript
// Search academic papers on arXiv
const response = await valyu.search("transformer architecture improvements", {
  searchType: "proprietary",
  includedSources: ["valyu/valyu-arxiv"],
  relevanceThreshold: 0.6,
  maxNumResults: 10,
});
```

### Web Search with Date Filtering

```javascript
// Search recent web content
const response = await valyu.search("AI safety developments", {
  searchType: "web",
  startDate: "2024-01-01",
  endDate: "2024-12-31",
  maxNumResults: 5,
});
```

### Hybrid Search

```javascript
// Search both web and proprietary sources
const response = await valyu.search("quantum computing breakthroughs", {
  searchType: "all",
  category: "technology",
  relevanceThreshold: 0.6,
  maxPrice: 50,
});
```

### Processing Results

```javascript
const response = await valyu.search("climate change solutions");

if (response.success) {
  console.log(`Search cost: $${response.total_deduction_dollars.toFixed(4)}`);
  console.log(
    `Sources: Web=${response.results_by_source.web}, Proprietary=${response.results_by_source.proprietary}`
  );

  response.results.forEach((result, i) => {
    console.log(`\n${i + 1}. ${result.title}`);
    console.log(`   Source: ${result.source}`);
    if (result.relevance_score !== undefined) {
      console.log(`   Relevance: ${result.relevance_score.toFixed(2)}`);
    }
    console.log(`   Content: ${result.content.substring(0, 200)}...`);
  });
} else {
  console.log(`Search failed: ${response.error}`);
}
```

### Content Extraction Examples

#### Basic Content Extraction

```javascript
// Extract raw content from URLs
const response = await valyu.contents([
  "https://techcrunch.com/2025/08/28/anthropic-users-face-a-new-choice-opt-out-or-share-your-data-for-ai-training/",
]);

if (response.success) {
  response.results.forEach((result) => {
    console.log(`Title: ${result.title}`);
    console.log(`Content: ${result.content.substring(0, 500)}...`);
  });
}
```

#### Content with AI Summary

```javascript
// Extract content with automatic summarization
const response = await valyu.contents(["https://docs.python.org/3/tutorial/"], {
  summary: true,
  responseLength: "max",
});

response.results.forEach((result) => {
  console.log(`Summary: ${result.summary}`);
});
```

#### Structured Data Extraction

```javascript
// Extract structured data using JSON schema
const companySchema = {
  type: "object",
  properties: {
    company_name: { type: "string" },
    founded_year: { type: "integer" },
    key_products: {
      type: "array",
      items: { type: "string" },
      maxItems: 3,
    },
  },
};

const response = await valyu.contents(
  ["https://en.wikipedia.org/wiki/OpenAI"],
  {
    summary: companySchema,
    responseLength: "max",
  }
);

if (response.success) {
  response.results.forEach((result) => {
    if (result.summary) {
      console.log(
        `Structured data: ${JSON.stringify(result.summary, null, 2)}`
      );
    }
  });
}
```

#### Multiple URLs

```javascript
// Process multiple URLs with a cost limit
const response = await valyu.contents(
  [
    "https://www.valyu.ai/",
    "https://docs.valyu.ai/overview",
    "https://www.valyu.ai/blogs/why-ai-agents-and-llms-struggle-with-search-and-data-access",
  ],
  {
    summary:
      "Provide key takeaways in bullet points, and write in very emphasised singaporean english",
  }
);

console.log(
  `Processed ${response.urls_processed}/${response.urls_requested} URLs`
);
console.log(`Cost: $${response.total_cost_dollars.toFixed(4)}`);
```

## Authentication

Set your API key in one of these ways:

1. **Environment variable** (recommended):

   ```bash
   export VALYU_API_KEY="your-api-key-here"
   ```

2. **Direct initialization**:
   ```javascript
   const valyu = new Valyu("your-api-key-here");
   ```

## Error Handling

The SDK handles errors gracefully and returns structured error responses:

```javascript
const response = await valyu.search("test query");

if (!response.success) {
  console.log(`Error: ${response.error}`);
  console.log(`Transaction ID: ${response.tx_id}`);
} else {
  // Process successful results
  response.results.forEach((result) => {
    console.log(result.title);
  });
}
```

## TypeScript Support

The SDK includes full TypeScript support with type definitions for all parameters:

```typescript
import {
  Valyu,
  SearchOptions,
  SearchResponse,
  ContentsOptions,
  ContentsResponse,
  CountryCode,
  ResponseLength,
} from "valyu";

const valyu = new Valyu("your-api-key");

// Search API with types
const searchOptions: SearchOptions = {
  searchType: "proprietary",
  maxNumResults: 10,
  relevanceThreshold: 0.6,
  excludeSources: ["reddit.com", "twitter.com"],
  countryCode: "US" as CountryCode,
  responseLength: "medium" as ResponseLength,
};

const searchResponse: SearchResponse = await valyu.search(
  "machine learning",
  searchOptions
);

// Contents API with types
const contentsOptions: ContentsOptions = {
  summary: true,
  extractEffort: "high",
  responseLength: "medium",
  maxPriceDollars: 0.1,
};

const contentsResponse: ContentsResponse = await valyu.contents(
  ["https://example.com"],
  contentsOptions
);
```

## Backward Compatibility

The legacy `context()` method is still supported but deprecated:

```javascript
// Legacy method (deprecated)
const response = await valyu.context("neural networks basics", {
  searchType: "all",
  maxNumResults: 5,
  queryRewrite: true,
  similarityThreshold: 0.5,
  dataSources: ["valyu/valyu-arxiv"],
});
```

**Migration from v1 to v2:**

- `context()` → `search()`
- `similarityThreshold` → `relevanceThreshold`
- `dataSources` → `includedSources`
- `queryRewrite` → `isToolCall`
- Default `relevanceThreshold` changed from `0.4` to `0.5`
- Default `maxPrice` changed from `1` to `30`

## Getting Started

1. Sign up for a free account at [Valyu](https://platform.valyu.ai)
2. Get your API key from the dashboard
3. Install the SDK: `npm install valyu-js`
4. Start building with the examples above

## Testing

Run the integration tests:

```bash
npm run test:integration
```

Run the Search API examples:

```bash
node examples/search-examples.js
```

Run the Contents API examples:

```bash
node examples/contents-examples.js
```

## Support

- **Documentation**: [docs.valyu.ai](https://docs.valyu.ai)
- **API Reference**: Full parameter documentation above
- **Examples**: Check the `examples/` directory in this repository
- **Issues**: Report bugs on GitHub

## License

This project is licensed under the MIT License.
