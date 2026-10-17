#!/usr/bin/env node

import { existsSync, readFileSync, realpathSync, statSync } from "node:fs";
import { createRequire } from "node:module";
import { join, relative, resolve, sep } from "node:path";
import { createHash } from "node:crypto";
import { pathToFileURL } from "node:url";

const approvedCollections = [
  "skills-db",
  "skills-db-bundle-docs",
  "skills-db-archive",
  "skills-db-backlog",
  "skills-db-workshop",
];
const approvedQueryCollections = ["skills-db", "skills-db-bundle-docs"];
const modelKinds = ["embed", "generate", "rerank"];

function fail(message, details = {}) {
  process.stdout.write(`${JSON.stringify({ status: "error", error: message, ...details })}\n`);
  process.exitCode = 1;
}

function seedOfficialRuntimeEnvironment() {
  if (process.platform === "darwin" && process.env.QMD_METAL_KEEP_RESIDENCY !== "1") {
    process.env.GGML_METAL_NO_RESIDENCY = process.env.GGML_METAL_NO_RESIDENCY || "1";
  }
  process.env.LLAMA_LOG_LEVEL = process.env.LLAMA_LOG_LEVEL || "error";
  process.env.GGML_LOG_LEVEL = process.env.GGML_LOG_LEVEL || "error";
  process.env.GGML_BACKEND_SILENT = process.env.GGML_BACKEND_SILENT || "1";
}

async function resolveConfiguredModels(config, qmdLlm, resolveModelFile) {
  const uris = {
    embed: qmdLlm.resolveEmbedModel(config.models),
    generate: qmdLlm.resolveGenerateModel(config.models),
    rerank: qmdLlm.resolveRerankModel(config.models),
  };
  const models = {};
  for (const kind of modelKinds) {
    const uri = uris[kind];
    if (typeof uri !== "string" || !uri) {
      throw integrityError("qmd_model_unavailable", `configured QMD ${kind} model URI is missing`);
    }
    let resolved;
    try {
      resolved = await resolveModelFile(uri, {
        directory: qmdLlm.DEFAULT_MODEL_CACHE_DIR,
        download: false,
        cli: false,
      });
    } catch (error) {
      throw integrityError(
        "qmd_model_unavailable",
        `configured QMD ${kind} model is not cached: ${String(error?.message || error).slice(0, 220)}`,
      );
    }
    if (typeof resolved !== "string" || !existsSync(resolved)) {
      throw integrityError("qmd_model_unavailable", `configured QMD ${kind} model is not cached: ${uri}`);
    }
    const path = realpathSync(resolved);
    const stats = statSync(path);
    const inspection = qmdLlm.inspectGgufFile(path);
    if (!stats.isFile() || !inspection?.valid) {
      throw integrityError(
        "qmd_model_unavailable",
        `configured QMD ${kind} model is not a valid cached GGUF: ${inspection?.details || path}`,
      );
    }
    models[kind] = {
      uri,
      path,
      sizeBytes: stats.size,
      mtimeMs: stats.mtimeMs,
      dev: stats.dev,
      ino: stats.ino,
    };
  }
  return models;
}

function integrityError(code, message) {
  const error = new Error(message);
  error.code = code;
  return error;
}

async function verifyIndexIntegrity(request, manifest) {
  if (
    !request ||
    typeof request.dbPath !== "string" ||
    typeof request.configPath !== "string" ||
    !request.roots ||
    JSON.stringify(request.collections) !== JSON.stringify(approvedCollections) ||
    typeof request.model !== "string" ||
    !Array.isArray(manifest?.documents) ||
    request.expectedDocuments !== manifest.documents.length
  ) {
    throw integrityError("qmd_index_integrity", "integrity request is malformed or unscoped");
  }
  if (!existsSync(request.dbPath) || !existsSync(request.configPath)) {
    throw integrityError("qmd_index_integrity", "QMD index or configuration is missing");
  }

  const packageRoot = join(
    process.env.QMD_PREFIX || join(process.env.HOME || "", ".local", "share", "qmd", "npm"),
    "lib", "node_modules", "@tobilu", "qmd",
  );
  const require = createRequire(join(packageRoot, "package.json"));
  const yaml = require("yaml");
  const Database = require("better-sqlite3");
  const sqliteVec = require("sqlite-vec");
  const config = yaml.parse(readFileSync(request.configPath, "utf8"));
  if (!config || typeof config !== "object" || !config.collections || typeof config.collections !== "object") {
    throw integrityError("qmd_index_integrity", "QMD configuration is malformed");
  }

  const roots = {};
  for (const name of approvedCollections) {
    const item = config.collections[name];
    if (!item || typeof item.path !== "string" || item.pattern !== "**/*.md") {
      throw integrityError("qmd_index_integrity", `QMD collection definition is invalid: ${name}`);
    }
    let actualRoot;
    let requestedRoot;
    try {
      actualRoot = realpathSync(item.path);
      requestedRoot = realpathSync(request.roots[name]);
    } catch {
      throw integrityError("qmd_index_integrity", `QMD collection root is unavailable: ${name}`);
    }
    if (actualRoot !== requestedRoot) {
      throw integrityError("qmd_index_integrity", `QMD collection root changed during integrity check: ${name}`);
    }
    roots[name] = actualRoot;
  }

  const qmdLlm = await import(pathToFileURL(join(packageRoot, "dist", "llm.js")).href);
  const { getEmbeddingFingerprint } = await import(pathToFileURL(join(packageRoot, "dist", "store.js")).href);
  const effectiveModel = qmdLlm.resolveEmbedModel(config.models);
  if (effectiveModel !== request.model) {
    throw integrityError("qmd_index_integrity", "configured QMD embedding model changed during integrity check");
  }
  const fingerprint = getEmbeddingFingerprint(effectiveModel);
  const expectedByKey = new Map();
  const expectedSourceIds = new Set();
  for (const item of manifest.documents) {
    if (
      !item ||
      typeof item.source_id !== "string" ||
      typeof item.source_relative_path !== "string" ||
      typeof item.file_path !== "string" ||
      typeof item.source_sha256 !== "string" ||
      !/^[a-f0-9]{64}$/.test(item.source_sha256) ||
      !approvedCollections.includes(item.collection) ||
      typeof item.path !== "string" ||
      item.source_id !== `skills-db/${item.source_relative_path}` ||
      item.source_relative_path.split("/").some((part) => !part || part === "." || part === "..") ||
      item.path.split("/").some((part) => !part || part === "." || part === "..")
    ) {
      throw integrityError("qmd_index_integrity", "canonical QMD manifest contains an invalid occurrence");
    }
    if (expectedSourceIds.has(item.source_id)) {
      throw integrityError("qmd_index_integrity", `duplicate canonical source ID: ${item.source_id}`);
    }
    expectedSourceIds.add(item.source_id);
    const key = `${item.collection}\0${item.path}`;
    if (expectedByKey.has(key)) {
      throw integrityError("qmd_index_integrity", `duplicate canonical QMD path: ${item.collection}/${item.path}`);
    }
    let filePath;
    try {
      filePath = realpathSync(item.file_path);
    } catch {
      throw integrityError("stale_qmd_index", `canonical source is missing: ${item.source_id}`);
    }
    const collectionRoot = roots[item.collection];
    const relative = relativePath(collectionRoot, filePath);
    if (relative == null || relative !== item.path) {
      throw integrityError("qmd_index_integrity", `canonical path does not map to its QMD occurrence: ${item.source_id}`);
    }
    let stats;
    let bytes;
    try {
      stats = statSync(filePath);
      if (!stats.isFile() || stats.size > 64 * 1024 * 1024) {
        throw integrityError("qmd_index_integrity", `canonical Markdown file exceeds the integrity read bound: ${item.source_id}`);
      }
      bytes = readFileSync(filePath);
    } catch (error) {
      if (error?.code) throw error;
      throw integrityError("stale_qmd_index", `canonical source cannot be read: ${item.source_id}`);
    }
    const sourceSha256 = createHash("sha256").update(bytes).digest("hex");
    if (sourceSha256 !== item.source_sha256) {
      throw integrityError("stale_qmd_index", `canonical source changed after catalog validation: ${item.source_id}`);
    }
    const normalizedBody = bytes.toString("utf8");
    const indexedBodySha256 = createHash("sha256").update(normalizedBody, "utf8").digest("hex");
    expectedByKey.set(key, { ...item, indexedBodySha256 });
  }

  let db;
  try {
    db = new Database(request.dbPath, { readonly: true, fileMustExist: true });
    sqliteVec.load(db);
    const snapshot = db.transaction(() => {
      const tableNames = new Set(db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all().map((row) => row.name));
      for (const required of ["documents", "content", "content_vectors", "vectors_vec"]) {
        if (!tableNames.has(required)) {
          throw integrityError("qmd_index_integrity", `QMD index is missing required table: ${required}`);
        }
      }
      const documentColumns = new Set(db.prepare("PRAGMA table_info(documents)").all().map((row) => row.name));
      const contentColumns = new Set(db.prepare("PRAGMA table_info(content)").all().map((row) => row.name));
      const vectorColumns = new Set(db.prepare("PRAGMA table_info(content_vectors)").all().map((row) => row.name));
      for (const column of ["collection", "path", "hash", "active"]) {
        if (!documentColumns.has(column)) throw integrityError("qmd_index_integrity", `QMD documents schema is missing ${column}`);
      }
      for (const column of ["hash", "doc"]) {
        if (!contentColumns.has(column)) throw integrityError("qmd_index_integrity", `QMD content schema is missing ${column}`);
      }
      for (const column of ["hash", "seq", "total_chunks", "model", "embed_fingerprint"]) {
        if (!vectorColumns.has(column)) throw integrityError("qmd_index_integrity", `QMD embedding schema is missing ${column}`);
      }

      const params = approvedCollections.map(() => "?").join(",");
      const actualRows = db.prepare(`
        SELECT d.collection, d.path, d.hash, c.doc AS body
        FROM documents d
        LEFT JOIN content c ON c.hash = d.hash
        WHERE d.active = 1 AND d.collection IN (${params})
      `).iterate(...approvedCollections);
      const seen = new Set();
      let actualDocuments = 0;
      let missingPaths = 0;
      let extraPaths = 0;
      let staleBodies = 0;
      const diagnostics = [];
      for (const row of actualRows) {
        actualDocuments++;
        const key = `${row.collection}\0${row.path}`;
        if (seen.has(key)) {
          extraPaths++;
          if (diagnostics.length < 8) diagnostics.push(`duplicate active QMD occurrence: ${row.collection}/${row.path}`);
          continue;
        }
        seen.add(key);
        const expected = expectedByKey.get(key);
        if (!expected) {
          extraPaths++;
          if (diagnostics.length < 8) diagnostics.push(`unowned active QMD occurrence: ${row.collection}/${row.path}`);
          continue;
        }
        if (!row.hash || typeof row.body !== "string") {
          staleBodies++;
          if (diagnostics.length < 8) diagnostics.push(`QMD content row is missing: ${expected.source_id}`);
          continue;
        }
        const bodySha256 = createHash("sha256").update(row.body, "utf8").digest("hex");
        if (bodySha256 !== expected.indexedBodySha256) {
          staleBodies++;
          if (diagnostics.length < 8) diagnostics.push(`QMD indexed body is stale: ${expected.source_id}`);
        }
      }
      for (const [key, expected] of expectedByKey) {
        if (!seen.has(key)) {
          missingPaths++;
          if (diagnostics.length < 8) diagnostics.push(`QMD occurrence is missing: ${expected.source_id}`);
        }
      }

      const ownedActiveHashes = new Set();
      for (const row of db.prepare(`
        SELECT DISTINCT hash FROM documents
        WHERE active = 1 AND collection IN (${params})
      `).iterate(...approvedCollections)) {
        if (typeof row.hash !== "string" || row.hash.length === 0) {
          throw integrityError("qmd_index_integrity", "QMD active document has an invalid content hash");
        }
        ownedActiveHashes.add(row.hash);
      }
      const metadataByHash = new Map();
      const requiredVectorIds = new Set();
      for (const row of db.prepare(`
        SELECT hash, seq, total_chunks
        FROM content_vectors
        WHERE model = ? AND embed_fingerprint = ?
      `).iterate(effectiveModel, fingerprint)) {
        if (!ownedActiveHashes.has(row.hash)) continue;
        const metadata = metadataByHash.get(row.hash) || { chunks: 0, expectedChunks: 0 };
        metadata.chunks++;
        metadata.expectedChunks = Math.max(metadata.expectedChunks, Number(row.total_chunks) || 0);
        metadataByHash.set(row.hash, metadata);
        requiredVectorIds.add(`${row.hash}_${row.seq}`);
      }
      let pendingEmbeddingHashes = 0;
      for (const hash of ownedActiveHashes) {
        const metadata = metadataByHash.get(hash);
        if (!metadata || !metadata.expectedChunks || metadata.chunks < metadata.expectedChunks) {
          pendingEmbeddingHashes++;
        }
      }
      const vectorKeys = new Set();
      for (const row of db.prepare("SELECT hash_seq FROM vectors_vec").iterate()) {
        if (typeof row.hash_seq !== "string") {
          throw integrityError("qmd_index_integrity", "QMD vector table contains an invalid identifier");
        }
        vectorKeys.add(row.hash_seq);
        if (vectorKeys.size > 2_000_000) {
          throw integrityError("qmd_index_integrity", "QMD vector ID scan exceeded its safety bound");
        }
      }
      let missingVectorIds = 0;
      for (const vectorId of requiredVectorIds) {
        if (!vectorKeys.has(vectorId)) missingVectorIds++;
      }

      return {
        actualDocuments,
        expectedDocuments: expectedByKey.size,
        missingPaths,
        extraPaths,
        staleBodies,
        pendingEmbeddingHashes,
        missingVectorIds,
        diagnostics,
      };
    });
    const audit = snapshot.deferred();
    if (audit.missingPaths || audit.extraPaths || audit.staleBodies) {
      throw integrityError("stale_qmd_index", `QMD canonical manifest mismatch: ${audit.diagnostics.join("; ")}`);
    }
    if (audit.pendingEmbeddingHashes || audit.missingVectorIds) {
      throw integrityError("qmd_index_integrity", `QMD embedding coverage is incomplete (pending=${audit.pendingEmbeddingHashes}, missing_vectors=${audit.missingVectorIds})`);
    }
    return {
      status: "integrity_checked",
      model: effectiveModel,
      fingerprint,
      ...audit,
    };
  } catch (error) {
    if (error?.code === "stale_qmd_index" || error?.code === "qmd_index_integrity") throw error;
    throw integrityError("qmd_index_integrity", `QMD read-only integrity check failed: ${String(error?.message || error).slice(0, 300)}`);
  } finally {
    if (db) db.close();
  }
}

function relativePath(root, file) {
  const relativeValue = relative(root, file);
  if (relativeValue === "" || relativeValue === "." || relativeValue.startsWith(`..${sep}`) || relativeValue === ".." || resolve(root, relativeValue) !== file) {
    return null;
  }
  return relativeValue.split(sep).join("/");
}

export function buildReadOnlyHybridStore({ db, cacheDb, llm, models, qmdStore }) {
  if (!db || !cacheDb || !llm || !models || !qmdStore) {
    throw integrityError("qmd_backend_error", "read-only QMD store dependencies are incomplete");
  }
  const failStage = (stage, error) =>
    integrityError("qmd_engine_failed", "QMD " + stage + " failed: " + String(error?.message || error).slice(0, 250));
  const vectorTable = db.prepare("SELECT sql FROM sqlite_master WHERE type='table' AND name='vectors_vec'").get();
  const dimensionMatch = vectorTable?.sql?.match(/float\[(\d+)\]/);
  const vectorDimension = dimensionMatch ? Number(dimensionMatch[1]) : null;
  if (vectorTable && (!Number.isSafeInteger(vectorDimension) || vectorDimension <= 0)) {
    throw integrityError("qmd_index_integrity", "QMD vector table has no valid embedding dimension");
  }

  const nativeExpand = llm.expandQuery.bind(llm);
  llm.expandQuery = async (...args) => {
    let swallowedFailure;
    const originalConsoleError = console.error;
    console.error = (...values) => {
      if (values[0] === "Structured query expansion failed:") {
        swallowedFailure = values[1] || new Error("QMD expansion failure was swallowed");
      }
      originalConsoleError(...values);
    };
    let expanded;
    try {
      expanded = await nativeExpand(...args);
    } catch (error) {
      throw failStage("query expansion", error);
    } finally {
      console.error = originalConsoleError;
    }
    if (swallowedFailure) throw failStage("query expansion", swallowedFailure);
    if (
      !Array.isArray(expanded) ||
      expanded.length === 0 ||
      expanded.some((item) =>
        !item ||
        !["lex", "vec", "hyde"].includes(item.type) ||
        typeof item.text !== "string" ||
        item.text.trim().length === 0
      )
    ) {
      throw integrityError("qmd_engine_failed", "QMD query expansion returned empty or malformed variants");
    }
    return expanded;
  };

  const nativeEmbedBatch = llm.embedBatch.bind(llm);
  llm.embedBatch = async (texts, ...args) => {
    let embeddings;
    try {
      embeddings = await nativeEmbedBatch(texts, ...args);
    } catch (error) {
      throw failStage("query embedding", error);
    }
    if (
      !Array.isArray(embeddings) ||
      embeddings.length !== texts.length ||
      embeddings.some((item) =>
        !item ||
        item.model !== llm.embedModelName ||
        !Array.isArray(item.embedding) ||
        item.embedding.length === 0 ||
        (vectorDimension !== null && item.embedding.length !== vectorDimension) ||
        item.embedding.some((value) => typeof value !== "number" || !Number.isFinite(value))
      )
    ) {
      throw integrityError("qmd_engine_failed", "QMD query embedding returned missing, incomplete, non-finite, or wrong-model vectors");
    }
    return embeddings;
  };

  const nativeRerank = llm.rerank.bind(llm);
  llm.rerank = async (query, documents, ...args) => {
    let response;
    try {
      response = await nativeRerank(query, documents, ...args);
    } catch (error) {
      throw failStage("reranking", error);
    }
    const expectedFiles = new Set(documents.map((document) => document.file));
    const actualFiles = new Set();
    if (
      !response ||
      response.model !== llm.rerankModelName ||
      !Array.isArray(response.results) ||
      response.results.length !== expectedFiles.size
    ) {
      throw integrityError("qmd_engine_failed", "QMD reranking returned a fallback or incomplete result");
    }
    for (const item of response.results) {
      if (
        !item ||
        typeof item.file !== "string" ||
        !expectedFiles.has(item.file) ||
        actualFiles.has(item.file) ||
        typeof item.score !== "number" ||
        !Number.isFinite(item.score)
      ) {
        throw integrityError("qmd_engine_failed", "QMD reranking returned an invalid or incomplete score");
      }
      actualFiles.add(item.file);
    }
    if (actualFiles.size !== expectedFiles.size) {
      throw integrityError("qmd_engine_failed", "QMD reranking omitted candidate files");
    }
    return response;
  };

  return {
    db,
    llm,
    searchFTS: (query, limit, collection) => qmdStore.searchFTS(db, query, limit, collection),
    searchVec: (query, model, limit, collection, session, embedding) =>
      qmdStore.searchVec(db, query, model, limit, collection, session, embedding, llm),
    expandQuery: async (query) => {
      const expanded = await qmdStore.expandQuery(query, models.generate.uri, cacheDb, llm);
      if (
        !Array.isArray(expanded) ||
        expanded.length === 0 ||
        expanded.some((item) =>
          !item ||
          !["lex", "vec", "hyde"].includes(item.type) ||
          typeof item.query !== "string" ||
          item.query.trim().length === 0
        )
      ) {
        throw integrityError("qmd_engine_failed", "QMD query expansion returned empty or malformed variants");
      }
      return expanded;
    },
    invalidateExpansionCache: (query) =>
      qmdStore.deleteExpansionCacheEntry(cacheDb, query, models.generate.uri),
    rerank: async (query, documents, _model, intent) => {
      const results = await qmdStore.rerank(query, documents, models.rerank.uri, cacheDb, intent, llm);
      const expectedFiles = new Set(documents.map((document) => document.file));
      const seenFiles = new Set();
      if (!Array.isArray(results) || results.length !== expectedFiles.size) {
        throw integrityError("qmd_engine_failed", "QMD reranking omitted candidate results");
      }
      for (const item of results) {
        if (
          !item ||
          !expectedFiles.has(item.file) ||
          seenFiles.has(item.file) ||
          typeof item.score !== "number" ||
          !Number.isFinite(item.score)
        ) {
          throw integrityError("qmd_engine_failed", "QMD reranking returned invalid or incomplete results");
        }
        seenFiles.add(item.file);
      }
      return results;
    },
    getContextForFile: (filepath) => qmdStore.getContextForFile(db, filepath),
  };
}

async function queryReadOnlyHybrid(request) {
  if (
    typeof request.dbPath !== "string" ||
    typeof request.configPath !== "string" ||
    typeof request.query !== "string" ||
    Buffer.byteLength(request.query, "utf8") === 0 ||
    Buffer.byteLength(request.query, "utf8") > 8192 ||
    JSON.stringify(request.collections) !== JSON.stringify(approvedQueryCollections) ||
    request.limit !== 50 ||
    request.candidateLimit !== 50 ||
    !request.roots ||
    !request.models
  ) {
    throw integrityError("qmd_backend_error", "QMD query request is malformed or unscoped");
  }

  const packageRoot = join(
    process.env.QMD_PREFIX || join(process.env.HOME || "", ".local", "share", "qmd", "npm"),
    "lib", "node_modules", "@tobilu", "qmd",
  );
  const require = createRequire(join(packageRoot, "package.json"));
  const packageJson = require(join(packageRoot, "package.json"));
  if (packageJson.version !== "2.8.3") {
    throw integrityError("qmd_backend_error", "unsupported QMD SDK version: " + packageJson.version);
  }
  const yaml = require("yaml");
  const Database = require("better-sqlite3");
  const sqliteVec = require("sqlite-vec");
  const config = yaml.parse(readFileSync(request.configPath, "utf8"));
  if (!config || typeof config !== "object" || !config.collections || typeof config.collections !== "object") {
    throw integrityError("qmd_backend_error", "QMD configuration is malformed");
  }
  const roots = {};
  for (const name of approvedQueryCollections) {
    const item = config.collections[name];
    if (!item || typeof item.path !== "string" || item.pattern !== "**/*.md") {
      throw integrityError("qmd_backend_error", "QMD query collection is invalid: " + name);
    }
    try {
      const configuredRoot = realpathSync(item.path);
      if (configuredRoot !== realpathSync(request.roots[name])) {
        throw integrityError("qmd_backend_error", "QMD query collection changed: " + name);
      }
      roots[name] = configuredRoot;
    } catch (error) {
      if (error?.code === "qmd_backend_error") throw error;
      throw integrityError("qmd_backend_error", "QMD query collection is unavailable: " + name);
    }
  }

  const qmdLlm = await import(pathToFileURL(join(packageRoot, "dist", "llm.js")).href);
  const qmdStore = await import(pathToFileURL(join(packageRoot, "dist", "store.js")).href);
  const nodeLlamaEntry = join(packageRoot, "node_modules", "node-llama-cpp", "dist", "index.js");
  const { resolveModelFile } = await import(pathToFileURL(nodeLlamaEntry).href);
  for (const name of ["hybridQuery", "searchFTS", "searchVec", "expandQuery", "deleteExpansionCacheEntry", "rerank", "getContextForFile", "parseVirtualPath"]) {
    if (typeof qmdStore[name] !== "function") {
      throw integrityError("qmd_backend_error", "installed QMD SDK lacks required query export: " + name);
    }
  }
  const models = await resolveConfiguredModels(config, qmdLlm, resolveModelFile);
  for (const kind of modelKinds) {
    const expected = request.models[kind];
    const actual = models[kind];
    if (
      !expected ||
      expected.uri !== actual.uri ||
      expected.path !== actual.path ||
      expected.sizeBytes !== actual.sizeBytes ||
      expected.mtimeMs !== actual.mtimeMs ||
      expected.dev !== actual.dev ||
      expected.ino !== actual.ino
    ) {
      throw integrityError("qmd_model_unavailable", "configured QMD " + kind + " model identity changed after preflight");
    }
  }
  const modelByUri = new Map(Object.values(models).map((model) => [model.uri, model]));

  let db;
  let cacheDb;
  let llm;
  let results;
  let failure;
  try {
    db = new Database(request.dbPath, { readonly: true, fileMustExist: true });
    sqliteVec.load(db);
    db.pragma("query_only = ON");
    cacheDb = new Database(":memory:");
    cacheDb.exec("CREATE TABLE llm_cache (hash TEXT PRIMARY KEY, result TEXT NOT NULL, created_at TEXT NOT NULL)");

    const LlamaCpp = qmdLlm.LlamaCpp;
    if (typeof LlamaCpp !== "function") {
      throw integrityError("qmd_backend_error", "installed QMD SDK lacks LlamaCpp");
    }
    llm = new LlamaCpp({
      embedModel: models.embed.uri,
      generateModel: models.generate.uri,
      rerankModel: models.rerank.uri,
      modelCacheDir: qmdLlm.DEFAULT_MODEL_CACHE_DIR,
      inactivityTimeoutMs: 0,
      disposeModelsOnInactivity: false,
    });
    const ensureLlamaWithoutBuild = llm.ensureLlama.bind(llm);
    llm.ensureLlama = async () => ensureLlamaWithoutBuild(false);
    llm.resolveModel = async (uri) => {
      const pinned = modelByUri.get(uri);
      if (!pinned) {
        throw integrityError("qmd_model_unavailable", "QMD requested an unvalidated model URI: " + String(uri));
      }
      let stats;
      try {
        stats = statSync(pinned.path);
      } catch {
        throw integrityError("qmd_model_unavailable", "prevalidated QMD model disappeared: " + pinned.uri);
      }
      if (
        !stats.isFile() ||
        realpathSync(pinned.path) !== pinned.path ||
        stats.size !== pinned.sizeBytes ||
        stats.mtimeMs !== pinned.mtimeMs ||
        stats.dev !== pinned.dev ||
        stats.ino !== pinned.ino ||
        !qmdLlm.inspectGgufFile(pinned.path)?.valid
      ) {
        throw integrityError("qmd_model_unavailable", "prevalidated QMD model changed before inference: " + pinned.uri);
      }
      return pinned.path;
    };

    const store = buildReadOnlyHybridStore({ db, cacheDb, llm, models, qmdStore });
    const nativeResults = await qmdStore.hybridQuery(store, request.query, {
      collection: approvedQueryCollections,
      limit: request.limit,
      candidateLimit: request.candidateLimit,
    });
    if (!Array.isArray(nativeResults)) {
      throw integrityError("qmd_backend_error", "QMD hybrid query returned a non-array result");
    }
    results = nativeResults.map((result) => {
      if (
        !result ||
        typeof result.file !== "string" ||
        typeof result.body !== "string" ||
        typeof result.title !== "string" ||
        typeof result.score !== "number" ||
        !Number.isFinite(result.score) ||
        result.score <= 0 ||
        result.score > 1
      ) {
        throw integrityError("qmd_backend_error", "QMD hybrid query returned an invalid candidate");
      }
      const parsed = qmdStore.parseVirtualPath(result.file);
      if (
        !parsed ||
        parsed.indexName ||
        !approvedQueryCollections.includes(parsed.collectionName) ||
        !parsed.path ||
        parsed.path.split("/").some((part) => !part || part === "." || part === "..")
      ) {
        throw integrityError("qmd_untrusted_source", "QMD returned an invalid virtual source path");
      }
      const root = roots[parsed.collectionName];
      let candidate;
      try {
        candidate = realpathSync(resolve(root, parsed.path));
      } catch {
        throw integrityError("qmd_untrusted_source", "QMD source path does not exist: " + parsed.collectionName + "/" + parsed.path);
      }
      const mapped = relativePath(root, candidate);
      if (mapped !== parsed.path || !statSync(candidate).isFile()) {
        throw integrityError("qmd_untrusted_source", "QMD source path escaped its collection: " + parsed.collectionName + "/" + parsed.path);
      }
      return { file: candidate, score: result.score, body: result.body, title: result.title };
    });
  } catch (error) {
    failure = error;
  } finally {
    for (const [name, cleanup] of [
      ["QMD model disposal", () => llm?.dispose()],
      ["QMD memory cache close", () => cacheDb?.close()],
      ["QMD read-only index close", () => db?.close()],
    ]) {
      try {
        await cleanup();
      } catch (error) {
        failure = failure || integrityError("qmd_backend_error", name + " failed: " + String(error?.message || error).slice(0, 250));
      }
    }
  }
  if (failure) throw failure;
  return results;
}

async function main() {
  let request;
  try {
    request = JSON.parse(process.argv[2] || "{}");
  } catch {
    fail("refresh request is malformed JSON");
    return;
  }
  if (!request || typeof request.configPath !== "string") {
    fail("QMD request must name the existing configuration file");
    return;
  }
  const packageRoot = join(
    process.env.QMD_PREFIX || join(process.env.HOME || "", ".local", "share", "qmd", "npm"),
    "lib", "node_modules", "@tobilu", "qmd",
  );
  if (!existsSync(request.configPath)) {
    fail("QMD configuration is missing");
    return;
  }

  if (request.operation === "query") {
    seedOfficialRuntimeEnvironment();
    try {
      const results = await queryReadOnlyHybrid(request);
      process.stdout.write(JSON.stringify({ status: "queried", results }) + "\n");
    } catch (error) {
      const code = ["qmd_engine_failed", "qmd_model_unavailable", "qmd_untrusted_source"].includes(error?.code)
        ? error.code
        : "qmd_backend_error";
      fail(String(error?.message || error).slice(0, 800), { code });
    }
    return;
  }

  if (request.operation === "integrity") {
    seedOfficialRuntimeEnvironment();
    try {
      const manifest = JSON.parse(readFileSync(0, "utf8"));
      const result = await verifyIndexIntegrity(request, manifest);
      process.stdout.write(`${JSON.stringify(result)}\n`);
    } catch (error) {
      const code = error?.code === "stale_qmd_index" ? "stale_qmd_index" : "qmd_index_integrity";
      fail(String(error?.message || error).slice(0, 800), { code });
    }
    return;
  }

  if (request.operation === "inspect") {
    let stage = "load configuration";
    try {
      stage = "seed official runtime settings";
      seedOfficialRuntimeEnvironment();
      stage = "create QMD package require";
      const require = createRequire(join(packageRoot, "package.json"));
      stage = "load YAML parser";
      const yaml = require("yaml");
      stage = "parse configuration";
      const config = yaml.parse(readFileSync(request.configPath, "utf8"));
      stage = "validate collection definitions";
      if (!config || typeof config !== "object" || !config.collections || typeof config.collections !== "object") {
        fail("QMD configuration must declare its existing collections");
        return;
      }
      const collections = {};
      for (const name of approvedCollections) {
        const item = config.collections[name];
        collections[name] = item && typeof item === "object"
          ? { path: item.path ?? null, pattern: item.pattern ?? null }
          : null;
      }
      stage = "load QMD model settings";
      const qmdLlm = await import(pathToFileURL(join(packageRoot, "dist", "llm.js")).href);
      const nodeLlamaEntry = join(packageRoot, "node_modules", "node-llama-cpp", "dist", "index.js");
      const { resolveModelFile } = await import(pathToFileURL(nodeLlamaEntry).href);
      stage = "resolve exact cached model identities";
      const models = await resolveConfiguredModels(config, qmdLlm, resolveModelFile);
      process.stdout.write(`${JSON.stringify({
        status: "inspected",
        collections,
        embedModel: models.embed.uri,
        embedModelPath: models.embed.path,
        models,
      })}\n`);
    } catch (error) {
      const code = typeof error?.code === "string" ? error.code : "qmd_backend_error";
      fail(`cannot inspect QMD configuration during ${stage}: ${String(error?.message || error).slice(0, 400)}`, { code });
    }
    return;
  }

  if (
    request.operation !== "refresh" ||
    typeof request.dbPath !== "string" ||
    JSON.stringify(request.collections) !== JSON.stringify(approvedCollections)
  ) {
    fail("refresh request does not match the approved skills-db scope");
    return;
  }
  if (request.force !== false || !Array.isArray(request.embedCollections) ||
      JSON.stringify(request.embedCollections) !== JSON.stringify(approvedCollections)) {
    fail("refresh request must embed pending documents one approved collection at a time without force");
    return;
  }

  // Match the official Darwin launcher before any QMD or llama.cpp module loads.
  seedOfficialRuntimeEnvironment();

  if (!existsSync(request.dbPath)) {
    fail("QMD index is missing");
    return;
  }
  const sdkEntry = join(packageRoot, "dist", "index.js");
  if (!existsSync(sdkEntry)) {
    fail("installed QMD SDK is missing");
    return;
  }

  let createStore;
  try {
    ({ createStore } = await import(pathToFileURL(sdkEntry).href));
  } catch (error) {
    fail(`cannot load the installed QMD SDK: ${String(error?.message || error).slice(0, 400)}`);
    return;
  }

  let store;
  let updateSummary = null;
  const embeds = [];
  let failureMessage = null;
  try {
    store = await createStore({ dbPath: request.dbPath, configPath: request.configPath });
    const update = await store.update({ collections: approvedCollections });
    updateSummary = {
      collections: update.collections,
      indexed: update.indexed,
      updated: update.updated,
      unchanged: update.unchanged,
      removed: update.removed,
      skipped: update.skipped,
    };
    if (update.collections !== approvedCollections.length || update.skipped !== 0) {
      failureMessage = "QMD update was incomplete";
    } else {
      for (const collection of approvedCollections) {
        const result = await store.embed({
          collection,
          force: false,
          maxDocsPerBatch: 50,
          maxBatchBytes: 16 * 1024 * 1024,
        });
        embeds.push({
          collection,
          force: false,
          docsProcessed: result.docsProcessed,
          chunksEmbedded: result.chunksEmbedded,
          errors: result.errors,
        });
        if (result.errors !== 0) {
          failureMessage = `QMD embedding was incomplete for ${collection}`;
          break;
        }
      }
    }
  } catch (error) {
    failureMessage = `QMD refresh failed: ${String(error?.message || error).slice(0, 400)}`;
  } finally {
    if (store) {
      try {
        await store.close();
      } catch (error) {
        failureMessage = failureMessage || `QMD close failed: ${String(error?.message || error).slice(0, 300)}`;
      }
    }
  }
  if (failureMessage) {
    fail(failureMessage, {
      ...(updateSummary ? { updatedCollections: approvedCollections, update: updateSummary } : {}),
      embeds,
    });
    return;
  }
  process.stdout.write(`${JSON.stringify({
    status: "complete",
    updatedCollections: approvedCollections,
    embedCollections: approvedCollections,
    force: false,
    update: updateSummary,
    embeds,
  })}\n`);
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  await main();
}
