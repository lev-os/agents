# Turborepo - Llms-Txt

**Pages:** 43

---

## Build the project

**URL:** llms-txt#build-the-project

COPY --from=prepare /app/out/full/ .

---

## Test each package that is:

**URL:** llms-txt#test-each-package-that-is:

---

## ENV TURBO_TEAM=$TURBO_TEAM

**URL:** llms-txt#env-turbo_team=$turbo_team

---

## ARG TURBO_TEAM

**URL:** llms-txt#arg-turbo_team

---

## Copy root package.json and lockfile

**URL:** llms-txt#copy-root-package.json-and-lockfile

COPY package.json ./
COPY package-lock.json ./

---

## Override Git comparison base

**URL:** llms-txt#override-git-comparison-base

TURBO_SCM_BASE=development turbo run build --affected

---

## Add lockfile and package.json's of isolated subworkspace

**URL:** llms-txt#add-lockfile-and-package.json's-of-isolated-subworkspace

---

## RUN yarn global add turbo@^2

**URL:** llms-txt#run-yarn-global-add-turbo@^2

RUN yarn global add turbo@^<your-major-version>
COPY . .

---

## Build '@acme/ui' if:

**URL:** llms-txt#build-'@acme/ui'-if:

---

## List only two packages

**URL:** llms-txt#list-only-two-packages

**Contents:**
- Flags
  - `--affected`
  - `--output <format>` <ExperimentalBadge />
- Options table
  - Caching
  - Messages
  - Task running and logs
  - Environment variables
  - Debugging outputs
  - Authentication

turbo ls web @repo/ui [package(s)]
bash title="Terminal"
TURBO_SCM_BASE=development turbo ls --affected
bash title="Terminal"
turbo ls --output=json
jsonc title="./apps/my-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      // Custom configuration for the build task in this package
    },
    "special-task": {} // New task specific to this package
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputs": ["dist/**"],
      "env": ["NODE_ENV"]
    }
  }
}
jsonc title="./apps/my-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      // This REPLACES the root outputs - "dist/**" is NOT included
      "outputs": [".next/**"]
    }
  }
}
jsonc title="./apps/my-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      // Inherits "dist/**" from root AND adds ".next/**"
      "outputs": ["$TURBO_EXTENDS$", ".next/**"]
    }
  }
}
jsonc title="./turbo.json"
{
  "futureFlags": {
    "nonRootExtends": true
  }
}
jsonc title="./apps/web/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      "outputs": [".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
jsonc title="./apps/docs/turbo.json"
{
  "extends": ["//", "web"],
  "tasks": {
    "build": {
      // Additional customization specific to this package
      "env": ["NEXT_PUBLIC_DOCS_URL"]
    }
  }
}
json title="./packages/shared-config/package.json"
    {
      "name": "shared-config",
      "private": true
    }
    jsonc title="./packages/shared-config/turbo.json"
    {
      "extends": ["//"],
      "tasks": {
        "build": {
          "outputs": ["dist/**"]
        },
        "dev": {
          "cache": false,
          "persistent": true
        }
      }
    }
    jsonc title="./apps/web/turbo.json"
    {
      "extends": ["//", "shared-config"],
      "tasks": {
        "build": {
          "env": ["MY_API_URL"]
        }
      }
    }
    jsonc title="./turbo.json"
{
  "futureFlags": {
    "nonRootExtends": true
  },
  "tasks": {
    "build": {},
    "lint": {},
    "test": {}
  }
}
jsonc title="./packages/ui/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "lint": {
      "extends": false // This package does not have a lint task
    }
  }
}
jsonc title="./packages/special-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      "extends": false, // Don't inherit from root
      "outputs": ["out/**"],
      "env": ["SPECIAL_VAR"]
    }
  }
}
jsonc title="./packages/base-config/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "lint": {
      "extends": false // Exclude lint from this config
    }
  }
}
jsonc title="./apps/web/turbo.json"
{
  "extends": ["//", "base-config"],
  "tasks": {
    // web does not inherit lint from root because base-config excluded it
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputs": [".next/**", "!.next/cache/**", ".svelte-kit/**"]
    }
  }
}
jsonc title="./apps/my-svelte-kit-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      "outputs": [".svelte-kit/**"]
    }
  }
}
diff title="./turbo.json"
{
  "tasks": {
    "build": {
-      "outputs": [".next/**", "!.next/cache/**", ".svelte-kit/**"]
+      "outputs": [".next/**", "!.next/cache/**"]
    }
  }
}
json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["compile"]
    },
    "compile": {}
  }
}
json title="./apps/my-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      "dependsOn": ["compile"]
    },
    "compile": {}
  }
}
diff title="./turbo.json"
{
  "tasks": {
+    "build": {}
-    "build": {
-      "dependsOn": ["compile"]
-    },
-    "compile": {}
  }
}
diff title="./apps/my-app/turbo.json"
{
+ "tags": ["my-tag"],
  "extends": ["//"],
  "tasks": {
    "build": {
      "dependsOn": ["compile"]
    },
    "compile": {}
  }
}
jsonc title="./apps/my-nextjs-app/turbo.json"
{
  "tasks": {
    "my-nextjs-app#build": {
      // This is not allowed. Even though it's
      // referencing the correct package, "my-nextjs-app"
      // is inferred, and we don't need to specify it again.
      // This syntax also has different behavior, so we do not want to allow it.
      // (see "Comparison to package-specific tasks" section)
    },
    "my-sveltekit-app#build": {
      // Changing configuration for the "my-sveltekit-app" package
      // from Package Configuration in "my-nextjs-app" is not allowed.
    },
    "build": {
      // Just use the task name!
    }
  }
}
jsonc title="./apps/my-nextjs-app/turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["some-pkg#compile"] // [!code highlight]
    }
  }
}
bash title="Terminal"
turbo prune [package]
bash title="Terminal"
turbo query [query] [flags]
bash title="Terminal"
turbo query
bash title="Terminal"
turbo query "query { packages { items { name } } }"
bash title="Terminal"
turbo query query.gql
bash title="Terminal"
turbo run [tasks] [options] [-- [args passed to tasks]]
bash title="Terminal"
turbo run
bash title="Terminal"
turbo run build lint test --affected
bash title="Terminal"

**Examples:**

Example 1 (unknown):
```unknown
## Flags

### `--affected`

Automatically filter to only packages that are affected by changes on the current branch.

By default the changes considered are those between `main` and `HEAD`.

* You can override `main` as the default base by setting `TURBO_SCM_BASE`.
* You can override `HEAD` as the default head by setting `TURBO_SCM_HEAD`.
```

Example 2 (unknown):
```unknown
### `--output <format>` <ExperimentalBadge />

Format to output the results. `json` or `pretty` (default)
```

Example 3 (unknown):
```unknown
- [Options overview](/reference/options-overview.md): Flags, configurations, and System Environment Variables for Turborepo

There are three ways to manage the behavior of a `turbo` invocation:

* [Configuration in `turbo.json`](/docs/reference/configuration)
* [System Environment Variables](/docs/reference/system-environment-variables)
* [Flags passed to the CLI invocation](/docs/reference/run)

The three strategies listed above are in order of precedence. Where a flag value is provided, for the same System Environment Variable or `turbo.json` configuration, the value for the flag will be used. Because of this, we recommend using:

* `turbo.json` configuration for defaults
* System Environment Variables for per-environment overrides
* Flags for per-invocation overrides

## Options table

### Caching

<div className="options-cheat-sheet-table">
  | Behavior                    | Flags                                                             | Environment Variables                                                                                                 | turbo.json                                                                 |
  | --------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
  | Force tasks to run          | [`--force`](/docs/reference/run#--force)                          | [`TURBO_FORCE`](/docs/reference/system-environment-variables#turbo_force)                                             | [`cache`](/docs/reference/configuration#cache)                             |
  | Remote Cache timeout        | [`--remote-cache-timeout`](/docs/reference/configuration#timeout) | [`TURBO_REMOTE_CACHE_TIMEOUT`](/docs/reference/system-environment-variables#turbo_remote_cache_timeout)               | [`remoteCache.timeout`](/docs/reference/configuration#timeout)             |
  | Remote Cache upload timeout | -                                                                 | [`TURBO_REMOTE_CACHE_UPLOAD_TIMEOUT`](/docs/reference/system-environment-variables#turbo_remote_cache_upload_timeout) | [`remoteCache.uploadTimeout`](/docs/reference/configuration#uploadtimeout) |
  | Cache signature key         | -                                                                 | [`TURBO_REMOTE_CACHE_SIGNATURE_KEY`](/docs/reference/system-environment-variables#turbo_remote_cache_signature_key)   | [`signature`](/docs/reference/configuration#signature)                     |
  | Preflight request           | [`--preflight`](/docs/reference/run#--preflight)                  | [`TURBO_PREFLIGHT`](/docs/reference/system-environment-variables#turbo_preflight)                                     | [`remoteCache.preflight`](/docs/reference/configuration#preflight)         |
  | Remote Cache base URL       | -                                                                 | [`TURBO_API`](/docs/reference/system-environment-variables#turbo_api)                                                 | [`remoteCache.apiUrl`](/docs/reference/configuration#remote-caching)       |
  | Cache sources               | [`--cache`](/docs/reference/run#--cache-options)                  | [`TURBO_CACHE`](/docs/reference/system-environment-variables#turbo_cache)                                             | -                                                                          |
  | Local cache directory       | [`--cache-dir`](/docs/reference/run#--cache-dir-path)             | [`TURBO_CACHE_DIR`](/docs/reference/system-environment-variables#turbo_cache_dir)                                     | [`cacheDir`](/docs/reference/configuration#cachedir)                       |
</div>

### Messages

<div className="options-cheat-sheet-table">
  | Behavior                       | Flags | Environment Variables                                                                                               | turbo.json                                                                                |
  | ------------------------------ | ----- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
  | Disable version print          | -     | [`TURBO_PRINT_VERSION_DISABLED`](/docs/reference/system-environment-variables#turbo_print_version_disabled)         | -                                                                                         |
  | Disable telemetry message      | -     | [`TURBO_TELEMETRY_MESSAGE_DISABLED`](/docs/reference/system-environment-variables#turbo_telemetry_message_disabled) | -                                                                                         |
  | Disable global `turbo` warning | -     | [`TURBO_GLOBAL_WARNING_DISABLED`](/docs/reference/system-environment-variables#turbo_global_warning_disabled)       | -                                                                                         |
  | No update notifier             | -     | [`TURBO_NO_UPDATE_NOTIFIER`](/docs/reference/system-environment-variables#turbo_no_update_notifier)                 | [`noUpdateNotifier`](https://turborepo.com/docs/reference/configuration#noupdatenotifier) |
</div>

### Task running and logs

<div className="options-cheat-sheet-table">
  | Behavior                          | Flags                                                                                                            | Environment Variables                                                                                                                             | turbo.json                                                                                                     |
  | --------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
  | Terminal UI                       | [`--ui`](/docs/reference/run#--ui)                                                                               | [`TURBO_UI`](/docs/reference/system-environment-variables#turbo_ui)                                                                               | [`ui`](/docs/reference/configuration#ui)                                                                       |
  | Run affected tasks                | [`--affected`](/docs/reference/run#--affected)                                                                   | -                                                                                                                                                 | -                                                                                                              |
  | Disable package manager check     | [`--dangerously-disable-package-manager-check`](/docs/reference/run#--dangerously-disable-package-manager-check) | [`TURBO_DANGEROUSLY_DISABLE_PACKAGE_MANAGER_CHECK`](/docs/reference/system-environment-variables#turbo_dangerously_disable_package_manager_check) | [`dangerouslyDisablePackageManagerCheck`](/docs/reference/configuration#dangerouslydisablepackagemanagercheck) |
  | Affected base ref                 | -                                                                                                                | [`TURBO_SCM_BASE`](/docs/reference/system-environment-variables#turbo_scm_base)                                                                   | -                                                                                                              |
  | Affected head ref                 | -                                                                                                                | [`TURBO_SCM_HEAD`](/docs/reference/system-environment-variables#turbo_scm_head)                                                                   | -                                                                                                              |
  | Only run directly specified tasks | [`--only`](/docs/reference/run#--only)                                                                           | -                                                                                                                                                 | -                                                                                                              |
  | Task concurrency                  | [`--concurrency`](/docs/reference/run#--concurrency-number--percentage)                                          | [`TURBO_CONCURRENCY`](/docs/reference/system-environment-variables#turbo_concurrency)                                                             | -                                                                                                              |
  | Task log order                    | [`--log-order`](/docs/reference/run#--log-order-option)                                                          | [`TURBO_LOG_ORDER`](/docs/reference/system-environment-variables#turbo_log_order)                                                                 | -                                                                                                              |
  | Current working directory         | [`--cwd`](/docs/reference/run#--cwd-path)                                                                        | -                                                                                                                                                 | -                                                                                                              |
  | Streamed logs prefix              | [`--log-prefix`](/docs/reference/run#--log-prefix-option)                                                        | -                                                                                                                                                 | -                                                                                                              |
  | Task logs output level            | [`--output-logs-option`](/docs/reference/run#--output-logs-option)                                               | -                                                                                                                                                 | [`outputLogs`](/docs/reference/configuration#outputlogs)                                                       |
  | Global inputs                     | [`--global-deps`](/docs/reference/run#--global-deps-file-glob)                                                   | -                                                                                                                                                 | [`globalDependencies`](/docs/reference/configuration#globaldependencies)                                       |
  | Terminal colors                   | [`--color`](/docs/reference#--color)                                                                             | [FORCE\_COLOR](/docs/reference/system-environment-variables#force_color)                                                                           | -                                                                                                              |
</div>

### Environment variables

<div className="options-cheat-sheet-table">
  | Behavior                      | Flags                                                                | Environment Variables                                                                             | turbo.json                                         |
  | ----------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
  | Environment variable mode     | [`--env-mode`](/docs/reference/run#--env-mode-option)                | -                                                                                                 | [`envMode`](/docs/reference/configuration#envmode) |
  | Vendor environment variables  | -                                                                    | [`TURBO_CI_VENDOR_ENV_KEY`](/docs/reference/system-environment-variables#turbo_ci_vendor_env_key) | -                                                  |
  | Framework variable exceptions | [`--framework-inference`](/docs/reference/run#--framework-inference) | -                                                                                                 | -                                                  |
</div>

### Debugging outputs

<div className="options-cheat-sheet-table">
  | Behavior            | Flags                                              | Environment Variables                                                                 | turbo.json |
  | ------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------- |
  | Run Summaries       | [`--summarize`](/docs/reference/run#--summarize)   | [`TURBO_RUN_SUMMARY`](/docs/reference/system-environment-variables#turbo_run_summary) | -          |
  | Graph visualization | [`--graph`](/docs/reference/run#--graph-file-name) | -                                                                                     | -          |
  | Dry run             | [`--dry`](/docs/reference/run#--dry----dry-run)    | -                                                                                     | -          |
</div>

### Authentication

<div className="options-cheat-sheet-table">
  | Behavior                                | Flags                                    | Environment Variables                                                       | turbo.json                                                       |
  | --------------------------------------- | ---------------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
  | Login URL                               | -                                        | [`TURBO_LOGIN`](/docs/reference/system-environment-variables#turbo_login)   | [`remoteCache.loginUrl`](/docs/reference/configuration#loginurl) |
  | Team name (for multi-team Remote Cache) | [`--team`](/docs/reference/run#--team)   | [`TURBO_TEAM`](/docs/reference/system-environment-variables#turbo_team)     | -                                                                |
  | Team ID (for multi-team Remote Cache)   | -                                        | [`TURBO_TEAMID`](/docs/reference/system-environment-variables#turbo_teamid) | -                                                                |
  | Authentication token                    | [`--token`](/docs/reference/run#--token) | [`TURBO_TOKEN`](/docs/reference/system-environment-variables#turbo_token)   | -                                                                |
</div>

### Other

<div className="options-cheat-sheet-table">
  | Behavior               | Flags                                                                      | Environment Variables                                                                                       | turbo.json                                       |
  | ---------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
  | Binary path            | -                                                                          | [`TURBO_BINARY_PATH`](/docs/reference/system-environment-variables#turbo_binary_path)                       | -                                                |
  | Download local `turbo` | -                                                                          | [`TURBO_DOWNLOAD_LOCAL_ENABLED`](/docs/reference/system-environment-variables#turbo_download_local_enabled) | -                                                |
  | Daemon                 | [`--daemon` / `--no-daemon`](/docs/reference/run#--daemon-and---no-daemon) | -                                                                                                           | [`daemon`](/docs/reference/configuration#daemon) |
</div>


- [Package Configurations](/reference/package-configurations.md): Learn how to use Package Configurations to bring greater task flexibility to your monorepo's package.

import { Callout } from '#components/callout';
import { ExperimentalBadge } from '#components/experimental-badge';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

Many monorepos can declare a `turbo.json` in the root directory with a
[task description](/docs/reference/configuration#tasks) that applies to all packages. But, sometimes, a monorepo can contain packages that need to configure their tasks differently.

To accommodate this, Turborepo enables you to extend the root configuration with a `turbo.json` in any package. This flexibility enables a more diverse set of apps and packages to co-exist in a Workspace, and allows package owners to maintain specialized tasks and configuration without affecting other apps and packages of the monorepo.

## How it works

To override the configuration for any task defined in the root `turbo.json`, add
a `turbo.json` file in any package of your monorepo with a top-level `extends`
key:
```

Example 4 (unknown):
```unknown
<Callout>
  By default, the only valid value for the `extends` key is `["//"]`. `//` is a
  special name used to identify the root directory of the monorepo. With the
  [`futureFlags.nonRootExtends`](/docs/reference/configuration#nonrootextends-pre-release)
  flag, you can also extend from other packages.
</Callout>

## Inheritance behavior

When a Package Configuration extends the root `turbo.json`, task properties are inherited differently depending on their type.

### Scalar fields are inherited

Scalar fields like `outputLogs`, `cache`, `persistent`, and `interactive` are **inherited** from the root configuration. You only need to specify them in a Package Configuration if you want to override them.

For example, if your root `turbo.json` sets `"outputLogs": "hash-only"` for a task, all packages inherit that setting automatically.

### Array fields replace by default

Array fields like `outputs`, `env`, `inputs`, `dependsOn`, and `passThroughEnv` **completely replace** the root configuration's values by default.
```

---

## Build everything that depends on changes between two Git SHAs

**URL:** llms-txt#build-everything-that-depends-on-changes-between-two-git-shas

turbo run build --filter=[a1b2c3d...e4f5g6h]

---

## Any packages in `apps` subdirectories except ./apps/admin

**URL:** llms-txt#any-packages-in-`apps`-subdirectories-except-./apps/admin

turbo run build --filter=./apps/* --filter=!./apps/admin

---

## Generate a partial monorepo with a pruned lockfile for a target workspace.

**URL:** llms-txt#generate-a-partial-monorepo-with-a-pruned-lockfile-for-a-target-workspace.

---

## Assuming "web" is the name entered in the project's package.json: { name: "web" }

**URL:** llms-txt#assuming-"web"-is-the-name-entered-in-the-project's-package.json:-{-name:-"web"-}

RUN turbo prune web --docker

---

## List all packages in the repository

**URL:** llms-txt#list-all-packages-in-the-repository

turbo ls
bash title="Terminal"

**Examples:**

Example 1 (unknown):
```unknown
When scoped to one or more packages, output includes package name, directory, internal dependencies, and all tasks.
```

---

## Copy the api package.json

**URL:** llms-txt#copy-the-api-package.json

COPY apps/api/package.json ./apps/api/package.json

---

## Create new versions of packages

**URL:** llms-txt#create-new-versions-of-packages

---

## Copy app source

**URL:** llms-txt#copy-app-source

**Contents:**
  - The lockfile changes too often
- The solution
  - The `--docker` flag
  - Example

CMD [ "node", "apps/api/server.js" ]
txt title=".dockerignore"
node_modules
npm-debug.log
bash title="Terminal"
turbo prune api --docker
bash title="Terminal"
docker build -f apps/web/Dockerfile .
docker title="./apps/web/Dockerfile"
FROM node:18-alpine AS base
RUN apk update
RUN apk add --no-cache libc6-compat

**Examples:**

Example 1 (unknown):
```unknown
This will copy the root `package.json` and the root lockfile to the Docker image. Then, it'll install dependencies, copy the app source and start the app.

You should also create a `.dockerignore` file to prevent node\_modules from being copied in with the app's source.
```

Example 2 (unknown):
```unknown
### The lockfile changes too often

Docker is pretty smart about how it deploys your apps. Just like Turborepo, it tries to do as [little work as possible](https://bitjudo.com/blog/2014/03/13/building-efficient-dockerfiles-node-dot-js/).

In our Dockerfile's case, it will only run `npm install` if the files it has in its image are *different* from the previous run. If not, it'll restore the `node_modules` directory it had before.

This means that whenever `package.json`, `apps/api/package.json` or `package-lock.json` change, the Docker image will run `npm install`.

This sounds great - until we realize something. The `package-lock.json` is *global* for the monorepo. That means that **if we install a new package inside `apps/web`, we'll cause `apps/api` to redeploy**.

In a large monorepo, this can result in a huge amount of lost time, as any change to a monorepo's lockfile cascades into tens or hundreds of deploys.

## The solution

The solution is to prune the inputs to the Dockerfile to only what is strictly necessary. Turborepo provides a simple solution - `turbo prune`.
```

Example 3 (unknown):
```unknown
Running this command creates a **pruned version of your monorepo** inside an `./out` directory. It only includes workspaces which `api` depends on. It also **prunes the lockfile** so that only the relevant `node_modules` will be downloaded.

### The `--docker` flag

By default, `turbo prune` puts all relevant files inside `./out`. But to optimize caching with Docker, we ideally want to copy the files over in two stages.

First, we want to copy over only what we need to install the packages. When running `--docker`, you'll find this inside `./out/json`.

<Files>
  <Folder name="out" defaultOpen>
    <Folder name="json" defaultOpen>
      <Folder name="apps" defaultOpen>
        <Folder name="api" defaultOpen>
          <File name="package.json" />
        </Folder>
      </Folder>

      <File name="package.json" />
    </Folder>

    <Folder name="full" defaultOpen>
      <Folder name="apps" defaultOpen>
        <Folder name="api" defaultOpen>
          <File name="server.js" />

          <File name="package.json" />
        </Folder>
      </Folder>

      <File name="package.json" />

      <File name="turbo.json" />
    </Folder>

    <File name="package-lock.json" />
  </Folder>
</Files>

Afterwards, you can copy the files in `./out/full` to add the source files.

Splitting up **dependencies** and **source files** in this way lets us **only run `npm install` when dependencies change** - giving us a much larger speedup.

<Callout type="info">
  Without `--docker`, all pruned files are placed inside `./out`.
</Callout>

### Example

Our detailed [`with-docker` example](https://github.com/vercel/turborepo/tree/main/examples/with-docker) goes into depth on how to use `prune` to its full potential. Here's the Dockerfile, copied over for convenience.

Build the Dockerfile from the root of your monorepo:
```

Example 4 (unknown):
```unknown
<Callout type="info">
  This Dockerfile is written for a [Next.js](https://nextjs.org/) app that is
  using the `standalone` [output
  mode](https://nextjs.org/docs/pages/api-reference/next-config-js/output).
</Callout>
```

---

## Uncomment and use build args to enable remote caching

**URL:** llms-txt#uncomment-and-use-build-args-to-enable-remote-caching

---

## - [Introduction](/index.md): Welcome to the Turborepo documentation!

**URL:** llms-txt#--[introduction](/index.md):-welcome-to-the-turborepo-documentation!

**Contents:**
- What is Turborepo?
- The monorepo problem
- The monorepo solution
- How to use these docs
- Join the community
- Package managers
- Platforms
- Node.js
- Version control
- LTS policy

Welcome to the Turborepo documentation!

## What is Turborepo?

Turborepo is a high-performance build system for JavaScript and TypeScript codebases. It is designed for scaling monorepos and also makes workflows in [single-package workspaces](/docs/guides/single-package-workspaces) faster, too.

From individual developers to the largest enterprise engineering organizations in the world, Turborepo is saving years of engineering time and millions of dollars in compute costs through a lightweight approach to optimizing the tasks you need to run in your repository.

## The monorepo problem

Monorepos have many advantages - but **they struggle to scale**. Each workspace has its own test suite, its own linting, and its own build process. A single monorepo might have **thousands of tasks to execute**.

![A representation of a typical monorepo. The first application took 110 seconds to complete its tasks. The second application took 140 seconds to complete its tasks. The shared package between them took 90 seconds to complete its tasks.](/images/docs/why-turborepo-problem.png)

These slowdowns can dramatically affect the way your teams build software, especially at scale. Feedback loops need to be fast so developers can deliver high-quality code quickly.

## The monorepo solution

![The monorepo from before using Turborepo, showing how it can hit cache to complete tasks for all three packages in 80 milliseconds.](/images/docs/why-turborepo-solution.png)

**Turborepo solves your monorepo's scaling problem**. [Remote Cache](/docs/core-concepts/remote-caching) stores the result of all your tasks, meaning that **your CI never needs to do the same work twice**.

Additionally, task scheduling can be difficult in a monorepo. You may need to build, *then* test, *then* lint...

Turborepo **schedules your tasks for maximum speed**, parallelizing work across all available cores.

Turborepo can be **adopted incrementally** and you can **add it to any repository in just a few minutes**. It uses the `package.json` scripts you've already written, the dependencies you've already declared, and a single `turbo.json` file. You can **use it with any package manager**, like `npm`, `yarn` or `pnpm` since Turborepo leans on the conventions of the npm ecosystem.

## How to use these docs

We will do our best to keep jargon to a minimum - but there are some need-to-know words that will be important to understand as you read through the docs. We've created [a glossary page](https://vercel.com/docs/vercel-platform/glossary) to help you out in case you're learning about these terms.

## Join the community

If you have questions about anything related to Turborepo, you're always welcome to ask the community on [GitHub Discussions](https://github.com/vercel/turborepo/discussions), [Vercel Community](https://community.vercel.com/tag/turborepo), and [Twitter](https://twitter.com/turborepo).

- [Support policy](/support-policy.md): Learn about Turborepo's Support policy.

import { Callout } from '#components/callout';

Core `turbo` functionality depends on the package managers in the JavaScript ecosystem and their implementations of Workspaces and
lockfile formats.

| Package manager | Support                            |
| --------------- | ---------------------------------- |
| pnpm 8+         | Stable                             |
| npm 8+          | Stable                             |
| yarn 1+         | Stable (Includes Yarn Plug'n'Play) |
| bun 1.2+        | Stable                             |

<Callout type="info">
  Package managers have their own release schedules, bugs, and features. While
  we intend to keep up with new major versions, we likely will not be able to
  release support immediately.
</Callout>

`turbo` is generally supported on Debian-based Linux distributions, macOS, and
Windows on both x86\_64 and ARM 64 architectures. Specifically, we build and ship
the following binaries via npm:

* `turbo-darwin-64` (macOS with Intel chips)
* `turbo-darwin-arm64` (macOS with Apple Silicon)
* `turbo-linux-64`
* `turbo-linux-arm64`
* `turbo-windows-64`\*
* `turbo-windows-arm64`\*

<small>
  \*: Requires [Windows C Runtime
  Libraries](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)
</small>

Core `turbo` functionality does not depend on the
active Node.js version on your system, but [some packages in the Turborepo ecosystem](/docs/reference#packages)
such as [`create-turbo`](/docs/reference/create-turbo), [`turbo-ignore`](/docs/reference/turbo-ignore), and [`eslint-config-turbo`](/docs/reference/eslint-config-turbo) do. For these features,
we intend to support the [Active and Maintenance LTS versions of Node.js](https://nodejs.org/en/about/previous-releases).

Turborepo's [examples](/docs/getting-started/examples) are also expected to work with these Node.js versions.

We support repositories that are version controlled with Git and repositories that don't have
version control at all. Any other version control system will be ignored.

Note that we use Git to hash files, so repositories without git may perform and behave differently.

Major versions of Turborepo will be supported for two years from the release date of the next major version.

Changes required for critical security fixes in older versions will be backported. Such situations will be rare and will land as semver-minor releases, even if they are breaking changes.

We highly encourage you to use the most current version of Turborepo whenever possible.

| Major version | Release date | End-of-life date |
| ------------- | ------------ | ---------------- |
| 2.x           | Jun. 4, 2024 | -                |
| 1.x           | Dec. 9, 2021 | Jun. 4, 2026     |

Stable builds of Turborepo follow semantic versioning (semver) and are thoroughly tested before being released.

Turborepo also offers specific APIs that may be released in an earlier phase of development. This is to allow early adopters to give valuable feedback and help the core team gain confidence in APIs ahead of their stable release. APIs that are available pre-stable will be marked as such in the documentation and within `turbo` itself whenever possible.

Not every API will be released in every phase. We use our best judgment to determine the phase for an API based on our confidence for the feature, weighing factors like the feature's complexity, possible use cases, and feedback from early users of the API.

The Turborepo core team would like to thank any users who do use features early and express our appreciation for any feedback you provide.

When an API reaches stability, it is considered ready for use in production. APIs marked as stable will only change in a backward-compatible way in a major release.

* If a stable API is going to **have breaking changes** in an upcoming major release, warnings and documentation will be provided to help with migrations and next steps.
* If a stable API is going to be **removed** in an upcoming major release, it will be marked as [Deprecated](#deprecated) to provide early notice of future removal.

Beta APIs require more confidence around reliability before a stable release. In the Beta phase, we are confident about the overall design of the feature and expect to be able to promote the feature to stable with relatively few changes. In rare cases, an API may require a breaking change and will not be covered by semver.

We encourage early adopters to use Beta APIs to help us gain certainty around the feature's design and stability. Depending on your risk tolerance, you can use the feature in production as you see fit.

**APIs currently in the Beta phase:**

Experimental APIs lack essential capabilities required to be ready for stability. The design of the feature is considered to be under active development and can change at any time.

We encourage you to help us test experimental APIs in side projects, proof-of-concepts, and other environments where stability is non-essential. This gives you the opportunity to aid in the API's development by providing early feedback to the core team as the feature develops. We do not recommend using experimental APIs where reliability is essential.

**APIs currently in the Experimental phase:**

* [`turbo query`](/docs/reference/query)
* [`turbo boundaries`](/docs/reference/boundaries) and [Tags](/docs/reference/boundaries#tags)
* [`--experimental-write-cache` for `turbo watch`](/docs/reference/watch#caching)
* [`--output=json` for `turbo ls --affected` flag](/docs/reference/ls)

Deprecated APIs are in the process of being removed. Any feature we intend to remove will include documentation for existing users with next steps and information on when to expect the feature to be removed.

**APIs that are currently deprecated:**

* `TURBO_REMOTE_ONLY` and `--remote-only`: Use [`TURBO_CACHE`](/docs/reference/system-environment-variables) or [--cache](/docs/reference/run#--cache-options)

- [Core concepts](/core-concepts/index.md): Learn about the core concepts behind Turborepo.

import { Card, Cards } from '#components/card';

Learn more about the core concepts of Turborepo:

<Cards>
  <Card title="Remote Caching" href="/docs/core-concepts/remote-caching" description="Save time by never doing the same work twice" />

<Card title="Package types" href="/docs/core-concepts/package-types" description="Application and Library Packages" />

<Card title="Internal Packages" href="/docs/core-concepts/internal-packages" description="Easily share code inside your repository" />

<Card title="Package and Task Graphs" href="/docs/core-concepts/package-and-task-graph" description="How Turborepo relates your tasks to each other" />
</Cards>

- [Internal Packages](/core-concepts/internal-packages.md): Learn how to build Internal Packages in your monorepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

Internal Packages are libraries whose source code is inside your Workspace. You can quickly make Internal Packages to share code within your monorepo and choose to [publish them to the npm registry](/docs/guides/publishing-libraries) if you need to later.

Internal Packages are used in your repository by installing them in `package.json` similar to an external package coming from the npm registry. However, instead of marking a version to install, you can reference the package using your package manager's workspace installation syntax:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

In the [Creating an Internal Package guide](/docs/crafting-your-repository/creating-an-internal-package), you can build an Internal Package from the beginning using [the Compiled Package strategy](#compiled-packages). On this page, we'll describe other strategies for creating Internal Packages and their tradeoffs, including [publishing the package to the npm registry](#publishable-packages) to create an External Package.

You can then import the package into your code like you're used to doing with an external package:

## Compilation Strategies

Depending on what you need from your library, you can choose one of three compilation strategies:

* [**Just-in-Time Packages**](#just-in-time-packages): Create minimal configuration for your package by allowing application bundlers to compile the package as it uses it.
* [**Compiled Packages**](#compiled-packages): With a moderate amount of configuration, compile your package using a build tool like `tsc` or a bundler.
* [**Publishable Packages**](#publishable-packages): Compile and prepare a package to publish to the npm registry. This approach requires the most configuration.

### Just-in-Time Packages

A Just-in-Time package is compiled by the application that uses it. This means you can use your TypeScript (or uncompiled JavaScript) files directly, requiring much less configuration than the other strategies on this page.

This strategy is most useful when:

* Your applications are built using a modern bundler like Turbopack, webpack, or Vite.
* You want to avoid configuration and setup steps.
* You're satisfied with your applications' build times, even when you can't hit cache for the package.

A `package.json` for a Just-in-Time package may look like this one:

There are a few important things to notice in this `package.json`:

* **Directly exporting TypeScript**: The `exports` field marks the entrypoints for the package and, in this case, you're **referencing TypeScript files directly**. This is possible because the bundler for the application will compile the code as it uses it in its build process.
* **No `build` script**: Because this package is exporting TypeScript, it doesn't need a build step for transpiling the package. This means you don't have to configure a build tool in this package to make it work in your Workspace.

#### Limitations and tradeoffs

* **Only applicable when consumers do transpiling**: This strategy can only be used when the package is going to be used in tooling that uses a bundler or natively understands TypeScript. The consumer's bundler is responsible for transpiling the TypeScript packages to JavaScript. If your builds or other usages of the package are not able to consume TypeScript, you will need to move to the [Compiled Packages](#compiled-packages) strategy.
* **No TypeScript `paths`**: A library that is being transpiled by its consumer cannot use the `compilerOptions.paths` configuration because TypeScript assumes that source code is being transpiled in the package where it is written. If you're using TypeScript 5.4 or later, we recommend [using Node.js subpath imports](https://devblogs.microsoft.com/typescript/announcing-typescript-5-4/#auto-import-support-for-subpath-imports). To learn how, visit [our TypeScript page](/docs/guides/tools/typescript#use-nodejs-subpath-imports-instead-of-typescript-compiler-paths).
* **Turborepo cannot cache a build for a Just-in-Time Package**: Because the package doesn't have its own `build` step, it can't be cached by Turborepo. This tradeoff may make sense for you if you want to keep configuration to a minimum and are okay with the build times for your applications.
* **Errors in internal dependencies will be reported**: When directly exporting TypeScript, type-checking in a dependent package will fail if code in an internal dependency has TypeScript errors. You may find this confusing or problematic in some situations.

### Compiled Packages

A Compiled Package is a package that handles its own compilation using a build tool, like [`tsc` (the TypeScript compiler)](https://www.typescriptlang.org/docs/handbook/compiler-options.html#handbook-content).

Compiling your library produces compiled JavaScript outputs into a directory (`dist`, `build`, etc.) that you will use for the entrypoints for your package. The build outputs will be cached by Turborepo once they're added to the [`outputs` key of the task](/docs/reference/configuration#outputs), allowing you to have faster build times.

#### Limitations and tradeoffs

* **Using the TypeScript compiler**: The majority of Compiled Packages should use `tsc`. Since the package is highly likely to be consumed by an application that is using a bundler, the application's bundler will prepare the library package for distribution in the application's final bundles, handling polyfilling, downleveling, and other concerns. A bundler should only be used if you have a specific use case that requires it, like bundling static assets into your package's outputs.
* **More configuration**: Compiled Packages require deeper knowledge and configuration to create build outputs. There are [many configurations for the TypeScript compiler](https://www.typescriptlang.org/docs/handbook/compiler-options.html#compiler-options) that can be difficult to manage and understand, and further configuration to optimize for bundlers, like [the `sideEffects` key in `package.json`](https://webpack.js.org/guides/tree-shaking/#mark-the-file-as-side-effect-free). You can find some of our recommendations in [our dedicated TypeScript guide](/docs/guides/tools/typescript).

### Publishable packages

Publishing a package to the npm registry comes with the most strict requirements of the packaging strategies on this page. Because you don't know anything about how your package will be used by consumers who download the package from the registry, you may find it difficult due to the numerous configurations required for a robust package.

Additionally, the process of publishing a package to the npm registry requires specialized knowledge and tooling. We recommend [`changesets`](https://github.com/changesets/changesets) for managing versioning, changelogs, and the publishing process.

For a detailed guide, visit [our Publishing packages guide](/docs/guides/publishing-libraries).

- [Package and Task Graphs](/core-concepts/package-and-task-graph.md): Turborepo builds a Task Graph based on your configuration and repository structure.

import { File, Folder, Files } from '#components/files';
import { Callout } from '#components/callout';

The Package Graph is the structure of your monorepo created by your package manager. When you install [Internal Packages](/docs/core-concepts/internal-packages) into each other, Turborepo will automatically identify those dependency relationships to build a foundational understanding of your Workspace.

This sets the groundwork for the Task Graph, where you'll define how **tasks** relate to each other.

In `turbo.json`, you express how tasks relate to each other. You can think of these relationships as
dependencies between tasks, but we have a more formal name for them: the Task Graph.

<Callout type="good-to-know">
  You can generate a visualization of the task graph for your tasks using [the
  `--graph` flag](/docs/reference/run#--graph-file-type).
</Callout>

Turborepo uses a data structure called a [directed acyclic graph (DAG)](https://en.wikipedia.org/wiki/Directed_acyclic_graph) to
understand your repository and its tasks. A graph is made up of "nodes" and
"edges". In the Task Graph, the nodes are tasks and the edges are the
dependencies between tasks. A *directed* graph indicates that the edges
connecting each node have a direction, so if Task A points to Task B, we can say
that Task A depends on Task B. The direction of the edge depends on which task
depends on which.

For example, let's say you have a monorepo with an application in `./apps/web` that
depends on two packages: `@repo/ui` and `@repo/utils`:

<Files>
  <Folder name="apps" defaultOpen>
    <Folder name="web" />
  </Folder>

<Folder name="packages" defaultOpen>
    <Folder name="ui" />

<Folder name="utils" />
  </Folder>
</Files>

You also have a `build` task that depends on `^build`:

Turborepo will build a task graph like this:

![Task graph visualization. The diagram has one node at the top named "apps/web" with two lines that connect to other nodes, "packages/ui" and "packages/utils" respectively.](/images/docs/simple-task-graph.png)

A challenge when building a Task Graph is handling nested dependencies. For
example, let's say your monorepo has a `docs` app that depends on the `ui`
package, which depends on the `core` package:

<Files>
  <Folder name="apps" defaultOpen>
    <Folder name="docs" />
  </Folder>

<Folder name="packages" defaultOpen>
    <Folder name="ui" />

<Folder name="core" />
  </Folder>
</Files>

Let's assume the `docs` app and the `core` package each have a `build` task, but
the `ui` package does not. You also have a `turbo.json` that configures the
`build` task the same way as above with `"dependsOn": ["^build"]`. When you run
`turbo run build`, what would you expect to happen?

Turborepo will build this Task Graph:

![A Task Graph visualization with a Transit Node. The diagram has one node at the top named "apps/doc" with a line that connects to a "packages/ui" node. This node does not have a "build" task. The "packages/ui" node has another line to a "packages/core" node that does have a "build" task.](/images/docs/transitive-nodes.png)

You can think of this graph in a series of steps:

* The `docs` app only depends on `ui`.
* The `ui` package does **not** have a build script.
* The `ui` package's *dependencies* have a `build` script, so the task graph knows to include those.

Turborepo calls the `ui` package a Transit Node in this scenario, because it
doesn't have its own `build` script. Since it doesn't have a `build` script,
Turborepo won't execute anything for it, but it's still part of the graph for
the purpose of including its own dependencies.

#### Transit Nodes as entry points

What if the `docs/` package didn't implement the `build` task? What would
you expect to happen in this case? Should the `ui` and `core` packages still
execute their build tasks? Should *anything* happen here?

Turborepo's mental model is that all nodes in the Task Graph are the same. In other words,
Transit Nodes are included in the graph regardless of where they appear in the graph.
This model can have unexpected consequences. For example, let's say you've configured
your `build` task to depend on `^test`:

Let's say your monorepo has many apps and many packages. All packages have
`test` tasks, but only one app has a `build` task. Turborepo's mental model
says that when you run `turbo run build`, even if an app doesn't implement `build`
the `test` task of all packages that are dependencies will show up in the graph.

- [Package types](/core-concepts/package-types.md): Learn about the different types of packages in a workspace.

import { Callout } from '#components/callout';

In Turborepo, we talk about two types of packages:

* [Application Packages](#application-packages)
* [Library Packages](#library-packages)

## Application Packages

An Application Package is a package in your workspace that will be deployed from your workspace. Examples of Application Packages are Next.js, Svelte, Vite, or CLI applications that are commonly found in the `./apps` directory.

It's best practice that your Application Packages are the "end" of your [Package Graph](/docs/core-concepts/package-and-task-graph#package-graph), not being installed into other packages of your repository. Your CI/CD pipelines will most often finalize at these nodes of your Package and Task Graphs.

### Installing an application package into another package

In rare cases, you may need to install an Application Package into another package. This should be the exception. If you find you are doing this often, you may want to rethink your package structure.

An example of an exception for this rule is installing your Application Package into a package that handles end-to-end testing. Once installed, you can depend on the Application Package in your end-to-end testing package so it is aware of re-deploys of the application.

Library Packages contain code that you intend to share around your workspace. They aren't independently deployable. Instead, they support the Application Packages to create the final deployables from your repository. You might also refer to these packages as [Internal Packages](/docs/core-concepts/internal-packages), which have their own sub-types.

- [Remote Caching](/core-concepts/remote-caching.md): Share cache artifacts across machines for even faster builds.

import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { ThemeAwareImage } from '#components/theme-aware-image';

Turborepo's [task cache](/docs/crafting-your-repository/caching) saves time by never doing the same work twice.

But there's a problem: **the cache is local to your machine**. When you're working with a Continuous Integration system, this can result in a lot of duplicated work:

<ThemeAwareImage
  dark={{
  alt: 'Local caching creates a cache on each system.',
  src: '/images/docs/local-caching-dark.png',
  props: {
    width: 896,
    height: 345,
  },
}}
  light={{
  alt: 'Local caching creates a cache on each system.',
  src: '/images/docs/local-caching-light.png',
  props: {
    width: 896,
    height: 345,
  },
}}
/>

Since Turborepo only caches to the local filesystem by default, the same task (`turbo run build`) must be **re-executed on each machine** (by you, by your teammates, by your CI, by your PaaS, etc.) even when all of the task inputs are identical — which **wastes time and resources**.

<Callout type="good-to-know">
  You don't have to use Remote Caching to use Turborepo. While Remote Caching
  will bring the most significant speedups, you can make your existing workflows
  faster without Remote Caching, too.
</Callout>

## A single, shared cache

What if you could share a single Turborepo cache across your entire team (and even your CI)?

<ThemeAwareImage
  dark={{
  alt: 'Remote caching creates a shared cache for your entire team.',
  src: '/images/docs/remote-caching-dark.png',
  props: {
    width: 896,
    height: 489,
  },
}}
  light={{
  alt: 'Remote caching creates a shared cache for your entire team.',
  src: '/images/docs/remote-caching-light.png',
  props: {
    width: 896,
    height: 489,
  },
}}
/>

Turborepo can securely communicate with a remote cache - a cloud server that stores the results of your tasks. This can save enormous amounts of time by **preventing duplicated work across your entire organization**.

Remote Caching is free and can be used with both [managed providers](https://turborepo.com/docs/core-concepts/remote-caching#managed-remote-cache-with-vercel) or as a [self-hosted cache](https://turborepo.com/docs/core-concepts/remote-caching#self-hosting).

<Callout>
  Remote Caching is a powerful feature of Turborepo, but, with great power,
  comes great responsibility. Make sure you are caching correctly first and
  double check [handling of environment
  variables](/docs/crafting-your-repository/using-environment-variables). Please
  also remember Turborepo treats logs as artifacts, so be aware of what you are
  printing to the console.
</Callout>

[Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching) is free to use on all plans, even if you do not host your applications on Vercel. Follow the steps below to enable Remote Caching for your repository.

### For Local Development

To link your local Turborepo to your Remote Cache, authenticate the Turborepo CLI with your Vercel account:

You can also use your package manager if you do not have [global `turbo`](/docs/getting-started/installation#global-installation) installed:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

<Callout>
  If your Remote Cache is configured to use single-sign-on you will need to run
  `npx turbo login --sso-team=team-name` in order to get a cache token with the
  correct privileges.
</Callout>

Now, link your Turborepo to your Remote Cache:

Once enabled, make some changes to a package you are currently caching and run tasks against it with `turbo run`.
Your cache artifacts will now be stored locally *and* in your Remote Cache.

To verify, delete your local Turborepo cache with:

<Tabs groupId="platform-tabs" items={['UNIX', 'Windows']} persist>
  <Tab value="UNIX">
    
  </Tab>

<Tab value="Windows">
    
  </Tab>
</Tabs>

Then, run the same build again. If things are working properly, `turbo` should not execute tasks locally. Instead, it will download the logs and artifacts from your Remote Cache and replay them back to you.

### Remote Caching on Vercel

If you are building and hosting your apps on Vercel, Remote Caching will be automatically set up on your behalf once you use `turbo`. Refer to the [Vercel documentation](https://vercel.com/docs/concepts/monorepos/remote-caching?utm_source=turborepo.com\&utm_medium=referral\&utm_campaign=docs-link) for more information.

### Artifact Integrity and Authenticity Verification

Turborepo can sign artifacts with a secret key before uploading them to the Remote Cache. Turborepo uses `HMAC-SHA256` signatures on artifacts using a secret key you provide.
Turborepo will verify the Remote Cache artifacts' integrity and authenticity when they're downloaded.
Any artifacts that fail to verify will be ignored and treated as a cache miss by Turborepo.

To enable this feature, set the `remoteCache` options on your `turbo.json` config to include `signature: true`. Then specify your secret key by declaring the `TURBO_REMOTE_CACHE_SIGNATURE_KEY` environment variable.

A Remote Cache can be implemented by any HTTP server that meets Turborepo's Remote Caching API specification.

### Managed Remote Cache with Vercel

[Vercel](https://vercel.com), the creators and maintainers of Turborepo, provide a managed Remote Cache that is fully compatible with Turborepo.

Using [Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching) is zero-configuration and automatically integrates with [Vercel deployments](https://vercel.com/docs/deployments/overview) through the open-source [Vercel Remote Cache SDK](https://github.com/vercel/remote-cache).

Learn more about [Turborepo on Vercel](https://vercel.com/docs/monorepos/turborepo) or [deploy a template for free](https://vercel.com/templates?search=turborepo) to try it out.

You can also self-host your own Remote Cache and log into it using the `--manual` flag to provide API URL, team, and token information.

#### OpenAPI specification

* [Human-readable viewer](/docs/openapi)
* [JSON](/api/remote-cache-spec)

At this time, all versions of `turbo` are compatible with the `v8` endpoints.

#### Community implementations

The Turborepo community has created open-source implementations of the Remote Cache.

* [`brunojppb/turbo-cache-server`](https://github.com/brunojppb/turbo-cache-server)
* [`ducktors/turborepo-remote-cache`](https://github.com/ducktors/turborepo-remote-cache)
* [`Tapico/tapico-turborepo-remote-cache`](https://github.com/Tapico/tapico-turborepo-remote-cache)

- [Add to an existing repository](/getting-started/add-to-existing-repository.md): Using Turborepo with your existing repository

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';
import { Step, Steps } from '#components/steps';
import { LinkToDocumentation } from '#components/link-to-documentation';

Turborepo can be incrementally adopted in **any repository, single or multi-package**, to speed up the developer and CI workflows of the repository.

After installing `turbo` and configuring your tasks in `turbo.json`, you'll notice how [caching](/docs/crafting-your-repository/caching) helps you run tasks much faster.

## Preparing a single-package workspace

A [single-package workspace](https://vercel.com/docs/vercel-platform/glossary#single-package-workspace) is, for example, what you get after running `npx create-next-app` or `npm create vite`. You don't need to do any extra work for Turborepo to handle your repo so you can jump to the first step below.

To learn more about Turborepo in single-package workspaces, visit [the dedicated guide](/docs/guides/single-package-workspaces).

## Preparing a multi-package workspace (monorepo)

`turbo` is built on top of Workspaces, a feature of the major package managers in the JavaScript ecosystem. This makes it easy to adopt in your existing codebase.

<Callout type="good-to-know">
  If you're finding that `turbo` is having issues like not being able to
  discover packages in your workspace or not following your dependency graph,
  visit our [Structuring a
  repository](/docs/crafting-your-repository/structuring-a-repository) page for
  tips.
</Callout>

Note that you don't have to start running *all* your tasks for *all* your
packages using `turbo` right away. You can start with a single task in just a
few packages and incrementally add more tasks and packages as you get more
familiar with Turborepo.

## Adding Turborepo to your repository

<Steps>
  <Step>
    ### Install `turbo`

We recommend you install `turbo` both globally and into your repository's root for the best developer experience.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        Ensure you have created a `pnpm-workspace.yaml` file before you begin the installation. Failure to have this file will result in an error that says: ` --workspace-root may only be used inside a workspace`.

<Tab value="yarn">
        
      </Tab>

<Tab value="npm">
        
      </Tab>

<Tab value="bun">
        
      </Tab>
    </Tabs>

To learn more about why we recommend both installations, visit the [Installation page](/docs/getting-started/installation).
  </Step>

<Step>
    ### Add a `turbo.json` file

In the root of your repository, create a `turbo.json` file.

We'll be using `build` and `check-types` tasks in this guide but you can replace these with other tasks that interest you, like `lint` or `test`.

<Tabs items={['Next.js', 'Vite']} storageKey="framework-preference">
      <Tab value="Next.js">

For more information on configuring your `turbo.json`, see the [Configuration Options](/docs/reference/configuration) documentation.

In your Next.js application, make sure you have a `check-types` script for `turbo` to run.

Some Vite starters ship with a `package.json` that looks like this:

We recommend splitting these into a `check-types` and `build` script so that `turbo` can run them in parallel.

In a multi-package workspace, you may also want to add a `check-types` script
    to one or more of your library packages to see how multiple scripts across
    different packages run with one `turbo` command.
  </Step>

<Step>
    ### Edit `.gitignore`

Add `.turbo` to your `.gitignore` file. The `turbo` CLI uses these folders for persisting logs, outputs, and other functionality.

<Step>
    ### Add a `packageManager` field to root `package.json`

Turborepo optimizes your repository using information from your package manager. To declare which package manager you're using, add a [`packageManager`](https://nodejs.org/api/packages.html#packagemanager) field to your root `package.json` if you don't have one already.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        
      </Tab>

<Tab value="yarn">
        
      </Tab>

<Tab value="npm">
        
      </Tab>

<Tab value="bun">
        
      </Tab>
    </Tabs>

<Callout type="good-to-know">
      Depending on your repository, you may need to use the
      [`dangerouslyDisablePackageManagerCheck`](/docs/reference/configuration#dangerouslydisablepackagemanagercheck)
      while migrating or in situations where you can't use the `packageManager` key
      yet.
    </Callout>
  </Step>

<Step>
    ### Set up package manager workspaces

For [multi-package workspaces](https://vercel.com/docs/glossary#multi-package-workspace), you'll need to configure your package manager to recognize your workspace structure.

The `workspaces` field tells your package manager which directories contain your packages. Common patterns include `apps/*` for applications and `packages/*` for shared libraries.

<Callout type="good-to-know">
      If you're working with a single-package repository, you can skip this step as
      workspaces aren't needed.
    </Callout>

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">

<LinkToDocumentation href="https://pnpm.io/pnpm-workspace_yaml">pnpm workspace documentation</LinkToDocumentation>
      </Tab>

<LinkToDocumentation href="https://yarnpkg.com/features/workspaces#how-are-workspaces-declared">yarn workspace documentation</LinkToDocumentation>
      </Tab>

<LinkToDocumentation href="https://docs.npmjs.com/cli/v7/using-npm/workspaces#defining-workspaces">npm workspace documentation</LinkToDocumentation>
      </Tab>

<LinkToDocumentation href="https://bun.sh/docs/install/workspaces">bun workspace documentation</LinkToDocumentation>
      </Tab>
    </Tabs>

For more details on how to structure your repository, see [Structuring a Repository](/docs/crafting-your-repository/structuring-a-repository#declaring-directories-for-packages).
  </Step>

<Step>
    ### Run tasks with `turbo`

You can now run the tasks you added to `turbo.json` earlier using Turborepo. Using the example tasks from above:

This runs the `build` and `check-types` tasks at the same time. The dependency graph of your [Workspace](/docs/crafting-your-repository/structuring-a-repository#anatomy-of-a-workspace) will be used to run tasks in the right order.
  </Step>

<Step>
    **Without making any changes to the code, try running `build` and `check-types` again:**

You should see terminal output like this:

Congratulations! **You just built and type checked your code in milliseconds**.

To learn more about how `turbo` makes this possible, check out [the caching documentation](/docs/crafting-your-repository/caching).
  </Step>

<Step>
    ### Begin developing by running `dev` with `turbo`

In a multi-package workspace, you can run `turbo dev` to start the development tasks for all your packages at once.

You can also [use a filter](/docs/crafting-your-repository/running-tasks#using-filters) to focus on a specific package and its dependencies.

<Callout type="info">
      Note that this step doesn't provide much value in a single-package workspace since:

* You don't cache the outputs for a development task.
      * There's only one development script so there's nothing to run in parallel.
    </Callout>
  </Step>

<Step>
    ## Next steps

You're now up and running with Turborepo! To learn about more ways you can improve your workflow and get the most out of `turbo`, we recommend checking out the following pages:

* [Enabling Remote Caching for development machines](/docs/crafting-your-repository/constructing-ci#enabling-remote-caching)
    * [Enabling Remote Caching in CI](/docs/crafting-your-repository/constructing-ci)
    * [Handling environment variables](/docs/crafting-your-repository/using-environment-variables)
    * [Filtering tasks](/docs/reference/run#--filter-string)
  </Step>
</Steps>

- [Editor integration](/getting-started/editor-integration.md): Making the most of Turborepo

import { Callout } from '#components/callout';

To get the best experience with `turbo`, Turborepo provides a few utilities for integrating with your editor.

## JSON Schema for `turbo.json`

Turborepo uses [JSON Schema](https://json-schema.org/) to give you auto-complete in your
`turbo.json` file. By including the `$schema` key in your `turbo.json`, your editor is able to
provide full documentation and linting in case you have invalid shapes or missing keys.

### Sourcing from the web

A `schema.json` is accessible at the URL shown below. This has the advantage of not needing to run your package manager's install command to see in-editor validation.

There is also a major versioned `schema.json` available, following the format of `https://turborepo.com/schema.<version>.json`.

### Sourcing from `node_modules`

Starting in Turborepo 2.4, `schema.json` is available in `node_modules` once you've run your package manager's install command:

<Callout title="node_modules location">
  We recommend installing `turbo` at the root of your repository, so the path
  for the schema should point to `node_modules` at the root of your repository.
  In [Package Configurations](/docs/reference/package-configurations), you may
  need to use a path like `../../node_modules/turbo/schema.json`.
</Callout>

## Linting for environment variables

Handling environment variables is an important part of building applications in a Turborepo.

[The `eslint-config-turbo` package](/docs/reference/eslint-config-turbo) extends your ESLint setup to help you make sure you've taken care of all of your environment variables.

Enable even more auto-complete and linting than provided by JSON Schema, with in-editor hinting for invalid globs, references to non-existent tasks or packages, and
extra repository visibility tools.

Visit the [VSCode Extension Marketplace](https://marketplace.visualstudio.com/items?itemName=Vercel.turbo-vsc) to install.

<Callout type="info" title="Not using Visual Studio Code?">
  The language server can be used on any editors that support the [Language
  Server Protocol](https://microsoft.github.io/language-server-protocol/). Log a
  request in our [issue tracker](https://github.com/vercel/turborepo/issues) to
  express your interest.
</Callout>

- [Start with an example](/getting-started/examples.md): Start with an example Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { ExamplesTable } from '#components/examples-table';
import { Callout } from '#components/callout';

Use `create-turbo` to bootstrap an example with your favorite tooling.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

## Core-maintained examples

The following examples are maintained by the Turborepo core team. Dependencies are kept as up-to-date as possible and GitHub Issues are accepted and addressed for these examples.

<ExamplesTable coreMaintained />

## Community-maintained examples

The community curates a set of examples to showcase ways to use common tools and libraries with Turborepo. To bootstrap your monorepo with one of the examples, use the `--example` flag:

<Callout type="good-to-know">
  GitHub Issues for these examples will be closed. If you find problems, please
  submit a pull request with fixes.
</Callout>

- [Getting started](/getting-started/index.md): Get started with Turborepo.

import { Card, Cards } from '#components/card';
import { Step, Steps } from '#components/steps';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

If you're new to Turborepo, you can follow these steps to get started.

<Steps>
  <Step>
    ## Install Turborepo

Install `turbo` globally so you can conveniently run `turbo` commands in your terminal from anywhere in your repository.

<Tabs items={["npm", "yarn", "pnpm"]} storageKey="selected-pkg-manager">
      <Tab value="npm">
        
      </Tab>

<Tab value="yarn">
        
      </Tab>

<Tab value="pnpm">
        
      </Tab>
    </Tabs>

To learn more about installing `turbo`, see the [installation guide](/docs/getting-started/installation).
  </Step>

<Step>
    ## Choose your learning path

<Cards>
      <Card href="/docs/getting-started/installation" title="Use create-turbo" description="Start with a template" />

<Card href="/docs/getting-started/examples" title="Use an example" description="Start with a framework-specific example" />

<Card href="/docs/crafting-your-repository" title="Follow the in-depth guides" description="From zero to monorepo" />

<Card href="/docs/getting-started/add-to-existing-repository" title="Add to an existing repository" description="Make your current repo fast" />
    </Cards>
  </Step>
</Steps>

- [Installation](/getting-started/installation.md): Learn how to get started with Turborepo.

import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

Get started with Turborepo in a few moments using:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

The starter repository will have:

* Two deployable applications
* Three shared libraries for use in the rest of the monorepo

For more details on the starter, [visit the README for the basic starter on GitHub](https://github.com/vercel/turborepo/tree/main/examples/basic). You can also [use an example](/docs/getting-started/examples) that more closely fits your tooling interests.

## Installing `turbo`

`turbo` can be installed both globally **and** in your repository. We highly recommend installing both ways so you can take advantage of fast, convenient workflows *and* a stable version of `turbo` for all developers working in your repository.

### Global installation

A global install of `turbo` brings flexibility and speed to your local workflows.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

Once installed globally, you can run your scripts through `turbo` from your terminal, quickly running one-off commands to use within your repository. For example:

* `turbo build`: Run `build` scripts following your repository's dependency graph
* `turbo build --filter=docs --dry`: Quickly print an outline of the `build` task for your `docs` package (without running it)
* `turbo generate`: Run [Generators](/docs/guides/generating-code) to add new code to your repository
* `cd apps/docs && turbo build`: Run the `build` script in the `docs` package and its dependencies. For more, visit the [Automatic Package Scoping section](/docs/crafting-your-repository/running-tasks#automatic-package-scoping).

<Callout type="good-to-know">
  `turbo` is an alias for [`turbo run`](/docs/reference/run). For example,
  `turbo build` and `turbo run build` will both run your `build` task.
</Callout>

<Callout type="error" title="Avoid multiple global installations">
  If you've installed global `turbo` before, make sure you use the same package
  manager as your existing installation to avoid unexpected behaviors. You can
  quickly check which package manager you previously used with [`turbo
    bin`](/docs/reference/bin).
</Callout>

#### Using global `turbo` in CI

You can also take advantage of global `turbo` when creating your CI pipelines. Visit the [Constructing CI](/docs/crafting-your-repository/constructing-ci#global-turbo-in-ci) guide for more information.

### Repository installation

When collaborating with other developers in a repository, it's a good idea to pin versions of dependencies. You can do this with `turbo` by adding it as a `devDependency` in the root of your repository:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

You can continue to use your global installation of `turbo` to run commands. Global `turbo` will defer to the local version of your repository if it exists.

This lets you to get the best of both installations: easily run commands in your terminal while maintaining a pinned version for consistent usage for all developers in the repository.

- [Caching](/crafting-your-repository/caching.md): Learn about caching in Turborepo.

import { Step, Steps } from '#components/steps';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';

Turborepo uses caching to speed up builds, ensuring you **never do the same work twice**. When your task is cacheable, Turborepo will restore the results of your task from cache using a fingerprint from the first time the task ran.

![12 tasks are being ran in 3 packages, resulting in a ">>> FULL TURBO" cache hit. The total time it takes to restore these tasks from cache is 80 milliseconds.](/images/docs/why-turborepo-solution.png)

Turborepo's caching results in significant time savings when working locally - and is even more powerful when [Remote Caching](/docs/core-concepts/remote-caching) is enabled, sharing a cache among your entire team and CI.

On this page, you'll learn:

* [How to hit your first Turborepo cache](#hit-your-first-turborepo-cache)
* [How to enable Remote Caching](/docs/core-concepts/remote-caching)
* [What Turborepo uses for the inputs and outputs to a hash](/docs/crafting-your-repository/caching#task-inputs)
* [How to troubleshoot caching issues](#troubleshooting)

<Callout type="good-to-know">
  Turborepo assumes that your tasks are **deterministic**. If a task is able to
  produce different outputs given the set of inputs that Turborepo is aware of,
  caching may not work as expected.
</Callout>

## Hit your first Turborepo cache

You can try out Turborepo's caching behavior in three steps:

<Steps>
  <Step>
    ### Create a new Turborepo project

Use `npx create-turbo@latest` and follow the prompts to create a new Turborepo.

<Step>
    ### Run a build for the first time

If you have [`turbo` installed globally](/docs/getting-started/installation#global-installation), run `turbo build` in your repository.

Alternatively, you can run the `build` script in `package.json` using your package manager.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        
      </Tab>

<Tab value="yarn">
        
      </Tab>

<Tab value="npm">
        
      </Tab>

<Tab value="bun">
        
      </Tab>
    </Tabs>

This will result in a cache miss, since you've never ran `turbo` before with this [set of inputs](/docs/crafting-your-repository/caching#task-inputs) in this repository. The inputs are turned into a hash to check for in your local filesystem cache or in [the Remote Cache](/docs/core-concepts/remote-caching).
  </Step>

<Step>
    ### Hit the cache

Run `turbo build` again. You will see a message like this:

![A terminal window showing two tasks that have been ran through turbo. They successfully complete in 116 milliseconds.](/images/docs/full-turbo.png)
  </Step>
</Steps>

Because the inputs' fingerprint is already in the cache, there's no reason to rebuild your applications from zero again. You can restore the results of the previous build from cache, saving resources and time.

Turborepo stores the results of tasks in the `.turbo/cache` directory on your machine. However, you can make your entire organization even faster by sharing this cache with your teammates and CI.

To learn more about Remote Caching and its benefits, visit the [Remote Caching page](/docs/core-concepts/remote-caching).

### Enabling Remote Cache

First, authenticate with your Remote Cache provider:

Then, link the repository on your machine to Remote Cache:

Now, when you run a task, Turborepo will automatically send the outputs of the task to Remote Cache. If you run the same task on a different machine that is also authenticated to your Remote Cache, it will hit cache the first time it runs the task.

For information on how to connect your CI machines to Remote Cache, visit [the Constructing CI guide](/docs/crafting-your-repository/constructing-ci#enabling-remote-caching).

<Callout type="info">
  By default, Turborepo uses [Vercel Remote
  Cache](https://vercel.com/docs/monorepos/remote-caching) with zero
  configuration. If you'd like to use a different Remote Cache, visit the
  [Remote Caching API
  documentation](/docs/core-concepts/remote-caching#self-hosting)
</Callout>

Turborepo caches two types of outputs: Task outputs and Logs.

Turborepo caches the file outputs of a task that are defined in [the `outputs` key](/docs/reference/configuration#outputs) of `turbo.json`. When there's a cache hit, Turborepo will restore the files from the cache.

The `outputs` key is optional, see [the API reference](/docs/reference/configuration#outputs) for how Turborepo behaves in this case.

<Callout type="warn" title="Providing file outputs">
  If you do not declare file outputs for a task, Turborepo will not cache them. This might be okay for some tasks (like linters) - but many tasks produce files that you will want to be cached.

If you're running into errors with files not being available when you hit cache, make sure that you have defined the outputs for your task.
</Callout>

Turborepo always captures the terminal outputs of your tasks, restoring those logs to your terminal from the first time that the task ran.

You can configure the verbosity of the replayed logs using [the `--output-logs` flag](/docs/reference/run#--output-logs-option) or [`outputLogs` configuration option](/docs/reference/configuration#outputlogs).

Inputs are hashed by Turborepo, creating a "fingerprint" for the task run. When "fingerprints" match, running the task will hit the cache.

Under the hood, Turborepo creates two hashes: a global hash and a task hash. If either of the hashes change, the task will miss cache.

### Global hash inputs

| Input                                                                                  | Example                                                                                                                                                                                                         |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Resolved task definition from root `turbo.json`<br /> and package `turbo.json`         | Changing [`outputs`](/docs/reference/configuration#outputs) in either root `turbo.json` or [Package Configuration](/docs/reference/package-configurations)                                                      |
| Lockfile changes that affect the Workspace root                                        | Updating dependencies in root `package.json` will cause **all** tasks to miss cache                                                                                                                             |
| [`globalDependencies`](/docs/reference/configuration#globaldependencies) file contents | Changing `./.env` when it is listed in `globalDependencies` will cause **all** tasks to miss cache                                                                                                              |
| Values of variables listed in [`globalEnv`](/docs/reference/configuration#globalenv)   | Changing the value of `GITHUB_TOKEN` when it is listed in `globalEnv`                                                                                                                                           |
| Flag values that affect task runtime                                                   | Using behavior-changing flags like `--cache-dir`, `--framework-inference`, or `--env-mode`                                                                                                                      |
| Arbitrary passthrough arguments                                                        | `turbo build -- --arg=value` will cause **all** tasks to miss cache when compared to either `turbo build` or `turbo build -- --arg=diff` (including dependencies of `build` that did not receive `--arg=value`) |

### Package hash inputs

| Input                                                                   | Example                                                 |
| ----------------------------------------------------------------------- | ------------------------------------------------------- |
| [Package Configuration](/docs/reference/package-configurations) changes | Changing a package's `turbo.json`                       |
| Lockfile changes that affect the package                                | Updating dependencies in a package's `package.json`     |
| Package's `package.json` changes                                        | Updating the `name` field in a package's `package.json` |
| File changes in source control                                          | Writing new code in `src/index.ts`                      |

Turborepo has a [`--dry` flag](/docs/reference/run#--dry----dry-run) that can be used to see what would happen if you ran a task without actually running it. This can be useful for debugging caching issues when you're not sure which tasks you're running.

For more details, visit the [`--dry` API reference](/docs/reference/run#--dry----dry-run).

### Using Run Summaries

Turborepo has a [`--summarize` flag](/docs/reference/run#--summarize) that can be used to get an overview of all of a task's inputs, outputs, and more. Comparing two summaries will show why two task's hashes are different. This can be useful for:

* Debugging inputs: There are many inputs to a task in Turborepo. If a task is missing cache when you expect it to hit, you can use a Run Summary to check which inputs are different that you weren't expecting.
* Debugging outputs: If cache hits aren't restoring the files you're expecting, a Run Summary can help you understand what outputs are being restored from cache.

<Callout type="info" title="Summaries viewer">
  While there is not a Turborepo-native Run Summaries UI viewer, there are
  several community-built tools available:

* [https://turbo.nullvoxpopuli.com](https://turbo.nullvoxpopuli.com) - Web-based UI viewer for Run Summaries
  * [`turborepo-summary`](https://github.com/charpeni/turborepo-summary) - Generate human-readable reports from Turborepo run summary JSON output
  * [`turborepo-summary-action`](https://github.com/charpeni/turborepo-summary-action) - GitHub Action wrapping `turborepo-summary` to append them to GitHub Actions Job Summary
</Callout>

### Turning off caching

Sometimes, you may not want to write the output of tasks to the cache. This can be set permanently for a task using [`"cache": false`](/docs/reference/configuration#cache) or for a whole run using [ the `--cache <options>` flag](/docs/reference/run#--no-cache).

### Overwriting a cache

If you want to force `turbo` to re-execute a task that has been cached, use [the `--force` flag](/docs/reference/run#--force). Note that this disables **reading** the cache, **not writing**.

### Caching a task is slower than executing the task

It's possible to create scenarios where caching ends up being slower than not caching. These cases are rare, but a few examples include:

* **Tasks that execute extremely fast**: If a task executes faster than a network round-trip to the [Remote Cache](/docs/core-concepts/remote-caching), you should consider not caching the task.
* **Tasks whose output assets are enormous**: It's possible to create an artifact that is so big that the time to upload or download it exceeds the time to regenerate it, like a complete Docker Container. In these cases, you should consider not caching the task.
* **Scripts that have their own caching**: Some tasks have their own internal caching behavior. In these cases, configuration can quickly become complicated to make Turborepo's cache and the application cache work together.

While these situations are rare, be sure to test the behavior of your projects to determine if disabling caching in specific places provides a performance benefit.

Now that you've seen how Turborepo's caching makes your repository faster, let's take a look at how to develop applications and libraries in your Turborepo.

- [Configuring tasks](/crafting-your-repository/configuring-tasks.md): Learn how to describe the workflows in your repository to get them done as fast as possible.

import { LinkToDocumentation } from '#components/link-to-documentation';
import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Files, File, Folder } from '#components/files';
import { ThemeAwareImage } from '#components/theme-aware-image';
import { ExperimentalBadge } from '#components/experimental-badge';

A task is a script that Turborepo runs. You can express relationships between tasks in your [`turbo.json` configuration](/docs/reference/configuration) and [Package Graph](/docs/core-concepts/package-and-task-graph#package-graph).

Turborepo will always parallelize any work that it can to ensure everything runs as fast as possible. This is faster than running tasks one at a time, and it's a part of what makes Turborepo so fast.

For example, <code style={{textWrap: "wrap"}}>yarn workspaces run lint && yarn workspaces run build && yarn workspaces run test</code> would look like this:

<ThemeAwareImage
  dark={{
  alt: 'A graphical representation of `turbo run lint test build`. It shows all tasks running in parallel, with much less empty space where scripts are not being ran.',
  src: '/images/docs/slow-tasks-dark.png',
  props: {
    width: 778,
    height: 331,
  },
}}
  light={{
  alt: 'A graphical representation of `turbo run lint test build`. It shows all tasks running in parallel, with much less empty space where scripts are not being ran.',
  src: '/images/docs/slow-tasks-light.png',
  props: {
    width: 778,
    height: 331,
  },
}}
/>

But, to get the same work done **faster** with Turborepo, you can use `turbo run lint build test`:

<ThemeAwareImage
  dark={{
  alt: 'A graphical representation of `turbo run lint test build`. It shows all tasks running in parallel, with much less empty space where scripts are not being ran.',
  src: '/images/docs/turborepo-tasks-fast-dark.png',
  props: {
    width: 778,
    height: 448,
  },
}}
  light={{
  alt: 'A graphical representation of `turbo run lint test build`. It shows all tasks running in parallel, with much less empty space where scripts are not being ran.',
  src: '/images/docs/turborepo-tasks-fast-light.png',
  props: {
    width: 778,
    height: 448,
  },
}}
/>

The root `turbo.json` file is where you'll register the tasks that Turborepo will run. Once you have your tasks defined, you'll be able to run one or more tasks using [`turbo run`](/docs/reference/run).

* If you're starting fresh, we recommend [creating a new repository using `create-turbo`](/docs/getting-started/installation) and editing the `turbo.json` file to try out the snippets in this guide.
* If you're adopting Turborepo in an existing repository, create a `turbo.json` file in the root of your repository. You'll be using it to learn about the rest of the configuration options in this guide.

<Files>
  <File name="turbo.json" green />

<File name="package.json" />

<Folder name="apps" />

<Folder name="packages" />
</Files>

Each key in the `tasks` object is a task that can be executed by `turbo run`. Turborepo will search your packages for **scripts in their `package.json` that have the same name as the task**.

To define a task, use [the `tasks` object](/docs/reference/configuration#tasks) in `turbo.json`. For example, a basic task with no dependencies and no outputs named `build` might look like this:

If you run `turbo run build` at this point, Turborepo will run all `build` scripts in your packages in parallel and won't cache any file outputs. **This will quickly lead to errors.** You're missing a few important pieces to make this work how you'd expect.

### Running tasks in the right order

[The `dependsOn` key](/docs/reference/configuration#dependson) is used to specify the tasks that must complete before a different task begins running. For example, in most cases, you want the `build` script for your libraries to complete before your application's `build` script runs. To do this, you'd use the following `turbo.json`:

You now have the build order you would expect, building *dependencies* before *dependents*.

**But be careful.** At this point, you haven't marked the build outputs for caching. To do so, jump to the [Specifying outputs](#specifying-outputs) section.

#### Depending on tasks in dependencies with `^`

The `^` microsyntax tells Turborepo to run the task in direct dependencies before the target package. If your application depends on a library named `ui` and the library has a `build` task, the `build` script in `ui` will run **first**. Once it has successfully completed, the `build` task in your application will run.

This is an important pattern as it ensures that your application's `build` task will have all of the necessary dependencies that it needs to compile. This concept also applies as your dependency graph grows to a more complex structure with many levels of task dependencies.

#### Depending on tasks in the same package

Sometimes, you may need to ensure that two tasks in the same package run in a specific order. For example, you may need to run a `build` task in your library before running a `test` task in the same library. To do this, specify the script in the `dependsOn` key as a plain string (without the `^`).

#### Depending on a specific task in a specific package

You can also specify an individual task in a specific package to depend on. In the example below, the `build` task in `utils` must be run before any `lint` tasks.

You can also be more specific about the dependent task, limiting it to a certain package:

With this configuration, the `lint` task in your `web` package can only be run after the `build` task in the `utils` package is complete.

Some tasks may not have any dependencies. For example, a task for finding typos in Markdown files likely doesn't need to care about the status of your other tasks. In this case, you can omit the `dependsOn` key or provide an empty array.

### Specifying `outputs`

<Callout type="info">
  Turborepo caches the outputs of your tasks so that you never do the same work
  twice. We'll discuss this in depth in [the Caching
  guide](/docs/crafting-your-repository/caching), but let's make sure your tasks
  are properly configured first.
</Callout>

The `outputs` key tells Turborepo **files and directories** it should cache when the task has successfully completed. **Without this key defined, Turborepo will not cache any files. Hitting cache on subsequent runs will not restore any file outputs.**

Below are a few examples of outputs for common tools:

<Tabs items={["Next.js", "Vite", "tsc"]} storageKey="outputs-tools">
  <Tab value="Next.js">
    
  </Tab>

<Tab value="Vite">
    
  </Tab>

<Tab value="tsc">
    
  </Tab>
</Tabs>

Globs are relative to the package, so `dist/**` will handle the `dist` that is outputted for each package, respectively. For more on building globbing patterns for the `outputs` key, see [the globbing specification](/docs/reference/globs).

### Specifying `inputs`

The `inputs` key is used to specify the files that you want to include in the task's hash for [caching](/docs/crafting-your-repository/caching). By default, Turborepo will include all files in the package that are tracked by Git. However, you can be more specific about which files are included in the hash using the `inputs` key.

As an example, a task for finding typos in Markdown files could be defined like this:

Now, **only** changes in Markdown files will cause the `spell-check` task to miss cache.

<Callout type="error">
  This feature opts out of all of Turborepo's default `inputs` behavior, including following along with changes tracked by source control. This means that your `.gitignore` file will no longer be respected, and you will need to ensure that you do not capture those files with your globs.

To restore the default behavior, use [the `$TURBO_DEFAULT$` microsyntax](#restoring-defaults-with-turbo_default).
</Callout>

#### Restoring defaults with `$TURBO_DEFAULT$`

[The default `inputs` behavior](/docs/reference/configuration#inputs) is often what you will want for your tasks. However, you can increase your cache hit ratios for certain tasks by fine-tuning your `inputs` to ignore changes to files that are known to not affect the task's output.

For this reason, you can use the `$TURBO_DEFAULT$` microsyntax to fine-tune the default `inputs` behavior:

In this task definition, Turborepo will use the default `inputs` behavior for the `build` task, but will ignore changes to the `README.md` file. If the `README.md` file is changed, the task will still hit cache.

### Registering Root Tasks

You can also run scripts in the `package.json` in the Workspace root using `turbo`. For example, you may want to run a `lint:root` task for the files in your Workspace's root directory in addition to the `lint` task in each package:

<Tabs items={["turbo.json", "package.json"]}>
  <Tab value="turbo.json">
    
  </Tab>

<Tab value="package.json">
    
  </Tab>
</Tabs>

With the Root Task now registered, `turbo run lint:root` will now run the task. You can also run `turbo run lint lint:root` to run all your linting tasks.

#### When to use Root Tasks

* **Linting and formatting of the Workspace root**: You might have code in your Workspace root that you want to lint and format. For example, you might want to run ESLint or Prettier in your root directory.
* **Incremental migration**: While you're migrating to Turborepo, you might have an in-between step where you have some scripts that you haven't moved to packages yet. In this case, you can create a Root Task to start migrating and fan the tasks out to packages later.
* **Scripts without a package scope**: You may have some scripts that don't make sense in the context of specific packages. Those scripts can be registered as Root Tasks so you can still run them with `turbo` for caching, parallelization, and workflow purposes.

## Advanced use cases

### Using Package Configurations

[Package Configurations](/docs/reference/package-configurations) are `turbo.json` files that are placed directly into a package. This allows a package to define specific behavior for its own tasks without affecting the rest of the repository.

In large monorepos with many teams, this allows teams greater control over their own tasks. To learn more, visit [the Package Configurations documentation](/docs/reference/package-configurations)

### Composing configurations

[Package Configurations](/docs/reference/package-configurations) can be composed for greater control with less configuration:

* [**Extending from other packages**](/docs/reference/package-configurations#extending-from-other-packages-pre-release): Create shared configuration packages that multiple packages can extend from, enabling shared `turbo.json` configurations.
* [**Adding to extended configurations**](/docs/reference/package-configurations#extending-arrays-with-turbo_extends-pre-release): Use the `$TURBO_EXTENDS$` microsyntax to add to inherited array values like `outputs` and `env` instead of replacing them.

### Long-running tasks with runtime dependencies

You might have a long-running task that requires another task to always be running at the same time. For this, use [the `with` key](/docs/reference/configuration#with).

A long-running task never exits, meaning you can't depend on it. Instead, the `with` keyword will run the `api#dev` task whenever the `web#dev` task runs.

### Performing side-effects

Some tasks should always be run no matter what, like a deployment script after a cached build. For these tasks, add `"cache": false` to your task definition.

### Dependent tasks that can be run in parallel

Some tasks can be run in parallel despite being dependent on other packages. An example of tasks that fit this description are type checkers, since a type checker doesn't need to wait for outputs in dependencies to run successfully.

Because of this, you may be tempted to define your `check-types` task like this:

This runs your tasks in parallel - but doesn't account for source code changes in dependencies. This means you can:

1. Make a breaking change to the interface of your `ui` package.
2. Run `turbo check-types`, hitting cache in an application package that depends on `ui`.

This is incorrect, since the application package will show a successful cache hit, despite not being updated to use the new interface. Checking for TypeScript errors in your application package manually in your editor is likely to reveal errors.

Because of this, you make a small change to your `check-types` task definition:

If you test out making breaking changes in your `ui` package again, you'll notice that the caching behavior is now correct. However, tasks are no longer running in parallel.

To meet both requirements (correctness and parallelism), you can introduce [Transit Nodes](/docs/core-concepts/package-and-task-graph#transit-nodes) to your Task Graph:

These Transit Nodes create a relationship between your package dependencies using a task that doesn't do anything because it doesn't match a script in any `package.json`s. Because of this, your tasks can run in parallel **and** be aware of changes to their internal dependencies.

<Callout type="info">
  In this example, we used the name `transit` - but you can name the task
  anything that isn't already a script in your Workspace.
</Callout>

There are more options available in [the Configuring `turbo.json` documentation](/docs/reference/configuration) that you will explore in the coming guides. For now, you can start running a few tasks to see how the basics work.

- [Constructing CI](/crafting-your-repository/constructing-ci.md): Learn how Turborepo can help you efficiently complete all the necessary tasks and accelerate your development workflow.

import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Step, Steps } from '#components/steps';

Turborepo speeds up builds, lints, tests, and any other tasks that you need to do in your Continuous Integration pipelines. Through parallelization and [Remote Caching](/docs/core-concepts/remote-caching), Turborepo makes your CI dramatically faster.

For examples of how to connect your CI vendor to Remote Cache and run tasks, visit our [CI guides](/docs/guides/ci-vendors).

## Enabling Remote Caching

To enable Remote Caching for your CI, setup the environment variables for Turborepo to access your Remote Cache.

| Environment Variable | Description                                                                                                                                                                                                                                                                                                                  |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TURBO_TOKEN`        | The Bearer token to access the Remote Cache                                                                                                                                                                                                                                                                                  |
| `TURBO_TEAM`         | The account name associated with your repository. When using{' '} <a href="https://vercel.com/docs/monorepos/remote-caching#vercel-remote-cache" rel="noreferrer noopener" target="_blank">Vercel Remote Cache</a>, this is [your team's slug](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fsettings\&title=Get+team+slug). |

When you run tasks through `turbo`, your CI will be able to hit cache, speeding up your pipelines.

<Callout type="info" title="Remote Cache hosting">
  Vercel's built-in CI/CD is automatically connected to your managed Vercel Remote Cache with zero configuration. To retrieve a token for connecting your other CI vendors to Vercel Remote Cache, visit the [Vercel Remote Cache documentation](https://vercel.com/docs/monorepos/remote-caching#use-remote-caching-from-external-ci/cd).

For self-hosted Remote Cache options, visit [Turborepo's Remote Cache documentation](/docs/core-concepts/remote-caching#remote-cache-api).
</Callout>

## Running tasks in CI

By [installing `turbo` globally](/docs/getting-started/installation#global-installation) onto your development and CI machines, you can use one mental model to run your entire repository, from development to ship. The tasks that you've registered in your `turbo.json` will work exactly the same in CI.

* For more information on how to set up tasks, visit the [Configuring Tasks](/docs/crafting-your-repository/configuring-tasks) page.
* For examples of running tasks in CI, visit our [CI guides](/docs/guides/ci-vendors).

### Filtering for entry points

You can filter your tasks using [the `--filter` flag](/docs/reference/run#--filter-string) exactly the same as when you're working with `turbo` locally. Filtering by packages, directories, and Git history are all supported in CI.

<Callout type="info" title="Using Git history in CI">
  Filtering using source control changes is only possible when history is
  available on the machine. If you are using shallow clones, history will not be
  available.
</Callout>

You can also use [the `--affected` flag](#running-only-affected-tasks) to only run tasks in packages that have changes.

Docker is an important part of many deployment pipelines. [Turborepo's `prune` subcommand](/docs/reference/prune) helps you ship lightweight images by removing unnecessary dependencies and code from your images.

For more on how to deploy from a Turborepo with Docker, visit [the dedicated Docker guide](/docs/guides/tools/docker).

## Skipping tasks and other unnecessary work

### Running only affected tasks

You can use the `--affected` flag to only run tasks that have changes.

You'll want to use this flag in situations like:

* You're running many tasks across packages in your monorepo, and only want to run those tasks in packages with code changes.
* You’re *not* using a Remote Cache, but still want to do as little work as possible in CI.
* You *are* using a Remote Cache, and you’re in a large repository. By minimizing the amount of tasks that will be restored from cache, there will be less data to send across the network, resulting in faster cache restoration.
* You’re already using [advanced filtering techniques](/docs/reference/run#advanced-filtering-examples) or [`turbo-ignore`](/docs/reference/turbo-ignore) to create the same or similar behavior as `--affected`. You likely have the opportunity to simplify your scripting using this new flag.
  * `--affected` will can handle shallow clones more gracefully than bespoke filtering because it falls back to running all tasks.

#### Using `--affected` in GitHub Actions

CI/CD pipelines are a perfect place to use `--affected`. With `--affected`, Turborepo can automatically detect that you're running in GitHub Actions by inspecting environment variables set by GitHub, like `GITHUB_BASE_REF`.

In the context of a PR, this means that Turborepo can determine which packages have changed between the PR's base branch and the PR's head branch. This allows you to run tasks only for the packages that are affected by the changes in the PR.

While `GITHUB_BASE_REF` works well in `pull_request` and `pull_request_target` events, it is not available during regular push events. In those cases, we use `GITHUB_EVENT_PATH` to determine the base branch to compare your commit to. In force pushes and pushing branch with no additional commits, we compare to the parent of the first commit on the branch.

### Using `turbo-ignore`

As your codebase and CI grow, you may start to look for more ways to get even faster. While hitting cache is useful, you also may be able to skip work entirely. Using `turbo-ignore`, you can skip lengthy container preparation steps like dependency installation that will end up resulting in a cache hit, anyway.

<Steps>
  <Step>
    ### Checkout the repository

Start by cloning your repository. Note that a clone with history to the cloning depth you plan on using is necessary for comparisons.

<Callout type="good-to-know">
      By default, `turbo-ignore` uses the parent commit. To customize for more
      depth, see [the turbo-ignore reference](/docs/reference/turbo-ignore).
    </Callout>
  </Step>

<Step>
    ### Run `turbo-ignore` for the package and task

By default, `turbo-ignore` will use the `build` task in the current working directory.

* To check for changes to a different task, use the `--task` flag.
    * To check for changes for a specific package and its dependencies, add the package's name as an argument.

<Tabs items={["web#build (Named)", "web#build (Inferred)", "docs#test (--task flag)"]}>
      <Tab value="web#build (Named)">
        Check for changes for the `build` task for the `web` package and its dependencies by adding the `web` package as an argument:

<Tab value="web#build (Inferred)">
        Check for changes for the `build` task for the `web` package and its dependencies using [Automatic Package Scoping](/docs/crafting-your-repository/running-tasks#automatic-package-scoping):

<Tab value="docs#test (--task flag)">
        Check for changes for the `test` task for the `docs` package and its dependencies using [Automatic Package Scoping](/docs/crafting-your-repository/running-tasks#automatic-package-scoping) and the `--task` flag:

</Tab>
    </Tabs>
  </Step>

<Step>
    ### Handle the result

If changes are detected in the package or its [Internal Dependencies](/docs/core-concepts/internal-packages), `turbo` will exit with a `1` status code. If no changes are detected, it will exit with `0`.

Using this status code, you can choose what the rest of your CI pipeline should do. For instance, a `1` exit code likely means that you should move forward with installing dependencies and running tasks.
  </Step>
</Steps>

For more advanced use cases, see the [`turbo-ignore` reference](/docs/reference/turbo-ignore).

Turborepo's caching abilities allow you to create fast CI pipelines with minimal complexity. Through [Remote Caching](/docs/core-concepts/remote-caching) and using the `--filter` flag to target packages for builds, Turborepo will handle change detection for large monorepos with little overhead.

For example, your CI could run these two commands to quickly handle quality checks and build your target application:

* `turbo run lint check-types test`: Run quality checks for your entire repository. Any packages that haven't changed will hit cache.
* `turbo build --filter=web`: Build the `web` package using the `build` task you've registered in `turbo.json`. If the `web` package or its dependencies haven't changed, the build will also hit cache.

As your codebase scales, you may find more specific opportunities to optimize your CI - but relying on caching is a great place to start.

### Global `turbo` in CI

Using global `turbo` is convenient in CI workflows, allowing you to easily run commands specific to your CI and take advantage of [Automatic Workspace Scoping](/docs/crafting-your-repository/running-tasks#automatic-package-scoping).

However, in some cases, you may be running `turbo` commands or scripts that use `turbo` **before installing packages with your package manager**. One example of this is [using `turbo prune` to create a Docker image](/docs/guides/tools/docker#example). In this situation, global `turbo` will not be able to use the version from `package.json` because the binary for that version hasn't been installed yet.

For this reason, we encourage you to **pin your global installation of `turbo` in CI to the major version in `package.json`** since breaking changes will not be introduced within a major version. You could additionally opt for added stability by pinning an exact version, trading off for maintenance burden to receive bug fixes in patch releases.

### Use `turbo run` in CI

`turbo run` is the most common command you will use when working in your Turborepo so it is aliased to `turbo` for convenience. While this is great for working locally, there are other subcommands for `turbo` like [`turbo prune`](/docs/reference/prune) and [`turbo generate`](/docs/reference/generate).

We're always working to make `turbo` better so we may add more subcommands in the future. For this reason, you can prevent naming collisions by using `turbo run` in your CI.

As an example, if you have a `turbo deploy` command in your CI pipelines, it may conflict with a potential `deploy` subcommand built directly into the `turbo` CLI. To avoid this, use `turbo run deploy` in your CI pipeline instead.

### Hitting cache results in broken builds

If your task is **passing when you miss cache but failing when you hit cache**, you likely haven't configured [the `outputs` key](/docs/reference/configuration#outputs) for your task correctly.

### Deployment using the wrong environment variables

If you haven't defined the `env` or `globalEnv` keys for your task, Turborepo will not be able to use them when creating hashes. This means your task can hit cache despite being in a different environment.

Check your configuration for the `env` and `globalEnv` keys.

You now have everything you need to ship applications with Turborepo. To learn more about specific use cases, [check the Guides](/docs/guides) or [dive deeper into core concepts](/docs/core-concepts).

- [Creating an Internal Package](/crafting-your-repository/creating-an-internal-package.md): Learn how to create an Internal Package for your monorepo.

import { Callout } from '#components/callout';
import { Steps, Step } from '#components/steps';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Files, File, Folder } from '#components/files';

[Internal Packages](/docs/core-concepts/internal-packages) are the building blocks of your workspace, giving you a powerful way to share code and functionality across your repo. Turborepo automatically understands the relationships between Internal Packages using the dependencies in `package.json`, creating a [Package Graph](/docs/core-concepts/package-and-task-graph#package-graph) under the hood to optimize your repository's workflows.

![Visual representation of a Package Graph in a Turborepo.](/images/docs/package-graph.png)

Let's create your first Internal Package to share math utilities in your repo using the guidance in the [Anatomy of a package](/docs/crafting-your-repository/structuring-a-repository#anatomy-of-a-package) section and the [Compiled Packages](/docs/core-concepts/internal-packages#compiled-packages) pattern. In the steps below, we assume you've [created a new repository using `create-turbo`](/docs/getting-started/installation) or are using a similarly structured repository.

<Steps>
  <Step>
    ### Create an empty directory

You'll need a directory to put the package in. Let's create one at `./packages/math`.

<Files>
      <File name="package.json" />

<File name="turbo.json" />

<Folder name="apps" />

<Folder name="packages" defaultOpen>
        <Folder name="math" green defaultOpen />

<Folder name="ui">
          <File name="package.json" />
        </Folder>

<Folder name="eslint-config">
          <File name="package.json" />
        </Folder>

<Folder name="typescript-config">
          <File name="package.json" />
        </Folder>
      </Folder>
    </Files>
  </Step>

<Step>
    ### Add a package.json

Next, create the `package.json` for the package. By adding this file, you'll fulfill [the two requirements for an Internal Package](/docs/crafting-your-repository/structuring-a-repository#specifying-packages-in-a-monorepo), making it discoverable to Turborepo and the rest of your Workspace.

<Callout type="warn">
      The `name` field in your `package.json` determines how your package can be
      imported throughout your workspace. The name you choose here (e.g.
      `@repo/math`) is exactly how other packages will import it (e.g. `import {add}
        from '@repo/math/add'`).
    </Callout>

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        
      </Tab>

<Tab value="yarn">
        
      </Tab>

<Tab value="npm">
        
      </Tab>

<Tab value="bun">
        
      </Tab>
    </Tabs>

Let's break down this `package.json` piece-by-piece:

* **`name`**: This is the most critical field for package discoverability. The value `@repo/math` becomes the exact identifier used in import statements throughout your workspace. If you change this name, you must update all import statements accordingly.
    * **`scripts`**: The `dev` and `build` script compile the package using [the TypeScript compiler](https://www.typescriptlang.org/docs/handbook/compiler-options.html). The `dev` script will watch for changes to source code and automatically recompile the package.
    * **`devDependencies`**: `typescript` and `@repo/typescript-config` are `devDependencies` so you can use those packages in the `@repo/math` package. In a real-world package, you will likely have more `devDependencies` and `dependencies` - but we can keep it simple for now.
    * **`exports`**: Defines multiple entrypoints for the package so it can be used in other packages (`import { add } from '@repo/math/add'`).

Notably, this `package.json` declares an Internal Package, `@repo/typescript-config`, as a dependency. Turborepo will recognize `@repo/math` as a dependent of `@repo/typescript-config` for ordering your tasks.
  </Step>

<Step>
    ### Add a `tsconfig.json`

Specify the TypeScript configuration for this package by adding a `tsconfig.json` file to **the root of the package**. TypeScript has [an `extends` key](https://www.typescriptlang.org/tsconfig#extends), allowing you to use a base configuration throughout your repository and overwrite with different options as needed.

You've done four important things here:

* The `@repo/typescript-config/base.json` configuration that lives in `./packages/typescript-config` has all the configuration you need so you extend from it.
    * [The `outDir` key](https://www.typescriptlang.org/tsconfig/#outDir) in `compilerOptions` tells TypeScript where to put the compiled output. It matches the directory specified in your `exports` in `package.json`.
    * [The `rootDir` key in `compilerOptions`](https://www.typescriptlang.org/tsconfig/#rootDir) ensures that the output in `outDir` uses the same structure as the `src` directory.
    * The [`include`](https://www.typescriptlang.org/tsconfig/#include) and [`exclude`](https://www.typescriptlang.org/tsconfig/#exclude) keys are not inherited from the base configuration, [according to the TypeScript specification](https://www.typescriptlang.org/tsconfig#include), so you've included them here.

<Callout type="info">
      There's a lot more to learn about TypeScript configuration, but this is a good
      place to start for now. If you'd like to learn more, visit [the official
      TypeScript documentation](https://www.typescriptlang.org/tsconfig) or [our
      TypeScript guide](/docs/guides/tools/typescript).
    </Callout>
  </Step>

<Step>
    ### Add a `src` directory with source code

You can now write some code for your package. Create two files inside a `src` directory:

<Tabs items={['add.ts', 'subtract.ts']}>
      <Tab value="add.ts">
        
      </Tab>

<Tab value="subtract.ts">
        
      </Tab>
    </Tabs>

These files map to the outputs that will be created by `tsc` when you run `turbo build` in a moment.
  </Step>

<Step>
    ### Add the package to an application

You're ready to use your new package in an application. Let's add it to the `web` application.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        
      </Tab>

<Tab value="yarn">
        
      </Tab>

<Tab value="npm">
        
      </Tab>

<Tab value="bun">
        
      </Tab>
    </Tabs>

<Callout type="warn">
      You just changed the dependencies in your repo. Make sure to run your package
      manager's installation command to update your lockfile.
    </Callout>

`@repo/math` is now available in the `web` application, you can use it in your code:

<Step>
    ### Edit `turbo.json`

Add the artifacts for the new `@repo/math` library to the `outputs` for the `build` task in `turbo.json`. This ensures that its build outputs will be cached by Turborepo, so they can be restored instantly when you start running builds.

<Step>
    ### Run `turbo build`

If you've [installed `turbo` globally](/docs/getting-started/installation#global-installation), run `turbo build` in your terminal at the root of your Workspace. You can also run the `build` script from `package.json` with your package manager, which will use `turbo run build`.

The `@repo/math` package built before the `web` application built so that the runtime code in `./packages/math/dist` is available to the `web` application when it bundles.

<Callout type="info">
      You can run `turbo build` again to see your `web` application rebuild in
      **milliseconds**. We'll discuss this at length in [the Caching
      guide](/docs/crafting-your-repository/caching).
    </Callout>
  </Step>
</Steps>

## Best practices for Internal Packages

### One "purpose" per package

When you're creating Internal Packages, it's recommended to create packages that have a single "purpose". This isn't a strict science or rule, but a best practice depending on your repository, your scale, your organization, what your teams need, and more. This strategy has several advantages:

* **Easier to understand**: As a repository scales, developers working in the repository will more easily be able to find the code they need.
* **Reducing dependencies per package**: Using fewer dependencies per package makes it so Turborepo can more effectively [prune the dependencies of your package graph](/docs/reference/prune).

Some examples include:

* **`@repo/ui`**: A package containing all of your shared UI components
* **`@repo/tool-specific-config`**: A package for managing configuration of a specific tool
* **`@repo/graphs`**: A domain-specific library for creating and manipulating graphical data

### Application Packages do not contain shared code

When you're creating [Application Packages](/docs/core-concepts/package-types#application-packages), it's best to avoid putting shared code in those packages. Instead, you should create a separate package for the shared code and have the application packages depend on that package.

Additionally, Application Packages are not meant to be installed into other packages. Instead, they should be thought of as an entrypoint to your [Package Graph](/docs/core-concepts/package-and-task-graph#package-graph).

<Callout type="good-to-know">
  There are [rare
  exceptions](/docs/core-concepts/package-types#installing-an-applicaiton-package-into-another-package)
  to this rule.
</Callout>

With a new Internal Package in place, you can start [configuring tasks](/docs/crafting-your-repository/configuring-tasks).

- [Developing applications](/crafting-your-repository/developing-applications.md): Learn how to develop applications in your repository.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { LinkToDocumentation } from '#components/link-to-documentation';

Developing applications in a monorepo unlocks powerful workflows, enabling you to make atomic commits to source control with easy access to code.

Most development tasks are long-running tasks that watch for changes to your code. Turborepo enhances this experience with a powerful terminal UI and other capabilities like:

* [Configuration for `dev` tasks](#configuring-development-tasks)
* [Interacting with tasks](#interacting-with-tasks)
* [Watch Mode](#watch-mode)
* [Running setup scripts](#running-setup-tasks-before-dev)
* [Filtering tasks to run a subset of your packages](#running-a-specific-application)

## Configuring development tasks

Defining a development task in `turbo.json` tells Turborepo that you'll be running a long-lived task. This is useful for things like running a development server, running tests, or building your application.

To register a `dev` task, add it to your `turbo.json` with two properties:

* **"cache": false**: Tells Turborepo to not attempt to cache the results of the task. Since this is a development task, you're likely to be making frequent changes to your code, so caching the results is not useful.
* **"persistent": true**: Tells Turborepo to keep the task running until you stop it. This key serves as a signal for your terminal UI to treat the task as long-running and interactive. Additionally, it prevents you from accidentally depending on a task that will not exit.

You can now run your `dev` task to start your development scripts in parallel:

### Running setup tasks before `dev`

You may also want to run scripts that set up your development environment or pre-build packages. You can make sure those tasks run before the `dev` task with `dependsOn`:

In this example, we're using a [Root Task](/docs/crafting-your-repository/configuring-tasks#registering-root-tasks) but you can use the same idea for [arbitrary tasks in packages](/docs/crafting-your-repository/configuring-tasks#depending-on-a-specific-task-in-a-specific-package).

### Running a specific application

The `--filter` flag allows you to pick a subset of your [Package Graph](/docs/core-concepts/package-and-task-graph#package-graph) so you can run your `dev` task for a specific application and its dependencies:

## Using the terminal UI

Turborepo's terminal UI enables a number of features that create a highly interactive experience around your tasks.

### Customizing your view

You can quickly adjust the UI to your needs using keybinds.

| Keybind | Action                                                            |
| ------- | ----------------------------------------------------------------- |
| `m`     | Toggle popup listing keybinds                                     |
| `↑`/`↓` | Select the next/previous task in the task list                    |
| `j`/`k` | Select the next/previous task in the task list                    |
| `p`     | Toggle selection pinning for selected task                        |
| `h`     | Toggle visibility of the task list                                |
| `c`     | When logs are highlighted, copy selection to the system clipboard |
| `u`/`d` | Scroll logs `u`p and `d`own                                       |

### Interacting with tasks

Some of your tools may allow you to type input into them. Examples of this include Drizzle ORM's interactive migrations or Jest's filtering and re-running of test suites.

You can interact with tasks that are [marked as interactive](/docs/reference/configuration#interactive) to give them input.

| Keybind  | Action            |
| -------- | ----------------- |
| `i`      | Begin interacting |
| `Ctrl+z` | Stop interacting  |

Many tools have a built-in watcher, like [`tsc --watch`](https://www.typescriptlang.org/docs/handbook/compiler-options.html#compiler-options),
that will respond to changes in your source code. However, some don't.

`turbo watch` adds a dependency-aware watcher to any tool. Changes to source code will follow [the Task Graph](/docs/core-concepts/package-and-task-graph#task-graph) that you've described in `turbo.json`, just like all your other tasks.

For example, using a package structure like [`create-turbo`](/docs/reference/create-turbo) with the following tasks and scripts:

<Tabs items={["turbo.json", "packages/ui", "apps/web"]}>
  <Tab value="turbo.json">
    
  </Tab>

<Tab value="packages/ui">
    
  </Tab>

<Tab value="apps/web">
    
  </Tab>
</Tabs>

When you run `turbo watch dev lint`, you'll see the `lint` scripts are re-run whenever you make source code changes, despite ESLint not having a built-in watcher. `turbo watch` is also aware of internal dependencies, so a code change in `@repo/ui` will re-run the task in both `@repo/ui` and `web`.

The Next.js development server in `web` and the TypeScript Compiler's built-in watcher in `@repo/ui` will continue to work as usual, since they are marked with `persistent`.

For more information, [visit the `turbo watch` reference](/docs/reference/watch).

In some cases, you may want to run a script when the `dev` task is stopped. Turborepo is unable to run those teardown scripts when exiting because `turbo` exits when your `dev` tasks exit.

Instead, create a `turbo dev:teardown` script that you run separately after you've exited your primary `turbo dev` task.

Once you have a version of your application that you'd like to deploy, it's time to learn how to configure environment variables in Turborepo.

- [Crafting your repository](/crafting-your-repository/index.md): Design and build your Turborepo.

import { Card, Cards } from '#components/card';
import { Callout } from '#components/callout';

Architecting a monorepo is a careful process. Through these guides, you'll learn how to design and build a monorepo that will make every team faster - no matter the size.

The guides in this section will take you through building a multi-package workspace, commonly referred to as a monorepo. They are meant to be read in order as they build on top of the knowledge from previous guides, but you can read them in any order or skip to the pages specific to your use case.

By the time you've read through all of this section, you should have a good understanding of how to design and build a monorepo with Turborepo.

<Callout type="info">
  Turborepo can also be used to speed up single-package workspaces. Visit the
  [single-package workspace](/docs/guides/single-package-workspaces) section for
  more information.
</Callout>

## From zero to `turbo`

<Cards>
  <Card href="/docs/crafting-your-repository/structuring-a-repository" title="1. Structuring a repository" description="Design the directory structure of your monorepo." />

<Card href="/docs/crafting-your-repository/managing-dependencies" title="2. Managing dependencies" description="Using dependencies for sharing code" />

<Card href="/docs/crafting-your-repository/creating-an-internal-package" title="3. Creating an internal package" description="Make a package in your repository" />

<Card href="/docs/crafting-your-repository/configuring-tasks" title="4. Configuring tasks" description="Design your task patterns" />

<Card href="/docs/crafting-your-repository/running-tasks" title="5. Running tasks" description="Run tasks as fast as possible" />

<Card href="/docs/crafting-your-repository/caching" title="6. Caching" description="Never do the same work twice" />

<Card href="/docs/crafting-your-repository/developing-applications" title="7. Developing apps" description="Run many apps in parallel" />

<Card href="/docs/crafting-your-repository/using-environment-variables" title="8. Using environment variables" description="Account for variables in your environment" />

<Card href="/docs/crafting-your-repository/constructing-ci" title="9. Constructing CI" description="Ship your applications" />

<Card href="/docs/crafting-your-repository/upgrading" title="10. Upgrading" description="Upgrading your Turborepo version" />

<Card href="/docs/crafting-your-repository/understanding-your-repository" title="11. Understanding your repository" description="Understanding your codebase with Turborepo" />
</Cards>

We also have more guides centered around [specific tools, use cases, and other topics](/docs/guides).

- [Managing dependencies](/crafting-your-repository/managing-dependencies.md): Learn how to manage dependencies in your monorepo's workspace.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';
import { LinkToDocumentation } from '#components/link-to-documentation';

* **External dependencies** come from [the npm registry](https://www.npmjs.com/), allowing you to leverage valuable code from the ecosystem to build your applications and libraries faster.
* **Internal dependencies** let you share functionality within your repository, dramatically improving discoverability and usability of shared code. We will discuss how to build an Internal Package in [the next guide](/docs/crafting-your-repository/creating-an-internal-package).

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

## Best practices for dependency installation

### Install dependencies where they're used

When you install a dependency in your repository, you should install it directly in the package that uses it. The package's `package.json` will have every dependency that the package needs. This is true for both external and internal dependencies.

<Callout type="good-to-know">
  Note that your package manager may choose to [use a different node\_modules
  location than the package](#node_modules-locations).
</Callout>

To quickly install dependencies in multiple packages, you can use your package manager:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">

<LinkToDocumentation href="https://pnpm.io/cli/recursive">pnpm documentation</LinkToDocumentation>
  </Tab>

<Tab value="yarn">
    Yarn 1:

<LinkToDocumentation href="https://classic.yarnpkg.com/en/docs/cli/add">
      Yarn 1 documentation
    </LinkToDocumentation>

<LinkToDocumentation href="https://yarnpkg.com/cli/workspaces/foreach#usage">
      Yarn 2+ documentation
    </LinkToDocumentation>
  </Tab>

<LinkToDocumentation href="https://docs.npmjs.com/cli/v7/using-npm/config#workspace">npm documentation</LinkToDocumentation>
  </Tab>

<LinkToDocumentation href="https://bun.sh/docs/install/workspaces">bun documentation</LinkToDocumentation>
  </Tab>
</Tabs>

This practice has several benefits:

* **Improved clarity**: It's easier to understand what a package depends on when its dependencies are listed in its `package.json`. Developers working in the repository can see at a glance what dependencies are used within the package.
* **Enhanced flexibility**: In a monorepo at scale, it can be unrealistic to expect each package to use the same version of an external dependency. When there are many teams working in the same codebase, there will be differing priorities, timelines, and needs due to the realities of [operating at scale](https://vercel.com/blog/how-to-scale-a-large-codebase). By installing dependencies in the package that uses them, you can enable your `ui` team to bump to the latest version of TypeScript, while your `web` team can prioritize shipping new features and bumping TypeScript later. Additionally, if you still want to keep dependency versions in sync, [you can do that, too](/docs/crafting-your-repository/managing-dependencies#keeping-dependencies-on-the-same-version).
* **Better caching ability**: If you install too many dependencies in the root of your repository, you'll be changing the workspace root whenever you add, update, or delete a dependency, leading to unnecessary cache misses.
* **Pruning unused dependencies**: For Docker users, [Turborepo's pruning feature](/docs/reference/prune) can remove unused dependencies from Docker images to create lighter images. When dependencies are installed in the packages that they are meant for, Turborepo can read your lockfile and remove dependencies that aren't used in the packages you need.

### Few dependencies in the root

Following the first principle above to [install dependencies in the package where they're used](#install-dependencies-where-theyre-used), you'll find that you naturally end up with few dependencies in the root of your workspace.

The only dependencies that belong in the workspace root are **tools for managing the repository** whereas dependencies for building applications and libraries are installed in their respective packages. Some examples of dependencies that make sense to install in the root are [`turbo`](https://www.npmjs.com/package/turbo), [`husky`](https://www.npmjs.com/package/husky), or [`lint-staged`](https://www.npmjs.com/package/lint-staged).

## Managing dependencies

### Turborepo does not manage dependencies

Note that Turborepo does not play a role in managing your dependencies, leaving that work up to your package manager of choice.

It's up to the package manager to handle things like downloading the right external dependency version, symlinking, and resolving modules. The recommendations on this page are best practices for managing dependencies in a Workspace, and are not enforced by Turborepo.

### Module resolution differs amongst package managers

Package managers have different module resolution algorithms, which leads to differences in behavior that can be difficult to predict.

In the Turborepo documentation, we make many recommendations according to the expected behaviors of the package managers. Our coverage of how to handle dependencies is best effort and you may need to adapt the documented behavior for your package manager or repository's needs.

However, if you find an issue with the documentation that appears to be universally incorrect for all package managers or a specific one, please let us know with a GitHub Issue so we can improve.

### node\_modules locations

Depending on your choice of package manager, version, settings, and where your dependencies are installed in your Workspace, you may see `node_modules` and the dependencies inside it in various locations within the Workspace. Dependencies could be found in the root `node_modules`, in packages' `node_modules`, or both.

As long as your scripts and tasks are able to find the dependencies they need, your package manager is working correctly.

<Callout type="info" title="Referencing `node_modules` in your code">
  The specific locations for `node_modules` within the Workspace are not a part of the public API of package managers. This means that referencing `node_modules` directly (like `node ./node_modules/a-package/dist/index.js`) can be brittle, since the location of the dependency on disk can change with other dependency changes around the Workspace.

Instead, rely on conventions of the Node.js ecosystem for accessing dependency modules whenever possible.
</Callout>

### Keeping dependencies on the same version

Some monorepo maintainers prefer to keep dependencies on the same version across all packages by rule. There are several ways to achieve this:

#### Using purpose-built tooling

Tools like [`syncpack`](https://www.npmjs.com/package/syncpack), [`manypkg`](https://www.npmjs.com/package/@manypkg/cli), and [`sherif`](https://www.npmjs.com/package/sherif) can be used for this specific purpose.

#### Using your package manager

You can use your package manager to update dependency versions in one command.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">

<small>[→ pnpm documentation](https://pnpm.io/cli/update#--recursive--r)</small>
  </Tab>

<Tab value="yarn">
    Yarn 1:

<small>[→ Yarn 1 documentation](https://classic.yarnpkg.com/en/docs/cli/upgrade-interactive)</small>

<small>[→ Yarn 2+ documentation](https://yarnpkg.com/cli/up)</small>
  </Tab>

<small>[→ npm documentation](https://docs.npmjs.com/cli/v7/using-npm/config#workspaces)</small>
  </Tab>

<Tab value="bun">
    No equivalent

<small>[→ Bun documentation](https://bun.sh/docs/install/workspaces)</small>
  </Tab>
</Tabs>

In pnpm v9.5+, you can use catalogs to define dependency version ranges as reusable constants. This will keep dependencies on the same version since you're referencing the same value across the workspace.

To learn more, [visit the pnpm catalogs documentation](https://pnpm.io/catalogs).

Your IDE's refactoring tooling can find and replace the version of a dependency across all `package.json` files in your repository at once. Try using a regex like `"next": ".*"` on `package.json` files to find all instances of the `next` package and replace them with the version you want. When you're done, make sure to run your package manager's install command to update your lockfile.

Now that you know how to manage dependencies effectively in a workspace, let's [create an Internal Package](/docs/crafting-your-repository/creating-an-internal-package) to be used as a dependency in your monorepo.

- [Running tasks](/crafting-your-repository/running-tasks.md): Learn how to run tasks in your repository through the `turbo` CLI.

import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { LinkToDocumentation } from '#components/link-to-documentation';
import { InVersion } from '#components/in-version';

Turborepo optimizes the developer workflows in your repository by automatically parallelizing and caching tasks. Once a task is [registered in `turbo.json`](/docs/crafting-your-repository/configuring-tasks), you have a powerful new toolset for running the scripts in your repository:

* [Use `scripts` in `package.json` for tasks you need to run often](#using-scripts-in-packagejson)
* [Use global `turbo` to quickly run custom tasks on-demand](#using-global-turbo)
* [Filter tasks by directories, package names, source control changes, and more](#using-filters)

Running tasks through `turbo` is powerful because you get one model for executing workflows throughout your repository in development and in your CI pipelines.

## Using `scripts` in `package.json`

For tasks that you run frequently, you can write your `turbo` commands directly into your root `package.json`.

<Callout type="good-to-know">
  `turbo` is an alias for `turbo run` - but we recommend using `turbo run` in
  `package.json` and CI workflows to avoid potential collisions with possible
  `turbo` subcommands that could be added in the future.
</Callout>

These scripts can then be run using your package manager.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

<Callout type="warn">
  You only want to write `turbo` commands in your root `package.json`. Writing `turbo` commands into the `package.json` of packages can lead to recursively
  calling `turbo`.
</Callout>

## Using global `turbo`

[Installing `turbo` globally](/docs/getting-started/installation#global-installation) lets you run commands directly from your terminal. This improves your local development experience since it makes it easier to run exactly what you need, when you need it.

Additionally, global `turbo` is useful in your CI pipelines, giving you maximum control of exactly which tasks to run at each point in your pipeline.

### Automatic Package Scoping

When you're in a package's directory, `turbo` will automatically scope commands to the [Package Graph](/docs/core-concepts/package-and-task-graph#package-graph) for that package. This means you can quickly write commands without having to [write filters](/docs/reference/run#--filter-string) for the package.

In the example above, the `turbo build` command will run the `build` task for the `docs` package using the `build` task registered in `turbo.json`.

<Callout type="good-to-know">
  [Using a filter](#using-filters) will override Automatic Package Scoping.
</Callout>

### Customizing behavior

In [the documentation for the `run` subcommand](/docs/reference/run), you'll find many useful flags to tailor the behavior of `turbo run` for what you need. When running global `turbo`, you can go faster using workflows like:

* **Variations of your most common commands**: The `build` script in `package.json` has the most utility when it is `turbo build` - but you might only be interested in a specific package at the moment. You can quickly filter for the specific package you're interested in using `turbo build --filter=@repo/ui`.
* **One-off commands**: Commands like `turbo build --dry` aren't needed often so you likely won't create a script in your `package.json` for it. Instead, you can run it directly in your terminal whenever you need it.
* **Overriding `turbo.json` configuration**: Some CLI flags have an equivalent in `turbo.json` that you can override. For instance, you may have a `turbo build` command configured to use [`"outputLogs": "full"` in `turbo.json`](/docs/reference/configuration#outputlogs) - but you're only interested in seeing errors at the moment. Using global `turbo`, you can use `turbo lint --output-logs=errors-only` to only show errors.

## Running multiple tasks

`turbo` is able to run multiple tasks, parallelizing whenever possible.

This command will run all of the tasks, automatically detecting where it can run a script as early as possible, according to your task definitions.

<Callout type="info" title="Ordering of tasks">
  `turbo test lint` will run tasks exactly the same as `turbo lint test`.

If you want to ensure that one task blocks the execution of another, express that relationship in your [task configurations](/docs/crafting-your-repository/configuring-tasks#defining-tasks).
</Callout>

While [caching](/docs/crafting-your-repository/running-tasks) ensures you stay fast by never doing the same work twice, you can also filter tasks to run only a subset of [the Task Graph](/docs/core-concepts/package-and-task-graph#task-graph).

There are many advanced use cases for filtering in [the `--filter` API reference](/docs/reference/run#--filter-string) but the most common use cases are discussed below.

### Filtering by package

Filtering by package is a simple way to only run tasks for the packages you're currently working on.

<InVersion version="2.2.4">
  You can also filter to a specific task for the package directly in your CLI command without needing to use `--filter`:

### Filtering by directory

Your repository might have a directory structure where related packages are grouped together. In this case, you can capture the glob for that directory to focus `turbo` on those packages.

### Filtering to include dependents

When you're working on a specific package, you might want to run tasks for the package and its dependents. The `...` microsyntax is useful when you're making changes to a package and want to ensure that the changes don't break any of its dependents.

### Filtering to include dependencies

To limit the scope to a package and its dependencies, append `...` to the package name. This runs the task for the specified package and all packages it depends on.

### Filtering by source control changes

Using filters to run tasks based on changes in source control is a great way to run tasks only for the packages that are affected by your changes. **Source control filters must be wrapped in `[]`**.

* **Comparing to the previous commit**: `turbo build --filter=[HEAD^1]`
* **Comparing to the main branch**: `turbo build --filter=[main...my-feature]`
* **Comparing specific commits using SHAs**: `turbo build --filter=[a1b2c3d...e4f5g6h]`
* **Comparing specific commits using branch names**: `turbo build --filter=[your-feature...my-feature]`

<Callout type="info">
  In general, you can rely on caching to keep your repository fast. When you're
  using [Remote Caching](/docs/core-concepts/remote-caching), you can count on
  hitting cache for unchanged packages.
</Callout>

### Combining filters

For even more specificity, you can combine filters to further refine the entrypoints into your [Task Graph](/docs/core-concepts/package-and-task-graph#task-graph).

Multiple filters are combined as a **union**, meaning that the [Task Graph](/docs/core-concepts/package-and-task-graph#task-graph) will include tasks that match any of the filters. For more information on advanced usage of filters, see [the `--filter` API reference](/docs/reference/run#--filter-string).

When you start running tasks in your repository, you might start noticing that your tasks get faster. Next, you'll explore [caching](/docs/crafting-your-repository/caching) and how `turbo` makes it so you never do the same work twice.

- [Structuring a repository](/crafting-your-repository/structuring-a-repository.md): Start by creating a repository using the conventions of the ecosystem.

import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Step, Steps } from '#components/steps';
import { File, Folder, Files } from '#components/files';
import { LinkToDocumentation } from '#components/link-to-documentation';

`turbo` is built on top of [Workspaces](https://vercel.com/docs/vercel-platform/glossary#workspace), a feature of package managers in the JavaScript ecosystem that allows you to group multiple packages in one repository.

Following these conventions is important because it allows you to:

* Lean on those conventions for all your repo's tooling
* Quickly, incrementally adopt Turborepo into an existing repository

In this guide, we'll walk through setting up a multi-package workspace (monorepo) so we can set the groundwork for `turbo`.

Setting up a workspace's structure can be tedious to do by hand. If you're new to monorepos, we recommend [using `create-turbo` to get started](/docs/getting-started/installation) with a valid workspace structure right away.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

You can then review the repository for the characteristics described in this guide.

## Anatomy of a workspace

In JavaScript, a workspace can either be [a single package](/docs/guides/single-package-workspaces) or a collection of packages. In these guides, we'll be focusing on [a multi-package workspace](https://vercel.com/docs/vercel-platform/glossary#monorepo), often called a "monorepo".

Below, the structural elements of `create-turbo` that make it a valid workspace are highlighted.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    <Files>
      <File name="package.json" green />

<File name="pnpm-lock.yaml" green />

<File name="pnpm-workspace.yaml" green />

<File name="turbo.json" />

<Folder name="apps" defaultOpen>
        <Folder name="docs" className="text-foreground" defaultOpen>
          <File name="package.json" green />
        </Folder>

<Folder name="web">
          <File name="package.json" green />
        </Folder>
      </Folder>

<Folder name="packages">
        <Folder name="ui">
          <File name="package.json" green />
        </Folder>
      </Folder>
    </Files>
  </Tab>

<Tab value="yarn">
    <Files>
      <File name="package.json" green />

<File name="yarn.lock" green />

<File name="turbo.json" />

<Folder name="apps" defaultOpen>
        <Folder name="docs" className="text-foreground" defaultOpen>
          <File name="package.json" green />
        </Folder>

<Folder name="web">
          <File name="package.json" green />
        </Folder>
      </Folder>

<Folder name="packages">
        <Folder name="ui">
          <File name="package.json" green />
        </Folder>
      </Folder>
    </Files>
  </Tab>

<Tab value="npm">
    <Files>
      <File name="package.json" green />

<File name="package-lock.json" green />

<File name="turbo.json" />

<Folder name="apps" defaultOpen>
        <Folder name="docs" className="text-foreground" defaultOpen>
          <File name="package.json" green />
        </Folder>

<Folder name="web">
          <File name="package.json" green />
        </Folder>
      </Folder>

<Folder name="packages">
        <Folder name="ui">
          <File name="package.json" green />
        </Folder>
      </Folder>
    </Files>
  </Tab>

<Tab value="bun">
    <Files>
      <File name="package.json" green />

<File name="bun.lock" green />

<File name="turbo.json" />

<Folder name="apps" defaultOpen>
        <Folder name="docs" className="text-foreground" defaultOpen>
          <File name="package.json" green />
        </Folder>

<Folder name="web">
          <File name="package.json" green />
        </Folder>
      </Folder>

<Folder name="packages">
        <Folder name="ui">
          <File name="package.json" green />
        </Folder>
      </Folder>
    </Files>
  </Tab>
</Tabs>

### Minimum requirements

* [Packages as described by your package manager](#specifying-packages-in-a-monorepo)
* [A package manager lockfile](#package-manager-lockfile)
* [Root `package.json`](#root-packagejson)
* [Root `turbo.json`](#root-turbojson)
* [`package.json` in each package](#packagejson-in-each-package)

### Specifying packages in a monorepo

<Steps>
  <Step>
    #### Declaring directories for packages

First, your package manager needs to describe the locations of your packages. We recommend starting with splitting your packages into `apps/` for applications and services and `packages/` for everything else, like libraries and tooling.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">

<LinkToDocumentation href="https://pnpm.io/pnpm-workspace_yaml">pnpm workspace documentation</LinkToDocumentation>
      </Tab>

<LinkToDocumentation href="https://yarnpkg.com/features/workspaces#how-are-workspaces-declared">yarn workspace documentation</LinkToDocumentation>
      </Tab>

<LinkToDocumentation href="https://docs.npmjs.com/cli/v7/using-npm/workspaces#defining-workspaces">npm workspace documentation</LinkToDocumentation>
      </Tab>

<LinkToDocumentation href="https://bun.sh/docs/install/workspaces">bun workspace documentation</LinkToDocumentation>
      </Tab>
    </Tabs>

Using this configuration, every directory **with a `package.json`** in the `apps` or `packages` directories will be considered a package.

<Callout type="error">
      Turborepo does not support nested packages like `apps/**` or `packages/**` due to ambiguous behavior among package managers in the JavaScript ecosystem. Using a structure that would put a package at `apps/a` and another at `apps/a/b` will result in an error.

If you'd like to group packages by directory, you can do this using globs like `packages/*` and `packages/group/*` and **not** creating a `packages/group/package.json` file.
    </Callout>
  </Step>

<Step>
    #### `package.json` in each package

In the directory of the package, there must be a `package.json` to make the package discoverable to your package manager and `turbo`. The [requirements for the `package.json` of a package](#anatomy-of-a-package) are below.
  </Step>
</Steps>

### Root `package.json`

The root `package.json` is the base for your workspace. Below is a common example of what you would find in a root `package.json`:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

### Root `turbo.json`

`turbo.json` is used to configure the behavior of `turbo`. To learn more about how to configure your tasks, visit the [Configuring tasks](/docs/crafting-your-repository/configuring-tasks) page.

### Package manager lockfile

A lockfile is key to reproducible behavior for both your package manager and `turbo`. Additionally, Turborepo uses the lockfile to understand the dependencies between your [Internal Packages](/docs/core-concepts/internal-packages) within your Workspace.

<Callout type="warn">
  If you do not have a lockfile present when you run `turbo`, you may see
  unpredictable behavior.
</Callout>

## Anatomy of a package

It's often best to start thinking about designing a package as its own unit within the Workspace. At a high-level, each package is almost like its own small "project", with its own `package.json`, tooling configuration, and source code. There are limits to this idea—but its a good mental model to *start* from.

Additionally, a package has specific entrypoints that other packages in your Workspace can use to access the package, specified by [`exports`](#exports).

### `package.json` for a package

[The `name` field](https://nodejs.org/api/packages.html#name) is used to identify the package. It should be unique within your workspace.

<Callout type="info">
  It's best practice to use a namespace prefix for your [Internal Packages](/docs/core-concepts/internal-packages) to avoid conflicts with other packages on the npm registry. For example, if your organization is named `acme`, you might name your packages `@acme/package-name`.

We use `@repo` in our docs and examples because it is an unused, unclaimable namespace on the npm registry. You can choose to keep it or use your own prefix.
</Callout>

The `scripts` field is used to define scripts that can be run in the package's context. Turborepo will use the name of these scripts to identify what scripts to run (if any) in a package. We talk more about these scripts on the [Running Tasks](/docs/crafting-your-repository/running-tasks) page.

[The `exports` field](https://nodejs.org/api/packages.html#exports) is used to specify the entrypoints for other packages that want to use the package. When you want to use code from one package in another package, you'll import from that entrypoint.

For example, if you had a `@repo/math` package, you might have the following `exports` field:

Note that this example uses the [Just-in-Time Package](/docs/core-concepts/internal-packages#just-in-time-packages) pattern for simplicity. It exports TypeScript directly, but you might choose to use the [Compiled Package](/docs/core-concepts/internal-packages#compiled-packages) pattern instead.

<Callout type="info">
  The `exports` field in this example requires modern versions of Node.js and
  TypeScript.
</Callout>

This would allow you to import `add` and `subtract` functions from the `@repo/math` package like so:

Using exports this way provides three major benefits:

* **Avoiding barrel files**: Barrel files are files that re-export other files in the same package, creating one entrypoint for the entire package. While they might appear convenient, they're [difficult for compilers and bundlers to handle](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js#what's-the-problem-with-barrel-files) and can quickly lead to performance problems.
* **More powerful features**: `exports` also has other powerful features compared to [the `main` field](https://nodejs.org/api/packages.html#main) like [Conditional Exports](https://nodejs.org/api/packages.html#conditional-exports). In general, we recommend using `exports` over `main` whenever possible as it is the more modern option.
* **IDE autocompletion**: By specifying the entrypoints for your package using `exports`, you can ensure that your code editor can provide auto-completion for the package's exports.

#### `imports` (optional)

[The `imports` field](https://nodejs.org/api/packages.html#imports) gives you a way to create subpaths to other modules within your package. You can think of these like "shortcuts" to write simpler import paths that are more resilient to refactors that move files. To learn how, visit [the TypeScript page](/docs/guides/tools/typescript#use-nodejs-subpath-imports-instead-of-typescript-compiler-paths).

<Callout type="info">
  You may be more familiar with TypeScript's `compilerOptions#paths` option, which accomplishes a similar goal. As of TypeScript 5.4, TypeScript can infer subpaths from `imports`, making it a better option since you'll be working with Node.js conventions. For more information, visit [our TypeScript guide](/docs/guides/tools/typescript#use-nodejs-subpath-imports-instead-of-typescript-compiler-paths).
</Callout>

Of course, you'll want some source code in your package. Packages commonly use a `src` directory to store their source code and compile to a `dist` directory (that should also be located within the package), although this is not a requirement.

* If you're using TypeScript, you likely don't need a `tsconfig.json` in the root of your workspace. Packages should independently specify their own configurations, usually building off of a shared `tsconfig.json` from a separate package in the workspace. For more information, visit [the TypeScript guide](/docs/guides/tools/typescript#you-likely-dont-need-a-tsconfigjson-file-in-the-root-of-your-project).
* You want to avoid accessing files across package boundaries as much as possible. If you ever find yourself writing `../` to get from one package to another, you likely have an opportunity to re-think your approach by installing the package where it's needed and importing it into your code.

With your Workspace configured, you can now use your package manager to [install dependencies into your packages](/docs/crafting-your-repository/managing-dependencies).

- [Understanding your repository](/crafting-your-repository/understanding-your-repository.md): Learn how to understand your repository structure using Turborepo.

import { PrereleaseBadge } from '#components/prerelease-badge';

Turborepo includes tools for understanding your repository structure, that can help you use and optimize your codebase.

## `turbo devtools` <PrereleaseBadge />

`turbo devtools` provides a browser-based visualization of your package graph. This tool can be helpful for diagnosing issues with your task graph and understanding the structure of your monorepo.

For more information, see the [reference documentation](/docs/reference/devtools).

To list your packages, you can run `turbo ls`. This will show the packages in your repository and where they're located.

You can [apply filters](/docs/crafting-your-repository/running-tasks#using-filters) to `ls`, just like `run`:

To determine which tasks can be run in your monorepo, simply call `turbo run` without any tasks. You will get a list of
tasks and the packages in which they are defined:

If you wish to dig into your repository structure, since `2.2.0`, Turborepo provides a GraphQL interface into your repository
via `turbo query`. You can execute queries such as finding all packages that have a `test` task:

This can be helpful for diagnosing potential problems in your package or task dependency graph. For instance, let's say
you're getting a lot of cache misses in your builds. This could be because there's a package that keeps getting changed
and is imported throughout your codebase.

To do this, we can run a query to find packages that are directly imported more than 10 times in your monorepo:

Now that we've found this package, we can try to split it up into smaller packages so that a small change won't
invalidate the whole dependency graph.

Or let's say you're using our new `--affected` flag, but you're still running more tasks than you'd like.
With `turbo query`, you can find all the packages and the reason why they were invalidated:

- [Upgrading](/crafting-your-repository/upgrading.md): Learn how to upgrade `turbo` to get the latest improvements to your repository.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Steps, Step } from '#components/steps';
import { Callout } from '#components/callout';

<Steps>
  <Step>
    ### Update `turbo.json`

Get started upgrading from 1.x to 2.0 by running:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        
      </Tab>

<Tab value="yarn">
        
      </Tab>

<Tab value="npm">
        
      </Tab>

<Tab value="bun">
        
      </Tab>
    </Tabs>

This will update your `turbo.json`(s) for many of the breaking changes from 1.x to 2.0.

Additionally, a `name` field will be added to any `package.json` in the Workspace that doesn't have one.

<Callout type="good-to-know">
      You may also manually run each codemod individually. Visit [the codemods
      page](/docs/reference/turbo-codemod#turborepo-2x) for more information.
    </Callout>
  </Step>

<Step>
    ### Add a `packageManager` field to root `package.json`

[The `packageManager` field](https://nodejs.org/api/packages.html#packagemanager) is a convention from the Node.js ecosystem that defines which package manager is expected to be used in the Workspace.

Turborepo 2.0 requires that your Workspace define this field as a way to improve the stability and behavioral predictability of your codebase. If you do not have one already, add this field to your root `package.json`:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        
      </Tab>

<Tab value="yarn">
        
      </Tab>

<Tab value="npm">
        
      </Tab>

<Tab value="bun">
        
      </Tab>
    </Tabs>
  </Step>

<Step>
    ### Update `eslint-config-turbo`

[`eslint-config-turbo`](/docs/reference/eslint-config-turbo) helps identify environment variables that need to be added to the [`env`](/docs/reference/configuration#env) key for caching. If you're using it, make sure you update it to match your major version.
  </Step>

<Step>
    ### Update `turbo run` commands

Turborepo 2.0 includes behavioral and correctness improvements with behavior of `turbo run` commands. Listed below is the summary of changes, which may or may not have an affect on your codebase:

* Strict Mode for environment variables is now the default, moving from Loose Mode ([PR](https://github.com/vercel/turborepo/pull/8182))
      * If it appears that the scripts in your tasks are missing environment variables, you can opt back out of this behavior using [the `--env-mode` option](/docs/reference/run#--env-mode-option) on a per-command basis to incrementally migrate. We encourage you to update [the `env` key](/docs/reference/configuration#env) in your task to account for all of its environment variables so you can drop the `--env-mode` option as soon as possible.
      * If you'd like to set the default for the repository back to Loose Mode, you can do so [using the `envMode` configuration](/docs/reference/configuration#envmode).
    * Workspace root directory is now an implicit dependency of all packages ([PR](https://github.com/vercel/turborepo/pull/8202))
      * The repository should have as little code in the root as possible, since changes to the root can affect all tasks in your repository. Additionally, if you're using [Internal Packages](/docs/core-concepts/internal-packages) in the Workspace root, changes to those dependencies will also cause cache misses for all tasks. In both cases, consider moving the code out of the root and [into a package](/docs/crafting-your-repository/structuring-a-repository).
    * `--ignore` removed in favor of `--filter` and graph correctness changes below ([PR](https://github.com/vercel/turborepo/pull/8201))
    * Removed `--scope` flag (deprecated since 1.2) ([PR](https://github.com/vercel/turborepo/pull/7970))
    * `engines` field in root `package.json` is now used in hashing ([PR](https://github.com/vercel/turborepo/pull/8173))
    * `--filter` no longer infers namespaces for package names ([PR](https://github.com/vercel/turborepo/pull/8137))
    * `--filter` now errors when no package names or directories are matched ([PR](https://github.com/vercel/turborepo/pull/8142))
    * `--only` restricts task dependencies instead of package dependencies ([PR](https://github.com/vercel/turborepo/pull/8163))
  </Step>
</Steps>

- [Using environment variables](/crafting-your-repository/using-environment-variables.md): Learn how to handle environments for your applications.

import { Fragment } from 'react';
import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Accordion, Accordions } from '#components/accordion';
import frameworks from '@turbo/types/src/json/frameworks.json';

Environment variable inputs are a vital part of your applications that you'll need to account for in your Turborepo configuration.

There are three important questions when working with environment variables in Turborepo:

* [Are my environment variables accounted for in the task hash?](#adding-environment-variables-to-task-hashes)
* [Which Environment Mode will `turbo` use?](#environment-modes)
* [Have I handled my `.env` files?](#handling-env-files)

<Callout type="error">
  Failing to account for environment variables in your configuration can result
  in shipping your application with the wrong configuration. This can cause
  serious issues like shipping your preview deployments to production.
</Callout>

<Callout type="good-to-know">
  Turborepo also uses [System Environment
  Variables](/docs/reference/system-environment-variables) to configure its own
  behavior. Below, you'll find information about environment variables for your
  task's runtime and how they affect task hashing.
</Callout>

## Adding environment variables to task hashes

Turborepo needs to be aware of your environment variables to account for changes in application behavior. To do this, use the `env` and `globalEnv` keys in your `turbo.json` file.

* **globalEnv**: Changes to the values of any environment variables in this list will change the hash for all tasks.
* **env**: Includes changes to the values of environment variables that affect the task, allowing for better granularity. For example, a `lint` task probably doesn't need to miss cache when the value of `API_KEY` changes, but a `build` task likely should.

<Callout type="good-to-know">
  Turborepo supports wildcards for environment variables so you can easily
  account for all environment variables with a given prefix. Visit [the API
  reference for `env`](/docs/reference/configuration#wildcards) for more.
</Callout>

### Framework Inference

Turborepo automatically adds prefix wildcards to your [`env`](/docs/reference/configuration#env) key for common frameworks. If you're using one of the frameworks below in a package, you don't need to specify environment variables with these prefixes:

<table>
  <thead>
    <tr>
      <th>Framework</th>

<th>
        <span>
          <code>env</code> wildcards
        </span>
      </th>
    </tr>
  </thead>

<tbody>
    {frameworks.map(({ name, envWildcards }) => (
          <tr key={name}>
            <td>{name}</td>
            <td>
              {envWildcards.map((envWildcard, index) => (
                <Fragment key={envWildcard}>
                  {index !== 0 ? <span>, </span> : null}
                  <code>{envWildcard}</code>
                </Fragment>
              ))}
            </td>
          </tr>
        ))}
  </tbody>
</table>

<Callout type="good-to-know">Framework inference is per-package.</Callout>

If you'd like to opt out of Framework Inference, you can do so by:

* Running your tasks with `--framework-inference=false`
* Adding a negative wildcard to the `env` key (for example, `"env": ["!NEXT_PUBLIC_*"]`)

Turborepo's Environment Modes allow you to control which environment variables are available to a task at runtime:

* [Strict Mode](#strict-mode) (Default): Filter environment variables to **only** those that are specified in the `env` and `globalEnv` keys in `turbo.json`.
* [Loose Mode](#loose-mode): Allow all environment variables for the process to be available.

Strict Mode filters the environment variables available to a task's runtime to **only** those that are specified in the `globalEnv` and `env` keys in `turbo.json`.

This means that tasks that do not account for all of the environment variables that they need are likely to fail. This is a good thing, since you don't want to cache a task that can potentially have different behavior in a different environment.

<Callout type="warn" title="Cache safety with Strict Mode">
  While Strict Mode makes it much more likely for your task to fail when you
  haven't accounted for all of your environment variables, it doesn't guarantee
  task failure. If your application is able to gracefully handle a missing
  environment variable, you could still successfully complete tasks and get
  unintended cache hits.
</Callout>

#### Passthrough variables

In advanced use cases, you may want to make some environment variables
available to a task without including them in the hash. Changes to these variables don't affect task outputs but still need to be available for the task to run successfully.

For these cases, add those environment variables to [`globalPassThroughEnv`](/docs/reference/configuration#globalpassthroughenv) and [`passThroughEnv`](/docs/reference/configuration#passthroughenv).

#### CI vendor compatibility

Strict Mode will filter out environment variables that come from your CI vendors until you've accounted for them using [`env`](/docs/reference/configuration#env), [`globalEnv`](/docs/reference/configuration#globalenv), [`passThroughEnv`](/docs/reference/configuration#passthroughenv), or [`globalPassThroughEnv`](/docs/reference/configuration#globalpassthroughenv).

If any of these variables are important to your tasks and aren't included by [Framework Inference](#framework-inference), make sure they are in your `turbo.json` configuration.

Loose Mode does not filter your environment variables according to your `globalEnv` and `env` keys. This makes it easier to get started with incrementally migrating to Strict Mode.

Use [the `--env-mode` flag](/docs/reference/run#--env-mode-option) to enable Loose Mode on any invocation where you're seeing environment variables cannot be found by your scripts:

As long as the environment variable is available when `turbo` is ran, your script will be able to use it. However, this also **lets you accidentally forget to account for an environment variable in your configuration much more easily**, allowing the task to hit cache when it shouldn't.

For example, you may have some code in your application that fetches data from an API, using an environment variable for the base URL:

You then build your application using a value for `MY_API_URL` that targets your preview environment. When you're ready to ship your application, you build for production and see a cache hit - even though the value of the `MY_API_URL` variable has changed! `MY_API_URL` changed - but Turborepo restored a version of your application from cache that uses the preview environment's `MY_API_URL` rather than production's.

When you're using Loose Mode, `MY_API_URL` is available in the task runtime **even though it isn't accounted for in the task hash**. To make this task more likely to fail and protect you from this misconfiguration, we encourage you to opt for [Strict Mode](#strict-mode).

### Platform Environment Variables

When deploying your application to [Vercel](https://vercel.com/new?ref=turborepo), you likely already have [environment variables](https://vercel.com/docs/projects/environment-variables) configured on your project. Turborepo will automatically check these variables against your `turbo.json` configuration to ensure that you've [accounted for them](/docs/crafting-your-repository/using-environment-variables#adding-environment-variables-to-task-hashes),
and will warn you about any missing variables.

This functionality can be disabled by setting `TURBO_PLATFORM_ENV_DISABLED=false`

## Handling `.env` files

`.env` files are great for working on an application locally. **Turborepo does not load .env files into your task's runtime**, leaving them to be handled by your framework, or tools like [`dotenv`](https://www.npmjs.com/package/dotenv).

However, it's important that `turbo` knows about changes to values in your `.env` files so that it can use them for hashing. If you change a variable in your `.env` files between builds, the `build` task should miss cache.

To do this, add the files to the [`inputs`](/docs/reference/configuration#inputs) key:

### Multiple `.env` files

You can capture multiple `.env` files at once using a `*`.

<Callout type="info">
  `.env` files can load variables into the task runtime even when the
  environment variables have not been added to [the `env`
  key](/docs/reference/configuration#env). Ensure that you add your environment
  variables for your builds the `env` key for CI and production builds.
</Callout>

### Use `.env` files in packages

Using a `.env` file at the root of the repository is not recommended. Instead, we recommend placing your `.env` files into the packages where they're used.

This practice more closely models the runtime behavior of your applications since environment variables exist in each application's runtime individually. Additionally, as your monorepo scales, this practice makes it easier to manage each application's environment, preventing environment variable leakage across applications.

<Callout type="good-to-know">
  You may find it easier to use a root `.env` file when incrementally migrating
  to a monorepo. Tools like [dotenv](https://www.npmjs.com/package/dotenv) can
  load `.env` files from different locations.
</Callout>

### Use `eslint-config-turbo`

[The `eslint-config-turbo` package](/docs/reference/eslint-config-turbo) helps you find environment variables that are used in your code that aren't listed in your `turbo.json`. This helps ensure that all your environment variables are accounted for in your configuration.

### Avoid creating or mutating environment variables at runtime

Turborepo hashes the environment variables for your task at the beginning of the task. If you create or mutate environment variables during the task, Turborepo will not know about these changes and will not account for them in the task hash.

For instance, Turborepo will not be able to detect the inline variable in the example below:

`MY_VARIABLE` is being added to the environment *after* the `dev` task has started, so `turbo` will not be able to use it for hashing.

Below are examples of proper environment variable configuration for a few popular frameworks:

<Accordions>
  <Accordion title="Next.js">
    The `turbo.json` below expresses:

* The `build` and `dev` tasks will have different hashes for changes to `MY_API_URL` and `MY_API_KEY`.
    * The `build` and `dev` tasks include the supported .env files for Next.js.
    * The `test` task does not use environment variables, so the `env` key is omitted. (Depending on your testing structure, your `test` task may need an `env` key.)

<Accordion title="Vite">
    The `turbo.json` below expresses:

* The `build` and `dev` tasks will have different hashes for changes to `MY_API_URL` and `MY_API_KEY`.
    * The `build` and `dev` tasks include the supported .env files for Vite.
    * The `test` task does not use environment variables, so the `env` key is omitted. (Depending on your testing structure, your `test` task may need an `env` key.)

</Accordion>
</Accordions>

### Use `--summarize`

[The `--summarize` flag](/docs/reference/run#--summarize) can be added to your `turbo run` command to produce a JSON file summarizing data about your task. Checking the diff for the `globalEnv` and `env` key can help you identify any environment variables that may be missing from your configuration.

Once you've accounted for your environment variables, you're ready to start building the CI pipelines that build, check, and deploy your applications, at the speed of `turbo`.

- [Generating code](/guides/generating-code.md): Learn how to generate code using Turborepo.

import { Callout } from '#components/callout';
import { File, Folder, Files } from '#components/files';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

Splitting your monorepo into packages is a great way to organize your code, speed up tasks, and improve the local development
experience. With Turborepo's code generation, it's easy to generate new source code for packages, modules,
and even individual UI components in a structured way that integrates with the rest of your repository.

## Add an empty package

Add a new, empty app or package to your monorepo.

View all available [options](/docs/reference/generate#workspace) for `gen workspace`.

## Copy an existing package

You can use an existing workspace as a template for your new app or package. This works for both workspaces within your existing monorepo,
and remote workspaces from other repositories (specified via GitHub URL).

Create a new package in your monorepo by copying from an existing package in your repo.

Create a new workspace in your monorepo by copying from a remote package.

<Callout>
  **Note**: When adding from a remote source, Turborepo is unable to verify that your repo has all of the required dependencies, and is using the correct package manager. In this case, some manual modifications may be required to get the new workspace working as expected within your repository.
</Callout>

View all available [options](/docs/reference/generate#workspace) for `gen workspace --copy`.

If a built-in generator does not fit your needs, you can create your own custom generator using [Plop](https://plopjs.com/) configurations.
Turborepo will automatically detect any generator configurations within your repo, and make them available to run from the command line.

<Callout type="info">
  While Turborepo Generators are built on top of Plop, they don't require `plop`
  to be installed as a dependency in your repo.
</Callout>

While Turborepo understands all Plop configuration options and features, it provides a few additional features to improve the experience of writing
generators within a repo configured with Turborepo.

1. Generators are automatically discovered, loaded, and organized per workspace (no need to manually `load` them within a single configuration file)
2. Generators are automatically run from the root of the workspace where they are defined
3. Generators can be invoked from anywhere within your repo (or outside it via the [`--root`](/docs/reference/generate#--root-path) flag)
4. TypeScript generators are supported with zero configuration
5. `plop` is not required to be installed as a dependency of your repo

<Callout type="info" title="Known issue">
  ESM dependencies are not currently supported within custom generators.
</Callout>

To build and run a custom generator, run the following command from anywhere within your monorepo using Turborepo.

You'll be prompted to select an existing generator or to create one if you don't have any yet. You can also create your configuration
manually at `turbo/generators/config.ts` (or `config.js`) at the root of your repo - or within *any* workspace.

<Callout type="info">
  If you are using TypeScript, you will need to install [the `@turbo/gen`
  package](https://github.com/vercel/turborepo/tree/main/packages/turbo-gen) as
  a `devDependency` to access the required TS types.
</Callout>

For example, the following illustrates a monorepo with three locations for generators:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    <Files>
      <Folder name="apps" defaultOpen>
        <Folder name="docs">
          <File name="package.json" />
        </Folder>

<Folder name="web" defaultOpen>
          <File name="package.json" />

<Folder name="turbo" green defaultOpen>
            <Folder name="generators">
              <File name="config.ts" />

<File name="templates" />
            </Folder>
          </Folder>
        </Folder>
      </Folder>

<Folder name="packages" defaultOpen>
        <Folder name="ui" defaultOpen>
          <File name="package.json" />

<Folder name="turbo" green defaultOpen>
            <Folder name="generators">
              <File name="config.ts" />

<File name="templates" />
            </Folder>
          </Folder>
        </Folder>
      </Folder>

<Folder name="turbo" green defaultOpen>
        <Folder name="generators">
          <File name="config.ts" />

<File name="templates" />
        </Folder>
      </Folder>

<File name="package.json" />

<File name="package-lock.yaml" />

<File name="pnpm-workspace.yaml" />

<File name="turbo.json" />
    </Files>
  </Tab>

<Tab value="yarn">
    <Files>
      <Folder name="apps" defaultOpen>
        <Folder name="docs">
          <File name="package.json" />
        </Folder>

<Folder name="web" defaultOpen>
          <File name="package.json" />

<Folder name="turbo" green defaultOpen>
            <Folder name="generators">
              <File name="config.ts" />

<File name="templates" />
            </Folder>
          </Folder>
        </Folder>
      </Folder>

<Folder name="packages" defaultOpen>
        <Folder name="ui" defaultOpen>
          <File name="package.json" />

<Folder name="turbo" green defaultOpen>
            <Folder name="generators">
              <File name="config.ts" />

<File name="templates" />
            </Folder>
          </Folder>
        </Folder>
      </Folder>

<Folder name="turbo" green defaultOpen>
        <Folder name="generators">
          <File name="config.ts" />

<File name="templates" />
        </Folder>
      </Folder>

<File name="package.json" />

<File name="yarn.lock" />

<File name="turbo.json" />
    </Files>
  </Tab>

<Tab value="npm">
    <Files>
      <Folder name="apps" defaultOpen>
        <Folder name="docs">
          <File name="package.json" />
        </Folder>

<Folder name="web" defaultOpen>
          <File name="package.json" />

<Folder name="turbo" green defaultOpen>
            <Folder name="generators">
              <File name="config.ts" />

<File name="templates" />
            </Folder>
          </Folder>
        </Folder>
      </Folder>

<Folder name="packages" defaultOpen>
        <Folder name="ui" defaultOpen>
          <File name="package.json" />

<Folder name="turbo" green defaultOpen>
            <Folder name="generators">
              <File name="config.ts" />

<File name="templates" />
            </Folder>
          </Folder>
        </Folder>
      </Folder>

<Folder name="turbo" green defaultOpen>
        <Folder name="generators">
          <File name="config.ts" />

<File name="templates" />
        </Folder>
      </Folder>

<File name="package.json" />

<File name="package-lock.json" />

<File name="turbo.json" />
    </Files>
  </Tab>

<Tab value="bun">
    <Files>
      <Folder name="apps" defaultOpen>
        <Folder name="docs">
          <File name="package.json" />
        </Folder>

<Folder name="web" defaultOpen>
          <File name="package.json" />

<Folder name="turbo" green defaultOpen>
            <Folder name="generators">
              <File name="config.ts" />

<File name="templates" />
            </Folder>
          </Folder>
        </Folder>
      </Folder>

<Folder name="packages" defaultOpen>
        <Folder name="ui" defaultOpen>
          <File name="package.json" />

<Folder name="turbo" green defaultOpen>
            <Folder name="generators">
              <File name="config.ts" />

<File name="templates" />
            </Folder>
          </Folder>
        </Folder>
      </Folder>

<Folder name="turbo" green defaultOpen>
        <Folder name="generators">
          <File name="config.ts" />

<File name="templates" />
        </Folder>
      </Folder>

<File name="package.json" />

<File name="bun.lock" />

<File name="turbo.json" />
    </Files>
  </Tab>
</Tabs>

Generators created within workspaces are automatically run from the workspace root, **not** the repo root, nor the location of the generator configuration.

This makes your generators more simple to write. Creating a file at `[workspace-root]` only needs to be specified as `<file>` rather than `../../<file>`.

Learn more about [creating custom generators using Plop](https://plopjs.com/documentation/#creating-a-generator).

### Writing generators

A generator configuration file is a function that returns a [Plop](https://plopjs.com/) configuration object. The configuration object is
used to define the generator's prompts, and actions.

In its simplest form, a generator configuration file looks like:

Prompts are written using [Plop prompts](https://plopjs.com/documentation/#using-prompts) and are used to gather information from the user.

Actions can use [built-in Plop actions](https://plopjs.com/documentation/#built-in-actions), or [custom action functions](https://plopjs.com/documentation/#functionsignature-custom-action) that you define yourself:

### Running generators

Once you have created your generator configuration file, you can skip the selection prompt and directly run a specified generator with:

Arguments can also be passed directly to the generator prompts using `--args`

See [bypassing prompts](https://plopjs.com/documentation/#bypassing-prompts) in the Plop documentation for more information.

View all available [options](/docs/reference/generate#run-generator-name) for `gen`.

- [Handling platforms](/guides/handling-platforms.md): Learn how to handle caching around operating systems, architectures, and other arbitrary conditions for Turborepo tasks.

To account for Node.js versions, use [the engines key in package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#engines). Turborepo will account for changes to this field and miss cache accordingly.

## Operating systems, architecture, and other arbitrary conditions

For advanced use cases, you may want the operating system (OS), architecture, or other external factors to contribute to your hash.

### 1. Write an arbitrary file to disk

First, create a script that accounts for the hash contributors that you are interested in. For example, here is a Node.js script that identifies platform and architecture and writes those details to a file (`turbo-cache-key.json`):

### 2. Add the file to your .gitignore

You won't want to commit this file to source control since it's dependent on environment. Add it to your `.gitignore`:

### 3. Add the file to the hash

Now, make sure that `turbo` is aware of the file by adding it to task inputs. You can do this two ways:

* **For specific tasks**: Include the file in [the `inputs` array](/docs/reference/configuration#inputs) of the task(s):

* **For all tasks**: Add the file to [`globalDependencies`](/docs/reference/configuration#globaldependencies)

### 4. Generate the file before running `turbo`

Last, you'll want to ensure that you run the script before running `turbo`. For example:

`turbo run build` will now take into account the contents of `turbo-cache-key.json` when calculating the hash for the `build` task.

- [Guides](/guides/index.md): Learn how to use your favorite tooling in a Turborepo.

import { Cards, Card } from '#components/card';

Turborepo works with your favorite frameworks, CI providers, tools, and use cases.

In our community-supported guides, you'll find examples of how to use `turbo` with the rest of your tooling.

<Cards>
  <Card title="Frameworks" description="Integrate frameworks into your Turborepo" href="/docs/guides/frameworks" />

<Card title="Continuous Integration" description="Use Turborepo with your CI" href="/docs/guides/ci-vendors" />

<Card title="Tools" description="Bring your favorite tooling" href="/docs/guides/tools" />

<Card title="Single-package workspaces" description="Integrate with a standalone application" href="/docs/guides/single-package-workspaces" />

<Card title="Generating code" description="Create new code fast" href="/docs/guides/generating-code" />

<Card title="Skipping tasks" description="Go fast by doing nothing" href="/docs/guides/skipping-tasks" />

<Card title="Publishing packages" description="Use your packages outside of your Turborepo" href="/docs/guides/publishing-libraries" />

<Card title="Handling platforms" description="OS, Node.js version, and other factors" href="/docs/guides/handling-platforms" />

<Card title="Multi-language support" description="Many languages, one repository" href="/docs/guides/multi-language" />
</Cards>

- [Microfrontends](/guides/microfrontends.md): Learn how to use Turborepo's built-in microfrontends proxy for local development.

import { Callout } from '#components/callout';
import { File, Folder, Files } from '#components/files';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

Microfrontends are an architectural pattern where a web application is decomposed into smaller, independently developed and deployed applications that work together.

Turborepo provides built-in support for running vertical microfrontends (sometimes called "zones") locally during development through an integrated proxy server. The proxy coordinates multiple applications and routes traffic between them.

Let's imagine you have a monorepo with multiple frontend applications:

<Files>
  <Folder name="apps" defaultOpen>
    <Folder name="web">
      <File name="package.json" />

<File name="next.config.js" />
    </Folder>

<Folder name="docs">
      <File name="package.json" />

<File name="next.config.js" />
    </Folder>

<Folder name="marketing">
      <File name="package.json" />

<File name="vite.config.ts" />
    </Folder>
  </Folder>

<File name="package.json" />

<File name="turbo.json" />
</Files>

In production, these applications might be deployed separately and composed together using a reverse proxy or edge routing. But during development, you want to:

* Run all applications simultaneously with a single command
* Access them through a unified URL (e.g., `http://localhost:3024`)
* Route requests to the correct application based on path patterns
* Support hot module reloading and WebSocket connections
* Avoid port conflicts and manual coordination

Turborepo provides a built-in proxy server that automatically routes traffic between your microfrontend applications during development. The proxy reads a `microfrontends.json` configuration file and starts when you run `turbo dev`.

<Callout>
  You can try the following instructions with the monorepo created by `npx
    create-turbo@latest -e with-microfrontends`.
</Callout>

### Create `microfrontends.json`

Create a `microfrontends.json` file in your parent application. This application is the one that all requests will fall through to when not matched by another application.

### Set application ports

Next, use the `turbo get-mfe-port` command to set the ports in your application's development scripts. This command injects the port number when running `turbo dev`:

<Tabs items={['Next.js', 'Vite']} storageKey="framework-preference">
  <Tab value="Next.js">
    
  </Tab>

<Tab value="Vite">
    
  </Tab>
</Tabs>

### Handle base paths

If you're using a framework, set the base path according to the needs of the framework.

<Tabs items={['Next.js', 'Vite']} storageKey="framework-preference">
  <Tab value="Next.js">
    
  </Tab>

<Tab value="Vite">
    
  </Tab>
</Tabs>

[Visit the Microfrontends section of your framework](/docs/guides/frameworks) for framework-specific guidance.

When you run `turbo dev`, Turborepo will:

1. **Start the proxy server** on the configured port (default: `3024`)
2. **Inject the `TURBO_MFE_PORT` environment variable** in tasks to set the applications' port
3. **Run development tasks** for all configured applications
4. **Route incoming requests** based on path patterns to the appropriate application

Now you can access all of your microfrontends applications at `http://localhost:3024`.

Each application in the `applications` object can have the following properties:

If not provided, the application key is used to match the name in \`package.json.

### `development.local`

The port where the application runs locally.

If you omit the port, Turborepo will generate a deterministic port based on the application name (between 3000-8000).

### `development.fallback`

Optionally provide a target to proxy to when an application is not running locally. This is most frequently used to route to production to make commands like `turbo dev --filter=web` that only run a subset of applications a seamless experience.

An array of path groups that should route to this application. If no routing is provided, the application becomes the **default application** that catches all unmatched routes.

Only one application can have no `routing` configuration. This is your "root" application that handles all routes not matched by other applications.

* Paths are **case-sensitive**: `/Blog` and `/blog` are different routes
* Trailing slashes are normalized: `/home` and `/home/` match the same route

These paths match exactly as written.

Segments starting with `:` match any single path segment. For example, `/blog/:slug` matches `/blog/hello` but not `/blog/hello/world`.

Parameters ending with `*` match zero or more path segments. For example, `/docs/:path*` matches `/docs`, `/docs/intro`, and `/docs/api/reference`.

You can also use the `+` modifier to match one or more segments (excluding the empty path):

This matches `/api/users` and `/api/users/123`, but not `/api` or `/api/`.

#### Complex routing patterns

You can define sophisticated routing with nested parameters:

Organize routes into logical groups for better maintainability:

The `group` field is for organizational purposes and doesn't affect routing behavior.

Optionally use the name of the package from `package.json` in your workspace.

### `options.localProxyPort`

Optionally change the proxy port using the `localProxyPort` option

## Integrating with production

The Turborepo microfrontends proxy is meant for local usage only. How you implement and integrate your production microfrontends depends on your production infrastructure. However, we can integrate your local and production environments to create a seamless experience across environments.

To start, we've built Turborepo's local proxy to integrate with Vercel's microfrontends. We look forward to working with any infrastructure providers that would also like to integrate.

### Microfrontends on Vercel

Vercel has native support for microfrontends that provide:

* Production proxy implementation with enhance performance
* Fallback URL support across environments
* Vercel toolbar integration
* Feature flag support
* Asset prefix handling

[Learn more in Vercel's documentation](https://vercel.com/docs/microfrontends).

#### Migrating to `@vercel/microfrontends`

If you install [`@vercel/microfrontends`](https://www.npmjs.com/package/@vercel/microfrontends) in any package or add it to your workspace, Turborepo will automatically defer to it instead of using the built-in proxy. This allows for a gradual migration path.

You can use the same `microfrontends.json` configuration as for Turborepo. Turborepo's `microfrontends.json` schema is a subset of Vercel's schema, so it is compatible with `@vercel/microfrontends`.

To learn more about `@vercel/microfrontends`, [visit the package on npm](https://www.npmjs.com/package/@vercel/microfrontends).

### Port already in use

By default, the microfrontends proxy will try to use port 3024. If you already use that port for a different purpose, you can change Turborepo's port using the [`options.localProxyPort`](#optionslocalproxyport).

### Missing CSS, images, or other assets, or routes not matching

Ensure that the paths that the microfrontends matches for in its [`routing` configuration](#routing) include the routes for the assets. Check your network tab to find paths that are or aren't matching as expected.

### Links across applications causing errors

If you use a Single-Page Application (SPA) link (like the Next.js `<Link>` component) to link across applications, this can result in errors. Even though the port and domain remain the same, the applications are different. This means the routing is, by definition, not a "single-page application".

### Visiting a proxied port does not redirect

You are still be able to reach a proxied port directly. For example, if `localhost:3000` is proxied to `localhost:3042`, you can still visit `localhost:3000` in your browser.

If you would like for `localhost:3000` to redirect to `localhost:3024`, you must set this up manually in your application.

### Applications not starting

1. The `packageName` matches your actual package name
2. The `task` specified exists in the package's `package.json`
3. Each application's port is available
4. All dependencies are installed

### `turbo get-mfe-port` not working

If you're getting an error when running `turbo get-mfe-port`, ensure that:

1. You're running the command from a package directory (not the repository root)
2. The package has a `name` field in its `package.json`
3. A `microfrontends.json` file exists in one of the packages
4. The current package is listed in the `applications` section of `microfrontends.json`
5. If using `--skip-infer`, you must also specify `--cwd` pointing to your repository root:

Here's a full example of a microfrontends configuration for an e-commerce platform:

With this configuration:

* The `web` app handles the homepage and any unmatched routes
* The `docs` app handles all documentation
* The `blog` app handles blog posts and author pages
* The `shop` app handles e-commerce functionality

- [Migrating from Nx](/guides/migrating-from-nx.md): Learn how to migrate to Turborepo from Nx.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

This guide will help you migrate an existing Nx repository to Turborepo.

* Explore key concepts by [migrating from an Nx starter to Turborepo](#migration-steps)
* Considerations for [more complex migration scenarios](#advanced-migration-considerations)

There are many reasons why you may be choosing to migrate from Nx to Turborepo. Below, we've listed the most common motivations that developers have referenced for their migrations.

### Using ecosystem standards

Turborepo's goal is to be lightweight, leaning on your repository as the source of truth. An example of this is Turborepo being [built on top of JavaScript package manager workspaces](/docs/crafting-your-repository/structuring-a-repository) for it's JavaScript/TypeScript support.

By contrast, Nx uses layers of plugins, dependencies, and other Nx-specific code to infer information about your repository. While these plugins can provide a layer of functionality and are optional, Nx users looking to migrate often cite removing Nx-specific code from their codebase as a key motivation for their change.

### Greater control of source code

Nx’s philosophy involves wrapping your code with layers of plugins, dependencies, and Nx-specific code. While these layers of code are optional, they provide a great deal of Nx's value and are recommended by Nx, so most Nx repos have them. When migrating to Turborepo, many developers explain that these layers tend to create a layer of obfuscation that abstracts their repository away from their control, causing issues.

Turborepo chooses to let you handle your tooling on your own terms, configuring (or not configuring) any of your tooling as you please.

### Less configuration for your repository manager

Migrating to Turborepo will likely require deleting previous configuration that you had for Nx and replacing it with less configuration for Turborepo, since Turborepo will automatically infer your repository's needs. For example, here are the tool-specific configurations you'll find in the equivalent starters for Turborepo and Nx [used below](#migration-steps).

<Tabs items={["Turborepo", "Nx"]}>
  <Tab value="Turborepo">
    
  </Tab>

Our goal for this migration is to get a working Turborepo task as quickly as possible, so that you can adopt Turborepo features incrementally. We’ll start by using the Nx scaffolder to create a repository with a Next.js app.

### Step 1: Update .gitignore

Turborepo uses the .turbo directory to hold local caches and other information about your repository. For this reason, it should be added to your `.gitignore`.

### Step 2: Add a workspace definition

Turborepo is built on top of package manager workspaces, a JavaScript ecosystem standard. Add the directory paths to the workspace that will contain packages.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

### Step 3: Add a package.json to the application

Rather than adding additional configuration files like `project.json`, Turborepo uses the standard `package.json` file.

Add a `package.json` to the `starter` application. Create a `package.json` at `./apps/starter/package.json` that contains a `dev` and `build` script.

### Step 4: Remove Nx plugin

Remove the Nx plugin from ./apps/starter/next.config.js. The example file below doesn’t have configuration, though your existing Next.js application may need some.

### Step 5: Add the `packageManager` field

The root package.json needs to have the `packageManager` field. This ensures developers in the repository use the correct package manager, and that Turborepo can optimize your package graph based on your lockfile.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

### Step 6: Run you package manager's install command

Update your lockfile by running your installation command.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

Once you've done this, you should see a lockfile diff, indicating that the package has been added to the package manager's workspace.

### Step 7: Install Turborepo

Add Turborepo to the root `package.json` of the workspace.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

You can also optionally install `turbo` globally for added convenience when working with Turborepo.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

### Step 8: Add a `turbo.json`

Create a `turbo.json` at the root to register your tasks and describe their task dependencies.

### Step 9: Run `turbo build`

Build the application with Turborepo. Using global `turbo`, this would be `turbo build`. You can also run the command through your package manager:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

### Step 10: Enable Remote Caching (optional)

By default, Turborepo will connect to the free-to-use Vercel Remote Cache when you run:

You may also configure a self-hosted Remote Cache.

## Advanced migration considerations

While the migration guide above is a good starting point, the breadth of possibilities and capabilities of monorepos means that its difficult to create generalized instructions for all cases. Below, we’ve listed some common next steps that you may be thinking about.

### Migrate complex monorepos incrementally

We encourage incremental migration, meaning you will have both of Nx and Turborepo in your repository at the same time. Make sure to spend time understanding how your Nx task graph is constructed. Splitting up the task graph may include strategies like:

* **Migrating one task at a time**: Changing `nx run lint` to `turbo run lint`
* **Migrating one package/project at a time**: Changing `nx run-many lint test --projects=web` to `turbo run lint test --filter=web`
* **Double-running some of your tasks**: To ensure stability, you may choose to run `turbo run lint` **and** `nx run lint` while you're still getting comfortable and building certainty in the early phases of your migration.

### Installing dependencies where they're used

Turborepo recommends [installing packages where they're used](/docs/crafting-your-repository/managing-dependencies#best-practices-for-dependency-installation) to improve cache hit ratios, help dependency pruning capability, and clarify for developers which dependencies are meant for which packages. This is different from the Nx strategy, where all dependencies are installed at the root of the repository, making all dependencies available to all packages in the workspace.

Historically, Nx has recommended installing all dependencies in the root of the repository, making all dependencies available to all packages in the Workspace. If you followed this guidance, we highly recommend that you move dependencies to the `package.json`'s for packages and applications that need them. [Visit our documentation on managing dependencies](/docs/crafting-your-repository/managing-dependencies) to learn more.

### Creating shared packages

You’ll follow roughly the same set of steps as above to add a package to your package manager’s workspace.

1. Ensure the package’s directory is included in the workspace definition (like `./packages/*` ).
2. Add a `package.json` to the package with the scripts it needs to run.
3. Check task dependencies in `turbo.json` to make sure your dependency graph meets your requirements.

### Multi-language monorepos

Turborepo natively supports JavaScript and TypeScript, with secondary support for any other languages you’d like to use. [Visit the Multi-Language support documentation](/docs/guides/multi-language) to learn more.

## Configuration equivalents

Configuration found in `nx.json` can be mapped to `turbo.json` using the tables below.

<Callout type="info">
  The majorify of globs for capturing files are the same between Nx and
  Turborepo. See [our file glob specification](/docs/reference/globs) for
  details and edge cases.
</Callout>

### Global configuration

| Nx                         | Turborepo                                                                |
| -------------------------- | ------------------------------------------------------------------------ |
| `sharedGlobals`            | [`globalDependencies`](/docs/reference/configuration#globaldependencies) |
| `sharedGlobals.env`        | [`globalEnv`](/docs/reference/configuration#globalenv)                   |
| `sharedGlobals.namedInput` | [`globalDependencies`](/docs/reference/configuration#globaldependencies) |
| `cacheDirectory`           | [`cacheDir`](/docs/reference/configuration#cachedir)                     |

### Task configuration

| Nx              | Turborepo                                                      |
| --------------- | -------------------------------------------------------------- |
| `inputs` files  | [`tasks[task].inputs`](/docs/reference/configuration#inputs)   |
| `inputs.env`    | [`tasks[task].env`](/docs/reference/configuration#env)         |
| `outputs` files | [`tasks[task].outputs`](/docs/reference/configuration#outputs) |
| `cache`         | [`tasks[task].cache`](/docs/reference/configuration#cache)     |

| Nx               | Turborepo                                                               |
| ---------------- | ----------------------------------------------------------------------- |
| `nx generate`    | [`turbo generate`](/docs/reference/generate)                            |
| `nx run`         | [`turbo run`](/docs/reference/run)                                      |
| `nx run-many`    | [`turbo run`](/docs/reference/run)                                      |
| `nx reset`       | [`--force`](/docs/reference/run#--force)                                |
| `--parallel`     | [`--concurrency`](/docs/reference/run#--concurrency-number--percentage) |
| `--nxBail`       | [`--continue`](/docs/reference/run#--continueoption)                    |
| `--projects`     | [`--filter`](/docs/reference/run#--filter-string)                       |
| `--graph`        | [`--graph`](/docs/reference/run#--graph-file-name)                      |
| `--output-style` | [`--log-order`](/docs/reference/run#--log-order-option)                 |
| `--no-cloud`     | [`--cache`](/docs/reference/run#--cache-options)                        |
| `--verbose`      | [`--verbosity`](/docs/reference/run#--verbosity)                        |

- [Multi-language support](/guides/multi-language.md): Learn how to use multiple languages with Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { LinkToDocumentation } from '#components/link-to-documentation';

Turborepo is built on the conventions of the JavaScript ecosystem to find scripts and tasks to execute - but it doesn't care what those scripts do. Following [the guidance for specifying a package in a JavaScript workspace](/docs/crafting-your-repository/structuring-a-repository#specifying-packages-in-a-monorepo), you can add any other language or toolchain to Turborepo.

As an example, you may have a Rust project in the `./cli` directory in your repository. To add this directory as a package to your JavaScript package manager's workspace, add the directory to the workspace definition:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">

<LinkToDocumentation href="https://pnpm.io/pnpm-workspace_yaml">pnpm workspace documentation</LinkToDocumentation>
  </Tab>

<LinkToDocumentation href="https://yarnpkg.com/features/workspaces#how-are-workspaces-declared">yarn workspace documentation</LinkToDocumentation>
  </Tab>

<LinkToDocumentation href="https://docs.npmjs.com/cli/v7/using-npm/workspaces#defining-workspaces">npm workspace documentation</LinkToDocumentation>
  </Tab>

<LinkToDocumentation href="https://bun.sh/docs/install/workspaces">Bun workspace documentation</LinkToDocumentation>
  </Tab>
</Tabs>

Then, add a `package.json` to the directory:

Now, when you use `turbo build`, the `"build"` script in `./cli/package.json` will be included into the tasks that `turbo` runs.

## Caching build artifacts

Ensure that the outputs for your builds are being cached with [the outputs key](/docs/reference/configuration#outputs) in `turbo.json`. In the case of a Rust CLI being compiled with cargo, a release build would be created in the `target/release` directory and we can cache it using:

## Creating dependency relationships

Because the directory is now a part of the package manager's workspace, you can create dependencies exactly the same as you do for your JavaScript packages.

For instance, if you wanted to make sure that the `rust-cli` "package" from above is built before your `web` application, install it into the dependencies for the `web` application:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    
  </Tab>

<Tab value="yarn">
    
  </Tab>

<Tab value="npm">
    
  </Tab>

<Tab value="bun">
    
  </Tab>
</Tabs>

Given a `turbo.json` with a `build` task like:

`turbo build` will first create the artifacts for the Rust CLI and then build the `web` application.

- [Publishing libraries](/guides/publishing-libraries.md): Learn how to publish libraries to the npm registry from a monorepo.

import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

Publishing a package to the npm registry from a monorepo can be a smooth experience, with the right tools.

While this guide cannot solve for every possible compiling, bundling, and publishing configuration needed for robust packages, it will explain some of the basics.

<Callout type="info">
  You should follow this setup if you want to publish some of your monorepo's
  packages to npm. If you don't need to publish to npm, you should use an
  [Internal
  Package](/docs/crafting-your-repository/creating-an-internal-package) instead.
  They're much easier to set up and use.
</Callout>

Unlike [Internal Packages](/docs/crafting-your-repository/creating-an-internal-package), external packages can be deployed to [npm](https://www.npmjs.com) *and* used locally. In this guide, we'll bundle a package to both [ECMAScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) (`esm`) and [CommonJS modules](https://en.wikipedia.org/wiki/CommonJS) (`cjs`), the most commonly used formats on npm.

## Setting up a build script

Let's start with a package created using the [Internal Packages](/docs/crafting-your-repository/creating-an-internal-package) tutorial.

There, we created a `@repo/math` package which contained a few helper functions for adding and subtracting numbers. We've decided that this package is good enough for npm, so we're going to bundle it.

We're going to add a `build` script to `@repo/math`, using a bundler. If you're unsure which one to choose, we recommend [`tsup`](https://tsup.egoist.dev/).

Install `tsup` inside the `./packages/math` package using your package manager and then create a build script for it:

`tsup` outputs files to the `dist` directory by default, so you should:

1. Add `dist` to your `.gitignore` files to make sure they aren't committed to source control.
2. Add `dist` to the outputs of `build` in your `turbo.json`.

That way, when `tsup` is run the outputs can be [cached](/docs/crafting-your-repository/caching) by Turborepo.

Finally, we should update our package entrypoints. Inside `package.json`, change `main` to point at `./dist/index.js` for clients using CommonJS modules (`cjs`), `module` to point at `./dist/index.mjs` for clients using ECMAScript modules (`esm`), and `types` to the type definition file - `./dist/index.d.ts`:

<Callout>
  It is not required to bundle to both `cjs` and `esm`. However, it is recommended, as it allows your package to be used in a wider variety of environments.

If you run into errors by using `main`, `module` and `types`, take a look at the [tsup docs](https://tsup.egoist.dev/#bundle-formats).

Bundling is a complicated topic, and we don't have space here to cover everything!
</Callout>

### Building our package before our app

Before we can run `turbo run build`, there's one thing we need to consider. We've just added a [task dependency](/docs/crafting-your-repository/running-tasks) into our monorepo. The `build` of `packages/math` needs to run **before** the `build` of `apps/web`.

Fortunately, we can use [`dependsOn`](/docs/reference/configuration#dependson) to easily configure this.

Now, we can run `turbo run build`, and it'll automatically build our packages *before* it builds our app.

### Setting up a dev script

There's a small issue with our setup. We are building our package just fine, but it's not working great in dev. Changes that we make to our `@repo/math` package aren't being reflected in our app.

That's because we don't have a `dev` script to rebuild our packages while we're working. We can add one easily:

This passes the `--watch` flag to `tsup`, meaning it will watch for file changes.

If we've already set up [dev scripts](/docs/crafting-your-repository/developing-applications#configuring-development-tasks) in our `turbo.json`, running `turbo run dev` will run our `packages/math` dev task in parallel with our `apps/web` dev task.

Our package is now in a spot where we can consider deploying to npm. In our [versioning and publishing](#versioning-and-publishing) section, we'll do just that.

## Versioning and publishing

Manually versioning and publishing packages in a monorepo can be tiresome. Luckily, there's a tool that makes things easy - the [Changesets](https://github.com/changesets/changesets) CLI.

We recommend Changesets because it's intuitive to use, and - just like Turborepo - fits with the monorepo tools you're already used to.

Some alternatives are:

* [intuit/auto](https://github.com/intuit/auto) - Generate releases based on semantic version labels on pull requests
* [microsoft/beachball](https://github.com/microsoft/beachball) - The Sunniest Semantic Version Bumper

Once your package has been bundled, you can then publish it to the npm registry.

We recommend taking a look at the Changesets docs. Here's our recommended reading order:

1. [Why use changesets?](https://github.com/changesets/changesets/blob/main/docs/intro-to-using-changesets.md) - an intro that takes you through the fundamentals.
2. [Installation instructions](https://github.com/changesets/changesets/blob/main/packages/cli/README.md)
3. If you're using GitHub, consider using the [Changeset GitHub bot](https://github.com/apps/changeset-bot) - a bot to nudge you to add changesets to PR's.
4. You should also consider adding the [Changesets GitHub action](https://github.com/changesets/action) - a tool which makes publishing extremely easy.

## Using Changesets with Turborepo

Once you've started using Changesets, you'll gain access to three useful commands:

```bash title="Terminal"

**Examples:**

Example 1 (unknown):
```unknown
</Tab>

  <Tab value="yarn">
```

Example 2 (unknown):
```unknown
</Tab>

  <Tab value="npm">
```

Example 3 (unknown):
```unknown
</Tab>

  <Tab value="bun">
```

Example 4 (unknown):
```unknown
</Tab>
</Tabs>

In the [Creating an Internal Package guide](/docs/crafting-your-repository/creating-an-internal-package), you can build an Internal Package from the beginning using [the Compiled Package strategy](#compiled-packages). On this page, we'll describe other strategies for creating Internal Packages and their tradeoffs, including [publishing the package to the npm registry](#publishable-packages) to create an External Package.

You can then import the package into your code like you're used to doing with an external package:
```

---

## Build everything that depends on changes in branch 'my-feature'

**URL:** llms-txt#build-everything-that-depends-on-changes-in-branch-'my-feature'

turbo run build --filter=...[origin/my-feature]

---

## - Or, changed since the previous commit

**URL:** llms-txt#--or,-changed-since-the-previous-commit

**Contents:**
  - `--force`
  - `--framework-inference`
  - `--global-deps <file glob>`
  - `--graph <file name>`
  - `--log-order <option>`
  - `--log-prefix <option>`
  - `--no-cache`
  - `--daemon` and `--no-daemon`
  - `--output-logs <option>`
  - `--only`

turbo run test --filter=@acme/*{./packages/*}[HEAD^1]
bash title="Terminal"
turbo run build --force
bash title="Terminal"
turbo run build --framework-inference=false
bash title="Terminal"
turbo run build --global-deps=".env"
turbo run build --global-deps=".env.*" --global-deps=".eslintrc" --global-deps="jest.config.ts"
bash title="Terminal"
turbo run build --graph
turbo run build test lint --graph=my-graph.svg
bash title="Terminal"
turbo run build --log-order=stream
bash title="Terminal"
turbo run dev --log-prefix=none
bash title="Terminal"
turbo run dev --no-cache
bash title="Terminal"
turbo run build --output-logs=errors-only
json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
bash title="Terminal"
turbo run test --only
bash title="Terminal"
turbo run lint --parallel
turbo run dev --parallel
bash title="Terminal"
turbo run build --preflight
bash title="Terminal"
turbo run build --profile=profile.json -vvv
bash title="Terminal"
turbo run build --remote-cache-timeout=60
bash title="Terminal"
turbo run build --remote-only
bash title="Terminal"
turbo run build --summarize
bash title="Terminal"
turbo run build --team=my-team --token=xxxxxxxxxxxxxxxxx
bash title="Terminal"
turbo run build --team=my-team
turbo run build --team=my-team --token=xxxxxxxxxxxxxxxxx
bash title="Terminal"
turbo run build --verbosity=2
turbo run build -vvv
bash title="Terminal"
turbo scan
bash title="Terminal"
turbo telemetry [argument]
bash title="Terminal"
turbo telemetry status
bash title="Terminal"
turbo telemetry enable
bash title="Terminal"
turbo telemetry disable
bash title="Terminal"
npx @turbo/codemod [transform] [path] [--dry] [--print]
bash title="Terminal"
npx @turbo/codemod
bash title="Terminal"
    npx @turbo/codemod update-schema-json-url
    diff title="./turbo.json"
    {
    - "$schema": "https://turborepo.com/schema.v1.json",
    + "$schema": "https://turborepo.com/schema.v2.json",
    }
    bash title="Terminal"
    npx @turbo/codemod add-package-names
    diff title="./packages/ui/package.json"
    {
    + "name": "@repo/ui",
    }
    bash title="Terminal"
    npx @turbo/codemod clean-globs
    diff title="./turbo.json"
    {
      "tasks": {
        "build": {
          "outputs": [
            // Collapse back-to-back doublestars
    -         "**/**.ext", // [!code highlight]
    +         "**.ext" // [!code highlight]
            // Ensure a file extension does not have a double-star
    -         "**.ext", // [!code highlight]
    +         "**/*.ext" // [!code highlight]
            // Proper expansion of directory names
    -         "prefix**/", // [!code highlight]
    +         "prefix*/**" // [!code highlight]
          ]
        }
      }
    }
    bash title="Terminal"
    npx @turbo/codemod migrate-dot-env
    diff title="./turbo.json"
    {
      "tasks": {
        "build": {
    -       "dotEnv": [".env"], // [!code highlight]
          "inputs": [
            "dist/**",
    +         ".env" // [!code highlight]
          ],
        }
      }
    }
    bash title="Terminal"
    npx @turbo/codemod rename-output-mode
    diff title="./turbo.json"
    {
      "tasks": {
        "build": {
    -     "outputMode": "errors-only" // [!code highlight]
    +     "outputLogs": "errors-only" // [!code highlight]
        }
      }
    }
    bash title="Terminal"
    npx @turbo/codemod rename-pipeline
    diff title="./turbo.json"
    {
    - "pipeline": {
    + "tasks": {
        "build": {
          ...
        },
        "dev": {
          ...
        },
        "lint": {
          ...
        }
      }
    }
    bash title="Terminal"
    npx @turbo/codemod stabilize-ui
    diff title="./turbo.json"
    {
    - "experimentalUI": true
    + "ui": true
    }
    bash title="Terminal"
    npx @turbo/codemod stabilize-env-mode
    diff title="./turbo.json"
    {
      "$schema": "https://turborepo.com/schema.json",
    - "experimentalGlobalPassThroughEnv": ["CC"],
    + "globalPassThroughEnv": ["CC"],
      "pipeline": {
        "build": {
    -     "experimentalPassThroughEnv": ["GOROOT"],
    +     "passThroughEnv": ["GOROOT"],
        }
      }
    }
    bash title="Terminal"
    npx @turbo/codemod transform-env-literals-to-wildcards
    diff title="./turbo.json"
    {
      "$schema": "https://turborepo.com/schema.json",
    - "globalEnv": ["THIS_*_IS_LITERAL"],
    - "globalPassThroughEnv": ["!LITERAL_LEADING_EXCLAMATION"],
    +  "globalEnv": ["THIS_\\*_IS_LITERAL"],
    +  "globalPassThroughEnv": ["\\!LITERAL_LEADING_EXCLAMATION"],
      "pipeline": {
        "build": {
    -     "env": ["50_PERCENT_OFF*_HAS_SMALL_PRINT"],
    -     "passThroughEnv": ["**BOLDED**"],
    +     "env": ["50_PERCENT_OFF\\*_HAS_SMALL_PRINT"],
    +     "passThroughEnv": ["\\*\\*BOLDED\\*\\*"],
        }
      }
    }
    bash title="Terminal"
    npx @turbo/codemod set-default-outputs
    diff title="turbo.json"
    {
      "$schema": "https://turborepo.com/schema.json",
      "globalDependencies": [".env"],
      "globalEnv": ["CI_ENV"],
      "pipeline": {
        "build": {
          "dependsOn": ["^build"],
          "env": ["API_BASE"],
          "outputs": [".next/**", "!.next/cache/**"]
        },
    -   "lint": {
    -     "outputs": []
    -    },
    +   "lint": {},
        "dev": {
          "cache": false,
          "persistent": true,
    +     "outputs": ["dist/**", "build/**"]
        }
      }
    }

bash title="Terminal"
    npx @turbo/codemod migrate-env-var-dependencies
    diff title="./turbo.json"
    // After, turbo.json
    {
      "$schema": "https://turborepo.com/schema.json",
    - "globalDependencies": [".env", "$CI_ENV"],
    + "globalDependencies": [".env"],
    + "globalEnv": ["CI_ENV"],
      "pipeline": {
        "build": {
    -     "dependsOn": ["^build", "$API_BASE"],
    +     "dependsOn": ["^build"],
    +     "env": ["API_BASE"],
          "outputs": [".next/**", "!.next/cache/**"],
        },
        "lint": {},
        "dev": {
          "cache": false,
          "persistent": true
        }
      }
    }
    bash title="Terminal"
    npx @turbo/codemod add-package-manager
    diff title="./package.json"
    {
      "name": "turborepo-basic",
      "version": "0.0.0",
      "private": true,
    +  "packageManager": "yarn@1.22.17",
      "workspaces": [
        "apps/*",
        "packages/*"
      ]
    }
    bash title="Terminal"
    npx @turbo/codemod create-turbo-config
    diff title="./package.json"
        // After, package.json
        {
          "name": "@acme/workspace",
          "private": true,
        - "turbo": {
        -   "pipeline": {
        -     ...
        -   }
        - },
        }
        diff title="./turbo.json"
        + {
        +   "$schema": "https://turborepo.com/schema.json",
        +   "pipeline": {
        +     ...
        +   }
        + }
        ts title="./turbo/generators/my-generator.ts"
import type { PlopTypes } from "@turbo/gen"; // [!code highlight]

// [!code word:PlopTypes]
export default function generator(plop: PlopTypes.NodePlopAPI): void {
  // Create a generator
  plop.setGenerator("Generator name", {
    description: "Generator description",
    // Gather information from the user
    prompts: [
      ...
    ],
    // Perform actions based on the prompts
    actions: [
      ...
    ],
  });
}
bash title="Terminal"
npx turbo-ignore [workspace] [flags...]
bash title="Terminal"
turbo unlink
bash title="Terminal"
turbo watch [tasks]
bash title="Terminal"
turbo watch
bash title="Terminal"
turbo watch your-tasks --experimental-write-cache
json title="./package.json"
{
  "name": "my-turborepo",
  "scripts": {
    "build": "turbo run build",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "latest"
  }
}
json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": {
      "outputs": [".next/**", "!.next/cache/**"],
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
yaml title=".buildkite/pipeline.yml"
    steps:
      - label: ":test_tube: Test"
        command: |
          pnpm install
          pnpm test

- label: ":hammer: Build"
        command: |
          pnpm install
          pnpm build
    yaml title=".buildkite/pipeline.yml"
    steps:
      - label: ":test_tube: Test"
        command: |
          yarn
          yarn test

- label: ":hammer: Build"
        command: |
          yarn
          yarn build
    yaml title=".buildkite/pipeline.yml"
    steps:
      - label: ":test_tube: Test"
        command: |
          npm install
          npm test

- label: ":hammer: Build"
        command: |
          npm install
          npm run build
    yaml title=".buildkite/pipeline.yml"
    steps:
      - label: ":test_tube: Test"
        command: |
          bun install
          bun run test

- label: ":hammer: Build"
        command: |
          bun install
          bun run build
    yaml title=".buildkite/pipeline.yml"
steps:
  - label: ':pipeline:'
    command: buildkite-agent pipeline upload
yaml title=".buildkite/pipeline.yml"
   steps:
     - label: ':test_tube: Test'
       command: |
         npm install
         npm test
       plugins:
         - secrets:
             variables:
               TURBO_TOKEN: TURBO_TOKEN
               TURBO_TEAM: TURBO_TEAM

- label: ':hammer: Build'
       command: |
         npm install
         npm run build
       plugins:
         - secrets:
             variables:
               TURBO_TOKEN: TURBO_TOKEN
               TURBO_TEAM: TURBO_TEAM
   json title="./package.json"
{
  "name": "my-turborepo",
  "scripts": {
    "build": "turbo run build",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "latest"
  }
}
json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": {
      "outputs": [".next/**", "!.next/cache/**"],
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
yaml title=".circleci/config.yml"
    version: 2.1
    orbs:
      node: circleci/node@5.0.2
    workflows:
      test:
        jobs:
          - test
    jobs:
      test:
        docker:
          - image: cimg/node:lts
        steps:
          - checkout
          - node/install-packages
          - run:
            command: npm i -g pnpm
            environment:
              TURBO_UI: "false"
          - run:
            command: pnpm build
            environment:
              TURBO_UI: "false"
          - run:
            command: pnpm test
            environment:
              TURBO_UI: "false"
    yaml title=".circleci/config.yml"
    version: 2.1
    orbs:
      node: circleci/node@5.0.2
    workflows:
      test:
        jobs:
          - test
    jobs:
      test:
        docker:
          - image: cimg/node:lts
        steps:
          - checkout
          - node/install-packages:
            pkg-manager: yarn
          - run:
            command: yarn build
            environment:
              TURBO_UI: "false"
          - run:
            command: yarn test
            environment:
              TURBO_UI: "false"
    yaml title=".circleci/config.yml"
    version: 2.1
    orbs:
      node: circleci/node@5.0.2
    workflows:
      test:
        jobs:
          - test
    jobs:
      test:
        docker:
          - image: cimg/node:lts
        steps:
          - checkout
          - node/install-packages
          - run:
            command: npm run build
            environment:
              TURBO_UI: "false"

- run:
            command: npm run test
            environment:
              TURBO_UI: "false"
    yaml title=".circleci/config.yml"
    version: 2.1
    orbs:
      node: circleci/node@5.0.2
    workflows:
      test:
        jobs:
          - test
    jobs:
      test:
        docker:
          - image: cimg/node:lts
        steps:
          - checkout
          - node/install-packages
          - run:
            command: npm i -g bun
            environment:
              TURBO_UI: "false"
          - run:
            command: bun run build
            environment:
              TURBO_UI: "false"
          - run:
            command: bun run test
            environment:
              TURBO_UI: "false"
    json title="./package.json"
{
  "name": "my-turborepo",
  "scripts": {
    "build": "turbo run build",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "latest"
  }
}
json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": {
      "outputs": [".next/**", "!.next/cache/**", "other-output-dirs/**"],
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
yaml title=".github/workflows/ci.yml"
    name: CI

on:
      push:
        branches: ["main"]
      pull_request:
        types: [opened, synchronize]

jobs:
      build:
        name: Build and Test
        timeout-minutes: 15
        runs-on: ubuntu-latest
        # To use Remote Caching, uncomment the next lines and follow the steps below.
        # env:
        #  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
        #  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

steps:
          - name: Check out code
            uses: actions/checkout@v4
            with:
              fetch-depth: 2

- uses: pnpm/action-setup@v3
            with:
              version: 8

- name: Setup Node.js environment
            uses: actions/setup-node@v4
            with:
              node-version: 20
              cache: 'pnpm'

- name: Install dependencies
            run: pnpm install

- name: Build
            run: pnpm build

- name: Test
            run: pnpm test
    yaml title=".github/workflows/ci.yml"
    name: CI

on:
      push:
        branches: ["main"]
      pull_request:
        types: [opened, synchronize]

jobs:
      build:
        name: Build and Test
        timeout-minutes: 15
        runs-on: ubuntu-latest
        # To use Remote Caching, uncomment the next lines and follow the steps below.
        # env:
        #  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
        #  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

steps:
          - name: Check out code
            uses: actions/checkout@v4
            with:
              fetch-depth: 2

- name: Setup Node.js environment
            uses: actions/setup-node@v4
            with:
              node-version: 20
              cache: 'yarn'

- name: Install dependencies
            run: yarn

- name: Build
            run: yarn build

- name: Test
            run: yarn test
    yaml title=".github/workflows/ci.yml"
    name: CI

on:
      push:
        branches: ["main"]
      pull_request:
        types: [opened, synchronize]

jobs:
      build:
        name: Build and Test
        timeout-minutes: 15
        runs-on: ubuntu-latest
        # To use Remote Caching, uncomment the next lines and follow the steps below.
        # env:
        #  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
        #  TURBO_TEAM: ${{ vars.TURBO_TEAM }}
        #  TURBO_REMOTE_ONLY: true

steps:
          - name: Check out code
            uses: actions/checkout@v4
            with:
              fetch-depth: 2

- name: Setup Node.js environment
            uses: actions/setup-node@v4
            with:
              node-version: 20
              cache: 'npm'

- name: Install dependencies
            run: npm install

- name: Build
            run: npm run build

- name: Test
            run: npm run test
    yaml title=".github/workflows/ci.yml"
    name: CI

on:
      push:
        branches: ["main"]
      pull_request:
        types: [opened, synchronize]

jobs:
      build:
        name: Build and Test
        timeout-minutes: 15
        runs-on: ubuntu-latest
        # To use Remote Caching, uncomment the next lines and follow the steps below.
        # env:
        #  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
        #  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

steps:
          - name: Check out code
            uses: actions/checkout@v4
            with:
              fetch-depth: 2

- uses: oven-sh/setup-bun@v2

- name: Setup Node.js environment
            uses: actions/setup-node@v4
            with:
              node-version: 20

- name: Install dependencies
            run: bun install

- name: Build
            run: bun run build

- name: Test
            run: bun run test
    yaml title=".github/workflows/ci.yml"
    # ...

jobs:
      build:
        name: Build and Test
        timeout-minutes: 15
        runs-on: ubuntu-latest
        # To use Turborepo Remote Caching, set the following environment variables for the job.
        env: # [!code highlight]
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }} # [!code highlight]
          TURBO_TEAM: ${{ vars.TURBO_TEAM }} # [!code highlight]

steps:
          - name: Check out code
            uses: actions/checkout@v4
            with:
              fetch-depth: 2
        # ...
    json title="./package.json"
    {
      "name": "my-turborepo",
      "scripts": {
        "build": "turbo run build"
      },
      "devDependencies": {
        "turbo": "1.2.5"
      }
    }
    yaml title=".github/workflows/ci.yml"
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Check out code
            uses: actions/checkout@v4

- name: Cache turbo build setup # [!code highlight]
            uses: actions/cache@v4 # [!code highlight]
            with: # [!code highlight]
              path: .turbo # [!code highlight]
              key: ${{ runner.os }}-turbo-${{ github.sha }} # [!code highlight]
              restore-keys: | # [!code highlight]
                ${{ runner.os }}-turbo-

- name: Setup Node.js environment
            uses: actions/setup-node@v4
            with:
              node-version: 20
              cache: 'npm'

- name: Install dependencies
            run: npm install

- name: Build
            run: npm run build
    json title="./package.json"
{
  "name": "my-turborepo",
  "scripts": {
    "build": "turbo run build",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "latest"
  }
}
json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": {
      "outputs": [".svelte-kit/**"],
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
yaml title=".gitlab-ci.yml"
    image: node:latest
    stages:
      - build
    build:
      stage: build
      before_script:
        - curl -f https://get.pnpm.io/v6.16.js | node - add --global pnpm@6.32.2
        - pnpm config set store-dir .pnpm-store
      script:
        - pnpm install
        - pnpm build
        - pnpm test
      cache:
        key:
          files:
            - pnpm-lock.yaml
        paths:
          - .pnpm-store
    yaml title=".gitlab-ci.yml"
    image: node:latest
    stages:
      - build
    build:
      stage: build
      script:
        - yarn install
        - yarn build
        - yarn test
      cache:
        paths:
          - node_modules/
          - .yarn
    yaml title=".gitlab-ci.yml"
    image: node:latest
    stages:
      - build
    build:
      stage: build
      script:
        - npm install
        - npm run build
        - npm run test
    yaml title=".gitlab-ci.yml"
    default:
      image: oven/bun:1.2
      cache:
        key:
          files:
            - bun.lock
        paths:
          - node_modules/
      before_script:
          - bun install

build:
    script: - bun run build

test:
    script: - bun run test

json title="./package.json"
{
  "name": "my-turborepo",
  "scripts": {
    "build": "turbo run build",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "latest"
  }
}
json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": {
      "outputs": [".svelte-kit/**"],
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
yaml title=".travis.yml"
    language: node_js
    node_js:
      - lts/*
    cache:
      npm: false
      directories:
        - "~/.pnpm-store"
    before_install:
      - curl -f https://get.pnpm.io/v6.16.js | node - add --global pnpm@6.32.2
      - pnpm config set store-dir ~/.pnpm-store
    install:
      - pnpm install
    script:
      - pnpm build
    script:
      - pnpm test
    yaml title=".travis.yml"
    language: node_js
    node_js:
      - lts/*
    install:
      - yarn
    script:
      - yarn build
    script:
      - yarn test
    yaml title=".travis.yml"
    language: node_js
    node_js:
      - lts/*
    install:
      - npm install
    script:
      - npm run build
    script:
      - npm run test
    yaml title=".travis.yml"
    language: node_js
    node_js:
      - lts/*
    cache:
      npm: false
      directories:
        - "~/.pnpm-store"
    before_install:
      - curl -fsSL https://bun.sh/install | bash
    install:
      - bun install
    script:
      - bun run build
    script:
      - bun run test
    json title="./packages/ui/package.json"
{
  "name": "@repo/ui",
  "peerDependencies": {
    "next": "*"
  }
}
tsx title="./packages/ui/src/link.tsx"
import Link from 'next/link';
import type { ComponentProps } from 'react';

type CustomLinkProps = ComponentProps<typeof Link>;

export function CustomLink({ children, ...props }: CustomLinkProps) {
  return (
    <Link className="text-underline hover:text-green-400" {...props}>
      {children}
    </Link>
  );
}
json title="./packages/ui/package.json"
{
  "exports": {
    "./link": "./dist/link.js",
    "./next-js/link": "./dist/next-js/link.js"
  },
  "peerDependencies": {
    "next": "*"
  }
}
bash title="Terminal"
    pnpm dlx create-turbo@latest
    bash title="Terminal"
    yarn dlx create-turbo@latest
    bash title="Terminal"
    npx create-turbo@latest
    bash title="Terminal"
    bunx create-turbo@latest
    bash title="Terminal"
    pnpm dlx create-next-app@latest apps/my-app
    bash title="Terminal"
    yarn dlx create-next-app@latest apps/my-app
    bash title="Terminal"
    npx create-next-app@latest apps/my-app
    bash title="Terminal"
    bunx create-next-app@latest apps/my-app
    diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ts title="./apps/my-app/next.config.ts"
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  basePath: '/docs',
};

export default nextConfig;
bash title="Terminal"
    pnpm dlx create-turbo@latest -e with-vue-nuxt
    bash title="Terminal"
    yarn dlx create-turbo@latest -e with-vue-nuxt
    bash title="Terminal"
    npx create-turbo@latest -e with-vue-nuxt
    bash title="Terminal"
    bunx create-turbo@latest -e with-vue-nuxt
    bash title="Terminal"
    pnpm dlx nuxi@latest init apps/my-app
    bash title="Terminal"
    yarn dlx nuxi@latest init apps/my-app
    bash title="Terminal"
    npx nuxi@latest init apps/my-app
    bash title="Terminal"
    bunx nuxi@latest init apps/my-app
    diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ts title="./apps/my-app/vite.config.ts"
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/admin',
});
bash title="Terminal"
    pnpm dlx create-turbo@latest -e with-svelte
    bash title="Terminal"
    yarn dlx create-turbo@latest -e with-svelte
    bash title="Terminal"
    npx create-turbo@latest -e with-svelte
    bash title="Terminal"
    bunx create-turbo@latest -e with-svelte
    bash title="Terminal"
    pnpm dlx sv create
    bash title="Terminal"
    yarn dlx sv create
    bash title="Terminal"
    npx sv create
    bash title="Terminal"
    bunx sv create
    diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ts title="./apps/my-app/vite.config.ts"
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/admin',
});
bash title="Terminal"
    pnpm dlx create-turbo@latest -e with-vite
    bash title="Terminal"
    yarn dlx create-turbo@latest -e with-vite
    bash title="Terminal"
    npx create-turbo@latest -e with-vite
    bash title="Terminal"
    bunx create-turbo@latest -e with-vite
    bash title="Terminal"
    pnpm create vite@latest apps/my-app
    bash title="Terminal"
    yarn create vite@latest apps/my-app
    bash title="Terminal"
    npm create vite@latest apps/my-app
    bash title="Terminal"
    bun create vite@latest apps/my-app
    diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ts title="./apps/my-app/vite.config.ts"
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/admin',
});
json title="./package.json"
{
  "scripts": {
    "format-and-lint": "biome check .",
    "format-and-lint:fix": "biome check . --write"
  }
}
json title="./turbo.json"
{
  "tasks": {
    "//#format-and-lint": {},
    "//#format-and-lint:fix": {
      "cache": false
    }
  }
}
docker title="./apps/api/Dockerfile"
FROM node:16

**Examples:**

Example 1 (unknown):
```unknown
### `--force`

Ignore existing cached artifacts and re-execute all tasks.

<Callout type="good-to-know">
  `--force` will overwrite existing task caches.
</Callout>
```

Example 2 (unknown):
```unknown
The same behavior can also be set via [the `TURBO_FORCE` environment variable](/docs/reference/system-environment-variables).

### `--framework-inference`

Default: `true`

Specify whether or not to do [Framework Inference](/docs/crafting-your-repository/using-environment-variables#framework-inference) for tasks.

When `false`, [automatic environment variable inclusion](/docs/crafting-your-repository/using-environment-variables#framework-inference) is disabled.
```

Example 3 (unknown):
```unknown
### `--global-deps <file glob>`

Specify glob of global filesystem dependencies to be hashed. Useful for `.env` and files in the root directory that impact multiple packages.
```

Example 4 (unknown):
```unknown
<Callout type="info">
  We recommend specifying file globs that you'd like to include your hashes in
  [the `globalDependencies` key](/docs/reference/configuration#globaldeps) in
  `turbo.json` to make sure they are always accounted for.
</Callout>

### `--graph <file name>`

Default: `dot`

This command can output a graph file: `svg`, `png`, `jpg`, `pdf`, `json`, `html`, `mermaid`, or `dot`.

If [Graphviz](https://graphviz.org/) is not installed, or no filename is provided, this command prints the dot graph to `stdout`.
```

---

## Read from and write to local cache. Only read from Remote Cache.

**URL:** llms-txt#read-from-and-write-to-local-cache.-only-read-from-remote-cache.

turbo run build --cache=local:rw,remote:r

---

## Do not use local cache. Only read from Remote Cache.

**URL:** llms-txt#do-not-use-local-cache.-only-read-from-remote-cache.

**Contents:**
  - `--cache-dir <path>`
  - `--concurrency <number | percentage>`
  - `--continue[=<option>]`
  - `--cwd <path>`
  - `--dangerously-disable-package-manager-check`
  - `--dry / --dry-run`
  - `--env-mode <option>`
  - `--filter <string>`

turbo run build --cache=local:,remote:r
bash title="Terminal"
turbo run build --cache-dir="./my-cache"
bash title="Terminal"
turbo run build --concurrency=50%
turbo run test --concurrency=5
bash title="Terminal"
turbo run build --continue
bash title="Terminal"
turbo run build --cwd=./somewhere/else/in/your/repo
bash title="Terminal"
turbo run build --env-mode=loose
bash title="Terminal"
turbo run web#lint
bash title="Terminal"

**Examples:**

Example 1 (unknown):
```unknown
### `--cache-dir <path>`

Default: `.turbo/cache`

Specify the filesystem cache directory.
```

Example 2 (unknown):
```unknown
<Callout type="warn">
  Ensure the directory is in your `.gitignore` when changing it.
</Callout>

The same behavior can also be set via the `TURBO_CACHE_DIR=example/path` system variable.

### `--concurrency <number | percentage>`

Default: `10`

Set/limit the maximum concurrency for task execution. Must be an integer greater than or equal to `1` or a percentage value like `50%`.

* Use `1` to force serial execution (one task at a time).
* Use `100%` to use all available logical processors.
* This option is ignored if the [`--parallel`](#--parallel) flag is also passed.
```

Example 3 (unknown):
```unknown
### `--continue[=<option>]`

Default: `never`

Specify how `turbo` should handle current and pending tasks in the presence of an error (e.g. non-zero exit code from a task).

* When `--continue=never` and an error occurs, `turbo` will cancel all tasks.
* When `--continue=dependencies-successful` and an error occurs, `turbo` will cancel dependent tasks. Tasks whose dependencies have succeeded will continue to run.
* When `--continue=always` and an error occurs, `turbo` will continue running all tasks, even those whose dependencies have failed.
* When `--continue` is specified without a value, it will default to `always`.

In all cases, `turbo` will exit with the highest exit code value encountered during execution.
```

Example 4 (unknown):
```unknown
### `--cwd <path>`

Default: Directory of root `turbo.json`

Set the working directory of the command.
```

---

## https://nextjs.org/docs/advanced-features/output-file-tracing

**URL:** llms-txt#https://nextjs.org/docs/advanced-features/output-file-tracing

**Contents:**
- Remote Caching
- ESLint v9 (Flat Configs)
  - About the configuration package
  - Using the configuration package
- ESLint v8 (Legacy)
  - The `@repo/eslint-config` package
  - How to use the `@repo/eslint-config` package
- Setting up a `lint` task
- Setting up
- Running tests in watch mode

COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./apps/web/.next/static
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/public ./apps/web/public

CMD node apps/web/server.js
docker title="./apps/api/Dockerfile"
ARG TURBO_TEAM
ENV TURBO_TEAM=$TURBO_TEAM

ARG TURBO_TOKEN
ENV TURBO_TOKEN=$TURBO_TOKEN

RUN yarn turbo run build
bash title="Terminal"
docker build -f apps/web/Dockerfile . --build-arg TURBO_TEAM=“your-team-name” --build-arg TURBO_TOKEN=“your-token“ --no-cache
jsonc title="./apps/web/package.json"
    {
      "devDependencies": {
        "@repo/eslint-config": "workspace:*"
      }
    }
    jsonc title="./apps/web/package.json"
    {
      "devDependencies": {
        "@repo/eslint-config": "*"
      }
    }
    jsonc title="./apps/web/package.json"
    {
      "devDependencies": {
        "@repo/eslint-config": "*"
      }
    }
    jsonc title="./apps/web/package.json"
    {
      "devDependencies": {
        "@repo/eslint-config": "workspace:*"
      }
    }
    js title="./apps/web/eslint.config.js"
import { nextJsConfig } from '@repo/eslint-config/next-js';

/** @type {import("eslint").Linter.Config} */
export default nextJsConfig;
js title="./apps/web/eslint.config.js"
import { nextJsConfig } from '@repo/eslint-config/next-js';

/** @type {import("eslint").Linter.Config} */
export default [
  ...nextJsConfig,
  // Other configurations
];
js title="./packages/eslint-config/next.js"
/* Custom ESLint configuration for use with Next.js apps. */
module.exports = {
  extends: [
    'eslint-config-turbo',
    'eslint-config-next',
    // ...your other ESLint configurations
  ].map(require.resolve),
  // ...your other configuration
};
json title="./packages/eslint-config/package.json"
{
  "name": "@repo/eslint-config",
  "version": "0.0.0",
  "private": true,
  "devDependencies": {
    "eslint": "^8",
    "eslint-config-turbo": "latest",
    "eslint-config-next": "latest"
  }
}
jsonc title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/eslint-config": "workspace:*"
      }
    }
    jsonc title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/eslint-config": "*"
      }
    }
    jsonc title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/eslint-config": "*"
      }
    }
    jsonc title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/eslint-config": "workspace:*"
      }
    }
    js title="./apps/web/.eslintrc.js"
module.exports = {
  root: true,
  extends: ['@repo/eslint-config/next.js'],
};
json title="./packages/*/package.json"
{
  "scripts": {
    "lint": "eslint ."
  }
}
bash title="./turbo.json"
{
  "tasks": {
    "lint": {}
  }
}
json title="./package.json"
{
  "scripts": {
    "lint": "turbo run lint"
  }
}
bash title="Terminal"
    pnpm add jest --save-dev --filter=@repo/ui --filter=web
    bash title="Terminal"
    yarn workspace web add jest --dev
    yarn workspace @repo/ui add jest --dev
    bash title="Terminal"
    npm install jest --workspace=web --workspace=@repo/ui --save-dev
    bash title="Terminal"
    cd apps/web && bun install jest --dev
    cd packages/ui && bun install jest --dev
    json title="./apps/web/package.json"
    {
      "name": "web",
      "scripts": {
        "test": "jest"
      },
      "devDependencies": {
        "jest": "latest"
      }
    }
    json title="./packages/ui/package.json"
    {
      "name": "@repo/ui",
      "scripts": {
        "test": "jest"
      },
      "devDependencies": {
        "jest": "latest"
      }
    }
    json title="./turbo.json"
{
  "tasks": {
    "test": {}
  }
}
json title="./apps/web/package.json"
    {
      "name": "web",
      "scripts": {
        "test": "jest",
        "test:watch": "jest --watch" // [!code highlight]
      },
      "devDependencies": {
        "jest": "latest"
      }
    }
    json title="./packages/ui/package.json"
    {
      "name": "@repo/ui",
      "scripts": {
        "test": "jest",
        "test:watch": "jest --watch" // [!code highlight]
      },
      "devDependencies": {
        "jest": "latest"
      }
    }
    json title="./turbo.json"
{
  "tasks": {
    "test": {},
    "test:watch": {
      "cache": false, // [!code highlight]
      "persistent": true // [!code highlight]
    }
  }
}
bash title="Terminal"
    turbo test
    bash title="Terminal"
    turbo test:watch
    json title="./package.json"
    {
      "scripts": {
        "test": "turbo run test",
        "test:watch": "turbo run test:watch"
      }
    }
    json title="./turbo.json"
    {
      "tasks": {
        "e2e": {
          "passThroughEnv": ["PLAYWRIGHT_*"]
        }
      }
    }
    json title="./turbo.json"
    {
      "globalPassThroughEnv": ["PLAYWRIGHT_*"]
    }
    json title="./turbo.json"
    {
      "tasks": {
        "build": {
          "dependsOn": ["^build"]
        },
        "e2e": {
          "dependsOn": ["^build"] // [!code highlight]
        }
      }
    }
    json title="./tooling/playwright-web/package.json"
    {
      "name": "@repo/playwright-web",
      "dependencies": {
        "web": "workspace:*" // [!code highlight]
      }
    }
    json title="./packages/playwright-utilities/package.json"
    {
      "name": "@repo/playwright-utilities",
      "peerDependencies": {
        "playwright": "workspace:*"
    }
    }
    json title="./packages/playwright-utilities/package.json"
    {
      "name": "@repo/playwright-utilities",
      "peerDependencies": {
        "playwright": "*"
    }
    }
    json title="./packages/playwright-utilities/package.json"
    {
      "name": "@repo/playwright-utilities",
      "peerDependencies": {
        "playwright": "*"
      }
    }
    json title="./packages/playwright-utilities/package.json"
    {
      "name": "@repo/playwright-utilities",
      "peerDependencies": {
        "playwright": "workspace:*"
      }
    }
    bash title="Terminal"
npx create-turbo@latest -e with-prisma
bash title="Terminal"
    pnpm dlx shadcn@canary init
    bash title="Terminal"
    npx shadcn@canary init
    bash title="Terminal"
    npx shadcn@canary init
    bash title="Terminal"
    bunx shadcn@canary init
    bash title="Terminal"
    pnpm dlx shadcn@canary add [COMPONENT]
    bash title="Terminal"
    npx shadcn@canary add [COMPONENT]
    bash title="Terminal"
    npx shadcn@canary add [COMPONENT]
    bash title="Terminal"
    bunx shadcn@canary add [COMPONENT]
    bash title="Terminal"
    pnpm dlx create-turbo@latest -e design-system
    bash title="Terminal"
    yarn dlx create-turbo@latest -e design-system
    bash title="Terminal"
    npx create-turbo@latest -e design-system
    bash title="Terminal"
    bunx create-turbo@latest -e design-system
    bash title="Terminal"
        pnpm dlx create-turbo@latest
        bash title="Terminal"
        yarn dlx create-turbo@latest
        bash title="Terminal"
        npx create-turbo@latest
        bash title="Terminal"
        bunx create-turbo@latest
        bash title="Terminal"
    mkdir apps/storybook
    cd apps/storybook
    bash title="Terminal"
        pnpm create storybook@latest
        bash title="Terminal"
        yarn create storybook@latest
        bash title="Terminal"
        npm create storybook@latest
        bash title="Terminal"
        bun create storybook@latest
        bash title="Terminal"
        pnpm add @repo/ui --filter=storybook
        bash title="Terminal"
        yarn workspace storybook add @repo/ui
        bash title="Terminal"
        npm install @repo/ui --workspace=storybook
        bash title="Terminal"
        cd apps/storybook && bun install @repo/ui
        tsx title="./apps/storybook/src/stories/Button.stories.tsx"
    import type { Meta, StoryObj } from '@storybook/react';
    import { Button } from '@repo/ui/button';

const meta = {
      title: 'Example/Button',
      component: Button,
      tags: ['autodocs'],
    } satisfies Meta<typeof Button>;

export default meta;
    type Story = StoryObj<typeof meta>;

export const Primary: Story = {
      args: {
        appName: 'Button',
        children: 'I am a primary button.',
      },
    };
    json title="apps/storybook/package.json"
    {
      "scripts": {
        "dev": "storybook dev -p 6006", // [!code highlight]
        "build": "storybook build" // [!code highlight]
      }
    }
    diff title="turbo.json"
    {
      "tasks": {
        "build": {
          "outputs": [
            ".next/**",
            "!.next/cache/**"
    +       "storybook-static/**"
          ]
        }
      }
    }
    diff title=".gitignore"
      + storybook-static
      diff title="./apps/storybook/.storybook/main.ts"

const config = {
      stories: [
    -   "../src/**/*.mdx",
    -   "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
    +   "../../../packages/ui/src/**/*.stories.@(js|jsx|mjs|ts|tsx)",
    };
    diff title="./packages/ui/src/Button.stories.tsx"
    - import { Button } from "@repo/ui/button";
    + import { Button } from "./button";
    bash title="Terminal"
        pnpm add @storybook/react --filter=@repo/ui --save-dev
        bash title="Terminal"
        yarn workspace @repo/ui add @storybook/react --dev
        bash title="Terminal"
        npm install @storybook/react --workspace=@repo/ui --save-dev
        bash title="Terminal"
        cd packages/ui && bun install @storybook/react --dev
        json title="./turbo.json"
    {
      "tasks": {
        "build": {
          "dependsOn": ["^build"],
          "inputs": ["$TURBO_DEFAULT$", "!**/*.stories.{tsx,jsx,mdx}"], // [!code highlight]
          "outputs": [".next/**", "!.next/cache/**"]
        },
        "build:storybook": {} // [!code highlight]
      }
    }
    json title="./apps/storybook/turbo.json"
    {
      "extends": ["//"],
      "tasks": {
        "build:storybook": {
          "dependsOn": ["^build:storybook"],
          "outputs": ["storybook-static/**"]
        }
      }
    }
    json title="apps/storybook/package.json"
    {
      "scripts": {
        "dev": "storybook dev -p 6006",
        "build:storybook": "storybook build" // [!code highlight]
      }
    }
    bash title="Terminal"
    pnpm dlx create-turbo@latest -e with-tailwind
    bash title="Terminal"
    yarn dlx create-turbo@latest -e with-tailwind
    bash title="Terminal"
    npx create-turbo@latest -e with-tailwind
    bash title="Terminal"
    bunx create-turbo@latest -e with-tailwind
    bash title="Terminal"
        pnpm dlx create-turbo@latest
        bash title="Terminal"
        yarn dlx create-turbo@latest
        bash title="Terminal"
        npx create-turbo@latest
        bash title="Terminal"
        bunx create-turbo@latest
        json title="./packages/tailwind-config/package.json"
        {
          "name": "@repo/tailwind-config",
          "version": "0.0.0",
          "type": "module",
          "private": true,
          "exports": {
            ".": "./shared-styles.css",
            "./postcss": "./postcss.config.js"
          },
          "devDependencies": {
            "postcss": "^8.5.3",
            "tailwindcss": "^4.1.5"
          }
        }
        css title="./packages/tailwind-config/shared-styles.css"
        @import 'tailwindcss';

@theme {
          --blue-1000: #2a8af6;
          --purple-1000: #a853ba;
          --red-1000: #e92a67;
        }
        js title="./packages/tailwind-config/postcss.config.js"
        export const postcssConfig = {
          plugins: {
            '@tailwindcss/postcss': {},
          },
        };
        json title="./packages/ui/package.json"
        {
          "exports": {
            "./styles.css": "./dist/index.css",
            "./*": "./dist/*.js"
          },
          "scripts": {
            "build:styles": "tailwindcss -i ./src/styles.css -o ./dist/index.css",
            "build:components": "tsc",
            "dev:styles": "tailwindcss -i ./src/styles.css -o ./dist/index.css --watch",
            "dev:components": "tsc --watch"
          },
          "devDependencies": {
            "@repo/tailwind-config": "workspace:*",
            "@tailwindcss/cli": "^4.1.5",
            "@tailwindcss/postcss": "^4.1.5",
            "autoprefixer": "^10.4.20",
            "tailwindcss": "^4.1.5"
          }
        }
        json title="./packages/ui/turbo.json"
        {
          "extends": ["//"],
          "tasks": {
            "build": {
              "dependsOn": ["build:styles", "build:components"]
            },
            "build:styles": {
              "outputs": ["dist/**"]
            },
            "build:components": {
              "outputs": ["dist/**"]
            },
            "dev": {
              "with": ["dev:styles", "dev:components"]
            },
            "dev:styles": {
              "cache": false,
              "persistent": true
            },
            "dev:components": {
              "cache": false,
              "persistent": true
            }
          }
        }
        css title="./packages/ui/src/styles.css"
        /* Component-level styles for the UI package */
        @import 'tailwindcss' prefix(ui);
        bash title="Terminal"
        pnpm add @repo/ui @repo/tailwind-config --save-dev --filter=@repo/ui --filter=web
        bash title="Terminal"
        yarn workspace web add @repo/ui @repo/tailwind-config --dev
        yarn workspace @repo/ui add @repo/ui @repo/tailwind-config --dev
        bash title="Terminal"
        npm install @repo/ui @repo/tailwind-config --workspace=web --workspace=@repo/ui --save-dev
        bash title="Terminal"
        cd apps/web && bun install @repo/ui @repo/tailwind-config --dev
        cd packages/ui && bun install @repo/ui @repo/tailwind-config --dev
        css title="./apps/web/app/globals.css"
        @import 'tailwindcss';
        @import '@repo/tailwind-config';
        tsx title="./apps/web/app/layout.tsx"
        import '@repo/ui/styles.css';
        import './globals.css';
        js title="./apps/web/postcss.config.js"
        import { postcssConfig } from '@repo/tailwind-config/postcss';

export default postcssConfig;
        bash title="Terminal"
    pnpm dlx create-turbo@latest
    bash title="Terminal"
    yarn dlx create-turbo@latest
    bash title="Terminal"
    npx create-turbo@latest
    bash title="Terminal"
    bunx create-turbo@latest
    json title="./packages/typescript-config/base.json"
{
  "compilerOptions": {
    "esModuleInterop": true,
    "skipLibCheck": true,
    "target": "es2022",
    "allowJs": true,
    "resolveJsonModule": true,
    "moduleDetection": "force",
    "isolatedModules": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "module": "NodeNext"
  }
}
json title="packages/typescript-config/package.json"
{
  "name": "@repo/typescript-config"
}
json title="./apps/web/package.json"
    {
      "devDependencies": {
         "@repo/typescript-config": "workspace:*",
         "typescript": "latest",
      }
    }
    json title="./apps/web/package.json"
    {
      "devDependencies": {
         "@repo/typescript-config": "*",
         "typescript": "latest",
      }
    }
    json title="./apps/web/package.json"
    {
      "devDependencies": {
         "@repo/typescript-config": "*",
         "typescript": "latest",
      }
    }
    json title="./apps/web/package.json"
    {
      "devDependencies": {
         "@repo/typescript-config": "workspace:*",
         "typescript": "latest",
      }
    }
    json title="./apps/web/tsconfig.json"
{
  "extends": "@repo/typescript-config/nextjs.json",
  "compilerOptions": {
    "outDir": "dist"
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
json title="./packages/ui/package.json"
{
  "scripts": {
    "dev": "tsc --watch",
    "build": "tsc"
  }
}
json title="./packages/ui/package.json"
{
  "exports": {
    "./*": {
      "types": "./src/*.ts",
      "default": "./dist/*.js"
    }
  }
}
json title="./apps/web/package.json"
{
  "scripts": {
    "check-types": "tsc --noEmit"
  }
}
json title="./turbo.json"
{
  "tasks": {
    "topo": {
      "dependsOn": ["^topo"]
    },
    "check-types": {
      "dependsOn": ["topo"]
    }
  }
}
json title="./packages/ui/package.json"
    {
      "imports": {
        "#*": "./src/*"
      }
    }
    tsx title="./packages/ui/button.tsx"
    import { MY_STRING } from "#utils.ts" // Uses .ts extension // [!code highlight]

export const Button = () => {
      return (
        <button>{MY_STRING}</button>
      )
    }
    json title="./packages/ui/package.json"
    {
      "imports": {
        "#*": "./dist/*"
      }
    }
    tsx title="./packages/ui/button.tsx"
    import { MY_STRING } from '#utils.js'; // Uses .js extension // [!code highlight]

export const Button = () => {
      return <button>{MY_STRING}</button>;
    };
    json title="./apps/web/package.json"
{
  "scripts": {
    "test": "vitest run"
  },
  "devDependencies": {
    "vitest": "latest"
  }
}
json title="./turbo.json"
{
  "tasks": {
    "test": {
      "dependsOn": ["transit"]
    },
    "transit": {
      "dependsOn": ["^transit"]
    }
  }
}
json title="./apps/web/package.json"
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest --watch"
  }
}
json title="./turbo.json"
{
  "tasks": {
    "test": {
      "dependsOn": ["^test"]
    },
    "test:watch": {
      "cache": false,
      "persistent": true
    }
  }
}
bash title="Terminal"
    turbo run test

turbo run test:watch
    json title="./package.json"
    {
      "scripts": {
        "test": "turbo run test",
        "test:watch": "turbo run test:watch"
      }
    }
    json title="./turbo.json"
{
  "tasks": {
    "test": {
      "dependsOn": ["^test", "@repo/vitest-config#build"],
      "outputs": ["coverage.json"]
    },
    "merge-json-reports": {
      "inputs": ["coverage/raw/**"],
      "outputs": ["coverage/merged/**"]
    },
    "report": {
      "dependsOn": ["merge-json-reports"],
      "inputs": ["coverage/merge"],
      "outputs": ["coverage/report/**"]
    }
  }
}
json title="./turbo.json"
{
  "tasks": {
    "//#test": {
      "outputs": ["coverage/**"]
    },
    "//#test:watch": {
      "cache": false,
      "persistent": true
    }
  }
}
json title="./packages/vitest-config/package.json"
{
  "name": "@repo/vitest-config",
  "version": "0.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {
    "vitest": "latest"
  },
  "devDependencies": {
    "@repo/typescript-config": "workspace:*",
    "typescript": "latest"
  }
}
json title="./packages/vitest-config/tsconfig.json"
{
  "extends": "@repo/typescript-config/base.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["dist", "node_modules"]
}
ts title="./packages/vitest-config/src/index.ts"
export const sharedConfig = {
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    // Other shared configuration
  },
};
ts title="./vitest.config.ts"
import { defineConfig } from 'vitest/config';
import { sharedConfig } from '@repo/vitest-config';

export default defineConfig({
  ...sharedConfig,
  projects: [
    {
      name: 'packages',
      root: './packages/*',
      test: {
        ...sharedConfig.test,
        // Project-specific configuration
      },
    },
  ],
});
json title="./packages/ui/package.json"
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest --watch"
  },
  "devDependencies": {
    "@repo/vitest-config": "workspace:*",
    "vitest": "latest"
  }
}
ts title="./packages/ui/vitest.config.ts"
import { defineConfig } from 'vitest/config';
import { sharedConfig } from '@repo/vitest-config';

export default defineConfig({
  ...sharedConfig,
  test: {
    ...sharedConfig.test,
    // Package-specific overrides if needed
  },
});
json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["^test", "@repo/vitest-config#build"]
    },
    "test:watch": {
      "cache": false,
      "persistent": true
    }
  }
}
json title="./package.json"
{
  "scripts": {
    "test:projects": "vitest run",
    "test:projects:watch": "vitest --watch"
  }
}
```

This configuration allows developers to run `pnpm test:projects` or `pnpm test:projects:watch` at the root for a seamless local development experience using Vitest projects, while CI continues to use `turbo run test` to leverage package-level caching. **You'll still need to handle merged coverage reports manually as described in the previous section**.

**Examples:**

Example 1 (unknown):
```unknown
## Remote Caching

To take advantage of remote caches during Docker builds, you will need to make sure your build container has credentials to access your [Remote Cache](/docs/core-concepts/remote-caching).

There are many ways to take care of secrets in a Docker image. We will use a simple strategy here with multi-stage builds using secrets as build arguments that will get hidden for the final image.

Assuming you are using a Dockerfile similar to the one above, we will bring in some environment variables from build arguments right before `turbo build`:
```

Example 2 (unknown):
```unknown
`turbo` will now be able to hit your Remote Cache. To see a Turborepo cache hit for a non-cached Docker build image, run a command like this one from your project root:
```

Example 3 (unknown):
```unknown
- [ESLint](/guides/tools/eslint.md): Learn how to use ESLint in a monorepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';
import { Files, Folder, File } from '#components/files';
import { CreateTurboCallout } from './create-turbo-callout.tsx';

ESLint is a static analysis tool for quickly finding and fixing problems in your JavaScript code.

<CreateTurboCallout />

In this guide, we'll cover:

* [ESLint v9 with Flat Configuration](#eslint-v9-flat-configs)
* [ESLint v8 with legacy configuration](#eslint-v8-legacy)
* [How to set up a `lint` task (applies to both versions)](#setting-up-a-lint-task)

We will share configurations across the monorepo's Workspace, ensuring configuration is consistent across packages and composable to maintain high cache hit ratios.

## ESLint v9 (Flat Configs)

Using ESLint v9's Flat Configs, we will end up with a file structure like this:

<Files>
  <Folder name="apps" defaultOpen>
    <Folder name="docs" defaultOpen>
      <File name="package.json" />

      <File name="eslint.config.js" green />
    </Folder>

    <Folder name="web" defaultOpen>
      <File name="package.json" />

      <File name="eslint.config.js" green />
    </Folder>
  </Folder>

  <Folder name="packages" defaultOpen>
    <Folder name="eslint-config" defaultOpen>
      <File name="base.js" green />

      <File name="next.js" green />

      <File name="react-internal.js" green />

      <File name="package.json" />
    </Folder>

    <Folder name="ui" defaultOpen>
      <File name="eslint.config.js" green />

      <File name="package.json" />
    </Folder>
  </Folder>
</Files>

This structure includes:

* A package called `@repo/eslint-config` in `./packages/eslint-config` that holds all ESLint configuration
* Two applications, each with their own `eslint.config.js`
* A `ui` package that also has its own `eslint.config.js`

### About the configuration package

The `@repo/eslint-config` package has three configuration files, `base.js`, `next.js`, and `react-internal.js`. They are [exported from `package.json`](https://github.com/vercel/turborepo/blob/main/examples/basic/packages/eslint-config/package.json#L6) so that they can be used by other packages, according to needs. Examples of the configurations can be found [in the Turborepo GitHub repository](https://github.com/vercel/turborepo/tree/main/examples/basic/packages/eslint-config) and are available in `npx create-turbo@latest`.

Notably, the `next.js` and `react-internal.js` configurations use the `base.js` configuration for consistency, extending it with more configuration for their respective requirements. Additionally, notice that [the `package.json` for `eslint-config`](https://github.com/vercel/turborepo/blob/main/examples/basic/packages/eslint-config/package.json) has all of the ESLint dependencies for the repository. This is useful, since it means we don't need to re-specify the dependencies in the packages that import `@repo/eslint-config`.

### Using the configuration package

In our `web` app, we first need to add `@repo/eslint-config` as a dependency.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
```

Example 4 (unknown):
```unknown
</Tab>

  <Tab value="yarn">
```

---

## Only read from local cache. Read from and write to Remote Cache.

**URL:** llms-txt#only-read-from-local-cache.-read-from-and-write-to-remote-cache.

turbo run build --cache=local:r,remote:rw

---

## ENV TURBO_TOKEN=$TURBO_TOKEN

**URL:** llms-txt#env-turbo_token=$turbo_token

---

## Run the build task for the docs and web packages

**URL:** llms-txt#run-the-build-task-for-the-docs-and-web-packages

turbo run build --filter=docs --filter=web

---

## Publish all changed packages to npm

**URL:** llms-txt#publish-all-changed-packages-to-npm

**Contents:**
- Installation
  - Running a `package.json` script using global `turbo` (optional)
- Running many scripts with one command
- Parallelizing tasks
- Optimizing task using inputs
- Using `turbo-ignore`
- Customizing behavior
- Using `turbo-ignore` on Vercel
- Customizing behavior
- Why this error occurred

changeset publish
json title="./.changeset/config.json"
{
  // …
  "commit": true
  // …
}
json title="./package.json"
{
  "scripts": {
    // Include build, lint, test - all the things you need to run
    // before publishing
    "publish-packages": "turbo run build lint test && changeset version && changeset publish"
  }
}
json title="./.changeset/config.json"
{
  // …
  "access": "public"
  // …
}
bash title="Terminal"
    pnpm add turbo --save-dev
    bash title="Terminal"
    yarn add turbo --dev
    bash title="Terminal"
    npm install turbo --save-dev
    bash title="Terminal"
    bun install turbo --dev
    json title="package.json"
{
  "name": "@acme/my-app",
  "version": "0.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "check-types": "tsc --noEmit",
    "db:up": "docker-compose up -d",
    "db:push": "your-orm-tool schema-push",
    "db:seed": "node ./db-seed.js"
  }
}
json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "dev": {
      "dependsOn": ["db:seed"],
      "cache": false,
      "persistent": true
    },
    "db:seed": {
      "dependsOn": ["db:push"],
      "cache": false
    },
    "db:push": {
      "dependsOn": ["db:up"],
      "cache": false
    },
    "db:up": {
      "cache": false
    }
  }
}
json title="./package.json"
{
  "scripts": {
    "lint": "eslint .",
    "format": "prettier .",
    "check-types": "tsc --noEmit"
  }
}
json title="turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "lint": {},
    "format": {},
    "check-types": {}
  }
}
bash title="Terminal"
turbo check-types lint format
json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "check-types": {
      "inputs": ["**/*.{ts,tsx}"]
    }
  }
}
bash title="Terminal"
npx turbo-ignore web --task=test
bash title="Terminal"
npx turbo run build --filter=@example/web...3c8387ffd98b751305fe3f0284befdd00cbd4610 --dry=json
bash title="Terminal"
npx turbo-ignore web
json title="./turbo.json"
{
  "globalEnv": ["$MY_ENV_VAR"]
}
json title="./turbo.json"
{
  "globalEnv": ["MY_ENV_VAR"]
}
json title="./package.json"
{
  "scripts": {
    "build": "turbo run build"
  }
}
json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
json title="./turbo.json"
{
  "tasks": {
    "//#build": {}
  }
}
json title="./turbo.json"
{
  "tasks": {
    "app#build": {
      "cache": true
    }
  }
}
json title="./turbo.json"
{
  "tasks": {
    "build": {
      "cache": true
    }
  }
}
json title="./package.json"
{
  "scripts": {
    "build": "turbo run build"
  }
}
json title="./package.json"
{
  "scripts": {
    "build:app": "turbo run build"
  }
}
json title="./turbo.json"
{
  "tasks": {
    "web#build": {
      "dependsOn": ["lint"]
    }
  }
}
json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["lint"]
    }
  }
}
bash title="Terminal"
turbo bin
bash title="Terminal"
turbo boundaries
json title="./packages/ui/turbo.json"
{
  "tags": ["internal"]
}
json title="./turbo.json"
{
  "boundaries": {
    "tags": {
      "public": {
        "dependencies": {
          "deny": ["internal"]
        }
      }
    }
  }
}
json title="turbo.json"
{
  "boundaries": {
    "tags": {
      "public": {
        "dependencies": {
          "allow": ["public"]
        }
      }
    }
  }
}
json title="turbo.json"
{
  "boundaries": {
    "tags": {
      "private": {
        "dependents": {
          "deny": ["public"]
        }
      }
    }
  }
}
json title="turbo.json"
{
  "boundaries": {
    "tags": {
      "private": {
        "dependents": {
          "deny": ["@repo/my-pkg"]
        }
      }
    }
  }
}
jsonc title="./apps/web/turbo.json"
{
  "extends": ["//"]
}
jsonc title="./turbo.json"
{
  "globalDependencies": [".env", "tsconfig.json"]
}
jsonc title="./turbo.json"
{
  "globalEnv": ["GITHUB_TOKEN", "PACKAGE_VERSION", "NODE_ENV"]
}
jsonc title="./turbo.json"
{
  "globalPassThroughEnv": ["AWS_SECRET_KEY", "GITHUB_TOKEN"]
}
json title="./turbo.json"
{
  "ui": "tui" | "stream"
}
json title="./turbo.json"
{
  "noUpdateNotifier": true
}
jsonc title="./turbo.json"
{
  "concurrency": "1"
}
jsonc title="./turbo.json"
{
  "dangerouslyDisablePackageManagerCheck": true
}
jsonc title="./turbo.json"
{
  "cacheDir": ".turbo/cache"
}
jsonc title="./turbo.json"
{
  "daemon": true
}
jsonc title="./turbo.json"
{
  "envMode": "strict"
}
jsonc title="./turbo.json"
{
  "futureFlags": {
    "turboExtendsKeyword": true
  }
}
jsonc title="./turbo.json"
{
  "futureFlags": {
    "nonRootExtends": true
  }
}
jsonc title="./apps/web/turbo.json"
{
  "extends": ["//", "ui"],
  "tasks": {
    "build": {}
  }
}
jsonc title="./apps/web/turbo.json"
{
  "tags": ["utils"]
}
jsonc title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "outputs": ["coverage/**"],
      "dependsOn": ["build"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
jsonc title="./packages/ui/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "lint": {
      "extends": false // Exclude this task from the package
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "test": {
      "dependsOn": ["lint", "build"]
    }
  }
}
json title="./turbo.json"
{
  "tasks": {
    "web#lint": {
      "dependsOn": ["utils#build"]
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "env": ["DATABASE_URL"] // Impacts hash of all build tasks
    },
    "web#build": {
      "env": ["API_SERVICE_KEY"] // Impacts hash of web's build task
    }
  }
}
json title="./turbo.json"
{
  "tasks": {
    "build": {
      "env": ["MY_API_*"]
    }
  }
}
json title="./turbo.json"
{
  "tasks": {
    "build": {
      "env": ["!MY_API_URL"]
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      // Values will be available within `build` scripts
      "passThroughEnv": ["AWS_SECRET_KEY", "GITHUB_TOKEN"]
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      // Cache all files emitted to the packages's `dist` directory
      "outputs": ["dist/**"]
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputs": [".svelte-kit/**", "dist/**"] // File outputs will be cached
    },
    "dev": {
      "cache": false, // No outputs will be cached
      "persistent": true
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "test": {
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "test/**/*.ts"]
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "check-types": {
      // Consider all default inputs except the package's README
      "inputs": ["$TURBO_DEFAULT$", "!README.md"]
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "check-types": {
      // Consider all Typescript files in `src/` and the root tsconfig.json as inputs
      "inputs": ["$TURBO_ROOT$/tsconfig.json", "src/**/*.ts"]
    }
  }
}
jsonc title="./turbo.json"
{
  "futureFlags": {
    "turboExtendsKeyword": true
  },
  "tasks": {
    "build": {
      "outputs": ["dist/**"]
    }
  }
}
jsonc title="./apps/web/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      // Inherits "dist/**" from root, and adds ".next/**"
      "outputs": ["$TURBO_EXTENDS$", ".next/**", "!.next/cache/**"]
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputLogs": "new-only"
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "dev": {
      "persistent": true
    }
  }
}
jsonc title="./turbo.json"
{
  "tasks": {
    "test:watch": {
      "interactive": true,
      "persistent": true
    }
  }
}
json title="./apps/web/turbo.json"
{
  "tasks": {
    "dev": {
      "with": ["api#dev"],
      "persistent": true,
      "cache": false
    }
  }
}
json title="./turbo.json"
{
  "boundaries": {}
}
jsonc title="./turbo.json"
{
  "boundaries": {
    "utils": {
      "dependencies": {
        // permit only packages with the `ui` tag
        "allow": ["ui"],
        // and ban packages with the `unsafe` tag
        "deny": ["unsafe"]
      }
    }
  }
}
jsonc title="./turbo.json"
{
  "boundaries": {
    "utils": {
      "dependencies": {
        // only packages with the `unsafe` tag are banned, all other packages permitted
        "deny": ["unsafe"]
      }
    }
  }
}
jsonc title="./turbo.json"
{
  "boundaries": {
    "utils": {
      "dependents": {
        // only packages with the `web` tag can import packages with the `utils` tag
        "allow": ["web"]
      }
    }
  }
}
jsonc title="./turbo.json"
{
  "remoteCache": {}
}
bash title="Terminal"
    pnpm dlx create-turbo@latest
    bash title="Terminal"
    yarn dlx create-turbo@latest
    bash title="Terminal"
    npx create-turbo@latest
    bash title="Terminal"
    bunx create-turbo@latest
    bash title="Terminal"
    pnpm dlx create-turbo@latest --example [example-name]
    bash title="Terminal"
    yarn dlx create-turbo@latest --example [example-name]
    bash title="Terminal"
    npx create-turbo@latest --example [example-name]
    bash title="Terminal"
    bunx create-turbo@latest --example [example-name]
    bash title="Terminal"
    pnpm dlx create-turbo@latest --example [github-url]
    bash title="Terminal"
    yarn dlx create-turbo@latest --example [github-url]
    bash title="Terminal"
    npx create-turbo@latest --example [github-url]
    bash title="Terminal"
    bunx create-turbo@latest --example [github-url]
    txt title="Terminal"
-m, --package-manager to use (choices: "npm", "yarn", "pnpm", "bun")

--skip-install: Do not run a package manager install after creating the project (Default: false)

--skip-transforms: Do not run any code transformation after creating the project (Default: false)

--turbo-version <version>: Use a specific version of turbo (default: latest)

-e, --example [name]|[github-url]: An example to bootstrap the app with. You can use an example name from the official Turborepo repo or a GitHub URL. The URL can use any branch and/or subdirectory

-p, --example-path <path-to-example>: In a rare case, your GitHub URL might contain a branch name with a slash (e.g. bug/fix-1) and the path to the example (e.g. foo/bar). In this case, you must specify the path to the example separately: --example-path foo/bar

-v, --version:  Output the current version

-h, --help: Display help for command
bash title="Terminal"
turbo devtools [options]
bash title="Terminal"
turbo devtools --port 3000
bash title="Terminal"
turbo devtools --no-open
bash title="Terminal"
    pnpm add eslint-config-turbo --filter=@repo/eslint-config
    bash title="Terminal"
    yarn workspace @acme/eslint-config add eslint-config-turbo --dev
    bash title="Terminal"
    npm install --save-dev eslint-config-turbo -w @acme/eslint-config
    bash title="Terminal"
    cd packages/eslint-config && bun install eslint-config-turbo --dev
    js title="./packages/eslint-config/base.js"
import turboConfig from 'eslint-config-turbo/flat';

export default [
  ...turboConfig,
  // Other configuration
];
js title="./packages/eslint-config/base.js"
import turboConfig from 'eslint-config-turbo/flat';

export default [
  ...turboConfig,
  // Other configuration
  {
    rules: {
      'turbo/no-undeclared-env-vars': [
        'error',
        {
          allowList: ['^ENV_[A-Z]+$'],
        },
      ],
    },
  },
];
json title="./packages/eslint-config/base.json"
{
  "extends": ["turbo"]
}
json title="./packages/eslint-config/base.json"
{
  "plugins": ["turbo"],
  "rules": {
    "turbo/no-undeclared-env-vars": [
      "error",
      {
        "allowList": ["^ENV_[A-Z]+$"]
      }
    ]
  }
}
bash title="Terminal"
    pnpm add eslint-plugin-turbo --filter=@repo/eslint-config
    bash title="Terminal"
    yarn workspace @acme/eslint-config add eslint-plugin-turbo --dev
    bash title="Terminal"
    npm i --save-dev eslint-plugin-turbo -w @acme/eslint-config
    bash title="Terminal"
    cd packages/eslint-config && bun install eslint-plugin-turbo --dev
    js title="./packages/eslint-config/base.js"
import turbo from 'eslint-plugin-turbo';

export default [turbo.configs['flat/recommended']];
js title="./packages/eslint-config/base.js"
import turbo from 'eslint-plugin-turbo';

export default [
  {
    plugins: {
      turbo,
    },
    rules: {
      'turbo/no-undeclared-env-vars': 'error',
    },
  },
];
js title="./packages/eslint-config/base.js"
import turbo from 'eslint-plugin-turbo';

export default [
  {
    plugins: {
      turbo,
    },
    rules: {
      'turbo/no-undeclared-env-vars': [
        'error',
        {
          allowList: ['^ENV_[A-Z]+$'],
        },
      ],
    },
  },
];
json title="./packages/eslint-config/base.json"
{
  "plugins": ["turbo"]
}
json title="./packages/eslint-config/base.json"
{
  "rules": {
    "turbo/no-undeclared-env-vars": "error"
  }
}
json title="./packages/eslint-config/base.json"
{
  "plugins": ["turbo"],
  "rules": {
    "turbo/no-undeclared-env-vars": [
      "error",
      {
        "allowList": ["^ENV_[A-Z]+$"]
      }
    ]
  }
}
bash title="Terminal"
turbo generate
bash title="Terminal"
turbo gen run [generator-name]
bash title="Terminal"
turbo gen workspace [options]
bash title="Terminal"
--opt=value
--opt="value with a space"
--opt value
--opt "value with a space"
bash title="Terminal"
turbo info
txt title="Terminal"
CLI:
   Version: 2.3.0
   Path to executable: /path/to/turbo
   Daemon status: Running
   Package manager: pnpm

Platform:
   Architecture: aarch64
   Operating system: macos
   Available memory (MB): 12810
   Available CPU cores: 10

Environment:
   CI: None
   Terminal (TERM): xterm-256color
   Terminal program (TERM_PROGRAM): tmux
   Terminal program version (TERM_PROGRAM_VERSION): 3.4
   Shell (SHELL): /bin/zsh
   stdin: false
bash title="Terminal"
turbo link
bash title="Terminal"
turbo link --api=https://example.com
bash title="Terminal"
turbo link --yes
bash title="Terminal"
turbo link --scope=your-team
bash title="Terminal"
turbo login
bash title="Terminal"
turbo login --api=https://acme.com/api
bash title="Terminal"
turbo login --login=https://acme.com
bash title="Terminal"
turbo login --sso-team=slug-for-team
bash title="Terminal"
turbo logout
bash title="Terminal"
turbo ls [package(s)] [flags]
bash title="Terminal"

**Examples:**

Example 1 (unknown):
```unknown
Linking your publishing flow into Turborepo can make organizing your deploy a lot simpler and faster.

Our recommendation is to configure Changesets to automatically commit `changeset version`'s changes
```

Example 2 (unknown):
```unknown
and add a `publish-packages` script into your root `package.json`:
```

Example 3 (unknown):
```unknown
If your packages are public, set Changeset's `access` to `public`:
```

Example 4 (unknown):
```unknown
<Callout>
  We recommend `publish-packages` so that it doesn't conflict with npm's
  built-in `publish` script.
</Callout>

This means that when you run `publish-packages`, your monorepo gets built, linted, tested and published - and you benefit from all of Turborepo's speedups.


- [Single-package workspaces](/guides/single-package-workspaces.md): Learn how to use Turborepo in a single-package workspace.

import { Callout } from '#components/callout';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

While Turborepo is highly effective in [multi-package workspaces](https://vercel.com/docs/vercel-platform/glossary#multi-package-workspace) (commonly referred to as monorepos), it can also be used to make [single-package workspaces](https://vercel.com/docs/vercel-platform/glossary#single-package-workspace) faster.

Turborepo's most important features work in single-package workspaces including local and [Remote Caching](/docs/core-concepts/remote-caching) and task parallelization. Features that don't work are ones that don't make sense in the context of a single package, like package tasks (`app#build`).

<Callout type="good-to-know">
  Examples of single-package workspaces are the output of `npx create-next-app`
  or `npm create vite`.
</Callout>

## Installation

Install `turbo` into your application:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
```

---

## Don't run production as root for security reasons

**URL:** llms-txt#don't-run-production-as-root-for-security-reasons

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

---

## First install the dependencies (as they change less often)

**URL:** llms-txt#first-install-the-dependencies-(as-they-change-less-often)

COPY --from=prepare /app/out/json/ .
RUN yarn install

---

## Set working directory

**URL:** llms-txt#set-working-directory

---

## Replace <your-major-version> with the major version installed in your repository. For example:

**URL:** llms-txt#replace-<your-major-version>-with-the-major-version-installed-in-your-repository.-for-example:

---

## - Or, in the 'packages' directory

**URL:** llms-txt#--or,-in-the-'packages'-directory

---

## Any packages in `apps` subdirectories that have changed since the last commit

**URL:** llms-txt#any-packages-in-`apps`-subdirectories-that-have-changed-since-the-last-commit

turbo run build --filter={.apps/*}[HEAD^1]

---

## Add a new changeset

**URL:** llms-txt#add-a-new-changeset

---

## Read from and write to local cache. No Remote Cache activity.

**URL:** llms-txt#read-from-and-write-to-local-cache.-no-remote-cache-activity.

turbo run build --cache=local:rw

---

## - It or any of its dependencies have changed since the previous commit

**URL:** llms-txt#--it-or-any-of-its-dependencies-have-changed-since-the-previous-commit

turbo run build --filter=@acme/ui...[HEAD^1]

---

## ARG TURBO_TOKEN

**URL:** llms-txt#arg-turbo_token

---

## Override Git comparison head

**URL:** llms-txt#override-git-comparison-head

**Contents:**
  - `--cache <options>`

TURBO_SCM_HEAD=your-branch turbo run build --affected
bash title="Terminal"

**Examples:**

Example 1 (unknown):
```unknown
### `--cache <options>`

Default: `local:rw,remote:rw`

Specify caching sources for the run. Accepts a comma-separated list of options:

* `local`: Use the local filesystem cache
* `remote`: Use the Remote Cache

When a caching source is omitted, reading and writing are both disabled.

Cache sources use the following values:

* `rw`: Read and write
* `r`: Read only
* `w`: Write only
* None (`local:`) : Does not use cache. Equivalent to omitting the cache source option.
```

---

## ---

**URL:** llms-txt#---

---

## - In the '@acme' scope

**URL:** llms-txt#--in-the-'@acme'-scope

---

## Automatically leverage output traces to reduce image size

**URL:** llms-txt#automatically-leverage-output-traces-to-reduce-image-size

---
