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

      const incompleteHashes = db.prepare(`
        WITH expected_hashes AS (
          SELECT DISTINCT hash FROM documents
          WHERE active = 1 AND collection IN (${params})
        )
        SELECT h.hash, COUNT(cv.seq) AS chunks, MAX(cv.total_chunks) AS expected_chunks
        FROM expected_hashes h
        LEFT JOIN content_vectors cv
          ON cv.hash = h.hash AND cv.model = ? AND cv.embed_fingerprint = ?
        GROUP BY h.hash
      `).all(...approvedCollections, effectiveModel, fingerprint).filter((row) =>
        !row.expected_chunks || row.chunks < row.expected_chunks
      );
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
      const requiredVectors = db.prepare(`
        SELECT DISTINCT cv.hash, cv.seq
        FROM content_vectors cv
        JOIN (SELECT DISTINCT hash FROM documents WHERE active = 1 AND collection IN (${params})) h
          ON h.hash = cv.hash
        WHERE cv.model = ? AND cv.embed_fingerprint = ?
      `).iterate(...approvedCollections, effectiveModel, fingerprint);
      let missingVectorIds = 0;
      for (const row of requiredVectors) {
        if (!vectorKeys.has(`${row.hash}_${row.seq}`)) missingVectorIds++;
      }

      return {
        actualDocuments,
        expectedDocuments: expectedByKey.size,
        missingPaths,
        extraPaths,
        staleBodies,
        pendingEmbeddingHashes: incompleteHashes.length,
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
      const embedModel = qmdLlm.resolveEmbedModel(config.models);
      stage = "resolve cached model identity";
      const embedModelPath = await resolveModelFile(embedModel, {
        directory: qmdLlm.DEFAULT_MODEL_CACHE_DIR,
        download: false,
        cli: false,
      });
      stage = "inspect cached GGUF";
      const modelInspection = qmdLlm.inspectGgufFile(embedModelPath);
      if (!modelInspection.valid) {
        fail(`configured QMD embedding model is invalid: ${modelInspection.details || embedModelPath}`);
        return;
      }
      process.stdout.write(`${JSON.stringify({
        status: "inspected",
        collections,
        embedModel,
        embedModelPath,
      })}\n`);
    } catch (error) {
      fail(`cannot inspect QMD configuration during ${stage}: ${String(error?.message || error).slice(0, 400)}`);
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

await main();
