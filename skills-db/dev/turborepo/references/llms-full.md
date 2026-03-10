- [Introduction](/index.md): Welcome to the Turborepo documentation!

Welcome to the Turborepo documentation!

***

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

## Package managers

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

## Platforms

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

## Node.js

Core `turbo` functionality does not depend on the
active Node.js version on your system, but [some packages in the Turborepo ecosystem](/docs/reference#packages)
such as [`create-turbo`](/docs/reference/create-turbo), [`turbo-ignore`](/docs/reference/turbo-ignore), and [`eslint-config-turbo`](/docs/reference/eslint-config-turbo) do. For these features,
we intend to support the [Active and Maintenance LTS versions of Node.js](https://nodejs.org/en/about/previous-releases).

Turborepo's [examples](/docs/getting-started/examples) are also expected to work with these Node.js versions.

## Version control

We support repositories that are version controlled with Git and repositories that don't have
version control at all. Any other version control system will be ignored.

Note that we use Git to hash files, so repositories without git may perform and behave differently.

## LTS policy

Major versions of Turborepo will be supported for two years from the release date of the next major version.

Changes required for critical security fixes in older versions will be backported. Such situations will be rare and will land as semver-minor releases, even if they are breaking changes.

We highly encourage you to use the most current version of Turborepo whenever possible.

| Major version | Release date | End-of-life date |
| ------------- | ------------ | ---------------- |
| 2.x           | Jun. 4, 2024 | -                |
| 1.x           | Dec. 9, 2021 | Jun. 4, 2026     |

## Release phases

Stable builds of Turborepo follow semantic versioning (semver) and are thoroughly tested before being released.

Turborepo also offers specific APIs that may be released in an earlier phase of development. This is to allow early adopters to give valuable feedback and help the core team gain confidence in APIs ahead of their stable release. APIs that are available pre-stable will be marked as such in the documentation and within `turbo` itself whenever possible.

Not every API will be released in every phase. We use our best judgment to determine the phase for an API based on our confidence for the feature, weighing factors like the feature's complexity, possible use cases, and feedback from early users of the API.

The Turborepo core team would like to thank any users who do use features early and express our appreciation for any feedback you provide.

### Stable

When an API reaches stability, it is considered ready for use in production. APIs marked as stable will only change in a backward-compatible way in a major release.

* If a stable API is going to **have breaking changes** in an upcoming major release, warnings and documentation will be provided to help with migrations and next steps.
* If a stable API is going to be **removed** in an upcoming major release, it will be marked as [Deprecated](#deprecated) to provide early notice of future removal.

### Beta

Beta APIs require more confidence around reliability before a stable release. In the Beta phase, we are confident about the overall design of the feature and expect to be able to promote the feature to stable with relatively few changes. In rare cases, an API may require a breaking change and will not be covered by semver.

We encourage early adopters to use Beta APIs to help us gain certainty around the feature's design and stability. Depending on your risk tolerance, you can use the feature in production as you see fit.

**APIs currently in the Beta phase:**

* None

### Experimental

Experimental APIs lack essential capabilities required to be ready for stability. The design of the feature is considered to be under active development and can change at any time.

We encourage you to help us test experimental APIs in side projects, proof-of-concepts, and other environments where stability is non-essential. This gives you the opportunity to aid in the API's development by providing early feedback to the core team as the feature develops. We do not recommend using experimental APIs where reliability is essential.

**APIs currently in the Experimental phase:**

* [`turbo query`](/docs/reference/query)
* [`turbo boundaries`](/docs/reference/boundaries) and [Tags](/docs/reference/boundaries#tags)
* [`--experimental-write-cache` for `turbo watch`](/docs/reference/watch#caching)
* [`--output=json` for `turbo ls --affected` flag](/docs/reference/ls)

### Deprecated

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
    ```json title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/ui": "workspace:*" // [!code highlight]
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```json title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/ui": "*" // [!code highlight]
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```json title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/ui": "*" // [!code highlight]
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```json title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/ui": "workspace:*" // [!code highlight]
      }
    }
    ```
  </Tab>
</Tabs>

In the [Creating an Internal Package guide](/docs/crafting-your-repository/creating-an-internal-package), you can build an Internal Package from the beginning using [the Compiled Package strategy](#compiled-packages). On this page, we'll describe other strategies for creating Internal Packages and their tradeoffs, including [publishing the package to the npm registry](#publishable-packages) to create an External Package.

You can then import the package into your code like you're used to doing with an external package:

```tsx title="./apps/web/app/page.tsx"
import { Button } from '@repo/ui'; // [!code highlight]

export default function Page() {
  return <Button>Submit</Button>;
}
```

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

```json title="./packages/ui/package.json"
{
  "name": "@repo/ui",
  "exports": {
    "./button": "./src/button.tsx", // [!code highlight]
    "./card": "./src/card.tsx" // [!code highlight]
  },
  "scripts": {
    "lint": "eslint . --max-warnings 0", // [!code highlight]
    "check-types": "tsc --noEmit" // [!code highlight]
  }
}
```

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

```json title="./packages/ui/package.json"
{
  "name": "@repo/ui",
  "exports": {
    "./button": {
      "types": "./src/button.tsx", // [!code highlight]
      "default": "./dist/button.js" // [!code highlight]
    },
    "./card": {
      "types": "./src/card.tsx", // [!code highlight]
      "default": "./dist/card.js" // [!code highlight]
    }
  },
  "scripts": {
    "build": "tsc" // [!code highlight]
  }
}
```

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

## Package Graph

The Package Graph is the structure of your monorepo created by your package manager. When you install [Internal Packages](/docs/core-concepts/internal-packages) into each other, Turborepo will automatically identify those dependency relationships to build a foundational understanding of your Workspace.

This sets the groundwork for the Task Graph, where you'll define how **tasks** relate to each other.

## Task Graph

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

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

Turborepo will build a task graph like this:

![Task graph visualization. The diagram has one node at the top named "apps/web" with two lines that connect to other nodes, "packages/ui" and "packages/utils" respectively.](/images/docs/simple-task-graph.png)

### Transit Nodes

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

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^test"]
    }
  }
}
```

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

## Library Packages

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

## Vercel

[Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching) is free to use on all plans, even if you do not host your applications on Vercel. Follow the steps below to enable Remote Caching for your repository.

### For Local Development

To link your local Turborepo to your Remote Cache, authenticate the Turborepo CLI with your Vercel account:

```bash title="Terminal"
turbo login
```

You can also use your package manager if you do not have [global `turbo`](/docs/getting-started/installation#global-installation) installed:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx turbo login
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx turbo login
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx turbo login
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx turbo login
    ```
  </Tab>
</Tabs>

<Callout>
  If your Remote Cache is configured to use single-sign-on you will need to run
  `npx turbo login --sso-team=team-name` in order to get a cache token with the
  correct privileges.
</Callout>

Now, link your Turborepo to your Remote Cache:

```bash title="Terminal"
turbo link
```

Once enabled, make some changes to a package you are currently caching and run tasks against it with `turbo run`.
Your cache artifacts will now be stored locally *and* in your Remote Cache.

To verify, delete your local Turborepo cache with:

<Tabs groupId="platform-tabs" items={['UNIX', 'Windows']} persist>
  <Tab value="UNIX">
    ```bash title="Terminal"
    rm -rf ./.turbo/cache
    ```
  </Tab>

  <Tab value="Windows">
    ```bash title="Terminal"
    rd /s /q "./.turbo/cache"
    ```
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

```jsonc title="./turbo.json"
{
  "remoteCache": {
    "signature": true // [!code highlight]
  }
}
```

## Remote Cache API

A Remote Cache can be implemented by any HTTP server that meets Turborepo's Remote Caching API specification.

### Managed Remote Cache with Vercel

[Vercel](https://vercel.com), the creators and maintainers of Turborepo, provide a managed Remote Cache that is fully compatible with Turborepo.

Using [Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching) is zero-configuration and automatically integrates with [Vercel deployments](https://vercel.com/docs/deployments/overview) through the open-source [Vercel Remote Cache SDK](https://github.com/vercel/remote-cache).

Learn more about [Turborepo on Vercel](https://vercel.com/docs/monorepos/turborepo) or [deploy a template for free](https://vercel.com/templates?search=turborepo) to try it out.

### Self-hosting

You can also self-host your own Remote Cache and log into it using the `--manual` flag to provide API URL, team, and token information.

```bash title="Terminal"
turbo login --manual
```

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

        ```bash title="Terminal"
        # Global install
        pnpm add turbo --global
        # Install in repository
        pnpm add turbo --save-dev --workspace-root
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        # Global install
        yarn global add turbo
        # Install in repository
        yarn add turbo --dev
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        # Global install
        npm install turbo --global
        # Install in repository
        npm install turbo --save-dev
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        # Global install
        bun install turbo --global
        # Install in repository
        bun install turbo --dev
        ```
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
        ```json title="./turbo.json"
        {
          "$schema": "https://turborepo.com/schema.json",
          "tasks": {
            "build": {
              "dependsOn": ["^build"],
              "outputs": [".next/**", "!.next/cache/**"]
            },
            "check-types": {
              "dependsOn": ["^check-types"]
            },
            "dev": {
              "persistent": true,
              "cache": false
            }
          }
        }
        ```

        For more information on configuring your `turbo.json`, see the [Configuration Options](/docs/reference/configuration) documentation.

        In your Next.js application, make sure you have a `check-types` script for `turbo` to run.

        ```diff title="apps/web/package.json"
        {
          "scripts": {
        +   "check-types": "tsc --noEmit"
          }
        }
        ```
      </Tab>

      <Tab value="Vite">
        ```json title="./turbo.json"
        {
          "$schema": "https://turborepo.com/schema.json",
          "tasks": {
            "build": {
              "outputs": ["dist/**"]
            },
            "check-types": {
              "dependsOn": ["^check-types"]
            },
            "dev": {
              "persistent": true,
              "cache": false
            }
          }
        }
        ```

        Some Vite starters ship with a `package.json` that looks like this:

        ```json title="package.json"
        {
          "scripts": {
            "build": "tsc && vite build"
          }
        }
        ```

        We recommend splitting these into a `check-types` and `build` script so that `turbo` can run them in parallel.

        ```json title="apps/web/package.json"
        {
          "scripts": {
            "build": "vite build",
            "check-types": "tsc --noEmit"
          }
        }
        ```
      </Tab>
    </Tabs>

    In a multi-package workspace, you may also want to add a `check-types` script
    to one or more of your library packages to see how multiple scripts across
    different packages run with one `turbo` command.
  </Step>

  <Step>
    ### Edit `.gitignore`

    Add `.turbo` to your `.gitignore` file. The `turbo` CLI uses these folders for persisting logs, outputs, and other functionality.

    ```diff title=".gitignore"
    + .turbo
    ```
  </Step>

  <Step>
    ### Add a `packageManager` field to root `package.json`

    Turborepo optimizes your repository using information from your package manager. To declare which package manager you're using, add a [`packageManager`](https://nodejs.org/api/packages.html#packagemanager) field to your root `package.json` if you don't have one already.

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```diff title="package.json"
        {
        +  "packageManager": "pnpm@10.0.0"
        }
        ```
      </Tab>

      <Tab value="yarn">
        ```diff title="package.json"
        {
        +  "packageManager": "yarn@1.22.19"
        }
        ```
      </Tab>

      <Tab value="npm">
        ```diff title="package.json"
        {
        +  "packageManager": "npm@8.5.0"
        }
        ```
      </Tab>

      <Tab value="bun">
        ```diff title="package.json"
        {
        +  "packageManager": "bun@1.2.0"
        }
        ```
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
        ```json title="pnpm-workspace.yaml"
        packages:
          - "apps/*"
          - "packages/*"
        ```

        <LinkToDocumentation href="https://pnpm.io/pnpm-workspace_yaml">pnpm workspace documentation</LinkToDocumentation>
      </Tab>

      <Tab value="yarn">
        ```json title="./package.json"
        {
          "workspaces": [
            "apps/*",
            "packages/*"
          ]
        }
        ```

        <LinkToDocumentation href="https://yarnpkg.com/features/workspaces#how-are-workspaces-declared">yarn workspace documentation</LinkToDocumentation>
      </Tab>

      <Tab value="npm">
        ```json title="./package.json"
        {
          "workspaces": [
            "apps/*",
            "packages/*"
          ]
        }
        ```

        <LinkToDocumentation href="https://docs.npmjs.com/cli/v7/using-npm/workspaces#defining-workspaces">npm workspace documentation</LinkToDocumentation>
      </Tab>

      <Tab value="bun">
        ```json title="./package.json"
        {
          "workspaces": [
            "apps/*",
            "packages/*"
          ]
        }
        ```

        <LinkToDocumentation href="https://bun.sh/docs/install/workspaces">bun workspace documentation</LinkToDocumentation>
      </Tab>
    </Tabs>

    For more details on how to structure your repository, see [Structuring a Repository](/docs/crafting-your-repository/structuring-a-repository#declaring-directories-for-packages).
  </Step>

  <Step>
    ### Run tasks with `turbo`

    You can now run the tasks you added to `turbo.json` earlier using Turborepo. Using the example tasks from above:

    ```bash title="Terminal"
    turbo build check-types
    ```

    This runs the `build` and `check-types` tasks at the same time. The dependency graph of your [Workspace](/docs/crafting-your-repository/structuring-a-repository#anatomy-of-a-workspace) will be used to run tasks in the right order.
  </Step>

  <Step>
    **Without making any changes to the code, try running `build` and `check-types` again:**

    ```bash title="Terminal"
    turbo check-types build
    ```

    You should see terminal output like this:

    ```bash title="Terminal"
    Tasks:    2 successful, 2 total
    Cached:    2 cached, 2 total
    Time:    185ms >>> FULL TURBO
    ```

    Congratulations! **You just built and type checked your code in milliseconds**.

    To learn more about how `turbo` makes this possible, check out [the caching documentation](/docs/crafting-your-repository/caching).
  </Step>

  <Step>
    ### Begin developing by running `dev` with `turbo`

    In a multi-package workspace, you can run `turbo dev` to start the development tasks for all your packages at once.

    ```bash title="Terminal"
    turbo dev
    ```

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

```json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json"
}
```

There is also a major versioned `schema.json` available, following the format of `https://turborepo.com/schema.<version>.json`.

```json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.v1.json"
}
```

### Sourcing from `node_modules`

Starting in Turborepo 2.4, `schema.json` is available in `node_modules` once you've run your package manager's install command:

```json title="turbo.json"
{
  "$schema": "./node_modules/turbo/schema.json"
}
```

<Callout title="node_modules location">
  We recommend installing `turbo` at the root of your repository, so the path
  for the schema should point to `node_modules` at the root of your repository.
  In [Package Configurations](/docs/reference/package-configurations), you may
  need to use a path like `../../node_modules/turbo/schema.json`.
</Callout>

## Linting for environment variables

Handling environment variables is an important part of building applications in a Turborepo.

[The `eslint-config-turbo` package](/docs/reference/eslint-config-turbo) extends your ESLint setup to help you make sure you've taken care of all of your environment variables.

## Turborepo LSP

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
    ```bash title="Terminal"
    # Use an example listed below
    pnpm dlx create-turbo@latest --example [example-name]

    # Use a GitHub repository from the community
    pnpm dlx create-turbo@latest --example [github-url]
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    # Use an example listed below
    yarn dlx create-turbo@latest --example [example-name]

    # Use a GitHub repository from the community
    yarn dlx create-turbo@latest --example [github-url]
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    # Use an example listed below
    npx create-turbo@latest --example [example-name]

    # Use a GitHub repository from the community
    npx create-turbo@latest --example [github-url]
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    # Use an example listed below
    bunx create-turbo@latest --example [example-name]

    # Use a GitHub repository from the community
    bunx create-turbo@latest --example [github-url]
    ```
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

<ExamplesTable />


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
        ```bash title="Terminal"
        npm install turbo --global
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn global add turbo
        ```
      </Tab>

      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm add turbo --global
        ```
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
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest
    ```
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
    ```bash title="Terminal"
    pnpm add turbo --global
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn global add turbo
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install turbo --global
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bun install turbo --global
    ```
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
    ```bash title="Terminal"
    pnpm add turbo --save-dev --ignore-workspace-root-check
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn add turbo --dev --ignore-workspace-root-check
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install turbo --save-dev
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bun install turbo --dev
    ```
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

    ```bash title="Terminal"
    npx create-turbo@latest
    ```
  </Step>

  <Step>
    ### Run a build for the first time

    If you have [`turbo` installed globally](/docs/getting-started/installation#global-installation), run `turbo build` in your repository.

    Alternatively, you can run the `build` script in `package.json` using your package manager.

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm run build
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn build
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        npm run build
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        bun run build
        ```
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

## Remote Caching

Turborepo stores the results of tasks in the `.turbo/cache` directory on your machine. However, you can make your entire organization even faster by sharing this cache with your teammates and CI.

To learn more about Remote Caching and its benefits, visit the [Remote Caching page](/docs/core-concepts/remote-caching).

### Enabling Remote Cache

First, authenticate with your Remote Cache provider:

```bash title="Terminal"
npx turbo login
```

Then, link the repository on your machine to Remote Cache:

```bash title="Terminal"
npx turbo link
```

Now, when you run a task, Turborepo will automatically send the outputs of the task to Remote Cache. If you run the same task on a different machine that is also authenticated to your Remote Cache, it will hit cache the first time it runs the task.

For information on how to connect your CI machines to Remote Cache, visit [the Constructing CI guide](/docs/crafting-your-repository/constructing-ci#enabling-remote-caching).

<Callout type="info">
  By default, Turborepo uses [Vercel Remote
  Cache](https://vercel.com/docs/monorepos/remote-caching) with zero
  configuration. If you'd like to use a different Remote Cache, visit the
  [Remote Caching API
  documentation](/docs/core-concepts/remote-caching#self-hosting)
</Callout>

## What gets cached?

Turborepo caches two types of outputs: Task outputs and Logs.

### Task outputs

Turborepo caches the file outputs of a task that are defined in [the `outputs` key](/docs/reference/configuration#outputs) of `turbo.json`. When there's a cache hit, Turborepo will restore the files from the cache.

The `outputs` key is optional, see [the API reference](/docs/reference/configuration#outputs) for how Turborepo behaves in this case.

<Callout type="warn" title="Providing file outputs">
  If you do not declare file outputs for a task, Turborepo will not cache them. This might be okay for some tasks (like linters) - but many tasks produce files that you will want to be cached.

  If you're running into errors with files not being available when you hit cache, make sure that you have defined the outputs for your task.
</Callout>

### Logs

Turborepo always captures the terminal outputs of your tasks, restoring those logs to your terminal from the first time that the task ran.

You can configure the verbosity of the replayed logs using [the `--output-logs` flag](/docs/reference/run#--output-logs-option) or [`outputLogs` configuration option](/docs/reference/configuration#outputlogs).

## Task inputs

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

## Troubleshooting

### Using dry runs

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

## Next steps

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

## Getting started

The root `turbo.json` file is where you'll register the tasks that Turborepo will run. Once you have your tasks defined, you'll be able to run one or more tasks using [`turbo run`](/docs/reference/run).

* If you're starting fresh, we recommend [creating a new repository using `create-turbo`](/docs/getting-started/installation) and editing the `turbo.json` file to try out the snippets in this guide.
* If you're adopting Turborepo in an existing repository, create a `turbo.json` file in the root of your repository. You'll be using it to learn about the rest of the configuration options in this guide.

<Files>
  <File name="turbo.json" green />

  <File name="package.json" />

  <Folder name="apps" />

  <Folder name="packages" />
</Files>

## Defining tasks

Each key in the `tasks` object is a task that can be executed by `turbo run`. Turborepo will search your packages for **scripts in their `package.json` that have the same name as the task**.

To define a task, use [the `tasks` object](/docs/reference/configuration#tasks) in `turbo.json`. For example, a basic task with no dependencies and no outputs named `build` might look like this:

```json title="./turbo.json"
{
  "tasks": {
    "build": {} // Incorrect! // [!code highlight]
  }
}
```

If you run `turbo run build` at this point, Turborepo will run all `build` scripts in your packages in parallel and won't cache any file outputs. **This will quickly lead to errors.** You're missing a few important pieces to make this work how you'd expect.

### Running tasks in the right order

[The `dependsOn` key](/docs/reference/configuration#dependson) is used to specify the tasks that must complete before a different task begins running. For example, in most cases, you want the `build` script for your libraries to complete before your application's `build` script runs. To do this, you'd use the following `turbo.json`:

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"] // [!code highlight]
    }
  }
}
```

You now have the build order you would expect, building *dependencies* before *dependents*.

**But be careful.** At this point, you haven't marked the build outputs for caching. To do so, jump to the [Specifying outputs](#specifying-outputs) section.

#### Depending on tasks in dependencies with `^`

The `^` microsyntax tells Turborepo to run the task in direct dependencies before the target package. If your application depends on a library named `ui` and the library has a `build` task, the `build` script in `ui` will run **first**. Once it has successfully completed, the `build` task in your application will run.

This is an important pattern as it ensures that your application's `build` task will have all of the necessary dependencies that it needs to compile. This concept also applies as your dependency graph grows to a more complex structure with many levels of task dependencies.

#### Depending on tasks in the same package

Sometimes, you may need to ensure that two tasks in the same package run in a specific order. For example, you may need to run a `build` task in your library before running a `test` task in the same library. To do this, specify the script in the `dependsOn` key as a plain string (without the `^`).

```json title="./turbo.json"
{
  "tasks": {
    "test": {
      "dependsOn": ["build"] // [!code highlight]
    }
  }
}
```

#### Depending on a specific task in a specific package

You can also specify an individual task in a specific package to depend on. In the example below, the `build` task in `utils` must be run before any `lint` tasks.

```json title="./turbo.json"
{
  "tasks": {
    "lint": {
      "dependsOn": ["utils#build"] // [!code highlight]
    }
  }
}
```

You can also be more specific about the dependent task, limiting it to a certain package:

```json title="./turbo.json"
{
  "tasks": {
    "web#lint": {
      "dependsOn": ["utils#build"] // [!code highlight]
    }
  }
}
```

With this configuration, the `lint` task in your `web` package can only be run after the `build` task in the `utils` package is complete.

#### No dependencies

Some tasks may not have any dependencies. For example, a task for finding typos in Markdown files likely doesn't need to care about the status of your other tasks. In this case, you can omit the `dependsOn` key or provide an empty array.

```json title="./turbo.json"
{
  "tasks": {
    "spell-check": {
      "dependsOn": [] // [!code highlight]
    }
  }
}
```

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
    ```json title="./turbo.json"
    {
      "tasks": {
        "build": {
          "outputs": [".next/**", "!.next/cache/**"] // [!code highlight]
        }
      }
    }
    ```
  </Tab>

  <Tab value="Vite">
    ```json title="./turbo.json"
    {
      "tasks": {
        "build": {
          "outputs": ["dist/**"] // [!code highlight]
        }
      }
    }
    ```
  </Tab>

  <Tab value="tsc">
    ```json title="./turbo.json"
    {
      "tasks": {
        "build": {
          "outputs": ["dist/**"] // [!code highlight]
        }
      }
    }
    ```
  </Tab>
</Tabs>

Globs are relative to the package, so `dist/**` will handle the `dist` that is outputted for each package, respectively. For more on building globbing patterns for the `outputs` key, see [the globbing specification](/docs/reference/globs).

### Specifying `inputs`

The `inputs` key is used to specify the files that you want to include in the task's hash for [caching](/docs/crafting-your-repository/caching). By default, Turborepo will include all files in the package that are tracked by Git. However, you can be more specific about which files are included in the hash using the `inputs` key.

As an example, a task for finding typos in Markdown files could be defined like this:

```json title="./turbo.json"
{
  "tasks": {
    "spell-check": {
      "inputs": ["**/*.md", "**/*.mdx"] // [!code highlight]
    }
  }
}
```

Now, **only** changes in Markdown files will cause the `spell-check` task to miss cache.

<Callout type="error">
  This feature opts out of all of Turborepo's default `inputs` behavior, including following along with changes tracked by source control. This means that your `.gitignore` file will no longer be respected, and you will need to ensure that you do not capture those files with your globs.

  To restore the default behavior, use [the `$TURBO_DEFAULT$` microsyntax](#restoring-defaults-with-turbo_default).
</Callout>

#### Restoring defaults with `$TURBO_DEFAULT$`

[The default `inputs` behavior](/docs/reference/configuration#inputs) is often what you will want for your tasks. However, you can increase your cache hit ratios for certain tasks by fine-tuning your `inputs` to ignore changes to files that are known to not affect the task's output.

For this reason, you can use the `$TURBO_DEFAULT$` microsyntax to fine-tune the default `inputs` behavior:

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$", "!README.md"] // [!code highlight]
    }
  }
}
```

In this task definition, Turborepo will use the default `inputs` behavior for the `build` task, but will ignore changes to the `README.md` file. If the `README.md` file is changed, the task will still hit cache.

### Registering Root Tasks

You can also run scripts in the `package.json` in the Workspace root using `turbo`. For example, you may want to run a `lint:root` task for the files in your Workspace's root directory in addition to the `lint` task in each package:

<Tabs items={["turbo.json", "package.json"]}>
  <Tab value="turbo.json">
    ```json title="./turbo.json"
    {
      "tasks": {
        "lint": {
          "dependsOn": ["^lint"]
        },
        "//#lint:root": {} // [!code highlight]
      }
    }
    ```
  </Tab>

  <Tab value="package.json">
    ```json title="./package.json"
    {
      "scripts": {
        "lint": "turbo run lint lint:root",
        "lint:root": "eslint ." // [!code highlight]
      }
    }
    ```
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

```json title="./apps/web/turbo.json"
{
  "tasks": {
    "dev": {
      "with": ["api#dev"],
      "persistent": true,
      "cache": false
    }
  }
}
```

A long-running task never exits, meaning you can't depend on it. Instead, the `with` keyword will run the `api#dev` task whenever the `web#dev` task runs.

### Performing side-effects

Some tasks should always be run no matter what, like a deployment script after a cached build. For these tasks, add `"cache": false` to your task definition.

```json title="./turbo.json"
{
  "tasks": {
    "deploy": {
      "dependsOn": ["^build"],
      "cache": false // [!code highlight]
    },
    "build": {
      "outputs": ["dist/**"]
    }
  }
}
```

### Dependent tasks that can be run in parallel

Some tasks can be run in parallel despite being dependent on other packages. An example of tasks that fit this description are type checkers, since a type checker doesn't need to wait for outputs in dependencies to run successfully.

Because of this, you may be tempted to define your `check-types` task like this:

```json title="./turbo.json"
{
  "tasks": {
    "check-types": {} // Incorrect! // [!code highlight]
  }
}
```

This runs your tasks in parallel - but doesn't account for source code changes in dependencies. This means you can:

1. Make a breaking change to the interface of your `ui` package.
2. Run `turbo check-types`, hitting cache in an application package that depends on `ui`.

This is incorrect, since the application package will show a successful cache hit, despite not being updated to use the new interface. Checking for TypeScript errors in your application package manually in your editor is likely to reveal errors.

Because of this, you make a small change to your `check-types` task definition:

```json title="./turbo.json"
{
  "tasks": {
    "check-types": {
      "dependsOn": ["^check-types"] // This works...but could be faster! // [!code highlight]
    }
  }
}
```

If you test out making breaking changes in your `ui` package again, you'll notice that the caching behavior is now correct. However, tasks are no longer running in parallel.

To meet both requirements (correctness and parallelism), you can introduce [Transit Nodes](/docs/core-concepts/package-and-task-graph#transit-nodes) to your Task Graph:

```json title="./turbo.json"
{
  "tasks": {
    "transit": {
      "dependsOn": ["^transit"]
    },
    "check-types": {
      "dependsOn": ["transit"]
    }
  }
}
```

These Transit Nodes create a relationship between your package dependencies using a task that doesn't do anything because it doesn't match a script in any `package.json`s. Because of this, your tasks can run in parallel **and** be aware of changes to their internal dependencies.

<Callout type="info">
  In this example, we used the name `transit` - but you can name the task
  anything that isn't already a script in your Workspace.
</Callout>

## Next steps

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

## Docker

Docker is an important part of many deployment pipelines. [Turborepo's `prune` subcommand](/docs/reference/prune) helps you ship lightweight images by removing unnecessary dependencies and code from your images.

For more on how to deploy from a Turborepo with Docker, visit [the dedicated Docker guide](/docs/guides/tools/docker).

## Skipping tasks and other unnecessary work

### Running only affected tasks

You can use the `--affected` flag to only run tasks that have changes.

```bash title="Terminal"
turbo run build --affected
```

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

        ```bash title="Terminal"
        npx turbo-ignore web
        ```
      </Tab>

      <Tab value="web#build (Inferred)">
        Check for changes for the `build` task for the `web` package and its dependencies using [Automatic Package Scoping](/docs/crafting-your-repository/running-tasks#automatic-package-scoping):

        ```bash title="Terminal"
        cd apps/web
        npx turbo-ignore
        ```
      </Tab>

      <Tab value="docs#test (--task flag)">
        Check for changes for the `test` task for the `docs` package and its dependencies using [Automatic Package Scoping](/docs/crafting-your-repository/running-tasks#automatic-package-scoping) and the `--task` flag:

        ```bash title="Terminal"
        cd apps/docs
        npx turbo-ignore --task=test
        ```
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

## Best practices

### Rely on caching

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

## Troubleshooting

### Hitting cache results in broken builds

If your task is **passing when you miss cache but failing when you hit cache**, you likely haven't configured [the `outputs` key](/docs/reference/configuration#outputs) for your task correctly.

### Deployment using the wrong environment variables

If you haven't defined the `env` or `globalEnv` keys for your task, Turborepo will not be able to use them when creating hashes. This means your task can hit cache despite being in a different environment.

Check your configuration for the `env` and `globalEnv` keys.

## Next steps

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
        ```json title="./packages/math/package.json"
        {
          "name": "@repo/math",
          "type": "module",
          "scripts": {
            "dev": "tsc --watch",
            "build": "tsc"
          },
          "exports": {
            "./add": {
              "types": "./src/add.ts",
              "default": "./dist/add.js"
            },
            "./subtract": {
              "types": "./src/subtract.ts",
              "default": "./dist/subtract.js"
            }
          },
          "devDependencies": {
            "@repo/typescript-config": "workspace:*",
            "typescript": "latest"
          }
        }
        ```
      </Tab>

      <Tab value="yarn">
        ```json title="./packages/math/package.json"
        {
          "name": "@repo/math",
          "type": "module",
          "scripts": {
            "dev": "tsc --watch",
            "build": "tsc"
          },
          "exports": {
            "./add": {
              "types": "./src/add.ts",
              "default": "./dist/add.js"
            },
            "./subtract": {
              "types": "./src/subtract.ts",
              "default": "./dist/subtract.js"
            }
          },
          "devDependencies": {
            "@repo/typescript-config": "workspace:*",
            "typescript": "latest"
          }
        }
        ```
      </Tab>

      <Tab value="npm">
        ```json title="./packages/math/package.json"
        {
          "name": "@repo/math",
          "type": "module",
          "scripts": {
            "dev": "tsc --watch",
            "build": "tsc"
          },
          "exports": {
            "./add": {
              "types": "./src/add.ts",
              "default": "./dist/add.js"
            },
            "./subtract": {
              "types": "./src/subtract.ts",
              "default": "./dist/subtract.js"
            }
          },
          "devDependencies": {
            "@repo/typescript-config": "*",
            "typescript": "latest"
          }
        }
        ```
      </Tab>

      <Tab value="bun">
        ```json title="./packages/math/package.json"
        {
          "name": "@repo/math",
          "type": "module",
          "scripts": {
            "dev": "tsc --watch",
            "build": "tsc"
          },
          "exports": {
            "./add": {
              "types": "./src/add.ts",
              "default": "./dist/add.js"
            },
            "./subtract": {
              "types": "./src/subtract.ts",
              "default": "./dist/subtract.js"
            }
          },
          "devDependencies": {
            "@repo/typescript-config": "workspace:*",
            "typescript": "latest"
          }
        }
        ```
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

    ```json title="./packages/math/tsconfig.json"
    {
      "extends": "@repo/typescript-config/base.json",
      "compilerOptions": {
        "outDir": "dist",
        "rootDir": "src"
      },
      "include": ["src"],
      "exclude": ["node_modules", "dist"]
    }
    ```

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
        ```ts title="./packages/math/src/add.ts"
        export const add = (a: number, b: number) => a + b;
        ```
      </Tab>

      <Tab value="subtract.ts">
        ```ts title="./packages/math/src/subtract.ts"
        export const subtract = (a: number, b: number) => a - b;
        ```
      </Tab>
    </Tabs>

    These files map to the outputs that will be created by `tsc` when you run `turbo build` in a moment.
  </Step>

  <Step>
    ### Add the package to an application

    You're ready to use your new package in an application. Let's add it to the `web` application.

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```diff title="apps/web/package.json"
          "dependencies": {
        +   "@repo/math": "workspace:*",
            "next": "latest",
            "react": "latest",
            "react-dom": "latest"
          },
        ```
      </Tab>

      <Tab value="yarn">
        ```diff title="apps/web/package.json"
          "dependencies": {
        +   "@repo/math": "*",
            "next": "latest",
            "react": "latest",
            "react-dom": "latest"
          },
        ```
      </Tab>

      <Tab value="npm">
        ```diff title="apps/web/package.json"
          "dependencies": {
        +   "@repo/math": "*",
            "next": "latest",
            "react": "latest",
            "react-dom": "latest"
          },
        ```
      </Tab>

      <Tab value="bun">
        ```diff title="apps/web/package.json"
          "dependencies": {
        +   "@repo/math": "workspace:*",
            "next": "latest",
            "react": "latest",
            "react-dom": "latest"
          },
        ```
      </Tab>
    </Tabs>

    <Callout type="warn">
      You just changed the dependencies in your repo. Make sure to run your package
      manager's installation command to update your lockfile.
    </Callout>

    `@repo/math` is now available in the `web` application, you can use it in your code:

    ```tsx title="apps/web/src/app/page.tsx"
    import { add } from '@repo/math/add';

    function Page() {
      return <div>{add(1, 2)}</div>;
    }

    export default Page;
    ```
  </Step>

  <Step>
    ### Edit `turbo.json`

    Add the artifacts for the new `@repo/math` library to the `outputs` for the `build` task in `turbo.json`. This ensures that its build outputs will be cached by Turborepo, so they can be restored instantly when you start running builds.

    ```json title="./turbo.json"
    // [!code word:"dist/**"]
    {
      "tasks": {
        "build": {
          "dependsOn": ["^build"],
          "outputs": [".next/**", "!.next/cache/**", "dist/**"]
        }
      }
    }
    ```
  </Step>

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

## Next steps

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

```json title="./turbo.json"
{
  "tasks": {
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

* **"cache": false**: Tells Turborepo to not attempt to cache the results of the task. Since this is a development task, you're likely to be making frequent changes to your code, so caching the results is not useful.
* **"persistent": true**: Tells Turborepo to keep the task running until you stop it. This key serves as a signal for your terminal UI to treat the task as long-running and interactive. Additionally, it prevents you from accidentally depending on a task that will not exit.

You can now run your `dev` task to start your development scripts in parallel:

```bash title="Terminal"
turbo dev
```

### Running setup tasks before `dev`

You may also want to run scripts that set up your development environment or pre-build packages. You can make sure those tasks run before the `dev` task with `dependsOn`:

```json title="./turbo.json"
{
  "tasks": {
    "dev": {
      "cache": false,
      "persistent": true,
      "dependsOn": ["//#dev:setup"]
    },
    "//#dev:setup": {
      "outputs": [".codegen/**"]
    }
  }
}
```

In this example, we're using a [Root Task](/docs/crafting-your-repository/configuring-tasks#registering-root-tasks) but you can use the same idea for [arbitrary tasks in packages](/docs/crafting-your-repository/configuring-tasks#depending-on-a-specific-task-in-a-specific-package).

### Running a specific application

The `--filter` flag allows you to pick a subset of your [Package Graph](/docs/core-concepts/package-and-task-graph#package-graph) so you can run your `dev` task for a specific application and its dependencies:

```bash title="Terminal"
turbo dev --filter=web
```

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

## Watch Mode

Many tools have a built-in watcher, like [`tsc --watch`](https://www.typescriptlang.org/docs/handbook/compiler-options.html#compiler-options),
that will respond to changes in your source code. However, some don't.

`turbo watch` adds a dependency-aware watcher to any tool. Changes to source code will follow [the Task Graph](/docs/core-concepts/package-and-task-graph#task-graph) that you've described in `turbo.json`, just like all your other tasks.

For example, using a package structure like [`create-turbo`](/docs/reference/create-turbo) with the following tasks and scripts:

<Tabs items={["turbo.json", "packages/ui", "apps/web"]}>
  <Tab value="turbo.json">
    ```json title="turbo.json"
    {
      "tasks": {
        "dev": {
          "persistent": true,
          "cache": false
        },
        "lint": {
          "dependsOn": ["^lint"]
        }
      }
    }
    ```
  </Tab>

  <Tab value="packages/ui">
    ```json title="package.json"
    {
      "name": "@repo/ui"
      "scripts": {
        "dev": "tsc --watch",
        "lint": "eslint ."
      }
    }
    ```
  </Tab>

  <Tab value="apps/web">
    ```json title="package.json"
    {
      "name": "web"
      "scripts": {
        "dev": "next dev",
        "lint": "eslint ."
      },
      "dependencies": {
          "@repo/ui": "workspace:*"
        }
    }
    ```
  </Tab>
</Tabs>

When you run `turbo watch dev lint`, you'll see the `lint` scripts are re-run whenever you make source code changes, despite ESLint not having a built-in watcher. `turbo watch` is also aware of internal dependencies, so a code change in `@repo/ui` will re-run the task in both `@repo/ui` and `web`.

The Next.js development server in `web` and the TypeScript Compiler's built-in watcher in `@repo/ui` will continue to work as usual, since they are marked with `persistent`.

For more information, [visit the `turbo watch` reference](/docs/reference/watch).

## Limitations

### Teardown tasks

In some cases, you may want to run a script when the `dev` task is stopped. Turborepo is unable to run those teardown scripts when exiting because `turbo` exits when your `dev` tasks exit.

Instead, create a `turbo dev:teardown` script that you run separately after you've exited your primary `turbo dev` task.

## Next steps

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

## More guides

We also have more guides centered around [specific tools, use cases, and other topics](/docs/guides).


- [Managing dependencies](/crafting-your-repository/managing-dependencies.md): Learn how to manage dependencies in your monorepo's workspace.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';
import { LinkToDocumentation } from '#components/link-to-documentation';

* **External dependencies** come from [the npm registry](https://www.npmjs.com/), allowing you to leverage valuable code from the ecosystem to build your applications and libraries faster.
* **Internal dependencies** let you share functionality within your repository, dramatically improving discoverability and usability of shared code. We will discuss how to build an Internal Package in [the next guide](/docs/crafting-your-repository/creating-an-internal-package).

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```json title="./apps/web/package.json"
    {
      "dependencies": {
        "next": "latest", // External dependency
        "@repo/ui": "workspace:*" // Internal dependency
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```json title="./apps/web/package.json"
    {
      "dependencies": {
        "next": "latest", // External dependency
        "@repo/ui": "*" // Internal dependency
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```json title="./apps/web/package.json"
    {
      "dependencies": {
        "next": "latest", // External dependency
        "@repo/ui": "*" // Internal dependency
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```json title="./apps/web/package.json"
    {
      "dependencies": {
        "next": "latest", // External dependency
        "@repo/ui": "workspace:*" // Internal dependency
      }
    }
    ```
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
    ```bash title="Terminal"
    pnpm add jest --save-dev --recursive --filter=web --filter=@repo/ui --filter=docs
    ```

    <LinkToDocumentation href="https://pnpm.io/cli/recursive">pnpm documentation</LinkToDocumentation>
  </Tab>

  <Tab value="yarn">
    Yarn 1:

    ```bash title="Terminal"
    yarn workspace web add jest --dev
    yarn workspace @repo/ui add jest --dev
    ```

    <LinkToDocumentation href="https://classic.yarnpkg.com/en/docs/cli/add">
      Yarn 1 documentation
    </LinkToDocumentation>

    Yarn 2+:

    ```bash title="Terminal"
    yarn workspaces foreach -R --from '{web,@repo/ui}' add jest --dev
    ```

    <LinkToDocumentation href="https://yarnpkg.com/cli/workspaces/foreach#usage">
      Yarn 2+ documentation
    </LinkToDocumentation>
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install jest --workspace=web --workspace=@repo/ui --save-dev
    ```

    <LinkToDocumentation href="https://docs.npmjs.com/cli/v7/using-npm/config#workspace">npm documentation</LinkToDocumentation>
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    cd apps/web && bun install jest --dev
    cd packages/ui && bun install jest --dev
    ```

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
    ```bash title="Terminal"
    pnpm up --recursive typescript@latest
    ```

    <small>[→ pnpm documentation](https://pnpm.io/cli/update#--recursive--r)</small>
  </Tab>

  <Tab value="yarn">
    Yarn 1:

    ```bash title="Terminal"
    yarn upgrade-interactive --latest
    ```

    <small>[→ Yarn 1 documentation](https://classic.yarnpkg.com/en/docs/cli/upgrade-interactive)</small>

    Yarn 2+:

    ```bash title="Terminal"
    yarn upgrade typescript@latest --upgrade
    ```

    <small>[→ Yarn 2+ documentation](https://yarnpkg.com/cli/up)</small>
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install typescript@latest --workspaces
    ```

    <small>[→ npm documentation](https://docs.npmjs.com/cli/v7/using-npm/config#workspaces)</small>
  </Tab>

  <Tab value="bun">
    No equivalent

    <small>[→ Bun documentation](https://bun.sh/docs/install/workspaces)</small>
  </Tab>
</Tabs>

#### pnpm catalogs

In pnpm v9.5+, you can use catalogs to define dependency version ranges as reusable constants. This will keep dependencies on the same version since you're referencing the same value across the workspace.

To learn more, [visit the pnpm catalogs documentation](https://pnpm.io/catalogs).

#### Using an IDE

Your IDE's refactoring tooling can find and replace the version of a dependency across all `package.json` files in your repository at once. Try using a regex like `"next": ".*"` on `package.json` files to find all instances of the `next` package and replace them with the version you want. When you're done, make sure to run your package manager's install command to update your lockfile.

## Next steps

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

```jsonc title="./package.json"
{
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "test": "turbo run test",
    "lint": "turbo run lint"
  }
}
```

<Callout type="good-to-know">
  `turbo` is an alias for `turbo run` - but we recommend using `turbo run` in
  `package.json` and CI workflows to avoid potential collisions with possible
  `turbo` subcommands that could be added in the future.
</Callout>

These scripts can then be run using your package manager.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dev
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dev
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm run dev
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bun run dev
    ```
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

```bash title="Terminal"
cd apps/docs
turbo build
```

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

```bash title="Terminal"
turbo run build test lint check-types
```

This command will run all of the tasks, automatically detecting where it can run a script as early as possible, according to your task definitions.

<Callout type="info" title="Ordering of tasks">
  `turbo test lint` will run tasks exactly the same as `turbo lint test`.

  If you want to ensure that one task blocks the execution of another, express that relationship in your [task configurations](/docs/crafting-your-repository/configuring-tasks#defining-tasks).
</Callout>

## Using filters

While [caching](/docs/crafting-your-repository/running-tasks) ensures you stay fast by never doing the same work twice, you can also filter tasks to run only a subset of [the Task Graph](/docs/core-concepts/package-and-task-graph#task-graph).

There are many advanced use cases for filtering in [the `--filter` API reference](/docs/reference/run#--filter-string) but the most common use cases are discussed below.

### Filtering by package

Filtering by package is a simple way to only run tasks for the packages you're currently working on.

```bash title="Terminal"
turbo build --filter=@acme/web
```

<InVersion version="2.2.4">
  You can also filter to a specific task for the package directly in your CLI command without needing to use `--filter`:

  ```bash title="Terminal"
  # Run the `build` task for the `web` package
  turbo run web#build

  # Run the `build` task for the `web` package, and the `lint` task for the `docs` package
  turbo run web#build docs#lint
  ```
</InVersion>

### Filtering by directory

Your repository might have a directory structure where related packages are grouped together. In this case, you can capture the glob for that directory to focus `turbo` on those packages.

```bash title="Terminal"
turbo lint --filter="./packages/utilities/*"
```

### Filtering to include dependents

When you're working on a specific package, you might want to run tasks for the package and its dependents. The `...` microsyntax is useful when you're making changes to a package and want to ensure that the changes don't break any of its dependents.

```bash title="Terminal"
turbo build --filter=...ui
```

### Filtering to include dependencies

To limit the scope to a package and its dependencies, append `...` to the package name. This runs the task for the specified package and all packages it depends on.

```bash title="Terminal"
turbo dev --filter=web...
```

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

```bash title="Terminal"
turbo build --filter=...ui --filter={./packages/*} --filter=[HEAD^1]
```

Multiple filters are combined as a **union**, meaning that the [Task Graph](/docs/core-concepts/package-and-task-graph#task-graph) will include tasks that match any of the filters. For more information on advanced usage of filters, see [the `--filter` API reference](/docs/reference/run#--filter-string).

## Next steps

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

## Getting started

Setting up a workspace's structure can be tedious to do by hand. If you're new to monorepos, we recommend [using `create-turbo` to get started](/docs/getting-started/installation) with a valid workspace structure right away.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest
    ```
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
        ```json title="pnpm-workspace.yaml"
        packages:
          - "apps/*"
          - "packages/*"
        ```

        <LinkToDocumentation href="https://pnpm.io/pnpm-workspace_yaml">pnpm workspace documentation</LinkToDocumentation>
      </Tab>

      <Tab value="yarn">
        ```json title="./package.json"
        {
          "workspaces": [
            "apps/*",
            "packages/*"
          ]
        }
        ```

        <LinkToDocumentation href="https://yarnpkg.com/features/workspaces#how-are-workspaces-declared">yarn workspace documentation</LinkToDocumentation>
      </Tab>

      <Tab value="npm">
        ```json title="./package.json"
        {
          "workspaces": [
            "apps/*",
            "packages/*"
          ]
        }
        ```

        <LinkToDocumentation href="https://docs.npmjs.com/cli/v7/using-npm/workspaces#defining-workspaces">npm workspace documentation</LinkToDocumentation>
      </Tab>

      <Tab value="bun">
        ```json title="./package.json"
        {
          "workspaces": [
            "apps/*",
            "packages/*"
          ]
        }
        ```

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
    ```json title="./package.json"
    {
      "private": true,
      "scripts": {
        "build": "turbo run build",
        "dev": "turbo run dev",
        "lint": "turbo run lint"
      },
      "devDependencies": {
        "turbo": "latest"
      },
      "packageManager": "pnpm@9.0.0"
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```json title="./package.json"
    {
      "private": true,
      "scripts": {
        "build": "turbo run build",
        "dev": "turbo run dev",
        "lint": "turbo run lint"
      },
      "devDependencies": {
        "turbo": "latest"
      },
      "packageManager": "yarn@1.22.19",
      "workspaces": ["apps/*", "packages/*"]
    }
    ```
  </Tab>

  <Tab value="npm">
    ```json title="./package.json"
    {
      "private": true,
      "scripts": {
        "build": "turbo run build",
        "dev": "turbo run dev",
        "lint": "turbo run lint"
      },
      "devDependencies": {
        "turbo": "latest"
      },
      "packageManager": "npm@10.0.0",
      "workspaces": ["apps/*", "packages/*"]
    }
    ```
  </Tab>

  <Tab value="bun">
    ```json title="./package.json"
    {
      "private": true,
      "scripts": {
        "build": "turbo run build",
        "dev": "turbo run dev",
        "lint": "turbo run lint"
      },
      "devDependencies": {
        "turbo": "latest"
      },
      "packageManager": "bun@1.2.0",
      "workspaces": ["apps/*", "packages/*"]
    }
    ```
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

#### `name`

[The `name` field](https://nodejs.org/api/packages.html#name) is used to identify the package. It should be unique within your workspace.

<Callout type="info">
  It's best practice to use a namespace prefix for your [Internal Packages](/docs/core-concepts/internal-packages) to avoid conflicts with other packages on the npm registry. For example, if your organization is named `acme`, you might name your packages `@acme/package-name`.

  We use `@repo` in our docs and examples because it is an unused, unclaimable namespace on the npm registry. You can choose to keep it or use your own prefix.
</Callout>

#### `scripts`

The `scripts` field is used to define scripts that can be run in the package's context. Turborepo will use the name of these scripts to identify what scripts to run (if any) in a package. We talk more about these scripts on the [Running Tasks](/docs/crafting-your-repository/running-tasks) page.

#### `exports`

[The `exports` field](https://nodejs.org/api/packages.html#exports) is used to specify the entrypoints for other packages that want to use the package. When you want to use code from one package in another package, you'll import from that entrypoint.

For example, if you had a `@repo/math` package, you might have the following `exports` field:

```json title="./packages/math/package.json"
{
  "exports": {
    ".": "./src/constants.ts",
    "./add": "./src/add.ts",
    "./subtract": "./src/subtract.ts"
  }
}
```

Note that this example uses the [Just-in-Time Package](/docs/core-concepts/internal-packages#just-in-time-packages) pattern for simplicity. It exports TypeScript directly, but you might choose to use the [Compiled Package](/docs/core-concepts/internal-packages#compiled-packages) pattern instead.

<Callout type="info">
  The `exports` field in this example requires modern versions of Node.js and
  TypeScript.
</Callout>

This would allow you to import `add` and `subtract` functions from the `@repo/math` package like so:

```ts title="./apps/my-app/src/index.ts"
import { GRAVITATIONAL_CONSTANT, SPEED_OF_LIGHT } from '@repo/math';
import { add } from '@repo/math/add';
import { subtract } from '@repo/math/subtract';
```

Using exports this way provides three major benefits:

* **Avoiding barrel files**: Barrel files are files that re-export other files in the same package, creating one entrypoint for the entire package. While they might appear convenient, they're [difficult for compilers and bundlers to handle](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js#what's-the-problem-with-barrel-files) and can quickly lead to performance problems.
* **More powerful features**: `exports` also has other powerful features compared to [the `main` field](https://nodejs.org/api/packages.html#main) like [Conditional Exports](https://nodejs.org/api/packages.html#conditional-exports). In general, we recommend using `exports` over `main` whenever possible as it is the more modern option.
* **IDE autocompletion**: By specifying the entrypoints for your package using `exports`, you can ensure that your code editor can provide auto-completion for the package's exports.

#### `imports` (optional)

[The `imports` field](https://nodejs.org/api/packages.html#imports) gives you a way to create subpaths to other modules within your package. You can think of these like "shortcuts" to write simpler import paths that are more resilient to refactors that move files. To learn how, visit [the TypeScript page](/docs/guides/tools/typescript#use-nodejs-subpath-imports-instead-of-typescript-compiler-paths).

<Callout type="info">
  You may be more familiar with TypeScript's `compilerOptions#paths` option, which accomplishes a similar goal. As of TypeScript 5.4, TypeScript can infer subpaths from `imports`, making it a better option since you'll be working with Node.js conventions. For more information, visit [our TypeScript guide](/docs/guides/tools/typescript#use-nodejs-subpath-imports-instead-of-typescript-compiler-paths).
</Callout>

### Source code

Of course, you'll want some source code in your package. Packages commonly use a `src` directory to store their source code and compile to a `dist` directory (that should also be located within the package), although this is not a requirement.

## Common pitfalls

* If you're using TypeScript, you likely don't need a `tsconfig.json` in the root of your workspace. Packages should independently specify their own configurations, usually building off of a shared `tsconfig.json` from a separate package in the workspace. For more information, visit [the TypeScript guide](/docs/guides/tools/typescript#you-likely-dont-need-a-tsconfigjson-file-in-the-root-of-your-project).
* You want to avoid accessing files across package boundaries as much as possible. If you ever find yourself writing `../` to get from one package to another, you likely have an opportunity to re-think your approach by installing the package where it's needed and importing it into your code.

## Next steps

With your Workspace configured, you can now use your package manager to [install dependencies into your packages](/docs/crafting-your-repository/managing-dependencies).


- [Understanding your repository](/crafting-your-repository/understanding-your-repository.md): Learn how to understand your repository structure using Turborepo.

import { PrereleaseBadge } from '#components/prerelease-badge';

Turborepo includes tools for understanding your repository structure, that can help you use and optimize your codebase.

## `turbo devtools` <PrereleaseBadge />

`turbo devtools` provides a browser-based visualization of your package graph. This tool can be helpful for diagnosing issues with your task graph and understanding the structure of your monorepo.

```bash title="Terminal"
turbo devtools
```

For more information, see the [reference documentation](/docs/reference/devtools).

## `turbo ls`

To list your packages, you can run `turbo ls`. This will show the packages in your repository and where they're located.

```bash title="Terminal"
> turbo ls

  @repo/eslint-config packages/eslint-config
  @repo/typescript-config packages/typescript-config
  @repo/ui packages/ui
  docs apps/docs
  web apps/web
```

You can [apply filters](/docs/crafting-your-repository/running-tasks#using-filters) to `ls`, just like `run`:

```bash title="Terminal"
> turbo ls --filter ...ui
3 packages (pnpm9)

  @repo/ui packages/ui
  docs apps/docs
  web apps/web
```

## `turbo run`

To determine which tasks can be run in your monorepo, simply call `turbo run` without any tasks. You will get a list of
tasks and the packages in which they are defined:

```bash title="Terminal"
> turbo run
No tasks provided, here are some potential ones

  lint
    @repo/ui, docs, web
  build
    docs, web
  dev
    docs, web
  start
    docs, web
  generate:component
    @repo/ui
```

## `turbo query`

If you wish to dig into your repository structure, since `2.2.0`, Turborepo provides a GraphQL interface into your repository
via `turbo query`. You can execute queries such as finding all packages that have a `test` task:

```bash title="Terminal"
> turbo query "query { packages(filter: { has: { field: TASK_NAME, value: \"build\"}}) { items { name } } }"
{
  "data": {
    "packages": {
      "items": [
        {
          "name": "//"
        },
        {
          "name": "docs"
        },
        {
          "name": "web"
        }
      ]
    }
  }
}
```

This can be helpful for diagnosing potential problems in your package or task dependency graph. For instance, let's say
you're getting a lot of cache misses in your builds. This could be because there's a package that keeps getting changed
and is imported throughout your codebase.

To do this, we can run a query to find packages that are directly imported more than 10 times in your monorepo:

```bash title="Terminal"
> turbo query "query { packages(filter: { greaterThan: { field: DIRECT_DEPENDENT_COUNT, value: 10 } }) { items { name } } }"
{
  "data": {
    "packages": {
      "items": [
        {
          "name": "utils"
        }
      ]
    }
  }
}
```

Now that we've found this package, we can try to split it up into smaller packages so that a small change won't
invalidate the whole dependency graph.

Or let's say you're using our new `--affected` flag, but you're still running more tasks than you'd like.
With `turbo query`, you can find all the packages and the reason why they were invalidated:

```bash title="Terminal"
> turbo query "query { affectedPackages(base: \"HEAD^\", head: \"HEAD\") { items { reason {  __typename } } } }"
{
  "data": {
    "affectedPackages": {
      "items": [
        {
          "name": "utils",
          "reason": {
            "__typename": "FileChanged"
          }
        },
        {
          "name": "web",
          "reason": {
            "__typename": "DependencyChanged"
          }
        },
        {
          "name": "docs",
          "reason": {
            "__typename": "DependencyChanged"
          }
        },
        {
          "name": "cli",
          "reason": {
            "__typename": "DependencyChanged"
          }
        },
      ]
    }
  }
}
```


- [Upgrading](/crafting-your-repository/upgrading.md): Learn how to upgrade `turbo` to get the latest improvements to your repository.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Steps, Step } from '#components/steps';
import { Callout } from '#components/callout';

## Upgrading to 2.0

<Steps>
  <Step>
    ### Update `turbo.json`

    Get started upgrading from 1.x to 2.0 by running:

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm dlx @turbo/codemod migrate
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn dlx @turbo/codemod migrate
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        npx @turbo/codemod migrate
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        bunx @turbo/codemod migrate
        ```
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
        ```diff title="./package.json"
        {
        + "packageManager": "pnpm@9.2.0"
        }
        ```
      </Tab>

      <Tab value="yarn">
        ```diff title="./package.json"
        {
        + "packageManager": "yarn@1.22.19"
        }
        ```
      </Tab>

      <Tab value="npm">
        ```diff title="./package.json"
        {
        + "packageManager": "npm@10.8.1"
        }
        ```
      </Tab>

      <Tab value="bun">
        ```diff title="./package.json"
        {
        + "packageManager": "bun@1.2.0"
        }
        ```
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

```json title="./turbo.json"
{
  "globalEnv": ["IMPORTANT_GLOBAL_VARIABLE"],
  "tasks": {
    "build": {
      "env": ["MY_API_URL", "MY_API_KEY"]
    }
  }
}
```

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

## Environment Modes

Turborepo's Environment Modes allow you to control which environment variables are available to a task at runtime:

* [Strict Mode](#strict-mode) (Default): Filter environment variables to **only** those that are specified in the `env` and `globalEnv` keys in `turbo.json`.
* [Loose Mode](#loose-mode): Allow all environment variables for the process to be available.

### Strict Mode

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

### Loose Mode

Loose Mode does not filter your environment variables according to your `globalEnv` and `env` keys. This makes it easier to get started with incrementally migrating to Strict Mode.

Use [the `--env-mode` flag](/docs/reference/run#--env-mode-option) to enable Loose Mode on any invocation where you're seeing environment variables cannot be found by your scripts:

```bash title="Terminal"
turbo run build --env-mode=loose
```

As long as the environment variable is available when `turbo` is ran, your script will be able to use it. However, this also **lets you accidentally forget to account for an environment variable in your configuration much more easily**, allowing the task to hit cache when it shouldn't.

For example, you may have some code in your application that fetches data from an API, using an environment variable for the base URL:

```ts title="./apps/web/data-fetcher.ts"
const data = fetch(`${process.env.MY_API_URL}/resource/1`);
```

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

```json title="./turbo.json"
{
  "globalDependencies": [".env"], // All task hashes
  "tasks": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$", ".env"] // Only the `build` task hash
    }
  }
}
```

### Multiple `.env` files

You can capture multiple `.env` files at once using a `*`.

```json title="./turbo.json"
{
  "globalDependencies": [".env"], // All task hashes
  "tasks": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$", ".env*"] // Only the `build` task hash
    }
  }
}
```

<Callout type="info">
  `.env` files can load variables into the task runtime even when the
  environment variables have not been added to [the `env`
  key](/docs/reference/configuration#env). Ensure that you add your environment
  variables for your builds the `env` key for CI and production builds.
</Callout>

## Best practices

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

```json title="./apps/web/package.json"
{
  "scripts": {
    "dev": "export MY_VARIABLE=123 && next dev"
  }
}
```

`MY_VARIABLE` is being added to the environment *after* the `dev` task has started, so `turbo` will not be able to use it for hashing.

## Examples

Below are examples of proper environment variable configuration for a few popular frameworks:

<Accordions>
  <Accordion title="Next.js">
    The `turbo.json` below expresses:

    * The `build` and `dev` tasks will have different hashes for changes to `MY_API_URL` and `MY_API_KEY`.
    * The `build` and `dev` tasks include the supported .env files for Next.js.
    * The `test` task does not use environment variables, so the `env` key is omitted. (Depending on your testing structure, your `test` task may need an `env` key.)

    ```json title="./turbo.json"
    {
      "tasks": {
        "build": {
          "env": ["MY_API_URL", "MY_API_KEY"],
          "inputs": [
            "$TURBO_DEFAULT$",
            ".env.production.local",
            ".env.local",
            ".env.production",
            ".env"
          ]
        },
        "dev": {
          "inputs": [
            "$TURBO_DEFAULT$",
            ".env.development.local",
            ".env.local",
            ".env.development",
            ".env"
          ]
        },
        "test": {}
      }
    }
    ```
  </Accordion>

  <Accordion title="Vite">
    The `turbo.json` below expresses:

    * The `build` and `dev` tasks will have different hashes for changes to `MY_API_URL` and `MY_API_KEY`.
    * The `build` and `dev` tasks include the supported .env files for Vite.
    * The `test` task does not use environment variables, so the `env` key is omitted. (Depending on your testing structure, your `test` task may need an `env` key.)

    ```json title="./turbo.json"
    {
      "tasks": {
        "build": {
          "env": ["MY_API_URL", "MY_API_KEY"],
          "inputs": [
            "$TURBO_DEFAULT$",
            ".env.production.local",
            ".env.local",
            ".env.production",
            ".env"
          ]
        },
        "dev": {
          "inputs": [
            "$TURBO_DEFAULT$",
            ".env.development.local",
            ".env.local",
            ".env.development",
            ".env"
          ]
        },
        "test": {}
      }
    }
    ```
  </Accordion>
</Accordions>

## Troubleshooting

### Use `--summarize`

[The `--summarize` flag](/docs/reference/run#--summarize) can be added to your `turbo run` command to produce a JSON file summarizing data about your task. Checking the diff for the `globalEnv` and `env` key can help you identify any environment variables that may be missing from your configuration.

## Next steps

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

```sh title="Terminal"
turbo gen workspace
```

View all available [options](/docs/reference/generate#workspace) for `gen workspace`.

## Copy an existing package

You can use an existing workspace as a template for your new app or package. This works for both workspaces within your existing monorepo,
and remote workspaces from other repositories (specified via GitHub URL).

### Examples

Create a new package in your monorepo by copying from an existing package in your repo.

```sh title="Terminal"
turbo gen workspace --copy
```

Create a new workspace in your monorepo by copying from a remote package.

```sh title="Terminal"
turbo gen workspace --copy https://github.com/vercel/turborepo/tree/main/examples/with-tailwind/packages/tailwind-config
```

<Callout>
  **Note**: When adding from a remote source, Turborepo is unable to verify that your repo has all of the required dependencies, and is using the correct package manager. In this case, some manual modifications may be required to get the new workspace working as expected within your repository.
</Callout>

View all available [options](/docs/reference/generate#workspace) for `gen workspace --copy`.

## Custom generators

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

### Getting started

To build and run a custom generator, run the following command from anywhere within your monorepo using Turborepo.

```sh title="Terminal"
turbo gen
```

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

```ts title="turbo/generators/config.ts"
import type { PlopTypes } from "@turbo/gen";

export default function generator(plop: PlopTypes.NodePlopAPI): void {
  // create a generator
  plop.setGenerator("Generator name", {
    description: "Generator description",
    // gather information from the user
    prompts: [
      ...
    ],
    // perform actions based on the prompts
    actions: [
      ...
    ],
  });
}
```

#### Prompts

Prompts are written using [Plop prompts](https://plopjs.com/documentation/#using-prompts) and are used to gather information from the user.

#### Actions

Actions can use [built-in Plop actions](https://plopjs.com/documentation/#built-in-actions), or [custom action functions](https://plopjs.com/documentation/#functionsignature-custom-action) that you define yourself:

```ts title="turbo/generators/config.ts"
import type { PlopTypes } from "@turbo/gen";

const customAction: PlopTypes.CustomActionFunction = async (answers) => {
  // fetch data from a remote API
  const results = await fetchRemoteData();
  // add the response to the answers, making this data available to actions
  answers.results = results;
  // return a status string
  return 'Finished data fetching!';
}

export default function generator(plop: PlopTypes.NodePlopAPI): void {
  // create a generator
  plop.setGenerator("Generator name", {
    description: "Generator description",
    prompts: [
      ...
    ],
    actions: [
      customAction
      {/* actions now have access to `answers.results` */}
      ...
    ],
  });
}
```

### Running generators

Once you have created your generator configuration file, you can skip the selection prompt and directly run a specified generator with:

```sh title="Terminal"
turbo gen [generator-name]
```

Arguments can also be passed directly to the generator prompts using `--args`

```sh title="Terminal"
turbo gen [generator-name] --args answer1 answer2 ...
```

See [bypassing prompts](https://plopjs.com/documentation/#bypassing-prompts) in the Plop documentation for more information.

View all available [options](/docs/reference/generate#run-generator-name) for `gen`.


- [Handling platforms](/guides/handling-platforms.md): Learn how to handle caching around operating systems, architectures, and other arbitrary conditions for Turborepo tasks.

## Node.js versions

To account for Node.js versions, use [the engines key in package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#engines). Turborepo will account for changes to this field and miss cache accordingly.

## Operating systems, architecture, and other arbitrary conditions

For advanced use cases, you may want the operating system (OS), architecture, or other external factors to contribute to your hash.

### 1. Write an arbitrary file to disk

First, create a script that accounts for the hash contributors that you are interested in. For example, here is a Node.js script that identifies platform and architecture and writes those details to a file (`turbo-cache-key.json`):

```js title="./scripts/create-turbo-cache-key.js"
#!/usr/bin/env node

const { writeFileSync } = require('fs');
const { join } = require('path');

const { platform, arch } = process;
const file = 'turbo-cache-key.json';
const str = JSON.stringify({ platform, arch });
console.log(`Generating cache key: ${str}`);
writeFileSync(file, str);
```

### 2. Add the file to your .gitignore

You won't want to commit this file to source control since it's dependent on environment. Add it to your `.gitignore`:

```diff title=".gitignore"
+ turbo-cache-key.json
```

### 3. Add the file to the hash

Now, make sure that `turbo` is aware of the file by adding it to task inputs. You can do this two ways:

* **For specific tasks**: Include the file in [the `inputs` array](/docs/reference/configuration#inputs) of the task(s):

```json title="./turbo.json"
{
  "tasks": {
    "build-for-platforms": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", "turbo-cache-key.json"]
    }
  }
}
```

* **For all tasks**: Add the file to [`globalDependencies`](/docs/reference/configuration#globaldependencies)

```json title="./turbo.json"
{
  "globalDependencies": ["turbo-cache-key.json"],
  "tasks": {
    ...
  }
}
```

### 4. Generate the file before running `turbo`

Last, you'll want to ensure that you run the script before running `turbo`. For example:

```json title="./package.json"
{
  "scripts": {
    "build-for-platforms": "node ./scripts/create-turbo-cache-key.js && turbo run build"
  }
}
```

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

## Getting started

Turborepo provides a built-in proxy server that automatically routes traffic between your microfrontend applications during development. The proxy reads a `microfrontends.json` configuration file and starts when you run `turbo dev`.

<Callout>
  You can try the following instructions with the monorepo created by `npx
    create-turbo@latest -e with-microfrontends`.
</Callout>

### Create `microfrontends.json`

Create a `microfrontends.json` file in your parent application. This application is the one that all requests will fall through to when not matched by another application.

```json title="./apps/web/microfrontends.json"
{
  "$schema": "https://turborepo.com/microfrontends/schema.json",
  "applications": {
    "web": {
      "development": {
        "local": {
          "port": 3000
        }
      }
    },
    "docs": {
      "development": {
        "local": {
          "port": 3001
        }
      },
      "routing": [
        {
          "paths": ["/docs", "/docs/:path*"]
        }
      ]
    }
  }
}
```

### Set application ports

Next, use the `turbo get-mfe-port` command to set the ports in your application's development scripts. This command injects the port number when running `turbo dev`:

<Tabs items={['Next.js', 'Vite']} storageKey="framework-preference">
  <Tab value="Next.js">
    ```json title="./apps/web/package.json"
    {
      "scripts": {
        "dev": "next dev --port $(turbo get-mfe-port)"
      }
    }
    ```
  </Tab>

  <Tab value="Vite">
    ```json title="./apps/web/package.json"
    {
      "scripts": {
        "dev": "vite dev --port $TURBO_MFE_PORT"
      }
    }
    ```
  </Tab>
</Tabs>

### Handle base paths

If you're using a framework, set the base path according to the needs of the framework.

<Tabs items={['Next.js', 'Vite']} storageKey="framework-preference">
  <Tab value="Next.js">
    ```ts title="./apps/my-app/next.config.ts"
    import type { NextConfig } from 'next';

    const nextConfig: NextConfig = {
      basePath: '/docs',
    };

    export default nextConfig;
    ```
  </Tab>

  <Tab value="Vite">
    ```ts title="./apps/my-app/vite.config.ts"
    import { defineConfig } from 'vite';

    export default defineConfig({
      base: '/admin',
    });
    ```
  </Tab>
</Tabs>

[Visit the Microfrontends section of your framework](/docs/guides/frameworks) for framework-specific guidance.

### Run `turbo dev`

When you run `turbo dev`, Turborepo will:

1. **Start the proxy server** on the configured port (default: `3024`)
2. **Inject the `TURBO_MFE_PORT` environment variable** in tasks to set the applications' port
3. **Run development tasks** for all configured applications
4. **Route incoming requests** based on path patterns to the appropriate application

Now you can access all of your microfrontends applications at `http://localhost:3024`.

## Configuration

Each application in the `applications` object can have the following properties:

If not provided, the application key is used to match the name in \`package.json.

### `development.local`

The port where the application runs locally.

```json title="./apps/web/microfrontends.json"
{
  "development": {
    "local": {
      "port": 3000
    }
  }
}
```

If you omit the port, Turborepo will generate a deterministic port based on the application name (between 3000-8000).

### `development.fallback`

Optionally provide a target to proxy to when an application is not running locally. This is most frequently used to route to production to make commands like `turbo dev --filter=web` that only run a subset of applications a seamless experience.

```json title="./apps/web/microfrontends.json"
{
  "development": {
    "fallback": "example.com"
  }
}
```

### `routing`

An array of path groups that should route to this application. If no routing is provided, the application becomes the **default application** that catches all unmatched routes.

Only one application can have no `routing` configuration. This is your "root" application that handles all routes not matched by other applications.

```json title="./apps/web/microfrontends.json"
{
  "routing": [
    {
      "paths": ["/api/:version/users/:id"]
    },
    {
      "paths": ["/docs", "/docs/:path*"]
    }
  ]
}
```

* Paths are **case-sensitive**: `/Blog` and `/blog` are different routes
* Trailing slashes are normalized: `/home` and `/home/` match the same route

#### Exact matches

```json title="./apps/web/microfrontends.json"
{
  "paths": ["/pricing", "/about", "/contact"]
}
```

These paths match exactly as written.

#### Parameters

```json title="./apps/web/microfrontends.json"
{
  "paths": ["/blog/:slug", "/users/:id/profile"]
}
```

Segments starting with `:` match any single path segment. For example, `/blog/:slug` matches `/blog/hello` but not `/blog/hello/world`.

#### Wildcards

```json title="./apps/web/microfrontends.json"
{
  "paths": ["/docs/:path*", "/api/:version*"]
}
```

Parameters ending with `*` match zero or more path segments. For example, `/docs/:path*` matches `/docs`, `/docs/intro`, and `/docs/api/reference`.

You can also use the `+` modifier to match one or more segments (excluding the empty path):

```json title="./apps/web/microfrontends.json"
{
  "paths": ["/api/:path+"]
}
```

This matches `/api/users` and `/api/users/123`, but not `/api` or `/api/`.

#### Complex routing patterns

You can define sophisticated routing with nested parameters:

```json title="./apps/web/microfrontends.json"
{
  "routing": [
    {
      "paths": [
        "/api/:version/users",
        "/api/:version/users/:id",
        "/api/:version/posts/:postId/comments/:commentId"
      ]
    }
  ]
}
```

#### Group labels

Organize routes into logical groups for better maintainability:

```json title="./apps/web/microfrontends.json"
{
  "$schema": "https://turborepo.com/microfrontends/schema.json",
  "applications": {
    "marketing": {
      "development": {
        "local": 3002
      },
      "routing": [
        {
          "group": "blog",
          "paths": ["/blog", "/blog/:slug*"]
        },
        {
          "group": "sales",
          "paths": ["/pricing", "/contact", "/demo"]
        }
      ]
    }
  }
}
```

The `group` field is for organizational purposes and doesn't affect routing behavior.

### `packageName`

Optionally use the name of the package from `package.json` in your workspace.

```json title="./apps/main/microfrontends.json"
{
  "applications": {
    "main-site": {
      "packageName": "web"
    }
  }
}
```

### `options.localProxyPort`

Optionally change the proxy port using the `localProxyPort` option

Defaults to `3024`.

```json title="./apps/web/microfrontends.json"
{
  "options": {
    "localProxyPort": 8080
  }
}
```

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

## Troubleshooting

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

Verify that:

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

```bash title="Terminal"
turbo --skip-infer --cwd ../.. get-mfe-port
```

## Complete example

Here's a full example of a microfrontends configuration for an e-commerce platform:

```json title="./apps/web/microfrontends.json"
{
  "$schema": "https://turborepo.com/microfrontends/schema.json",
  "options": {
    "localProxyPort": 3024
  },
  "applications": {
    "web": {
      "packageName": "web",
      "development": {
        "local": {
          "port": 3000
        }
      }
    },
    "docs": {
      "packageName": "documentation",
      "development": {
        "local": {
          "port": 3001
        }
      },
      "routing": [
        {
          "group": "documentation",
          "paths": [
            "/docs",
            "/docs/:path*",
            "/api-reference",
            "/api-reference/:path*"
          ]
        }
      ]
    },
    "blog": {
      "development": {
        "local": {
          "port": 3002
        }
      },
      "routing": [
        {
          "group": "content",
          "paths": [
            "/blog",
            "/blog/:slug",
            "/blog/category/:category",
            "/authors/:author"
          ]
        }
      ]
    },
    "shop": {
      "development": {
        "local": {
          "port": 3003
        }
      },
      "routing": [
        {
          "group": "commerce",
          "paths": [
            "/products",
            "/products/:id",
            "/cart",
            "/checkout",
            "/orders/:orderId"
          ]
        }
      ]
    }
  }
}
```

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

## Why switch?

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
    ```json title="turbo.json"
    {
      "$schema": "/schema.json",
      "ui": "tui",
      "tasks": {
        "build": {
          "dependsOn": ["^build"],
          "inputs": ["$TURBO_DEFAULT$", ".env*"],
          "outputs": [".next/**", "!.next/cache/**"]
        },
        "lint": {
          "dependsOn": ["^lint"]
        },
        "check-types": {
          "dependsOn": ["^check-types"]
        },
        "dev": {
          "cache": false,
          "persistent": true
        }
      }
    }
    ```
  </Tab>

  <Tab value="Nx">
    ```json title="nx.json"
    {
      "$schema": "./node_modules/nx/schemas/nx-schema.json",
      "namedInputs": {
        "default": ["{projectRoot}/**/*", "sharedGlobals"],
        "production": [
          "default",
          "!{projectRoot}/.eslintrc.json",
          "!{projectRoot}/eslint.config.cjs",
          "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)?(.snap)",
          "!{projectRoot}/tsconfig.spec.json",
          "!{projectRoot}/jest.config.[jt]s",
          "!{projectRoot}/src/test-setup.[jt]s",
          "!{projectRoot}/test-setup.[jt]s"
        ],
        "sharedGlobals": ["{workspaceRoot}/.github/workflows/ci.yml"]
      },
      "nxCloudId": "6789ec521d90a2165398f39a",
      "plugins": [
        {
          "plugin": "@nx/next/plugin",
          "options": {
            "startTargetName": "start",
            "buildTargetName": "build",
            "devTargetName": "dev",
            "serveStaticTargetName": "serve-static"
          }
        },
        {
          "plugin": "@nx/playwright/plugin",
          "options": {
            "targetName": "e2e"
          }
        },
        {
          "plugin": "@nx/eslint/plugin",
          "options": {
            "targetName": "lint"
          }
        },
        {
          "plugin": "@nx/jest/plugin",
          "options": {
            "targetName": "test"
          }
        }
      ],
      "targetDefaults": {
        "e2e-ci--**/*": {
          "dependsOn": ["^build"]
        }
      },
      "generators": {
        "@nx/next": {
          "application": {
            "style": "tailwind",
            "linter": "eslint"
          }
        }
      }
    }
    ```

    ```json title="project.json"
    {
      "name": "starter",
      "$schema": "../../node_modules/nx/schemas/project-schema.json",
      "sourceRoot": "apps/starter",
      "projectType": "application",
      "tags": [],
      "// targets": "to see all targets run: nx show project starter --web",
      "targets": {}
    }
    ```
  </Tab>
</Tabs>

## Migration steps

Our goal for this migration is to get a working Turborepo task as quickly as possible, so that you can adopt Turborepo features incrementally. We’ll start by using the Nx scaffolder to create a repository with a Next.js app.

```bash title="Terminal"
npx create-nx-workspace --preset=next --ci=skip --e2eTestRunner=none --style=tailwind --nextAppDir=true --nextSrcDir=false --packageManager=pnpm --appName=starter
```

### Step 1: Update .gitignore

Turborepo uses the .turbo directory to hold local caches and other information about your repository. For this reason, it should be added to your `.gitignore`.

```txt title=".gitignore"
.turbo
```

### Step 2: Add a workspace definition

Turborepo is built on top of package manager workspaces, a JavaScript ecosystem standard. Add the directory paths to the workspace that will contain packages.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```yml title="pnpm-workspace.yaml"
    packages:
      - apps/*
    ```
  </Tab>

  <Tab value="yarn">
    ```json title="package.json"
    {
      "workspaces": ["apps/*"]
    }
    ```
  </Tab>

  <Tab value="npm">
    ```json title="package.json"
    {
      "workspaces": ["apps/*"]
    }
    ```
  </Tab>

  <Tab value="bun">
    ```json title="package.json"
    {
      "workspaces": ["apps/*"]
    }
    ```
  </Tab>
</Tabs>

### Step 3: Add a package.json to the application

Rather than adding additional configuration files like `project.json`, Turborepo uses the standard `package.json` file.

Add a `package.json` to the `starter` application. Create a `package.json` at `./apps/starter/package.json` that contains a `dev` and `build` script.

```json title="./apps/starter/package.json"
{
  "name": "starter",
  "scripts": {
    "dev": "next dev",
    "build": "next build"
  }
}
```

### Step 4: Remove Nx plugin

Remove the Nx plugin from ./apps/starter/next.config.js. The example file below doesn’t have configuration, though your existing Next.js application may need some.

```js title="./apps/starter/next.config.js"
/** @type {import('next').NextConfig} */
const nextConfig = {};

module.exports = nextConfig;
```

### Step 5: Add the `packageManager` field

The root package.json needs to have the `packageManager` field. This ensures developers in the repository use the correct package manager, and that Turborepo can optimize your package graph based on your lockfile.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```json title="./package.json"
    {
      "packageManager": "pnpm@9.0.0"
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```json title="./package.json"
    {
      "packageManager": "yarn@1.22.19"
    }
    ```
  </Tab>

  <Tab value="npm">
    ```json title="./package.json"
    {
      "packageManager": "npm@10.0.0"
    }
    ```
  </Tab>

  <Tab value="bun">
    ```json title="./package.json"
    {
      "packageManager": "bun@1.2.0"
    }
    ```
  </Tab>
</Tabs>

### Step 6: Run you package manager's install command

Update your lockfile by running your installation command.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm install
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn install
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bun install
    ```
  </Tab>
</Tabs>

Once you've done this, you should see a lockfile diff, indicating that the package has been added to the package manager's workspace.

### Step 7: Install Turborepo

Add Turborepo to the root `package.json` of the workspace.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm add turbo --save-dev --workspace-root
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
     yarn add turbo --save-dev --ignore-workspace-root-check
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install turbo --save-dev
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bun install turbo --dev
    ```
  </Tab>
</Tabs>

You can also optionally install `turbo` globally for added convenience when working with Turborepo.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm add turbo --global
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn global add turbo
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install turbo --global
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bun install turbo --global
    ```
  </Tab>
</Tabs>

### Step 8: Add a `turbo.json`

Create a `turbo.json` at the root to register your tasks and describe their task dependencies.

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Step 9: Run `turbo build`

Build the application with Turborepo. Using global `turbo`, this would be `turbo build`. You can also run the command through your package manager:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm exec turbo build
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
     yarn dlx turbo build
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx turbo run build
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx turbo run build
    ```
  </Tab>
</Tabs>

### Step 10: Enable Remote Caching (optional)

By default, Turborepo will connect to the free-to-use Vercel Remote Cache when you run:

```bash title="Terminal"
turbo login
turbo link
```

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

### CLI equivalents

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
    ```json title="pnpm-workspace.yaml"
    packages:
      - "apps/*"
      - "packages/*"
      - "cli" // [!code highlight]
    ```

    <LinkToDocumentation href="https://pnpm.io/pnpm-workspace_yaml">pnpm workspace documentation</LinkToDocumentation>
  </Tab>

  <Tab value="yarn">
    ```json title="./package.json"
    {
      "workspaces": [
        "apps/*"
        "packages/*",
        "cli" // [!code highlight]
      ]
    }
    ```

    <LinkToDocumentation href="https://yarnpkg.com/features/workspaces#how-are-workspaces-declared">yarn workspace documentation</LinkToDocumentation>
  </Tab>

  <Tab value="npm">
    ```json title="./package.json"
    {
      "workspaces": [
        "apps/*"
        "packages/*",
        "cli" // [!code highlight]
      ]
    }
    ```

    <LinkToDocumentation href="https://docs.npmjs.com/cli/v7/using-npm/workspaces#defining-workspaces">npm workspace documentation</LinkToDocumentation>
  </Tab>

  <Tab value="bun">
    ```json title="./package.json"
    {
      "workspaces": [
        "apps/*"
        "packages/*",
        "cli" // [!code highlight]
      ]
    }
    ```

    <LinkToDocumentation href="https://bun.sh/docs/install/workspaces">Bun workspace documentation</LinkToDocumentation>
  </Tab>
</Tabs>

Then, add a `package.json` to the directory:

```json title="./cli/package.json"
{
  "name": "@repo/rust-cli",
  "scripts": {
    "build": "cargo build --release"
  }
}
```

Now, when you use `turbo build`, the `"build"` script in `./cli/package.json` will be included into the tasks that `turbo` runs.

## Caching build artifacts

Ensure that the outputs for your builds are being cached with [the outputs key](/docs/reference/configuration#outputs) in `turbo.json`. In the case of a Rust CLI being compiled with cargo, a release build would be created in the `target/release` directory and we can cache it using:

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputs": ["target/release/**"] // [!code highlight]
    }
  }
}
```

## Creating dependency relationships

Because the directory is now a part of the package manager's workspace, you can create dependencies exactly the same as you do for your JavaScript packages.

For instance, if you wanted to make sure that the `rust-cli` "package" from above is built before your `web` application, install it into the dependencies for the `web` application:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```diff title="./web/package.json"
    {
      "devDependencies": {
    +   "@repo/rust-cli": "workspace:*"
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```diff title="./web/package.json"
    {
      "devDependencies": {
    +   "@repo/rust-cli": "*"
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```diff title="./web/package.json"
    {
      "devDependencies": {
    +   "@repo/rust-cli": "*"
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```diff title="./web/package.json"
    {
      "devDependencies": {
    +   "@repo/rust-cli": "workspace:*"
      }
    }
    ```
  </Tab>
</Tabs>

Given a `turbo.json` with a `build` task like:

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "target/release/**"]
    }
  }
}
```

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

## Bundling

Unlike [Internal Packages](/docs/crafting-your-repository/creating-an-internal-package), external packages can be deployed to [npm](https://www.npmjs.com) *and* used locally. In this guide, we'll bundle a package to both [ECMAScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) (`esm`) and [CommonJS modules](https://en.wikipedia.org/wiki/CommonJS) (`cjs`), the most commonly used formats on npm.

## Setting up a build script

Let's start with a package created using the [Internal Packages](/docs/crafting-your-repository/creating-an-internal-package) tutorial.

There, we created a `@repo/math` package which contained a few helper functions for adding and subtracting numbers. We've decided that this package is good enough for npm, so we're going to bundle it.

We're going to add a `build` script to `@repo/math`, using a bundler. If you're unsure which one to choose, we recommend [`tsup`](https://tsup.egoist.dev/).

Install `tsup` inside the `./packages/math` package using your package manager and then create a build script for it:

```json title="./packages/math/package.json"
{
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts"
  }
}
```

`tsup` outputs files to the `dist` directory by default, so you should:

1. Add `dist` to your `.gitignore` files to make sure they aren't committed to source control.
2. Add `dist` to the outputs of `build` in your `turbo.json`.

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputs": ["dist/**"]
    }
  }
}
```

That way, when `tsup` is run the outputs can be [cached](/docs/crafting-your-repository/caching) by Turborepo.

Finally, we should update our package entrypoints. Inside `package.json`, change `main` to point at `./dist/index.js` for clients using CommonJS modules (`cjs`), `module` to point at `./dist/index.mjs` for clients using ECMAScript modules (`esm`), and `types` to the type definition file - `./dist/index.d.ts`:

```json title="./packages/math/package.json"
{
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts"
}
```

<Callout>
  It is not required to bundle to both `cjs` and `esm`. However, it is recommended, as it allows your package to be used in a wider variety of environments.

  If you run into errors by using `main`, `module` and `types`, take a look at the [tsup docs](https://tsup.egoist.dev/#bundle-formats).

  Bundling is a complicated topic, and we don't have space here to cover everything!
</Callout>

### Building our package before our app

Before we can run `turbo run build`, there's one thing we need to consider. We've just added a [task dependency](/docs/crafting-your-repository/running-tasks) into our monorepo. The `build` of `packages/math` needs to run **before** the `build` of `apps/web`.

Fortunately, we can use [`dependsOn`](/docs/reference/configuration#dependson) to easily configure this.

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

Now, we can run `turbo run build`, and it'll automatically build our packages *before* it builds our app.

### Setting up a dev script

There's a small issue with our setup. We are building our package just fine, but it's not working great in dev. Changes that we make to our `@repo/math` package aren't being reflected in our app.

That's because we don't have a `dev` script to rebuild our packages while we're working. We can add one easily:

```json title="./packages/math/package.json"
// [!code word:--watch]
{
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch"
  }
}
```

This passes the `--watch` flag to `tsup`, meaning it will watch for file changes.

If we've already set up [dev scripts](/docs/crafting-your-repository/developing-applications#configuring-development-tasks) in our `turbo.json`, running `turbo run dev` will run our `packages/math` dev task in parallel with our `apps/web` dev task.

Our package is now in a spot where we can consider deploying to npm. In our [versioning and publishing](#versioning-and-publishing) section, we'll do just that.

## Versioning and publishing

Manually versioning and publishing packages in a monorepo can be tiresome. Luckily, there's a tool that makes things easy - the [Changesets](https://github.com/changesets/changesets) CLI.

We recommend Changesets because it's intuitive to use, and - just like Turborepo - fits with the monorepo tools you're already used to.

Some alternatives are:

* [intuit/auto](https://github.com/intuit/auto) - Generate releases based on semantic version labels on pull requests
* [microsoft/beachball](https://github.com/microsoft/beachball) - The Sunniest Semantic Version Bumper

## Publishing

Once your package has been bundled, you can then publish it to the npm registry.

We recommend taking a look at the Changesets docs. Here's our recommended reading order:

1. [Why use changesets?](https://github.com/changesets/changesets/blob/main/docs/intro-to-using-changesets.md) - an intro that takes you through the fundamentals.
2. [Installation instructions](https://github.com/changesets/changesets/blob/main/packages/cli/README.md)
3. If you're using GitHub, consider using the [Changeset GitHub bot](https://github.com/apps/changeset-bot) - a bot to nudge you to add changesets to PR's.
4. You should also consider adding the [Changesets GitHub action](https://github.com/changesets/action) - a tool which makes publishing extremely easy.

## Using Changesets with Turborepo

Once you've started using Changesets, you'll gain access to three useful commands:

```bash title="Terminal"
# Add a new changeset
changeset

# Create new versions of packages
changeset version

# Publish all changed packages to npm
changeset publish
```

Linking your publishing flow into Turborepo can make organizing your deploy a lot simpler and faster.

Our recommendation is to configure Changesets to automatically commit `changeset version`'s changes

```json title="./.changeset/config.json"
{
  // …
  "commit": true
  // …
}
```

and add a `publish-packages` script into your root `package.json`:

```json title="./package.json"
{
  "scripts": {
    // Include build, lint, test - all the things you need to run
    // before publishing
    "publish-packages": "turbo run build lint test && changeset version && changeset publish"
  }
}
```

If your packages are public, set Changeset's `access` to `public`:

```json title="./.changeset/config.json"
{
  // …
  "access": "public"
  // …
}
```

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
    ```bash title="Terminal"
    pnpm add turbo --save-dev
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn add turbo --dev
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install turbo --save-dev
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bun install turbo --dev
    ```
  </Tab>
</Tabs>

### Running a `package.json` script using global `turbo` (optional)

For even faster developer workflows, you can [install `turbo` globally](/docs/getting-started/installation#global-installation), too, and run commands directly from the command line.

Once installed, you can run `turbo build` and Turborepo will run your `build` script from `package.json`. Running `turbo build` again will hit the cache.

At this point, `turbo` isn't providing much value since you're likely to only be rebuilding your application when code changes and, when your code changes, `turbo` will miss the cache. In two short steps, you can get more out of `turbo`.

## Running many scripts with one command

In many repositories, there are setup tasks or pre-build steps to run. These tasks are often run one at a time - but you can easily turn them into one script with `turbo`.

For example, let's say you have a project where we always have to set up a development environment whenever you start working. You need to:

1. Start a Docker container for a database.
2. Push a database schema to the database.
3. Seed the database with data.
4. Start the development server.

You can schedule these tasks into one command using Turborepo. First, create scripts in your `package.json`:

```json title="package.json"
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
```

Then, create tasks in `turbo.json` to run these scripts in order:

```json title="./turbo.json"
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
```

The `dependsOn` arrays in the tasks above create a sequential order for the tasks. When you run `turbo dev`, the scripts for `db:up`, then `db:push`, then `db:seed` will be run first.

## Parallelizing tasks

Using `turbo` to parallelize tasks results in speeding up tasks by running all at once, when they can be. For instance, you can run your ESLint, TypeScript, and Prettier checks at the same time. Given scripts like:

```json title="./package.json"
{
  "scripts": {
    "lint": "eslint .",
    "format": "prettier .",
    "check-types": "tsc --noEmit"
  }
}
```

You can create a configuration like this one:

```json title="turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "lint": {},
    "format": {},
    "check-types": {}
  }
}
```

Then, to run all tasks at the same time:

```bash title="Terminal"
turbo check-types lint format
```

## Optimizing task using inputs

Because Turborepo will treat a single-package workspace as one package, it can help to optimize inputs to tasks to make sure unrelated changes don't create cache misses.

For instance, a script for checking types using `tsc --noEmit` can be configured with inputs that only include TypeScript files:

```json title="./turbo.json"
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "check-types": {
      "inputs": ["**/*.{ts,tsx}"]
    }
  }
}
```


- [Skipping tasks](/guides/skipping-tasks.md): Never do the same work twice.

import { Callout } from '#components/callout';

[Caching](/docs/crafting-your-repository/caching) dramatically speeds up your tasks - but you may be able to go even faster by using `npx turbo-ignore`. If a workspace is unaffected by your code changes, you can completely skip executing a task altogether.

Let's say you want to skip the unit tests for your `web` workspace when there aren't any changes to your `web` application (or its package dependencies). If you are already using [Remote Caching](https://turborepo.com/docs/core-concepts/remote-caching), you will probably get a cache hit - but you would still spend time provisioning the CI container, installing `npm` dependencies, and other things that can take a while.

Ideally, you would do a quick check to see if any of that work needs to happen in the first place.

***

After you've checked out the repo, but **before** any other work, you can take a few seconds to check that your `web` tests have changed since the parent commit.

```bash title="Terminal"
npx turbo-ignore web --task=test
```

This command will:

1. Filter for the `web` workspace.
2. Create the `dry` output for your `test` task compared to your parent commit.
3. Parse the output to determine which packages have changed.
4. Exit with a `1` code if changes are detected. Otherwise, exits with a `0`.

While you may have been able to hit a `>>> FULL TURBO` cache for this task, you just saved time with all of the other setup tasks required to run your CI.

## Using `turbo-ignore`

To skip unaffected work, first ensure that your Git history is available on the machine. Then, run `npx turbo-ignore`.

`turbo-ignore` uses a combination of the `--filter` and `--dry=json` flags to find changes from the parent commit to the current commit to identify affected packages. By default, `turbo-ignore` finds the difference for the **build task in the current working directory**, but you can [customize this behavior with flags](#customizing-behavior).

Here's an example of the command that will be built and run:

```bash title="Terminal"
npx turbo run build --filter=@example/web...3c8387ffd98b751305fe3f0284befdd00cbd4610 --dry=json
```

Note that a dry run does not *execute* the build task. Instead, it checks your packages to see if your code changes will affect your build (or other task) in only a few seconds.

If `turbo-ignore` finds that the task can be skipped, it will exit the process with a `0` code. If changes have been found, the process will exit with `1`.

<Callout type="info">
  On Vercel, the previously deployed SHA will be used instead of the parent
  commit.
</Callout>

## Customizing behavior

To specify a workspace, you can add it to your command like:

```bash title="Terminal"
npx turbo-ignore web
```

where `web` is your workspace's name running the default `build` task.

If you'd like to change the task, use the `--task` flag to specify the task for the command that `turbo-ignore` will invoke.

## Using `turbo-ignore` on Vercel

To use `npx turbo-ignore` on Vercel, you can use the [Ignored Build Step](https://vercel.com/docs/concepts/projects/overview#ignored-build-step) feature. Vercel will automatically infer the correct arguments to successfully run `turbo-ignore`.

## Customizing behavior

When not on Vercel, specify a commit for comparison using the `--fallback` flag.

On Vercel, you can specify the `--fallback` flag to give Vercel a git ref to compare against when the default comparison is not available. By default, Vercel compares to the most recently deployed SHA so this is useful for use cases like avoiding a deploy for the first commit to a branch.


- [Invalid environment variable prefix](/messages/invalid-env-prefix.md): Learn more about errors with invalid environment variable prefixes in Turborepo.

## Why this error occurred

When declaring environment variables in your `turbo.json`, you cannot prefix them with `$`. This
was an old syntax for declaring a dependency on an environment variable that was deprecated in Turborepo 1.5.

```json title="./turbo.json"
{
  "globalEnv": ["$MY_ENV_VAR"]
}
```

The environment variable declared above has the `$` prefix.

## Solution

Remove the `$` prefix from your environment variable declaration.

```json title="./turbo.json"
{
  "globalEnv": ["MY_ENV_VAR"]
}
```

You can migrate to the `env` and `globalEnv` keys using `npx @turbo/codemod migrate-env-var-dependencies`.
Check out [the codemod's documentation for more details](/docs/reference/turbo-codemod#turborepo-1x).


- [Missing root task in turbo.json](/messages/missing-root-task-in-turbo-json.md): Learn more about errors for missing root tasks in turbo.json in Turborepo.

## Why this error occurred

Root tasks are the scripts defined in the monorepo's root `package.json`. These tasks often call `turbo`. For example:

```json title="./package.json"
{
  "scripts": {
    "build": "turbo run build"
  }
}
```

This creates a problem when we declare [topological dependencies](/docs/reference/configuration#dependson). Topological
dependencies specify that your package's dependencies should execute their tasks before your package executes its own task.

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

Because the root package is a dependency for all packages inside your workspace, its task would get executed first.
But since its task calls `turbo`, this would cause an infinite loop.

## Solution

As long as the root task does *not* call `turbo`, you can add it to the `tasks` field in `turbo.json`:

```json title="./turbo.json"
{
  "tasks": {
    "//#build": {}
  }
}
```

This will permit tasks to depend on `//#build`.

However, if the root task does call `turbo`, this can cause infinite recursion. In this case, we don't recommend depending
on the root task. Instead, you can determine the tasks that this root task depends on, and depend on those directly.
For instance, if `//#build` depends on `app#lint` and `docs#lint`, then you can declare those as dependencies.


- [Package task in single-package workspace error](/messages/package-task-in-single-package-workspace.md): Learn more about errors with package tasks in single-package workspaces.

## Why this error occurred

In single package mode, there cannot be multiple packages in your repository. Therefore, declaring a task in the
`turbo.json` with a specified package name is not permitted.

```json title="./turbo.json"
{
  "tasks": {
    "app#build": {
      "cache": true
    }
  }
}
```

## Solution

Remove the package name from the task declaration.

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "cache": true
    }
  }
}
```

Alternatively, if you would like to have multiple packages, you can [specify the workspaces in your repository](/docs/getting-started/add-to-existing-repository).


- [Recursive `turbo` invocations](/messages/recursive-turbo-invocations.md): Learn more about errors with recursive scripts and tasks in Turborepo.

## Why this error occurred

When a cycle of `turbo` invocations is detected in a [single-package workspace](https://turborepo.com/docs/guides/single-package-workspaces), Turborepo will error to prevent the recursive calls to itself. Typically, this situation occurs for one of two reasons:

### Recursion in scripts and tasks

In a single-package workspace, a script in `package.json` that calls a Turborepo task with the same name causes a loop.

```json title="./package.json"
{
  "scripts": {
    "build": "turbo run build"
  }
}
```

Calling the `build` script calls `turbo run build`. `turbo run build` then calls the `build` script, initiating the loop of recursive calls.

To resolve this, ensure that the name of the script in `package.json` is not the same as the Turborepo task. For example, to fix the snippet above, renaming the script would break the cycle:

```json title="./package.json"
{
  "scripts": {
    "build:app": "turbo run build"
  }
}
```

### Package manager Workspace misconfiguration

A misconfigured workspace can make it appear that a [multi-package workspace](https://vercel.com/docs/vercel-platform/glossary#multi-package-workspace) is a single-package workspace. This causes Turborepo to infer that the repository is of the wrong type, causing it to see the script in `package.json` to be recursive.

Your repo can end up in this state in a few ways, with the most common being that the [packages are not defined according to your package manager](https://turborepo.com/docs/crafting-your-repository/structuring-a-repository#specifying-packages-in-a-monorepo). An npm workspace that is missing the `workspaces` field in `package.json` or a pnpm workspace that is missing a `pnpm-workspace.yaml` file can result in this error message.

Check that your repository is complying with standards for multi-package workspaces and correct any issues.


- [Unnecessary package task syntax error](/messages/unnecessary-package-task-syntax.md): Learn more about errors with unnecessary package task syntax in Turborepo.

## Why this error occurred

Turborepo supports adding additional `turbo.json` files in a package directory
to override the `turbo.json` file declared at the repository root, a feature called [Workspace Configurations](/docs/crafting-your-repository/structuring-a-repository#specifying-packages-in-a-monorepo).
In those additional `turbo.json` files, you can only configure tasks for that specific
package. Therefore, only the task name should be included in the task,
not the package and task name (`package#task`).

`turbo.json` file in `apps/web` directory:

```json title="./turbo.json"
{
  "tasks": {
    "web#build": {
      "dependsOn": ["lint"]
    }
  }
}
```

Since this `turbo.json` file is inside a package directory, the `web` prefix is unnecessary.

## Solution

Remove the package prefix from the task name:

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["lint"]
    }
  }
}
```


- [bin](/reference/bin.md): API reference for the `turbo bin` command

Get the path to the `turbo` binary.

```bash title="Terminal"
turbo bin
```

When using [**global `turbo`**](/docs/getting-started/installation#global-installation), this will be the path to the global `turbo` binary. You're likely to see a path to the global directory of the package manager you used to install `turbo`.

When using [**local `turbo`**](/docs/getting-started/installation#repository-installation), this will be the path to the local `turbo` binary. When `turbo` is installed in your repository, it is likely to be a path to `node_modules`.


- [boundaries](/reference/boundaries.md): API reference for the `turbo boundaries` command

import { ExperimentalBadge } from '#components/experimental-badge';
import { Callout } from '#components/callout';

<ExperimentalBadge>Experimental</ExperimentalBadge>

Boundaries ensure that Turborepo features work correctly by checking for package manager Workspace violations.

```bash title="Terminal"
turbo boundaries
```

<Callout title="Boundaries RFC">
  This feature is experimental, and we're looking for your feedback on [the
  Boundaries RFC](https://github.com/vercel/turborepo/discussions/9435).
</Callout>

This command will notify for two types of violations:

* Importing a file outside of the package's directory
* Importing a package that is not specified as a dependency in the package's `package.json`

## Tags

Boundaries also has a feature that lets you add tags to packages. These tags can be used to create rules
for Boundaries to check. For example, you can add an `internal` tag to your UI package:

```json title="./packages/ui/turbo.json"
{
  "tags": ["internal"]
}
```

And then declare a rule that packages with a `public` tag cannot depend on packages with an `internal` tag:

```json title="./turbo.json"
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
```

Alternatively, you may want `public` packages to only depend on other `public` packages:

```json title="turbo.json"
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
```

Likewise, you can add restrictions for a tag's dependents, i.e. packages that import packages with the tag.

```json title="turbo.json"
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
```

Package names can also be used in place of a tag in allow and deny lists.

```json title="turbo.json"
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
```

Tags allow you to ensure that the wrong package isn't getting imported somewhere in your graph. These rules are
applied even for dependencies of dependencies, so if you import a package that in turn imports another package
with a denied tag, you will still get a rule violation.


- [Configuring turbo.json](/reference/configuration.md): Learn how to configure Turborepo through `turbo.json`.

import { Callout } from '#components/callout';
import { InVersion } from '#components/in-version';
import { ExperimentalBadge } from '#components/experimental-badge';
import Link from 'next/link';

Configure the behavior of `turbo` by using a `turbo.json` file in your Workspace's root directory. You can also:

* Use [Package Configurations](/docs/reference/package-configurations) for more granular control.
* Use `turbo.jsonc` to add comments to your configuration with IDE support.

## Global options

### `extends`

```jsonc title="./apps/web/turbo.json"
{
  "extends": ["//"]
}
```

Extend from the root `turbo.json` to create specific configuration for a package using [Package Configurations](/docs/reference/package-configurations).

* By default, the only valid value for `extends` is `["//"]` to inherit configuration from the root `turbo.json`.
* With the [`futureFlags.nonRootExtends`](#nonrootextends) flag enabled, you can also extend from other packages (e.g., `["//", "shared-config"]`).
* If `extends` is used in the root `turbo.json`, it will be ignored.

### `globalDependencies`

```jsonc title="./turbo.json"
{
  "globalDependencies": [".env", "tsconfig.json"]
}
```

A list of globs that you want to include in all task hashes. **If any file matching these globs changes, all tasks will miss cache.** Globs are relative to the location of `turbo.json`.

By default, only the root package.json and lockfile are included in [the global hash](/docs/crafting-your-repository/caching) and can't be ignored. Any added `globalDependencies` will also be included in the global hash.

<Callout type="error">
  Globs must be in the repository's source control root. Globs outside of the
  repository aren't supported.
</Callout>

### `globalEnv`

```jsonc title="./turbo.json"
{
  "globalEnv": ["GITHUB_TOKEN", "PACKAGE_VERSION", "NODE_ENV"]
}
```

A list of environment variables that you want to impact the hash of all tasks. Any change to these environment variables will cause all tasks to miss cache.

For more on wildcard and negation syntax, [see the `env` section](#env).

### `globalPassThroughEnv`

```jsonc title="./turbo.json"
{
  "globalPassThroughEnv": ["AWS_SECRET_KEY", "GITHUB_TOKEN"]
}
```

A list of environment variables that you want to make available to tasks. Using this key opts all tasks into [Strict Environment Variable Mode](/docs/crafting-your-repository/using-environment-variables#strict-mode).

Additionally, Turborepo has a built-in set of global passthrough variables for common cases, like operating system environment variables. This includes variables like `HOME`, `PATH`, `APPDATA`, `SHELL`, `PWD`, and more. The full list can be found [in the source code](https://github.com/vercel/turborepo/blob/main/crates/turborepo-lib/src/task_hash.rs).

<Callout type="warn" title="Passthrough values do not contribute to hashes for caching">
  If you want changes in these variables to cause cache misses, you will need to
  include them in [`env`](#env) or [`globalEnv`](#globalenv).
</Callout>

### `ui`

Default: `"stream"`

Select a terminal UI for the repository.

`"tui"` allows for viewing each log at once and interacting with the task. `"stream"` outputs logs as they come in and is not interactive.

```json title="./turbo.json"
{
  "ui": "tui" | "stream"
}
```

### `noUpdateNotifier`

Default: `false`

When set to `true`, disables the update notification that appears when a new version of `turbo` is available.

```json title="./turbo.json"
{
  "noUpdateNotifier": true
}
```

### `concurrency`

Default: `"10"`

Set/limit the maximum concurrency for task execution. Must be an integer greater than or equal to `1` or a percentage value like `50%`.

* Use `1` to force serial execution (one task at a time).
* Use `100%` to use all available logical processors.
* This option is ignored if the [`--parallel`](/docs/reference/run#--parallel) flag is also passed.

```jsonc title="./turbo.json"
{
  "concurrency": "1"
}
```

### `dangerouslyDisablePackageManagerCheck`

Default: `false`

Turborepo uses your repository's lockfile to determine caching behavior, [Package Graphs](https://turborepo.com/docs/core-concepts/internal-packages), and more. Because of this, we use [the `packageManager` field](https://nodejs.org/api/packages.html#packagemanager) to help you stabilize your Turborepo.

To help with incremental migration or in situations where you can't use the `packageManager` field, you may use `--dangerously-disable-package-manager-check` to opt out of this check and assume the risks of unstable lockfiles producing unpredictable behavior. When disabled, Turborepo will attempt a best-effort discovery of the intended package manager meant for the repository.

```jsonc title="./turbo.json"
{
  "dangerouslyDisablePackageManagerCheck": true
}
```

<Callout type="info">
  You may also opt out of this check via
  [`flag`](/docs/reference/run#--dangerously-disable-package-manager-check) or
  the
  [`TURBO_DANGEROUSLY_DISABLE_PACKAGE_MANAGER_CHECK`](https://turborepo.com/docs/reference/system-environment-variables)
  environment variable.
</Callout>

### `cacheDir`

Default: `".turbo/cache"`

Specify the filesystem cache directory.

```jsonc title="./turbo.json"
{
  "cacheDir": ".turbo/cache"
}
```

### `daemon`

Default: `true`

Turborepo runs a background process to pre-calculate some expensive operations. This standalone process (daemon) is a performance optimization, and not required for proper functioning of `turbo`.

```jsonc title="./turbo.json"
{
  "daemon": true
}
```

<Callout type="good-to-know">
  When running in a CI environment the daemon is always disabled regardless of
  this setting.
</Callout>

### `envMode`

Default: `"strict"`

Turborepo's Environment Modes allow you to control which environment variables are available to a task at runtime:

* `"strict"`: Filter environment variables to only those that are specified in the `env` and `globalEnv` keys in `turbo.json`.
* `"loose"`: Allow all environment variables for the process to be available.

```jsonc title="./turbo.json"
{
  "envMode": "strict"
}
```

Read more about [Environment Modes](/docs/crafting-your-repository/using-environment-variables#environment-modes).

### `futureFlags`

```jsonc title="./turbo.json"
{
  "futureFlags": {
    "turboExtendsKeyword": true
  }
}
```

Enable experimental features that will become the default behavior in future versions of Turborepo.

<Callout type="info">
  `futureFlags` can only be set in the root `turbo.json`. An error will be
  thrown if set in a [Package
  Configuration](/docs/reference/package-configurations).
</Callout>

#### `turboExtendsKeyword`

Default: `false`

When enabled, allows using the [`$TURBO_EXTENDS$`](#turbo_extends) microsyntax in array fields. This microsyntax changes the behavior of [Package Configurations](/docs/reference/package-configurations) from replacing array fields to appending to them.

#### `nonRootExtends` <ExperimentalBadge>Pre-release</ExperimentalBadge>

Default: `false`

When enabled, allows [Package Configurations](/docs/reference/package-configurations) to extend from other packages' `turbo.json` files, not just the root. This enables composing shared task configurations across packages.

```jsonc title="./turbo.json"
{
  "futureFlags": {
    "nonRootExtends": true
  }
}
```

With this flag enabled, packages can extend from multiple configurations:

```jsonc title="./apps/web/turbo.json"
{
  "extends": ["//", "ui"],
  "tasks": {
    "build": {}
  }
}
```

<Callout type="warn">
  When using `nonRootExtends`, the root configuration (`"//"`) must always be
  listed **first** in the `extends` array.
</Callout>

See the [Package Configurations documentation](/docs/reference/package-configurations#extending-from-other-packages-pre-release) for more details and examples.

### `tags` <ExperimentalBadge>Experimental</ExperimentalBadge>

```jsonc title="./apps/web/turbo.json"
{
  "tags": ["utils"]
}
```

Adds a tag to a package for use with [Boundaries](/docs/reference/boundaries).

This key only works in [Package Configurations](/docs/reference/package-configurations). Using this key in a root `turbo.json` will result in an error.

## Defining tasks

### `tasks`

Each key in the `tasks` object is the name of a task that can be executed by [`turbo run`](/docs/reference/run). Turborepo will search the packages described in your [Workspace's configuration](/docs/crafting-your-repository/structuring-a-repository#specifying-packages-in-a-monorepo) for scripts in `package.json` with the name of the task.

Using the rest of the configuration described in the task, Turborepo will run the scripts in the described order, caching logs and file outputs in [the `outputs` key](#outputs) when provided.

In the example below, we've defined three tasks under the `tasks` key: `build`, `test`, and `dev`.

```jsonc title="./turbo.json"
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
```

## Task options

Using the options available in the tasks you define in `tasks`, you can describe how `turbo` will run your tasks.

### `extends` (task-level) <ExperimentalBadge>Pre-release</ExperimentalBadge>

<Callout type="info">
  This feature requires enabling
  [`futureFlags.nonRootExtends`](#nonrootextends-pre-release) in your root
  `turbo.json`.
</Callout>

Controls whether a task inherits configuration from the extends chain. This option is only available in [Package Configurations](/docs/reference/package-configurations), not in the root `turbo.json`.

```jsonc title="./packages/ui/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "lint": {
      "extends": false // Exclude this task from the package
    }
  }
}
```

| Value            | Behavior                                                                                                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `false`          | Task is excluded from inheritance. If no other config is provided, the task won't exist for this package. If other config is provided, creates a fresh task definition with no inheritance. |
| `true` (default) | Task inherits configuration normally from the extends chain.                                                                                                                                |

See [Excluding tasks from inheritance](/docs/reference/package-configurations#excluding-tasks-from-inheritance-pre-release) for examples and more details.

### `dependsOn`

A list of tasks that are required to complete before the task begins running.

There are three types of `dependsOn` relationships: [dependency relationships](#dependency-relationships), [same-package relationships](#same-package-relationships), and [arbitrary task relationships](#arbitrary-task-relationships).

#### Dependency relationships

Prefixing a string in `dependsOn` with a `^` tells `turbo` that the task must wait for tasks in the package's dependencies to complete first. For example, in the `turbo.json` below:

```jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

`turbo` starts at the "bottom" of the package graph and recursively visits each package until it finds a package with no internal dependencies. It will then run the `build` task at the end of the dependency chain first, working its way back to the "top" until all `build` tasks are completed in order.

#### Same package relationships

Task names without the `^` prefix describe a task that depends on a different task within the same package. For example, in the `turbo.json` below:

```jsonc title="./turbo.json"
{
  "tasks": {
    "test": {
      "dependsOn": ["lint", "build"]
    }
  }
}
```

The `test` task will only run after the `lint` and `build` tasks have completed **in the same package**.

#### Arbitrary task relationships

Specify a task dependency between specific package tasks.

```json title="./turbo.json"
{
  "tasks": {
    "web#lint": {
      "dependsOn": ["utils#build"]
    }
  }
}
```

In this `turbo.json`, the `web#lint` task will wait for the `utils#build` task to complete.

### `env`

The list of environment variables a task depends on.

```jsonc title="./turbo.json"
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
```

<Callout type="good-to-know">
  Turborepo automatically includes environment variables prefixed by common
  frameworks through [Framework
  Inference](/docs/crafting-your-repository/using-environment-variables#framework-inference).
  For example, if your package is a Next.js project, you do not need to specify
  any environment variables that [start with
  `NEXT_PUBLIC_`](https://nextjs.org/docs/basic-features/environment-variables#exposing-environment-variables-to-the-browser).
</Callout>

#### Wildcards

Turborepo supports wildcards for environment variables so you can easily account for all environment variables with a given prefix. For example, the `turbo.json` below include all environment variables that start with `MY_API_` into the hash:

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "env": ["MY_API_*"]
    }
  }
}
```

#### Negation

A leading `!` means that the entire pattern will be negated. For instance, the `turbo.json` below will ignore the `MY_API_URL` variable.

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "env": ["!MY_API_URL"]
    }
  }
}
```

#### Examples

| Pattern    | Description                                                                    |
| ---------- | ------------------------------------------------------------------------------ |
| `"*"`      | Matches every environment variable.                                            |
| `"!*"`     | Excludes every environment variable.                                           |
| `"FOO*"`   | Matches `FOO`, `FOOD`, `FOO_FIGHTERS`, etc.                                    |
| `"FOO\*"`  | Resolves to `"FOO*"` and matches `FOO`, `FOOD`, and `FOO_FIGHTERS`.            |
| `"FOO\\*"` | Matches a single environment variable named `FOO*`.                            |
| `"!FOO*"`  | Excludes all environment variables that start with `FOO`.                      |
| `"\!FOO"`  | Resolves to `"!FOO"`, and excludes a single environment variable named `!FOO`. |
| `"\\!FOO"` | Matches a single environment variable named `!FOO`.                            |
| `"FOO!"`   | Matches a single environment variable named `FOO!`.                            |

### `passThroughEnv`

An allowlist of environment variables that should be made available to this task's runtime, even when in [Strict Environment Mode](/docs/crafting-your-repository/using-environment-variables#strict-mode).

```jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      // Values will be available within `build` scripts
      "passThroughEnv": ["AWS_SECRET_KEY", "GITHUB_TOKEN"]
    }
  }
}
```

<Callout type="warn">
  Values provided in `passThroughEnv` do not contribute to the cache key for the
  task. If you'd like changes to these variables to cause cache misses, you will
  need to include them in [`env`](#env) or [`globalEnv`](#globalenv).
</Callout>

### `outputs`

A list of file glob patterns relative to the package's `package.json` to cache when the task is successfully completed.

See [`$TURBO_ROOT$`](#turbo_root) if output paths need to be relative to the repository root.

```jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      // Cache all files emitted to the packages's `dist` directory
      "outputs": ["dist/**"]
    }
  }
}
```

Omitting this key or passing an empty array tells `turbo` to cache nothing (except logs, which are always cached when caching is enabled).

### `cache`

Default: `true`

Defines if task outputs should be cached. Setting `cache` to false is useful for long-running development tasks and ensuring that a task always runs when it is in the task's execution graph.

```jsonc title="./turbo.json"
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
```

### `inputs`

Default: `[]`, all files in the package that are checked into source control

A list of file glob patterns relative to the package's `package.json` to consider when determining if a package has changed. The following files are **always** considered inputs, even if you try to explicitly ignore them:

* `package.json`
* `turbo.json`
* Package manager lockfiles

Visit the [file glob specification](/docs/reference/globs) for more information on globbing syntax.

```jsonc title="./turbo.json"
{
  "tasks": {
    "test": {
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "test/**/*.ts"]
    }
  }
}
```

<Callout type="warn">
  Using the `inputs` key opts you out of `turbo`'s default behavior of
  considering `.gitignore`. You must reconstruct the globs from `.gitignore` as
  desired or use `$TURBO_DEFAULT$` to build off of the default behavior.
</Callout>

#### `$TURBO_DEFAULT$`

Because specifying an `inputs` key immediately opts out of the default behavior, you may use
the special string `$TURBO_DEFAULT$` within the `inputs` array to restore `turbo`'s default behavior. This allows you to tweak the default behavior for more granularity.

```jsonc title="./turbo.json"
{
  "tasks": {
    "check-types": {
      // Consider all default inputs except the package's README
      "inputs": ["$TURBO_DEFAULT$", "!README.md"]
    }
  }
}
```

#### `$TURBO_ROOT$`

Tasks might reference a file that lies outside of their directory.

Starting a file glob with `$TURBO_ROOT$` will change the glob to be relative to the root of the repository instead of the package directory.

```jsonc title="./turbo.json"
{
  "tasks": {
    "check-types": {
      // Consider all Typescript files in `src/` and the root tsconfig.json as inputs
      "inputs": ["$TURBO_ROOT$/tsconfig.json", "src/**/*.ts"]
    }
  }
}
```

#### `$TURBO_EXTENDS$` <ExperimentalBadge>Pre-release</ExperimentalBadge>

<Callout type="info">
  This feature requires enabling
  [`futureFlags.turboExtendsKeyword`](#turboextendskeyword) in your root
  `turbo.json`.
</Callout>

When using [Package Configurations](/docs/reference/package-configurations), array fields completely replace the values from the root `turbo.json` by default. The `$TURBO_EXTENDS$` microsyntax changes this behavior to **append** instead of **replace**.

This microsyntax can be used in the following array fields:

* `dependsOn`
* `env`
* `inputs`
* `outputs`
* `passThroughEnv`
* `with`

For example, if your root `turbo.json` defines:

```jsonc title="./turbo.json"
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
```

A Package Configuration can add additional outputs while keeping the root outputs:

```jsonc title="./apps/web/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      // Inherits "dist/**" from root, and adds ".next/**"
      "outputs": ["$TURBO_EXTENDS$", ".next/**", "!.next/cache/**"]
    }
  }
}
```

Without `$TURBO_EXTENDS$`, the `outputs` array would be completely replaced with `[".next/**", "!.next/cache/**"]`, dropping the `"dist/**"` from the root configuration.

### `outputLogs`

Default: `full`

Set output logging verbosity. Can be overridden by the [`--output-logs`](/docs/reference/run#--output-logs-option) CLI option.

| Option        | Description                       |
| ------------- | --------------------------------- |
| `full`        | Displays all logs                 |
| `hash-only`   | Only show the hashes of the tasks |
| `new-only`    | Only show logs from cache misses  |
| `errors-only` | Only show logs from task failures |
| `none`        | Hides all task logs               |

```jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputLogs": "new-only"
    }
  }
}
```

### `persistent`

Default: `false`

Label a task as `persistent` to prevent other tasks from depending on long-running processes. Persistent tasks are made [interactive](#interactive) by default.

Because a long-running process won't exit, tasks that would depend on it would never run. Once you've labeled the task as persistent, `turbo` will throw an error if other tasks depend on it.

This option is most useful for development servers or other "watch" tasks.

```jsonc title="./turbo.json"
{
  "tasks": {
    "dev": {
      "persistent": true
    }
  }
}
```

Tasks marked with `persistent` are also `interactive` by default.

### `interactive`

Default: `false` (Defaults to `true` for tasks marked as `persistent`)

Label a task as `interactive` to make it accept inputs from `stdin` in the terminal UI. Must be used with `persistent`.

This option is most useful for scripts that can be manipulated while they are running, like Jest or Vitest.

```jsonc title="./turbo.json"
{
  "tasks": {
    "test:watch": {
      "interactive": true,
      "persistent": true
    }
  }
}
```

### `interruptible`

Default: `false`

Label a `persistent` task as `interruptible` to allow it to be restarted by `turbo watch`.

`turbo watch` watches for changes to your packages and automatically restarts tasks
that are affected. However, if a task is persistent, it will not be restarted by default.
To enable restarting persistent tasks, set `interruptible` to `true`.

### `with`

A list of tasks that will be ran alongside this task. This is most useful for long-running tasks that you want to ensure always run at the same time.

```json title="./apps/web/turbo.json"
{
  "tasks": {
    "dev": {
      "with": ["api#dev"],
      "persistent": true,
      "cache": false
    }
  }
}
```

## Boundaries

The `boundaries` tag allows you to define rules for the [`boundaries` command](/docs/reference/boundaries).

```json title="./turbo.json"
{
  "boundaries": {}
}
```

### `tags`

Each key in the `tags` object is the name of a tag that can be checked with [`turbo boundaries`](/docs/reference/boundaries).

In the configuration object for a tag, you can define rules for dependencies and dependents.

#### `dependencies` and `dependents`

Rules for a tag's dependencies and dependents.

You can add an allowlist and a denylist:

```jsonc title="./turbo.json"
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
```

Both the allowlist and the denylist can be omitted.

```jsonc title="./turbo.json"
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
```

Rules can also be added for a tag's dependents, i.e. packages that import this tag.

```jsonc title="./turbo.json"
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
```

## Remote caching

The global `remoteCache` option has a variety of fields for configuring remote cache usage

```jsonc title="./turbo.json"
{
  "remoteCache": {}
}
```

### `enabled`

Default: `true`

Enables remote caching.

When `false`, Turborepo will disable all remote cache operations, even if the repo has a valid token.
If true, remote caching is enabled, but still requires the user to login and link their repo to a remote cache.

### `signature`

Default: `false`

Enables signature verification for requests to the remote cache.
When `true`, Turborepo will sign every uploaded artifact using the value of the environment variable `TURBO_REMOTE_CACHE_SIGNATURE_KEY`.
Turborepo will reject any downloaded artifacts that have an invalid signature or are missing a signature.

### `preflight`

Default: `false`

When enabled, any HTTP request will be preceded by an OPTIONS request to determine if the request is supported by the endpoint.

### `timeout`

Default: `30`

Sets a timeout for remote cache operations.
Value is given in seconds and only whole values are accepted.
If `0` is passed, then there is no timeout for any cache operations.

### `uploadTimeout`

Default: `60`

Sets a timeout for remote cache uploads.
Value is given in seconds and only whole values are accepted.
If `0` is passed, then there is no timeout for any remote cache uploads.

### `apiUrl`

Default: `"https://vercel.com"`

Set endpoint for API calls to the remote cache.

### `loginUrl`

Default: `"https://vercel.com"`

Set endpoint for requesting tokens during `turbo login`.

### `teamId`

The ID of the Remote Cache team.
Value will be passed as `teamId` in the querystring for all Remote Cache HTTP calls.
Must start with `team_` or it will not be used.

### `teamSlug`

The slug of the Remote Cache team.
Value will be passed as `slug` in the querystring for all Remote Cache HTTP calls.


- [create-turbo](/reference/create-turbo.md): Quickly set up a new Turborepo repository from scratch.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { ExamplesTable } from '#components/examples-table';

The easiest way to get started with Turborepo is by using `create-turbo`. Use this CLI tool to quickly start building a new monorepo, with everything set up for you.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest
    ```
  </Tab>
</Tabs>

## Start with an example

The community curates a set of examples to showcase ways to use common tools and libraries with Turborepo. To bootstrap your monorepo with one of the examples, use the `--example` flag:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest --example [example-name]
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest --example [example-name]
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest --example [example-name]
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest --example [example-name]
    ```
  </Tab>
</Tabs>

Use any of the example's names below:

## Core-maintained examples

The following examples are maintained by the Turborepo core team. Dependencies are kept as up-to-date as possible and GitHub Issues are accepted and addressed for these examples.

<ExamplesTable coreMaintained />

## Community-maintained examples

The community curates a set of examples to showcase ways to use common tools and libraries with Turborepo. To bootstrap your monorepo with one of the examples, use the `--example` flag:

<ExamplesTable />

### Use a community example

You can also use a custom starter or example by using a GitHub URL. This is useful for using your own custom starters or examples from the community.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest --example [github-url]
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest --example [github-url]
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest --example [github-url]
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest --example [github-url]
    ```
  </Tab>
</Tabs>

## Options

```txt title="Terminal"
-m, --package-manager to use (choices: "npm", "yarn", "pnpm", "bun")

--skip-install: Do not run a package manager install after creating the project (Default: false)

--skip-transforms: Do not run any code transformation after creating the project (Default: false)

--turbo-version <version>: Use a specific version of turbo (default: latest)

-e, --example [name]|[github-url]: An example to bootstrap the app with. You can use an example name from the official Turborepo repo or a GitHub URL. The URL can use any branch and/or subdirectory

-p, --example-path <path-to-example>: In a rare case, your GitHub URL might contain a branch name with a slash (e.g. bug/fix-1) and the path to the example (e.g. foo/bar). In this case, you must specify the path to the example separately: --example-path foo/bar

-v, --version:  Output the current version

-h, --help: Display help for command
```


- [devtools](/reference/devtools.md): API reference for the `turbo devtools` command

import { PrereleaseBadge } from '#components/prerelease-badge';

<PrereleaseBadge />

Visualize your monorepo's package graph in the browser.

```bash title="Terminal"
turbo devtools [options]
```

This command starts a local server and opens your browser to a visualization of your monorepo's package graph.

## Options

### `--port`

The port to run the devtools server on. Defaults to `9876`.

```bash title="Terminal"
turbo devtools --port 3000
```

### `--no-open`

Do not automatically open the browser when the server starts.

```bash title="Terminal"
turbo devtools --no-open
```


- [eslint-config-turbo](/reference/eslint-config-turbo.md): Learn more about eslint-config-turbo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

[The `eslint-config-turbo` package](https://www.npmjs.com/package/eslint-config-turbo) helps you find environment variables that are used in your code that are not a part of Turborepo's hashing. Environment variables used in your source code that are not accounted for in `turbo.json` will be highlighted in your editor and errors will show as ESLint output.

## Installation

Install `eslint-config-turbo` into the location where your ESLint configuration is held:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm add eslint-config-turbo --filter=@repo/eslint-config
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn workspace @acme/eslint-config add eslint-config-turbo --dev
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install --save-dev eslint-config-turbo -w @acme/eslint-config
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    cd packages/eslint-config && bun install eslint-config-turbo --dev
    ```
  </Tab>
</Tabs>

## Usage (Flat Config `eslint.config.js`)

```js title="./packages/eslint-config/base.js"
import turboConfig from 'eslint-config-turbo/flat';

export default [
  ...turboConfig,
  // Other configuration
];
```

You can also configure rules available in the configuration:

```js title="./packages/eslint-config/base.js"
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
```

## Usage (Legacy `eslintrc*`)

Add `turbo` to the extends section of your eslint configuration file. You can omit the `eslint-config-` prefix:

```json title="./packages/eslint-config/base.json"
{
  "extends": ["turbo"]
}
```

You can also configure rules available in the configuration:

```json title="./packages/eslint-config/base.json"
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
```


- [eslint-plugin-turbo](/reference/eslint-plugin-turbo.md): Learn more about eslint-plugin-turbo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

[The `eslint-plugin-turbo` package](https://www.npmjs.com/package/eslint-plugin-turbo) helps you find environment variables that are used in your code that are not a part of Turborepo's hashing. Environment variables used in your source code that are not accounted for in `turbo.json` will be highlighted in your editor and errors will show as ESLint output.

## Installation

Install `eslint-plugin-turbo` into the location where your ESLint configuration is held:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm add eslint-plugin-turbo --filter=@repo/eslint-config
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn workspace @acme/eslint-config add eslint-plugin-turbo --dev
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm i --save-dev eslint-plugin-turbo -w @acme/eslint-config
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    cd packages/eslint-config && bun install eslint-plugin-turbo --dev
    ```
  </Tab>
</Tabs>

## Usage (Flat Config `eslint.config.js`)

ESLint v9 uses the Flat Config format seen below:

```js title="./packages/eslint-config/base.js"
import turbo from 'eslint-plugin-turbo';

export default [turbo.configs['flat/recommended']];
```

Otherwise, you may configure the rules you want to use under the rules section.

```js title="./packages/eslint-config/base.js"
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
```

## Example (Flat Config `eslint.config.js`)

```js title="./packages/eslint-config/base.js"
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
```

## Usage (Legacy `eslintrc*`)

Add `turbo` to the plugins section of your `.eslintrc` configuration file. You can omit the `eslint-plugin-` prefix:

```json title="./packages/eslint-config/base.json"
{
  "plugins": ["turbo"]
}
```

Then configure the rules you want to use under the rules section.

```json title="./packages/eslint-config/base.json"
{
  "rules": {
    "turbo/no-undeclared-env-vars": "error"
  }
}
```

## Example (Legacy `eslintrc*`)

```json title="./packages/eslint-config/base.json"
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
```


- [generate](/reference/generate.md): API reference for the `turbo generate` command

import { Callout } from '#components/callout';

Extend your Turborepo with new apps and packages.

```bash title="Terminal"
turbo generate
```

* [`turbo generate run [generator-name]`](#run-generator-name): Run custom generators defined in your repository.
* [`turbo generate workspace [options]`](#workspace): Create a new package in your repository by copying an existing one or from the start.

For more information and practical use cases for writing custom generators, visit [the "Generating code" guide](/docs/guides/generating-code).

<Callout type="good-to-know">
  `turbo gen` is an alias for `turbo generate`. Additionally, `run` is the
  default command so `turbo gen` is equivalent to `turbo generate run`.
</Callout>

## `run [generator-name]`

Run custom generators defined in your repository.

```bash title="Terminal"
turbo gen run [generator-name]
```

### Flag options

#### `--args`

Answers to pass directly to the generator's prompts.

#### `--config <path>`

Generator configuration file.

Default: `turbo/generators/config.js`

#### `--root <path>`

The root of your repository

Default: directory with root `turbo.json`

## `workspace`

Create a new workspace.

```bash title="Terminal"
turbo gen workspace [options]
```

### Flag options

#### `--name <name>`

The name for the new workspace to be used in the `package.json` `name` key. The `name` key is the unique identifier for the package in your repository.

#### `--empty`

Creates an empty workspace. Defaults to `true`.

#### `--copy <name>/<url>`

Name of local workspace within your monorepo or a fully qualified GitHub URL with any branch and/or subdirectory.

#### `--destination <path>`

Where the new workspace should be created.

#### `--type <app/package>`

The type of workspace to create (`app` or `package`).

#### `--root <path>`

The root of your repository. Defaults to the directory of the root `turbo.json`.

#### `--show-all-dependencies`

Prevent filtering dependencies by workspace type when selecting dependencies to add.

#### `--example-path <path>`, `-p <path>`

In a rare case, your GitHub URL might contain a branch name with a slash (e.g. `bug/fix-1`) and the path to the example (e.g. `foo/bar`). In this case, you must specify the path to the example separately.


- [File glob specification](/reference/globs.md): Learn about the file glob specification used by `turbo`.

File globs are used throughout Turborepo for configuring which files to include or exclude in various contexts, allowing you to specifically define the files you want `turbo` to use.

## Glob patterns

| Pattern     | Description                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------- |
| `*`         | Match all files in the directory                                                                     |
| `**`        | Recursively match all files and sub-directories                                                      |
| `some-dir/` | Match the `some-dir` directory and its contents                                                      |
| `some-dir`  | Match a file named `some-dir` or a `some-dir` directory and its contents                             |
| `some-dir*` | Match files and directories that start with `some-dir`, including contents when matching a directory |
| `*.js`      | Match all `.js` files in the directory                                                               |
| `!`         | Negate the whole glob (automatically applies `/**` to the end of the defined glob)                   |

## Examples

| Pattern            | Description                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| `dist/**`          | Match all files in the `dist` directory, its contents, and all sub-directories                    |
| `dist/`            | Match the `dist` directory and its contents                                                       |
| `dist`             | Match a file named `dist` or a `dist` directory, its contents, and all sub-directories            |
| `dist/some-dir/**` | Match all files in the `dist/some-dir` directory and all sub-directories in the current directory |
| `!dist`            | Ignore the `dist` directory and all of its contents                                               |
| `dist*`            | Match files and directories that start with `dist`                                                |
| `dist/*.js`        | Match all `.js` files in the `dist` directory                                                     |
| `!dist/*.js`       | Ignore all `.js` files in the `dist` directory                                                    |
| `dist/**/*.js`     | Recursively match all `.js` files in the `dist` directory and its sub-directories                 |
| `../scripts/**`    | Up one directory, match all files and sub-directories in the `scripts` directory                  |


- [Turborepo API reference](/reference/index.md): Learn about Turborepo's APIs using the reference.

import { Card, Cards } from '#components/card';

Turborepo's API reference is broken up into the following sections:

## Configuration

<Cards>
  <Card title="Configuring turbo.json" href="/docs/reference/configuration" description="Configure the behavior of `turbo`." />

  <Card title="Package Configurations" href="/docs/reference/package-configurations" description="Create configurations specific to a package." />

  <Card title="System environment variables" href="/docs/reference/system-environment-variables" description="Change `turbo`'s behavior using environment variables." />

  <Card title="File glob specification" href="/docs/reference/globs" description="Define files for `turbo` to use." />
</Cards>

## Commands

<Cards>
  <Card title="run" href="/docs/reference/run" description="Run tasks using `turbo`." />

  <Card title="watch" href="/docs/reference/watch" description="Dependency-aware, single-process task watcher." />

  <Card title="prune" href="/docs/reference/prune" description="Create partial monorepos for target workspaces." />

  <Card title="boundaries" href="/docs/reference/boundaries" description="Enforce best practices in your monorepo." />

  <Card title="ls" href="/docs/reference/ls" description="List packages in your monorepo." />

  <Card title="query" href="/docs/reference/query" description="Run GraphQL queries against your monorepo." />

  <Card title="generate" href="/docs/reference/generate" description="Extend your Turborepo with new apps and packages." />

  <Card title="login" href="/docs/reference/login" description="Log in to your Remote Cache provider." />

  <Card title="logout" href="/docs/reference/logout" description="Log out of your Remote Cache provider." />

  <Card title="link" href="/docs/reference/link" description="Link your repository to Remote Cache." />

  <Card title="unlink" href="/docs/reference/unlink" description="Disconnect your repository from Remote Cache." />

  <Card title="scan" href="/docs/reference/scan" description="Enable the fastest defaults for your Turborepo." />

  <Card title="bin" href="/docs/reference/bin" description="Get the path to the `turbo` binary." />

  <Card title="telemetry" href="/docs/reference/telemetry" description="Manage telemetry for the machine." />
</Cards>

## Packages

<Cards>
  <Card title="create-turbo" href="/docs/reference/create-turbo" description="Get started with Turborepo using an example." />

  <Card title="eslint-config-turbo" href="/docs/reference/eslint-config-turbo" description="Find environment variables not listed in `turbo.json`." />

  <Card title="turbo-ignore" href="/docs/reference/turbo-ignore" description="Skip work using `turbo-ignore`." />

  <Card title="@turbo/gen" href="/docs/reference/turbo-gen" description="Type definitions for Turborepo generators." />
</Cards>

## Flag syntax

Options that require a value can be passed with an equals sign, using quotes when spaces are needed.

```bash title="Terminal"
--opt=value
--opt="value with a space"
--opt value
--opt "value with a space"
```

## Global flags

### `--color`

Forces the use of color, even in non-interactive terminals. This is useful for enabling color output in CI environments like GitHub Actions that have support for rendering color.

### `--no-color`

Suppresses color in terminal output, even in interactive terminals.

### `--no-update-notifier`

Disables the update notification. This notification will be automatically disabled when running in CI environments, but can also be disabled manually via this flag.

Alternatively, you can disable the notification using [the `TURBO_NO_UPDATE_NOTIFIER` environment variable](/docs/reference/system-environment-variables).


- [info](/reference/info.md): API reference for the `turbo info` command

Print debugging information about your Turborepo.

```bash title="Terminal"
turbo info
```

Example output:

```txt title="Terminal"
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
```


- [link](/reference/link.md): API reference for the `turbo link` command

Link the repository to a Remote Cache provider.

```bash title="Terminal"
turbo link
```

The selected owner (either a user or an organization) will be able to share [cache artifacts](/docs/core-concepts/remote-caching) through [Remote Caching](/docs/core-concepts/remote-caching).

## Flag options

### `--api <url>`

Specifies the URL of your Remote Cache provider.

```bash title="Terminal"
turbo link --api=https://example.com
```

### `--yes`

Answer yes to all prompts

```bash title="Terminal"
turbo link --yes
```

### `--scope <scope>`

The scope to which you are linking. For example, when using Vercel, this is your Vercel team's slug.

```bash title="Terminal"
turbo link --scope=your-team
```


- [login](/reference/login.md): API reference for the `turbo login` command

Log in to your Remote Cache provider.

```bash title="Terminal"
turbo login
```

The default provider is [Vercel](https://vercel.com/). To specify a different provider, use the `--api` option.

## Flag options

### --api \<url>

Set the API URL of the Remote Cache provider.

```bash title="Terminal"
turbo login --api=https://acme.com/api
```

### --login \<url>

Set the URL for login requests that should dynamically generate tokens.

```bash title="Terminal"
turbo login --login=https://acme.com
```

### --sso-team \<team>

Connect to an SSO-enabled team by providing your team slug.

```bash title="Terminal"
turbo login --sso-team=slug-for-team
```

### --manual

Manually enter token instead of requesting one from a login service.


- [logout](/reference/logout.md): API reference for the `turbo logout` command

Log out of the account associated with your Remote Cache provider.

```bash title="Terminal"
turbo logout
```


- [ls](/reference/ls.md): API reference for the `turbo ls` command

import { ExperimentalBadge } from '#components/experimental-badge';

List packages in your monorepo.

```bash title="Terminal"
turbo ls [package(s)] [flags]
```

When scoped to the entire repository, output includes package manager, package count, and all package names and directories.

```bash title="Terminal"
# List all packages in the repository
turbo ls
```

When scoped to one or more packages, output includes package name, directory, internal dependencies, and all tasks.

```bash title="Terminal"
# List only two packages
turbo ls web @repo/ui [package(s)]
```

## Flags

### `--affected`

Automatically filter to only packages that are affected by changes on the current branch.

By default the changes considered are those between `main` and `HEAD`.

* You can override `main` as the default base by setting `TURBO_SCM_BASE`.
* You can override `HEAD` as the default head by setting `TURBO_SCM_HEAD`.

```bash title="Terminal"
TURBO_SCM_BASE=development turbo ls --affected
```

### `--output <format>` <ExperimentalBadge />

Format to output the results. `json` or `pretty` (default)

```bash title="Terminal"
turbo ls --output=json
```


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

```jsonc title="./apps/my-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      // Custom configuration for the build task in this package
    },
    "special-task": {} // New task specific to this package
  }
}
```

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

```jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputs": ["dist/**"],
      "env": ["NODE_ENV"]
    }
  }
}
```

```jsonc title="./apps/my-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      // This REPLACES the root outputs - "dist/**" is NOT included
      "outputs": [".next/**"]
    }
  }
}
```

### Extending arrays with `$TURBO_EXTENDS$` <ExperimentalBadge>Pre-release</ExperimentalBadge>

To **add** to inherited array values instead of replacing them, use the [`$TURBO_EXTENDS$` microsyntax](/docs/reference/configuration#turbo_extends-pre-release):

```jsonc title="./apps/my-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      // Inherits "dist/**" from root AND adds ".next/**"
      "outputs": ["$TURBO_EXTENDS$", ".next/**"]
    }
  }
}
```

The `$TURBO_EXTENDS$` marker must be the first element in the array. It works with `outputs`, `env`, `inputs`, `dependsOn`, `passThroughEnv`, and `with`.

### Extending from other packages <ExperimentalBadge>Pre-release</ExperimentalBadge>

By default, Package Configurations can only extend from the root `turbo.json`. With the [`futureFlags.nonRootExtends`](/docs/reference/configuration#nonrootextends-pre-release) flag, you can extend from any package that has a `turbo.json`.

First, enable the flag in your root `turbo.json`:

```jsonc title="./turbo.json"
{
  "futureFlags": {
    "nonRootExtends": true
  }
}
```

Then, extend from any package by using its `name` from `package.json` in your `extends` array. For example, if you have a Next.js app at `./apps/web` with `"name": "web"` in its `package.json`:

```jsonc title="./apps/web/turbo.json"
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
```

Another Next.js app can extend from it to share the same configuration:

```jsonc title="./apps/docs/turbo.json"
{
  "extends": ["//", "web"],
  "tasks": {
    "build": {
      // Additional customization specific to this package
      "env": ["NEXT_PUBLIC_DOCS_URL"]
    }
  }
}
```

<Callout type="warn">
  When extending from multiple configurations, the root (`"//"`) must always be
  listed **first** in the `extends` array.
</Callout>

#### Inheritance order

When extending from multiple configurations, task definitions are merged in the order they appear in the `extends` array:

1. Root `turbo.json` (`"//"`) is applied first
2. Each additional package configuration is applied in order
3. The current package's configuration is applied last

Later configurations override earlier ones for scalar fields. For array fields, see [Extending arrays with `$TURBO_EXTENDS$`](#extending-arrays-with-turbo_extends) to append instead of replace.

#### Patterns for sharing configuration

**Extend from an existing package**: If you already have a package with the configuration you want to share, other packages can extend from it directly. This works well when one package serves as the "canonical" example for similar packages (e.g., your main Next.js app that other Next.js apps can extend from).

**Create a dedicated configuration package**: For larger monorepos, you may want to create packages specifically for sharing configuration. This keeps configuration separate from application code and makes it clear that other packages depend on these settings. These packages typically only contain a `package.json` and `turbo.json`.

<Tabs items={["shared-config/package.json", "shared-config/turbo.json", "apps/web/turbo.json"]}>
  <Tab value="shared-config/package.json">
    ```json title="./packages/shared-config/package.json"
    {
      "name": "shared-config",
      "private": true
    }
    ```
  </Tab>

  <Tab value="shared-config/turbo.json">
    ```jsonc title="./packages/shared-config/turbo.json"
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
    ```
  </Tab>

  <Tab value="apps/web/turbo.json">
    ```jsonc title="./apps/web/turbo.json"
    {
      "extends": ["//", "shared-config"],
      "tasks": {
        "build": {
          "env": ["MY_API_URL"]
        }
      }
    }
    ```
  </Tab>
</Tabs>

### Excluding tasks from inheritance <ExperimentalBadge>Pre-release</ExperimentalBadge>

When extending from the root or other packages, your package inherits all their task definitions by default. With the [`futureFlags.nonRootExtends`](/docs/reference/configuration#nonrootextends-pre-release) flag, you can use the task-level `extends` field to opt out of specific tasks.

#### Excluding a task entirely

To completely exclude an inherited task from your package, set `extends: false` with no other configuration:

```jsonc title="./turbo.json"
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
```

```jsonc title="./packages/ui/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "lint": {
      "extends": false // This package does not have a lint task
    }
  }
}
```

When you run `turbo run lint`, the `ui` package will be skipped entirely for the `lint` task.

#### Creating a fresh task definition

To create a new task definition that doesn't inherit any configuration from the extends chain, use `extends: false` along with other task configuration:

```jsonc title="./packages/special-app/turbo.json"
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
```

This is useful when you need completely different task configuration that shouldn't merge with inherited values.

#### Exclusions propagate through the chain

When a package excludes a task, that exclusion propagates to packages that extend from it:

```jsonc title="./packages/base-config/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "lint": {
      "extends": false // Exclude lint from this config
    }
  }
}
```

```jsonc title="./apps/web/turbo.json"
{
  "extends": ["//", "base-config"],
  "tasks": {
    // web does not inherit lint from root because base-config excluded it
  }
}
```

<Callout type="info">
  Task-level `extends` is only available in Package Configurations. Using
  `extends` on a task in the root `turbo.json` will result in a validation
  error.
</Callout>

## Examples

### Different frameworks in one Workspace

Let's say your monorepo has multiple [Next.js](https://nextjs.org) apps, and one [SvelteKit](https://kit.svelte.dev)
app. Both frameworks create their build output with a `build` script in their
respective `package.json`. You *could* configure Turborepo to run these tasks
with a single `turbo.json` at the root like this:

```jsonc title="./turbo.json"
{
  "tasks": {
    "build": {
      "outputs": [".next/**", "!.next/cache/**", ".svelte-kit/**"]
    }
  }
}
```

Notice that both `.next/**` and `.svelte-kit/**` need to be specified as
[`outputs`](/docs/reference/configuration#outputs), even though Next.js apps do not generate a `.svelte-kit` directory, and
vice versa.

With Package Configurations, you can instead add custom
configuration in the SvelteKit package in `apps/my-svelte-kit-app/turbo.json`:

```jsonc title="./apps/my-svelte-kit-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      "outputs": [".svelte-kit/**"]
    }
  }
}
```

and remove the SvelteKit-specific [`outputs`](/docs/reference/configuration#outputs) from the root configuration:

```diff title="./turbo.json"
{
  "tasks": {
    "build": {
-      "outputs": [".next/**", "!.next/cache/**", ".svelte-kit/**"]
+      "outputs": [".next/**", "!.next/cache/**"]
    }
  }
}
```

This not only makes each configuration easier to read, it puts the configuration
closer to where it is used.

### Specialized tasks

In another example, say that the `build` task in one package `dependsOn` a
`compile` task. You could universally declare it as `dependsOn: ["compile"]`.
This means that your root `turbo.json` has to have an empty `compile` task
entry:

```json title="./turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["compile"]
    },
    "compile": {}
  }
}
```

With Package Configurations, you can move that `compile` task into the
`apps/my-custom-app/turbo.json`,

```json title="./apps/my-app/turbo.json"
{
  "extends": ["//"],
  "tasks": {
    "build": {
      "dependsOn": ["compile"]
    },
    "compile": {}
  }
}
```

and remove it from the root:

```diff title="./turbo.json"
{
  "tasks": {
+    "build": {}
-    "build": {
-      "dependsOn": ["compile"]
-    },
-    "compile": {}
  }
}
```

Now, the owners of `my-app`, can have full ownership over their `build` task,
but continue to inherit any other tasks defined at the root.

## Comparison to package-specific tasks

The [`package#task` syntax](/docs/crafting-your-repository/configuring-tasks#depending-on-a-specific-task-in-a-specific-package) in the root `turbo.json` **completely overwrites** all task configuration—nothing is inherited.

With Package Configurations, scalar fields are inherited and only the fields you specify are overridden. This means less duplication when you only need to change one or two properties.

<Callout type="info">
  Although there are no plans to remove package-specific task configurations, we
  expect that Package Configurations can be used for most use cases instead.
</Callout>

## Boundaries Tags <ExperimentalBadge>Experimental</ExperimentalBadge>

Package Configurations are also used to declare Tags for Boundaries. To do so, add a `tags` field to your `turbo.json`:

```diff title="./apps/my-app/turbo.json"
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
```

From there, you can define rules for which dependencies or dependents a tag can have. Check out the [Boundaries documentation](/docs/reference/boundaries#tags) for more details.

## Limitations

Although the general idea is the same as the root `turbo.json`, Package
Configurations come with a set of guardrails that can prevent packages from creating
potentially confusing situations.

### Package Configurations cannot use [the `workspace#task` syntax](/docs/crafting-your-repository/running-tasks) as task entries

The `package` is inferred based on the location of the configuration, and it is
not possible to change configuration for another package. For example, in a
Package Configuration for `my-nextjs-app`:

```jsonc title="./apps/my-nextjs-app/turbo.json"
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
```

Note that the `build` task can still depend on a package-specific task:

```jsonc title="./apps/my-nextjs-app/turbo.json"
{
  "tasks": {
    "build": {
      "dependsOn": ["some-pkg#compile"] // [!code highlight]
    }
  }
}
```

### Package Configurations can only override values in the `tasks` key

It is not possible to override [global configuration](/docs/reference/configuration#global-options) like `globalEnv` or `globalDependencies` in a Package Configuration. Configuration that would need to be altered in a Package Configuration is not truly global and should be configured differently.

### Root turbo.json cannot use the `extends` key

To avoid creating circular dependencies on packages, the root `turbo.json`
cannot extend from anything. The `extends` key will be ignored.

## Troubleshooting

In large monorepos, it can sometimes be difficult to understand how Turborepo is
interpreting your configuration. To help, we've added a `resolvedTaskDefinition`
to the [Dry Run](/docs/reference/run#--dry----dry-run) output. If you run `turbo run build --dry-run`, for example, the
output will include the combination of all `turbo.json` configurations that were
considered before running the `build` task.


- [prune](/reference/prune.md): API reference for the `turbo prune` command

import { File, Folder, Files } from '#components/files';

Generate a partial monorepo for a target package. The output will be placed into a directory named `out` containing the following:

* The full source code of all internal packages needed to build the target.
* A pruned lockfile containing the subset of the original lockfile needed to build the target.
* A copy of the root `package.json`.

```bash title="Terminal"
turbo prune [package]
```

### Example

Starting with a repository with the following structure:

<Files>
  <File name="package.json" />

  <File name="pnpm-lock.yaml" />

  <Folder name="apps" defaultOpen>
    <Folder name="admin">
      <File name="package.json" />

      <File name="next-env.d.ts" />

      <File name="next.config.js" />

      <Folder name="src">
        <Folder name="app">
          <File name="page.tsx" />
        </Folder>
      </Folder>

      <File name="tsconfig.json" />
    </Folder>

    <Folder name="frontend">
      <File name="package.json" />

      <File name="next-env.d.ts" />

      <File name="next.config.js" />

      <Folder name="src">
        <Folder name="app">
          <File name="page.tsx" />
        </Folder>
      </Folder>

      <File name="tsconfig.json" />
    </Folder>
  </Folder>

  <Folder name="packages" defaultOpen>
    <Folder name="scripts">
      <File name="package.json" />

      <Folder name="src">
        <File name="index.tsx" />
      </Folder>

      <File name="tsconfig.json" />
    </Folder>

    <Folder name="shared">
      <File name="package.json" />

      <Folder name="src">
        <Folder name="__tests__">
          <File name="sum.test.ts" />

          <File name="tsconfig.json" />
        </Folder>

        <File name="index.ts" />

        <File name="sum.ts" />
      </Folder>

      <File name="tsconfig.json" />
    </Folder>

    <Folder name="ui">
      <File name="package.json" />

      <Folder name="src">
        <File name="index.tsx" />
      </Folder>

      <File name="tsconfig.json" />
    </Folder>

    <Folder name="utils">
      <File name="package.json" />

      <Folder name="src">
        <File name="index.tsx" />
      </Folder>

      <File name="tsconfig.json" />
    </Folder>
  </Folder>
</Files>

Run `turbo prune frontend` to generate a pruned workspace for the `frontend` application in an `out` directory:

<Files>
  <File name="package.json" />

  <File name="pnpm-lock.yaml (partial)" />

  <Folder name="apps" defaultOpen>
    <Folder name="frontend">
      <File name="package.json" />

      <File name="next-env.d.ts" />

      <File name="next.config.js" />

      <Folder name="src">
        <Folder name="app">
          <File name="page.tsx" />
        </Folder>
      </Folder>

      <File name="tsconfig.json" />
    </Folder>
  </Folder>

  <Folder name="packages" defaultOpen>
    <Folder name="shared">
      <File name="package.json" />

      <Folder name="src">
        <Folder name="__tests__">
          <File name="sum.test.ts" />

          <File name="tsconfig.json" />
        </Folder>

        <File name="index.ts" />

        <File name="sum.ts" />
      </Folder>

      <File name="tsconfig.json" />
    </Folder>

    <Folder name="ui">
      <File name="package.json" />

      <Folder name="src">
        <File name="index.tsx" />
      </Folder>

      <File name="tsconfig.json" />
    </Folder>
  </Folder>
</Files>

### Options

#### `--docker`

Defaults to `false`.

Alter the output directory to make it easier to use with [Docker best practices and layer caching](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/). The directory will contain:

* A folder named `json` with the pruned workspace's `package.json` files.
* A folder named `full` with the pruned workspace's full source code for the internal packages needed to build the target.
* A pruned lockfile containing the subset of the original lockfile needed to build the target.

Using the same example from above, running `turbo prune frontend --docker` will generate the following:

<Files>
  <File name="pnpm-lock.yaml (partial)" />

  <Folder name="full" defaultOpen>
    <File name="package.json (from repo root)" />

    <Folder name="apps">
      <Folder name="frontend">
        <File name="package.json" />

        <File name="next-env.d.ts" />

        <File name="next.config.js" />

        <Folder name="src">
          <Folder name="app">
            <File name="page.tsx" />
          </Folder>
        </Folder>

        <File name="tsconfig.json" />
      </Folder>
    </Folder>

    <Folder name="packages">
      <Folder name="shared">
        <File name="package.json" />

        <Folder name="src">
          <Folder name="__tests__">
            <File name="sum.test.ts" />

            <File name="tsconfig.json" />
          </Folder>

          <File name="index.ts" />

          <File name="sum.ts" />
        </Folder>

        <File name="tsconfig.json" />
      </Folder>

      <Folder name="ui">
        <File name="package.json" />

        <Folder name="src">
          <File name="index.tsx" />
        </Folder>

        <File name="tsconfig.json" />
      </Folder>
    </Folder>
  </Folder>

  <Folder name="json" defaultOpen>
    <File name="package.json (from repo root)" />

    <Folder name="apps" defaultOpen>
      <Folder name="frontend" defaultOpen>
        <File name="package.json" />
      </Folder>
    </Folder>

    <Folder name="packages" defaultOpen>
      <Folder name="ui" defaultOpen>
        <File name="package.json" />
      </Folder>

      <Folder name="shared" defaultOpen>
        <File name="package.json" />
      </Folder>
    </Folder>
  </Folder>
</Files>

#### `--out-dir <path>`

Defaults to `./out`.

Customize the directory the pruned output is generated in.

#### `--use-gitignore[=<bool>]`

Default: `true`

Respect `.gitignore` file(s) when copying files to the output directory.

### Comparison to `pnpm deploy`

While both `turbo prune` and [`pnpm deploy`](https://pnpm.io/cli/deploy) are used to isolate packages in a monorepo, they serve different purposes and produce different outputs.

Where `turbo prune` generates a partial monorepo, `pnpm deploy` generates a directory that only contains the contents of the target package.

The `pnpm deploy` generated directory has a self-contained `node_modules` with hard linked internal dependencies.
This results in a portable package that can be directly copied to a server and used without additional steps.
The repository structure is not retained, as the focus is on producing a standalone deployable package.


- [query](/reference/query.md): API reference for the `turbo query` command

import { ExperimentalBadge } from '#components/experimental-badge';

<ExperimentalBadge />

Run GraphQL queries against your monorepo.

```bash title="Terminal"
turbo query [query] [flags]
```

When no arguments are passed, the command will open a GraphiQL playground to run queries.

```bash title="Terminal"
turbo query
```

When passed a query string, the command will run the query and output the results.

```bash title="Terminal"
turbo query "query { packages { items { name } } }"
```

When passed a file path, the command will read the file and run the query.

```bash title="Terminal"
turbo query query.gql
```


- [run](/reference/run.md): API reference for the `turbo run` command

import { Callout } from '#components/callout';

Run tasks specified in `turbo.json`.

```bash title="Terminal"
turbo run [tasks] [options] [-- [args passed to tasks]]
```

* **\[tasks]**: Turborepo can run one or many tasks at the same time. To run a task through `turbo`, it must be specified in `turbo.json`.
* **\[options]**: Options are used to control the behavior of the `turbo run` command. Available flag options are described below.
* **\[-- \[args passed to tasks]]**: You may also pass arguments to the underlying scripts. Note that all arguments will be passed to all tasks that are named in the run command.

<Callout type="good-to-know">
  `turbo run` is aliased to `turbo`. `turbo run build lint check-types` is the
  same as `turbo build lint check-types`. We recommend [using `turbo run` in CI
  pipelines](/docs/crafting-your-repository/constructing-ci#use-turbo-run-in-ci)
  and `turbo` with [global `turbo`
  locally](/docs/getting-started/installation#global-installation) for ease of
  use.
</Callout>

If no tasks are provided, `turbo` will display what tasks are available for the packages in the repository.

```bash title="Terminal"
turbo run
```

## Options

### `--affected`

Filter to only packages that are affected by changes on the current branch.

```bash title="Terminal"
turbo run build lint test --affected
```

By default, the flag is equivalent to `--filter=...[main...HEAD]`. This considers changes between `main` and `HEAD` from Git's perspective.

<Callout type="warn">
  The comparison requires everything between base and head to exist in the
  checkout. If the checkout is too shallow, then all packages will be considered
  changed.

  For example, setting up Git to check out with `--filter=blob:none --depth=0` will ensure `--affected` has the right history to work correctly.
</Callout>

You can override the default base and head with their respective [System Environment Variables](/docs/reference/system-environment-variables).

```bash title="Terminal"
# Override Git comparison base
TURBO_SCM_BASE=development turbo run build --affected

# Override Git comparison head
TURBO_SCM_HEAD=your-branch turbo run build --affected
```

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

```bash title="Terminal"
# Read from and write to local cache. Only read from Remote Cache.
turbo run build --cache=local:rw,remote:r

# Only read from local cache. Read from and write to Remote Cache.
turbo run build --cache=local:r,remote:rw

# Read from and write to local cache. No Remote Cache activity.
turbo run build --cache=local:rw

# Do not use local cache. Only read from Remote Cache.
turbo run build --cache=local:,remote:r
```

### `--cache-dir <path>`

Default: `.turbo/cache`

Specify the filesystem cache directory.

```bash title="Terminal"
turbo run build --cache-dir="./my-cache"
```

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

```bash title="Terminal"
turbo run build --concurrency=50%
turbo run test --concurrency=5
```

### `--continue[=<option>]`

Default: `never`

Specify how `turbo` should handle current and pending tasks in the presence of an error (e.g. non-zero exit code from a task).

* When `--continue=never` and an error occurs, `turbo` will cancel all tasks.
* When `--continue=dependencies-successful` and an error occurs, `turbo` will cancel dependent tasks. Tasks whose dependencies have succeeded will continue to run.
* When `--continue=always` and an error occurs, `turbo` will continue running all tasks, even those whose dependencies have failed.
* When `--continue` is specified without a value, it will default to `always`.

In all cases, `turbo` will exit with the highest exit code value encountered during execution.

```bash title="Terminal"
turbo run build --continue
```

### `--cwd <path>`

Default: Directory of root `turbo.json`

Set the working directory of the command.

```bash title="Terminal"
turbo run build --cwd=./somewhere/else/in/your/repo
```

### `--dangerously-disable-package-manager-check`

Turborepo uses your repository's lockfile to determine caching behavior, [Package Graphs](https://turborepo.com/docs/core-concepts/internal-packages), and more. Because of this, we use [the `packageManager` field](https://nodejs.org/api/packages.html#packagemanager) to help you stabilize your Turborepo.

To help with incremental migration or in situations where you cannot use the `packageManager` field, you may use `--dangerously-disable-package-manager-check` to opt out of this check and assume the risks of unstable lockfiles producing unpredictable behavior. When disabled, Turborepo will attempt a best-effort discovery of the intended package manager meant for the repository.

<Callout type="info">
  You may also opt out of this check using [configuration in
  `turbo.json`](/docs/reference/configuration#dangerouslydisablepacakgemanagercheck)
  or the
  [`TURBO_DANGEROUSLY_DISABLE_PACKAGE_MANAGER_CHECK`](/docs/reference/system-environment-variables)
  environment variable for broader coverage.
</Callout>

### `--dry / --dry-run`

Instead of executing tasks, display details about the packages and tasks that would be run.

Specify `--dry=json` to get the output in JSON format.

Task details include useful information like (list is non-exhaustive):

| Field                        | Description                                                            |
| ---------------------------- | ---------------------------------------------------------------------- |
| `taskId`                     | ID for the task, in the format of `package-name#task-name`             |
| `task`                       | The name of the task to be executed                                    |
| `package`                    | The package in which to run the task                                   |
| `hash`                       | The hash of the task (used for caching)                                |
| `hashOfExternalDependencies` | The global hash                                                        |
| `command`                    | The command used to run the task                                       |
| `inputs`                     | List of file inputs considered for hashing                             |
| `outputs`                    | List of file outputs that were cached                                  |
| `dependencies`               | Tasks that must run **before** this task                               |
| `dependents`                 | Tasks that must run **after** this task                                |
| `environmentVariables`       | Lists of environment variables specified in `env` and `passThroughEnv` |

### `--env-mode <option>`

`type: string`

Controls the available environment variables in the task's runtime.

<Callout type="good-to-know">
  `PATH`, `SHELL`, and `SYSTEMROOT` are always available to the task.
</Callout>

| option                      | description                                                        |
| --------------------------- | ------------------------------------------------------------------ |
| [strict](#strict) (Default) | Only allow explicitly listed environment variables to be available |
| [loose](#loose)             | Allow **all** environment variables to be available                |

```bash title="Terminal"
turbo run build --env-mode=loose
```

The same behavior can also be set via the `TURBO_ENV_MODE=strict` system variable.

#### `strict`

Only environment variables specified in the following keys are
available to the task:

* [`env`](/docs/reference/configuration#env)
* [`passThroughEnv`](/docs/reference/configuration#passthroughenv)
* [`globalEnv`](/docs/reference/configuration#globalenv)
* [`globalPassThroughEnv`](/docs/reference/configuration#globalpassthroughenv)

If Strict Mode is specified or inferred, **all** tasks are run in `strict` mode,
regardless of their configuration.

#### `loose`

All environment variables on the machine are made available to the task's runtime.

<Callout type="warn">
  This can be dangerous when environment variables are not accounted for in
  caching with the keys listed in `strict` above. You're much more likely to
  restore a version of your package with wrong environment variables from cache
  in `loose` mode.
</Callout>

### `--filter <string>`

Specify targets to execute from your repository's graph. Multiple filters can be combined to select distinct sets of targets.

Filters can be combined to create combinations of packages, directories, and git commits.

| Target type | Description                                                                                                                | Example                             |
| ----------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| Package     | Select a package by its name in `package.json`.                                                                            | `turbo run build --filter=ui`       |
| Directory   | Specify directories to capture a list of packages to run tasks. **When used with other filters, must be wrapped in `{}`**. | `turbo run build --filter=./apps/*` |
| Git commits | Using Git specifiers, specify packages with source control changes. **Must be wrapped in `[]`**.                           | `turbo run build --filter=[HEAD^1]` |

<Callout type="good-to-know">`-F` is an alias for `--filter`.</Callout>

#### Microsyntaxes for filtering

* `!`: Negate targets from the selection.
* `...` using packages: Select all packages in the [Package Graph](/docs/core-concepts/package-and-task-graph#package-graph) relative to the target. Using `...` **before** the package name will select **dependents** of the target while using `...` **after** the package name will select **dependencies** of the target.
* `...` using Git commits: Select a range using `[<from commit>]...[<to commit>]`.
* `^`: Omit the target from the selection when using `...`.

For in-depth discussion and practical use cases of filtering, visit [the Running Tasks page](/docs/crafting-your-repository/running-tasks).

#### Using a task identifier

You can also run a specific task for a specific package in the format of `package-name#task-name`.

```bash title="Terminal"
turbo run web#lint
```

<Callout type="good-to-know">
  This will also run the task's dependencies. To run a task without its
  dependencies, use [the `--only` flag](#--only).
</Callout>

#### Advanced filtering examples

You can combine multiple filters to further refine your targets. Multiple filters are combined as a union, with negated filters removing packages from the result of the union.

```bash title="Terminal"
# Any packages in `apps` subdirectories that have changed since the last commit
turbo run build --filter={.apps/*}[HEAD^1]

# Any packages in `apps` subdirectories except ./apps/admin
turbo run build --filter=./apps/* --filter=!./apps/admin

# Run the build task for the docs and web packages
turbo run build --filter=docs --filter=web

# Build everything that depends on changes in branch 'my-feature'
turbo run build --filter=...[origin/my-feature]

# Build everything that depends on changes between two Git SHAs
turbo run build --filter=[a1b2c3d...e4f5g6h]

# Build '@acme/ui' if:
# - It or any of its dependencies have changed since the previous commit
turbo run build --filter=@acme/ui...[HEAD^1]

# Test each package that is:
# - In the '@acme' scope
# - Or, in the 'packages' directory
# - Or, changed since the previous commit
turbo run test --filter=@acme/*{./packages/*}[HEAD^1]
```

### `--force`

Ignore existing cached artifacts and re-execute all tasks.

<Callout type="good-to-know">
  `--force` will overwrite existing task caches.
</Callout>

```bash title="Terminal"
turbo run build --force
```

The same behavior can also be set via [the `TURBO_FORCE` environment variable](/docs/reference/system-environment-variables).

### `--framework-inference`

Default: `true`

Specify whether or not to do [Framework Inference](/docs/crafting-your-repository/using-environment-variables#framework-inference) for tasks.

When `false`, [automatic environment variable inclusion](/docs/crafting-your-repository/using-environment-variables#framework-inference) is disabled.

```bash title="Terminal"
turbo run build --framework-inference=false
```

### `--global-deps <file glob>`

Specify glob of global filesystem dependencies to be hashed. Useful for `.env` and files in the root directory that impact multiple packages.

```bash title="Terminal"
turbo run build --global-deps=".env"
turbo run build --global-deps=".env.*" --global-deps=".eslintrc" --global-deps="jest.config.ts"
```

<Callout type="info">
  We recommend specifying file globs that you'd like to include your hashes in
  [the `globalDependencies` key](/docs/reference/configuration#globaldeps) in
  `turbo.json` to make sure they are always accounted for.
</Callout>

### `--graph <file name>`

Default: `dot`

This command can output a graph file: `svg`, `png`, `jpg`, `pdf`, `json`, `html`, `mermaid`, or `dot`.

If [Graphviz](https://graphviz.org/) is not installed, or no filename is provided, this command prints the dot graph to `stdout`.

```bash title="Terminal"
turbo run build --graph
turbo run build test lint --graph=my-graph.svg
```

<Callout type="info">
  **Known Bug**: All possible task nodes will be added to the graph at the
  moment, even if that script does not actually exist in a given package. This
  has no impact on execution, but the graph may overstate the number of packages
  and tasks involved.
</Callout>

### `--log-order <option>`

Default: `auto`

Set the ordering for log output.

By default, `turbo` will use `grouped` logs in CI environments and `stream` logs everywhere else. This flag is not applicable when using [the terminal UI](https://turborepo.com/docs/reference/configuration#ui).

```bash title="Terminal"
turbo run build --log-order=stream
```

| Option    | Description                                 |
| --------- | ------------------------------------------- |
| `stream`  | Show output as soon as it is available      |
| `grouped` | Group output by task                        |
| `auto`    | `turbo` decides based on its own heuristics |

### `--log-prefix <option>`

Default: `auto`

Control the `<package>:<task>:` prefix for log lines produced when running tasks.

```bash title="Terminal"
turbo run dev --log-prefix=none
```

| Option | Description                                             |
| ------ | ------------------------------------------------------- |
| `task` | Force prepending the `<package>:<task>:` prefix to logs |
| `none` | No prefixes                                             |
| `auto` | `turbo` decides based on its own heuristics             |

### `--no-cache`

<Callout type="warn" title="Deprecated">
  This flag is deprecated and will be removed in a future major release. Please
  use the [`--cache`](#--cache-options) flag instead.
</Callout>

Default `false`

Do not cache results of the task.

```bash title="Terminal"
turbo run dev --no-cache
```

### `--daemon` and `--no-daemon`

`turbo` can run a background process to pre-calculate values used for determining work that needs to be done. This standalone process (daemon) is an optimization, and not required for proper functioning of `turbo`.

The default daemon usage is set for your repository using [the `daemon` field in `turbo.json`](/docs/reference/configuration#daemon). Passing `--daemon` requires `turbo` to use the standalone process, while `--no-daemon` instructs `turbo` to avoid using or creating the standalone process.

The same behavior can also be set via the `TURBO_DAEMON=true` system variable.

### `--output-logs <option>`

Default: `full`

Set type of output logging, overriding [`outputLogs`](/docs/reference/configuration#outputlogs) if it's defined in `turbo.json`.

```bash title="Terminal"
turbo run build --output-logs=errors-only
```

| Option        | Description                       |
| ------------- | --------------------------------- |
| `full`        | Displays all logs                 |
| `hash-only`   | Only show the hashes of the tasks |
| `new-only`    | Only show logs from cache misses  |
| `errors-only` | Only show logs from task failures |
| `none`        | Hides all task logs               |

### `--only`

Default: `false`

Restricts execution to include specified tasks only.

#### Example

Given this `turbo.json`:

```json title="./turbo.json"
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
```

```bash title="Terminal"
turbo run test --only
```

The command will *only* execute the `test` tasks in each package. It will not run `build`.

Additionally, `--only` will only run tasks in specified packages, excluding dependencies. For example, `turbo run build --filter=web --only`, will **only** run the `build` script in the `web` package.

### `--parallel`

Default: `false`

Run commands in parallel across packages, ignoring the task dependency graph.

```bash title="Terminal"
turbo run lint --parallel
turbo run dev --parallel
```

<Callout type="info">
  The `--parallel` flag is typically used for long-running "dev" or "watch"
  tasks that don't exit. Starting in `turbo@1.7`, we recommend configuring these
  tasks using [`persistent`](/docs/reference/configuration#persistent) instead.
</Callout>

### `--preflight`

Only applicable when Remote Caching is configured. Enables sending a preflight request before every cache artifact and analytics request. The follow-up upload and download will follow redirects.

```bash title="Terminal"
turbo run build --preflight
```

The same behavior can also be set via the `TURBO_PREFLIGHT=true` system variable.

### `--profile`

Generates a trace of the run in Chrome Tracing format that you can use to analyze performance.

You must provide a verbosity flag (`-v`, `-vv`, or `-vvv`) with `--profile` to produce a trace.

```bash title="Terminal"
turbo run build --profile=profile.json -vvv
```

Profiles can be viewed in a tool like [Perfetto](https://ui.perfetto.dev/).

### `--remote-cache-timeout`

Default: `30`

Set the timeout for Remote Cache operations in seconds.

```bash title="Terminal"
turbo run build --remote-cache-timeout=60
```

### `--remote-only`

<Callout type="warn" title="Deprecated">
  This flag is deprecated and will be removed in a future major release. Please
  use the [`--cache`](#--cache-options) flag instead.
</Callout>

Default: `false`

Ignore the local filesystem cache for all tasks, using Remote Cache for reading and caching task outputs.

```bash title="Terminal"
turbo run build --remote-only
```

### `--summarize`

Generates a JSON file in `.turbo/runs` containing metadata about the run, including:

* Affected packages
* Executed tasks (including their timings and hashes)
* All the files included in the cached artifact

```bash title="Terminal"
turbo run build --summarize
```

This flag can be helpful for debugging to determine things like:

* How `turbo` interpreted your glob syntax for `inputs` and `outputs`
* What inputs changed between two task runs to produce a cache miss
* How task timings changed over time

<Callout type="info" title="Summaries viewer">
  While there is not a Turborepo-native Run Summaries UI viewer, there are
  several community-built tools available:

  * [https://turbo.nullvoxpopuli.com](https://turbo.nullvoxpopuli.com) - Web-based UI viewer for Run Summaries
  * [`turborepo-summary`](https://github.com/charpeni/turborepo-summary) - Generate human-readable reports from Turborepo run summary JSON output
  * [`turborepo-summary-action`](https://github.com/charpeni/turborepo-summary-action) - GitHub Action wrapping `turborepo-summary` to append them to GitHub Actions Job Summary
</Callout>

### `--token`

A bearer token for Remote Caching. Useful for running in non-interactive shells in combination with the `--team` flag.

```bash title="Terminal"
turbo run build --team=my-team --token=xxxxxxxxxxxxxxxxx
```

This value can also be set using [the `TURBO_TOKEN` system variable](/docs/reference/system-environment-variables). If both are present, the flag value will override the system variable.

<Callout type="good-to-know">
  If you are using [Vercel Remote
  Cache](https://vercel.com/docs/monorepos/remote-caching) and building your
  project on Vercel, you do not need to use this flag. This value will be
  automatically set for you.
</Callout>

### `--team`

The slug of the Remote Cache team. Useful for running in non-interactive shells in combination with the `--token` flag.

```bash title="Terminal"
turbo run build --team=my-team
turbo run build --team=my-team --token=xxxxxxxxxxxxxxxxx
```

This value can also be set using [the `TURBO_TEAM` system variable](/docs/reference/system-environment-variables). If both are present, the flag value will override the system variable.

### `--ui`

Specify the UI to use for output. Accepts `stream` or `tui`.

### `--verbosity`

To specify log level, use `--verbosity=<num>` or `-v, -vv, -vvv`.

| Level | Flag value      | Shorthand |
| ----- | --------------- | --------- |
| Info  | `--verbosity=1` | `-v`      |
| Debug | `--verbosity=2` | `-vv`     |
| Trace | `--verbosity=3` | `-vvv`    |

```bash title="Terminal"
turbo run build --verbosity=2
turbo run build -vvv
```


- [scan](/reference/scan.md): API reference for the `turbo scan` command

Enable faster tooling for your Turborepo locally with one, interactive command.

```bash title="Terminal"
turbo scan
```

You'll be taken through a short series of steps to enable the fastest settings for your Turborepo. These optimizations include:

* **Git FS Monitor**: `turbo` leans on Git to do file change discovery. Since we have to wait for `git` to tell us about changes, we can use [Git's built-in filesystem monitor](https://git-scm.com/docs/git-fsmonitor--daemon) to get those notifications sooner.
* **Turborepo Daemon**: Turborepo's daemon optimistically understands your repository in the background. By doing shared, common work that `turbo` will need to do when running tasks beforehand, `turbo` will run your tasks faster.
* **Remote Caching**: While Turborepo can cache your work locally, it can also share a cache across all of your machines. Enabling [Remote Caching](/docs/core-concepts/remote-caching) makes your caching **multiplayer**, ensuring that you, your teammates, and your CI machines, never do the same work twice.
* **Check `turbo` version**: We're always working towards making `turbo` better. To ensure you are using the latest version of Turborepo, we'll check your version and remind you to install `latest` if you aren't using it yet.
* **Check for Turborepo LSP**:
  Visit the [VSCode Extension Marketplace](https://marketplace.visualstudio.com/items?itemName=Vercel.turbo-vsc) and install the Turborepo LSP extension for your IDE.


- [System environment variables](/reference/system-environment-variables.md): Learn about system variables used by Turborepo.

import { Heading } from 'fumadocs-ui/components/heading';

By setting certain environment variables, you can change Turborepo's behavior. This can be useful for creating specific configurations for different environments and machines.

System environment variables are always overridden by flag values provided directly to your `turbo` commands.

<table id="system-environment-variables-table">
  <thead>
    <tr>
      <th>Variable</th>
      <th>Description</th>
    </tr>
  </thead>

  <tbody>
    <tr id="force_color">
      <td>
        <code>FORCE\_COLOR</code>
      </td>

      <td>Forces color to be shown in terminal logs</td>
    </tr>

    <tr id="turbo_api">
      <td>
        <code>TURBO\_API</code>
      </td>

      <td>
        Set the base URL for{' '}
        <a href="/docs/core-concepts/remote-caching">Remote Cache</a>.
      </td>
    </tr>

    <tr id="turbo_binary_path">
      <td>
        <code>
          <code>TURBO\_BINARY\_PATH</code>
        </code>
      </td>

      <td>
        Manually set the path to the <code>turbo</code> binary. By default,{' '}
        <code>turbo</code> will automatically discover the binary so you should
        only use this in rare circumstances.
      </td>
    </tr>

    <tr id="turbo_cache">
      <td>
        <code>
          <code>TURBO\_CACHE</code>
        </code>
      </td>

      <td>
        Control reading and writing for cache sources. Uses the same syntax as{' '}

        <a href="/docs/reference/run#--cache-options">
          {' '}

          <code>--cache</code>
        </a>

        .
      </td>
    </tr>

    <tr id="turbo_cache_dir">
      <td>
        <code>TURBO\_CACHE\_DIR</code>
      </td>

      <td>
        Sets the cache directory, similar to using{' '}

        <a href="/docs/reference/run#--cache-dir-path">
          {' '}

          <code>--cache-dir</code>
        </a>

        {' '}

        flag.
      </td>
    </tr>

    <tr id="turbo_ci_vendor_env_key">
      <td>
        <code>TURBO\_CI\_VENDOR\_ENV\_KEY</code>
      </td>

      <td>
        Set a prefix for environment variables that you want
        <strong>excluded</strong> from <a href="/docs/crafting-your-repository/using-environment-variables#framework-inference">
        Framework Inference
        </a>.<span />
        <strong>NOTE</strong>: This does not need to be set by the user and should
        be configured automatically by supported platforms.
      </td>
    </tr>

    <tr id="turbo_dangerously_disable_package_manager_check">
      <td>
        <code>TURBO\_DANGEROUSLY\_DISABLE\_PACKAGE\_MANAGER\_CHECK</code>
      </td>

      <td>
        Disable checking the <code>packageManager</code> field in{' '}
        <code>package.json</code>. You may run into{' '}

        <a href="/docs/reference/run#--dangerously-disable-package-manager-check">
          errors and unexpected caching behavior
        </a>

        {' '}

        when disabling this check. Use <code>true</code> or <code>1</code> to
        disable.
      </td>
    </tr>

    <tr id="turbo_download_local_enabled">
      <td>
        <code>TURBO\_DOWNLOAD\_LOCAL\_ENABLED</code>
      </td>

      <td>
        Enables global <code>turbo</code> to install the correct local version
        if one is not found.
      </td>
    </tr>

    <tr id="turbo_force">
      <td>
        <code>TURBO\_FORCE</code>
      </td>

      <td>
        Set to <code>true</code> to force all tasks to run in full, opting out
        of all caching.
      </td>
    </tr>

    <tr id="turbo_global_warning_disabled">
      <td>
        <code>TURBO\_GLOBAL\_WARNING\_DISABLED</code>
      </td>

      <td>
        Disable warning when global <code>turbo</code> cannot find a local
        version to use.
      </td>
    </tr>

    <tr id="turbo_print_version_disabled">
      <td>
        <code>TURBO\_PRINT\_VERSION\_DISABLED</code>
      </td>

      <td>
        Disable printing the version of <code>turbo</code> that is being
        executed.
      </td>
    </tr>

    <tr id="turbo_log_order">
      <td>
        <code>TURBO\_LOG\_ORDER</code>
      </td>

      <td>
        Set the <a href="/docs/reference/run#--log-order-option">log order</a>.
        Allowed values are <code>grouped</code> and <code>default</code>.
      </td>
    </tr>

    <tr id="turbo_login">
      <td>
        <code>TURBO\_LOGIN</code>
      </td>

      <td>
        Set the URL used to log in to{' '}
        <a href="/docs/core-concepts/remote-caching">Remote Cache</a>. Only
        needed for self-hosted Remote Caches that implement an endpoint that
        dynamically creates tokens.
      </td>
    </tr>

    <tr id="turbo_no_update_notifier">
      <td>
        <code>TURBO\_NO\_UPDATE\_NOTIFIER</code>
      </td>

      <td>
        Remove the update notifier that appears when a new version of{' '}
        <code>turbo</code> is available. You can also use{' '}
        <code>NO\_UPDATE\_NOTIFIER</code> per ecosystem convention.
      </td>
    </tr>

    <tr id="turbo_platform_env">
      <td>
        <code>TURBO\_PLATFORM\_ENV</code>
      </td>

      <td>
        A CSV of environment variable keys that are configured in a supported CI
        environment (Vercel). <strong>NOTE</strong>: This variable is meant for
        platforms looking to implement zero-configuration environment variables.
        You are not meant to use this variable as an end user.{' '}
      </td>
    </tr>

    <tr id="turbo_platform_env_disabled">
      <td>
        <code>TURBO\_PLATFORM\_ENV\_DISABLED</code>
      </td>

      <td>
        Disable checking environment variables configured in your{' '}
        <code>turbo.json</code> against those set on your supported platform
      </td>
    </tr>

    <tr id="turbo_preflight">
      <td>
        <code>TURBO\_PREFLIGHT</code>
      </td>

      <td>
        Enables sending a preflight request before every cache artifact and
        analytics request. The follow-up upload and download will follow
        redirects. Only applicable when{' '}
        <a href="/docs/core-concepts/remote-caching">Remote Caching</a> is
        configured.
      </td>
    </tr>

    <tr id="turbo_remote_cache_read_only">
      <td>
        <code>TURBO\_REMOTE\_CACHE\_READ\_ONLY</code>
      </td>

      <td>
        Prevent writing to the{' '}
        <a href="/docs/core-concepts/remote-caching">Remote Cache</a> - but
        still allow reading.
      </td>
    </tr>

    <tr id="turbo_remote_cache_signature_key">
      <td>
        <code>TURBO\_REMOTE\_CACHE\_SIGNATURE\_KEY</code>
      </td>

      <td>
        Sign artifacts with a secret key. For more information, visit{' '}

        <a href="/docs/core-concepts/remote-caching#artifact-integrity-and-authenticity-verification">
          the Artifact Integrity section
        </a>

        .
      </td>
    </tr>

    <tr id="turbo_remote_cache_timeout">
      <td>
        <code>TURBO\_REMOTE\_CACHE\_TIMEOUT</code>
      </td>

      <td>
        Set a timeout in seconds for <code>turbo</code> to get artifacts from{' '}
        <a href="/docs/core-concepts/remote-caching">Remote Cache</a>.
      </td>
    </tr>

    <tr id="turbo_remote_cache_upload_timeout">
      <td>
        <code>TURBO\_REMOTE\_CACHE\_UPLOAD\_TIMEOUT</code>
      </td>

      <td>
        Set a timeout in seconds for <code>turbo</code> to upload artifacts to{' '}
        <a href="/docs/core-concepts/remote-caching">Remote Cache</a>.
      </td>
    </tr>

    <tr id="turbo_remote_only">
      <td>
        <code>TURBO\_REMOTE\_ONLY</code>
      </td>

      <td>Always ignore the local filesystem cache for all tasks.</td>
    </tr>

    <tr id="turbo_run_summary">
      <td>
        <code>TURBO\_RUN\_SUMMARY</code>
      </td>

      <td>
        Generate a <a href="/docs/reference/run#--summarize">Run Summary</a>{' '}
        when you run tasks.
      </td>
    </tr>

    <tr id="turbo_scm_base">
      <td>
        <code>TURBO\_SCM\_BASE</code>
      </td>

      <td>
        Base used by <code>--affected</code> when calculating what has changed
        from <code>base...head</code>
      </td>
    </tr>

    <tr id="turbo_scm_head">
      <td>
        <code>TURBO\_SCM\_HEAD</code>
      </td>

      <td>
        Head used by <code>--affected</code> when calculating what has changed
        from <code>base...head</code>
      </td>
    </tr>

    <tr id="turbo_team">
      <td>
        <code>TURBO\_TEAM</code>
      </td>

      <td>
        The account name associated with your repository. When using{' '}

        <a href="https://vercel.com/docs/monorepos/remote-caching#vercel-remote-cache" rel="noreferrer noopener" target="_blank">
          Vercel Remote Cache
        </a>

        , this is [your team's slug](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fsettings\&title=Get+team+slug).
      </td>
    </tr>

    <tr id="turbo_teamid">
      <td>
        <code>TURBO\_TEAMID</code>
      </td>

      <td>
        The account identifier associated with your repository. When using{' '}

        <a href="https://vercel.com/docs/monorepos/remote-caching#vercel-remote-cache" rel="noreferrer noopener" target="_blank">
          Vercel Remote Cache
        </a>

        , this is your team's ID.
      </td>
    </tr>

    <tr id="turbo_telemetry_message_disabled">
      <td>
        <code>TURBO\_TELEMETRY\_MESSAGE\_DISABLED</code>
      </td>

      <td>
        Disable the message notifying you that{' '}
        <a href="/docs/telemetry">Telemetry</a> is enabled.
      </td>
    </tr>

    <tr id="turbo_token">
      <td>
        <code>TURBO\_TOKEN</code>
      </td>

      <td>
        The Bearer token for authentication to access{' '}
        <a href="/docs/core-concepts/remote-caching">Remote Cache</a>.
      </td>
    </tr>

    <tr id="turbo_ui">
      <td>
        <code>TURBO\_UI</code>
      </td>

      <td>
        Enables TUI when passed true or 1, disables when passed false or 0.
      </td>
    </tr>

    <tr id="turbo_concurrency">
      <td>
        <code>TURBO\_CONCURRENCY</code>
      </td>

      <td>
        Controls{' '}

        <a href="/repo/docs/reference/run#--concurrency-number--percentage">
          concurrency
        </a>

        {' '}

        settings in run or watch mode.
      </td>
    </tr>

    <tr id="turbo_sso_login_callback_port">
      <td>
        <code>TURBO\_SSO\_LOGIN\_CALLBACK\_PORT</code>
      </td>

      <td>
        Override the default port (9789) used for the SSO login callback server
        during authentication.
      </td>
    </tr>
  </tbody>
</table>

## Environment variables in tasks

Turborepo will make the following environment variables available within your tasks while they are executing:

| Variable       | Description                                                                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TURBO_HASH`   | The hash of the currently running task.                                                                                                              |
| `TURBO_IS_TUI` | When using the [TUI](/docs/reference/configuration#ui), this variable is set to `true`.                                                              |
| `TURBO_IS_MFE` | When using the [microfrontends](/docs/guides/microfrontends), this variable is set to the port defined in `microfrontends.json` for the application. |


- [telemetry](/reference/telemetry.md): API reference for the `turbo telemetry` command

import { LinkToDocumentation } from '#components/link-to-documentation';

```bash title="Terminal"
turbo telemetry [argument]
```

Manage telemetry for this machine.

<LinkToDocumentation href="/docs/telemetry">
  Learn more about Turborepo's telemetry.
</LinkToDocumentation>

## Arguments

### `status`

Retrieve the current state of telemetry for this machine.

```bash title="Terminal"
turbo telemetry status
```

### `enable`

Enable telemetry for this machine.

```bash title="Terminal"
turbo telemetry enable
```

### `disable`

Disable telemetry for this machine.

```bash title="Terminal"
turbo telemetry disable
```


- [@turbo/codemod](/reference/turbo-codemod.md): Learn more about how Turborepo uses codemods to make version migrations easy.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';
import { Accordion, Accordions } from '#components/accordion';

Turborepo provides codemod transformations and automatic migration scripts to help upgrade your Turborepo codebase when a feature is deprecated.

Codemods are transformations that run on your codebase programmatically. This allows for a large amount of changes to be applied without having to manually manage repetitive changes.

## Usage

First, ensure that you've run your package manager's install command.

```bash title="Terminal"
npx @turbo/codemod [transform] [path] [--dry] [--print]
```

* `transform` - name of transform, see available transforms below.
* `path` - files or directory to transform
* `--dry` - Do a dry-run (Code will not be edited)
* `--print` - Prints the changed output for comparison

## Upgrading Turborepo versions

In most cases, you can run:

```bash title="Terminal"
npx @turbo/codemod
```

All the codemods you need to upgrade will be run for you.

### Turborepo 2.x

The codemods below are used for migration paths in the second major version of Turborepo.

<Accordions>
  <Accordion title="update-schema-json-url (2.0.0)" id="update-schema-json-url">
    Updates a versioned schema.json URL to v2.

    ```bash title="Terminal"
    npx @turbo/codemod update-schema-json-url
    ```

    **Example**

    ```diff title="./turbo.json"
    {
    - "$schema": "https://turborepo.com/schema.v1.json",
    + "$schema": "https://turborepo.com/schema.v2.json",
    }
    ```
  </Accordion>

  <Accordion title="add-package-names (2.0.0)" id="add-package-names">
    Adds a name to `package.json` in any packages that don't have one.

    ```bash title="Terminal"
    npx @turbo/codemod add-package-names
    ```

    **Example**

    ```diff title="./packages/ui/package.json"
    {
    + "name": "@repo/ui",
    }
    ```
  </Accordion>

  <Accordion title="clean-globs (2.0.0)" id="clean-globs">
    Fix glob patterns that are invalid due to changes in processing of globs in `turbo`.

    ```bash title="Terminal"
    npx @turbo/codemod clean-globs
    ```

    **Example**

    ```diff title="./turbo.json"
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
    ```
  </Accordion>

  <Accordion title="migrate-dot-env (2.0.0)" id="migrate-dot-env">
    Move `.env` files from the removed `dotEnv` key to `inputs`.

    ```bash title="Terminal"
    npx @turbo/codemod migrate-dot-env
    ```

    **Example**

    ```diff title="./turbo.json"
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
    ```
  </Accordion>

  <Accordion title="rename-output-mode (2.0.0)" id="rename-output-mode">
    Rename the `outputMode` key to `outputLogs`.

    ```bash title="Terminal"
    npx @turbo/codemod rename-output-mode
    ```

    **Example**

    ```diff title="./turbo.json"
    {
      "tasks": {
        "build": {
    -     "outputMode": "errors-only" // [!code highlight]
    +     "outputLogs": "errors-only" // [!code highlight]
        }
      }
    }
    ```
  </Accordion>

  <Accordion title="rename-pipeline (2.0.0)" id="rename-pipeline">
    Rename the `pipeline` key to `tasks`.

    ```bash title="Terminal"
    npx @turbo/codemod rename-pipeline
    ```

    **Example**

    ```diff title="./turbo.json"
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
    ```
  </Accordion>

  <Accordion title="stabilize-ui (2.0.0)" id="stabilize-ui">
    Renames the `experimentalUI` key in `turbo.json` to `ui`.

    ```bash title="Terminal"
    npx @turbo/codemod stabilize-ui
    ```

    **Example**

    ```diff title="./turbo.json"
    {
    - "experimentalUI": true
    + "ui": true
    }
    ```
  </Accordion>
</Accordions>

### Turborepo 1.x

The codemods below are used for migration paths in the first major version of Turborepo.

<Accordions>
  <Accordion title="stabilize-env-mode (1.10.0)" id="stabilize-env-mode">
    Migrates `turbo.json`'s `experimentalGlobalPassThroughEnv` to `globalPassThroughEnv` and `experimentalPassThroughEnv` to `passThroughEnv`.

    ```bash title="Terminal"
    npx @turbo/codemod stabilize-env-mode
    ```

    **Example**

    ```diff title="./turbo.json"
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
    ```
  </Accordion>

  <Accordion title="transform-env-literals-to-wildcards (1.10.0)" id="transform-env-literals-to-wildcards">
    Updates any existing environment variable fields whose contents would be ambiguous to the new wildcard syntax.

    ```bash title="Terminal"
    npx @turbo/codemod transform-env-literals-to-wildcards
    ```

    **Example**

    ```diff title="./turbo.json"
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
    ```
  </Accordion>

  <Accordion title="set-default-outputs (1.7.0)" id="set-default-outputs">
    Migrates `turbo.json` outputs to include the previously inferred `dist/**` and `build/**`.

    ```bash title="Terminal"
    npx @turbo/codemod set-default-outputs
    ```

    **Example**

    ```diff title="turbo.json"
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

    ```
  </Accordion>

  <Accordion title="migrate-env-var-dependencies (1.5.0)" id="migrate-env-var-dependencies">
    Migrates all environment variable dependencies in `turbo.json` from `dependsOn` and `globalDependencies` to `env` and `globalEnv` respectively.

    ```bash title="Terminal"
    npx @turbo/codemod migrate-env-var-dependencies
    ```

    **Example**

    ```diff title="./turbo.json"
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
    ```
  </Accordion>

  <Accordion title="add-package-manager (1.1.0)" id="add-package-manager">
    Transforms the root `package.json` so that `packageManager` key as the detected package manager (`yarn`, `npm`, `pnpm`) and version (e.g. `yarn@1.22.17`). This key is now [supported by Node.js](https://nodejs.org/dist/latest-v17.x/docs/api/packages.html#packagemanager) and is used by Turborepo for faster package manager detection (vs. inferring from just the filesystem alone).

    ```bash title="Terminal"
    npx @turbo/codemod add-package-manager
    ```

    **Example**

    ```diff title="./package.json"
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
    ```
  </Accordion>

  <Accordion title="create-turbo-config (1.1.0)" id="create-turbo-config">
    Creates the `turbo.json` file at the root of your project based on the `"turbo"` key in `package.json`.
    The `"turbo"` key is subsequently deleted from `package.json`.

    ```bash title="Terminal"
    npx @turbo/codemod create-turbo-config
    ```

    **Example**

    <Tabs items={["package.json", "turbo.json"]}>
      <Tab value="package.json">
        ```diff title="./package.json"
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
        ```
      </Tab>

      <Tab value="turbo.json">
        ```diff title="./turbo.json"
        + {
        +   "$schema": "https://turborepo.com/schema.json",
        +   "pipeline": {
        +     ...
        +   }
        + }
        ```
      </Tab>
    </Tabs>
  </Accordion>
</Accordions>


- [@turbo/gen](/reference/turbo-gen.md): Quickly generate new code in your Turborepo.

Use this package for type definitions in your [Turborepo code generators](/docs/reference/generate).

```ts title="./turbo/generators/my-generator.ts"
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
```

For more information, [visit the Generating code guide](/docs/guides/generating-code).


- [turbo-ignore](/reference/turbo-ignore.md): Learn how to use turbo-ignore to skip tasks in CI.

Use `turbo` to determine if a package or its dependencies have changes. This can be useful for quickly skipping tasks in CI.

```bash title="Terminal"
npx turbo-ignore [workspace] [flags...]
```

To learn more, visit:

* [The introductory guide to skipping tasks](/docs/crafting-your-repository/constructing-ci#skipping-tasks-and-other-unnecessary-work)
* [The advanced guide for skipping tasks](/docs/guides/skipping-tasks)
* [Documentation for `turbo-ignore` on npm](https://www.npmjs.com/package/turbo-ignore)

## turbo-ignore versioning

Because `turbo-ignore` is most often used before installing dependencies into the repository, there won't be a `turbo` binary available when you run `turbo-ignore`. Instead `turbo-ignore` will search for the correct version to use with your repository with the following strategy:

* First, check for a `turbo` entry in root `package.json#devDependencies` or `package.json#dependencies`. If a version is found there, it will be used.
* If no `entry` is found in `package.json`, `turbo.json` will be read for its schema. If [the `tasks` key](/docs/reference/configuration#tasks) is found, use `turbo@^2`. If the `pipeline` from Turborepo v1 is found, use `turbo@^1`.


- [unlink](/reference/unlink.md): API reference for the `turbo unlink` command

Disconnect the repository from Remote Cache.

```bash title="Terminal"
turbo unlink
```


- [watch](/reference/watch.md): API reference for the `watch` command

Re-run tasks in your repository, based on code changes.

```bash title="Terminal"
turbo watch [tasks]
```

`turbo watch` is dependency-aware, meaning tasks will re-run in the order [configured in `turbo.json`](/docs/reference/configuration).

If no tasks are provided, `turbo` will display what tasks are available for the packages in the repository.

```bash title="Terminal"
turbo watch
```

## Using `turbo watch` with persistent tasks

Persistent tasks are marked with [`"persistent": true`](/docs/reference/configuration#persistent), meaning they won't exit. Because of this, they cannot be depended on in your task graph.

This means that persistent tasks will be ignored when using `turbo watch`, working the same way they do with [`turbo run`](/docs/reference/run), allowing persistent and non-persistent tasks to be run at the same time.

### Dependency-aware persistent tasks

When your script has a built-in watcher (like `next dev`) capable of detecting changes in dependencies, you don't need to use `turbo watch`. Instead, use your script's built-in watcher and mark the task as long-running using [`"persistent": true`](/docs/reference/configuration#persistent).

### Persistent tasks without dependency awareness

Some tools aren't monorepo-friendly, and do not hot-reload modules in dependencies. In those cases, you should
mark the task as [`interruptible: true`](/docs/reference/configuration#interruptible) to have `turbo watch`
restart the task when relevant changes are detected.

## Limitations

### Caching

Caching tasks with Watch Mode is currently experimental, under the `--experimental-write-cache` flag.

```bash title="Terminal"
turbo watch your-tasks --experimental-write-cache
```

### Task outputs

If you have tasks that write to files checked into source control, there is a possibility that Watch Mode will run in an infinite loop. This is because Watch Mode watches your
files for changes and will re-run tasks in packages that have changed. If a task creates a change, then that will trigger the task again.

Watch Mode has some logic to prevent this from happening using file hashes, but it isn't foolproof. To avoid this issue, we recommend removing any task outputs from git.


- [Buildkite](/guides/ci-vendors/buildkite.md): Learn how to use Buildkite with Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

The following example shows how to use Turborepo with [Buildkite](https://buildkite.com/).

For a given root `package.json`:

```json title="./package.json"
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
```

And a `turbo.json`:

```json title="./turbo.json"
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
```

Create a file called `.buildkite/pipeline.yml` in your repository with the following contents:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```yaml title=".buildkite/pipeline.yml"
    steps:
      - label: ":test_tube: Test"
        command: |
          pnpm install
          pnpm test

      - label: ":hammer: Build"
        command: |
          pnpm install
          pnpm build
    ```
  </Tab>

  <Tab value="yarn">
    ```yaml title=".buildkite/pipeline.yml"
    steps:
      - label: ":test_tube: Test"
        command: |
          yarn
          yarn test

      - label: ":hammer: Build"
        command: |
          yarn
          yarn build
    ```
  </Tab>

  <Tab value="npm">
    ```yaml title=".buildkite/pipeline.yml"
    steps:
      - label: ":test_tube: Test"
        command: |
          npm install
          npm test

      - label: ":hammer: Build"
        command: |
          npm install
          npm run build
    ```
  </Tab>

  <Tab value="bun">
    ```yaml title=".buildkite/pipeline.yml"
    steps:
      - label: ":test_tube: Test"
        command: |
          bun install
          bun run test

      - label: ":hammer: Build"
        command: |
          bun install
          bun run build
    ```
  </Tab>
</Tabs>

## Create a Pipeline

To create your pipeline in the Buildkite dashboard, you'll need to first upload the pipeline definition from your repository.

1. Select **Pipelines** to navigate to the Buildkite dashboard.

2. Select **New pipeline**.

3. Enter your pipeline's details in the respective **Name** and **Description** fields.

4. In the **Steps** editor, ensure there's a step to upload the definition from your repository:

```yaml title=".buildkite/pipeline.yml"
steps:
  - label: ':pipeline:'
    command: buildkite-agent pipeline upload
```

5. Select **Create Pipeline**, then click **New Build**, then select **Create Build**.

Run the pipeline whenever you make changes you want to verify.

## Remote Caching

To use Remote Caching, retrieve the team and token for the Remote Cache for your provider. In this example, we'll use [Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching):

* `TURBO_TOKEN` - The Bearer token to access the Remote Cache
* `TURBO_TEAM` - The account to which the monorepo belongs

To use Vercel Remote Caching, you can get the value of these variables in a few steps:

1. Create a Scoped Access Token to your account in the [Vercel Dashboard](https://vercel.com/account/tokens). Copy the value to a safe place. You'll need it in a moment.

   ![Vercel Access Tokens](/images/docs/vercel-create-token.png)

2. Obtain [your Team URL](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fsettings\&title=Find+Team+URL) and copy its value as well. Both values will be used in the next step.

3. In the Buildkite dashboard, create two new [Buildkite secrets](https://buildkite.com/docs/pipelines/security/secrets/buildkite-secrets), one for each value. Name them `TURBO_TOKEN` and `TURBO_TEAM`.

4. Update `pipeline.yml` to fetch and apply `TURBO_TOKEN` and `TURBO_TEAM` as environment variables with the [Buildkite Secrets](https://github.com/buildkite-plugins/secrets-buildkite-plugin) plugin as shown. (For additional secret-management options, read [Managing pipeline secrets](https://buildkite.com/docs/pipelines/security/secrets/managing) in the Buildkite documentation.)

   ```yaml title=".buildkite/pipeline.yml"
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
   ```

   Commit and push these changes to your repository, and on the next pipeline run, the secrets will be applied and Vercel Remote Caching will be active.


- [CircleCI](/guides/ci-vendors/circleci.md): Learn how to use CircleCI with Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';

The following example shows how to use Turborepo with [CircleCI](https://circleci.com/).

<Callout type="warn" title="TTY on CircleCI">
  CircleCI [uses interactive terminals
  (TTY)](https://discuss.circleci.com/t/reprise-allow-for-using-circle-ci-tooling-without-a-tty/23309)
  that crash Turborepo's terminal UI. To workaround this, set the
  `TURBO_UI=false` environment variable in your CircleCI configuration.
</Callout>

For a given root `package.json`:

```json title="./package.json"
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
```

And a `turbo.json`:

```json title="./turbo.json"
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
```

Create a file called `.circleci/config.yml` in your repository with the following contents:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```yaml title=".circleci/config.yml"
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
    ```
  </Tab>

  <Tab value="yarn">
    ```yaml title=".circleci/config.yml"
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
    ```
  </Tab>

  <Tab value="npm">
    ```yaml title=".circleci/config.yml"
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
    ```
  </Tab>

  <Tab value="bun">
    ```yaml title=".circleci/config.yml"
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
    ```
  </Tab>
</Tabs>

## Remote Caching

To use Remote Caching, retrieve the team and token for the Remote Cache for your provider. In this example, we'll use [Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching):

* `TURBO_TOKEN` - The Bearer token to access the Remote Cache
* `TURBO_TEAM` - The slug of the Vercel team to share the artifacts with

To use Vercel Remote Caching, you can get the value of these variables in a few steps:

1. Create a Scoped Access Token to your account in the [Vercel Dashboard](https://vercel.com/account/tokens)

![Vercel Access Tokens](/images/docs/vercel-create-token.png)

Copy the value to a safe place. You'll need it in a moment.

2. Go to your CircleCI project settings and click on the **Environment Variables** tab. Create a new secret called `TURBO_TOKEN` and enter the value of your Scoped Access Token.

![CircleCI Environment Variables](/images/docs/circleci-environment-variables.png)
![CircleCI Create Environment Variables](/images/docs/circleci-create-environment-variables.png)

3. Make a second secret called `TURBO_TEAM` and set it to your team slug - the part after `vercel.com/` in [your Team URL](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fsettings\&title=Find+Team+URL). For example, the slug for `vercel.com/acme` is `acme`.

4. CircleCI automatically loads environment variables stored in project settings into the CI environment. No modifications are necessary for the CI file.


- [GitHub Actions](/guides/ci-vendors/github-actions.md): Learn how to use GitHub Actions with Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Steps, Step } from '#components/steps';
import { Callout } from '#components/callout';

The following example shows how to use Turborepo with [GitHub Actions](https://github.com/features/actions).

For a given root `package.json`:

```json title="./package.json"
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
```

And a `turbo.json`:

```json title="./turbo.json"
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
```

Create a file called `.github/workflows/ci.yml` in your repository with the following contents:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```yaml title=".github/workflows/ci.yml"
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
    ```
  </Tab>

  <Tab value="yarn">
    ```yaml title=".github/workflows/ci.yml"
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
    ```
  </Tab>

  <Tab value="npm">
    ```yaml title=".github/workflows/ci.yml"
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
    ```
  </Tab>

  <Tab value="bun">
    ```yaml title=".github/workflows/ci.yml"
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
    ```
  </Tab>
</Tabs>

## Remote Caching with Vercel Remote Cache

To use Remote Caching with GitHub Actions, add the following environment variables to your GitHub Actions workflow
to make them available to your `turbo` commands.

* `TURBO_TOKEN` - The Bearer token to access the Remote Cache
* `TURBO_TEAM` - The slug of the Vercel team to share the artifacts with

To use Remote Caching, retrieve the team and token for the Remote Cache for your provider. In this example, we'll use [Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching).

<Steps>
  <Step>
    Create a Scoped Access Token to your account in the [Vercel Dashboard](https://vercel.com/account/tokens)

    ![Vercel Access Tokens](/images/docs/vercel-create-token.png)

    Copy the value to a safe place. You'll need it in a moment.
  </Step>

  <Step>
    Go to your GitHub repository settings and click on the **Secrets** and then **Actions** tab. Create a new secret called `TURBO_TOKEN` and enter the value of your Scoped Access Token.

    ![GitHub Secrets](/images/docs/github-actions-secrets.png)
    ![GitHub Secrets Create](/images/docs/github-actions-create-secret.png)
  </Step>

  <Step>
    Create a new repository variable (click the **Variables** tab) called `TURBO_TEAM` and set it to your team slug - the part after `vercel.com/` in [your Team URL](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fsettings\&title=Find+Team+URL). For example, the slug for `vercel.com/acme` is `acme`.

    <Callout type="good-to-know">
      Using a repository variable rather than a secret will keep GitHub Actions from
      censoring your team name in log output.
    </Callout>

    ![GitHub Repository Variables](/images/docs/vercel-team-repo-var.png)
  </Step>

  <Step>
    At the top of your GitHub Actions workflow, provide the following environment variables to jobs that use `turbo`:

    ```yaml title=".github/workflows/ci.yml"
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
    ```
  </Step>
</Steps>

## Using Remote Caching with Reusable Workflows

For information on passing secrets to reusable workflows, see [GitHub's documentation on passing secrets to nested workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows#passing-secrets-to-nested-workflows).

## Remote Caching with GitHub actions/cache

The following steps show how you could use [actions/cache](https://github.com/actions/cache) to cache your monorepo artifacts on GitHub.

<Steps>
  <Step>
    Supply a package.json script that will run tasks using Turborepo.

    Example `package.json` with a `build` script:

    ```json title="./package.json"
    {
      "name": "my-turborepo",
      "scripts": {
        "build": "turbo run build"
      },
      "devDependencies": {
        "turbo": "1.2.5"
      }
    }
    ```
  </Step>

  <Step>
    Configure your GitHub pipeline with a step which uses the `actions/cache@v4` action before the build steps of your CI file.

    * Make sure that the `path` attribute set within the `actions/cache` action matches the output location above. In the example below, `path` was set to `.turbo`.
    * State the cache key for the current run under the `key` attribute. In the example below, we used a combination of the runner os and GitHub sha as the cache key.
    * State the desired cache prefix pattern under the `restore-keys` attribute. Make sure this pattern will remain valid for future ci runs. In the example below, we used the `${{ runner.os }}-turbo-` as the cache key prefix pattern to search against. This allows us to hit the cache on any subsequent ci runs despite `github.sha` changing.

    Example `ci` yaml with `.turbo` as chosen cache folder:

    ```yaml title=".github/workflows/ci.yml"
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
    ```
  </Step>
</Steps>


- [GitLab CI](/guides/ci-vendors/gitlab-ci.md): Learn how to use GitLab CI with Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

The following example shows how to use Turborepo with [GitLab CI](https://docs.gitlab.com/ee/ci/).

For a given root `package.json`:

```json title="./package.json"
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
```

And a `turbo.json`:

```json title="./turbo.json"
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
```

Create a file called `.gitlab-ci.yml` in your repository with the following contents:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```yaml title=".gitlab-ci.yml"
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
    ```

    > For more information visit the pnpm documentation section on GitLab CI integration, view it [here](https://pnpm.io/continuous-integration#gitlab)
  </Tab>

  <Tab value="yarn">
    ```yaml title=".gitlab-ci.yml"
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
    ```
  </Tab>

  <Tab value="npm">
    ```yaml title=".gitlab-ci.yml"
    image: node:latest
    stages:
      - build
    build:
      stage: build
      script:
        - npm install
        - npm run build
        - npm run test
    ```
  </Tab>

  <Tab value="bun">
    ```yaml title=".gitlab-ci.yml"
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

    ```
  </Tab>
</Tabs>

## Remote Caching

To use Remote Caching, retrieve the team and token for the Remote Cache for your provider. In this example, we'll use [Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching):

* `TURBO_TOKEN` - The Bearer token to access the Remote Cache
* `TURBO_TEAM` - The slug of the Vercel team to share the artifacts with

To use Vercel Remote Caching, you can get the value of these variables in a few steps:

1. Create a Scoped Access Token to your account in the [Vercel Dashboard](https://vercel.com/account/tokens)

![Vercel Access Tokens](/images/docs/vercel-create-token.png)

Copy the value to a safe place. You'll need it in a moment.

2. Go to your GitLab repository settings and click on the **Settings** and then **CI/CD** tab. Create a new variable called `TURBO_TOKEN` and enter the value of your Scoped Access Token.

![GitLab CI Variables](/images/docs/gitlab-ci-variables.png)
![GitLab CI Create Variable](/images/docs/gitlab-ci-create-variable.png)

3. Make a second secret called `TURBO_TEAM` and set it to your team slug - the part after `vercel.com/` in [your Team URL](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fsettings\&title=Find+Team+URL). For example, the slug for `vercel.com/acme` is `acme`.

Remote Caching will now be operational in your GitLab workflows.


- [Continuous Integration](/guides/ci-vendors/index.md): Recipes for using Turborepo with Vercel, GitHub Actions, and other continuous integration providers.

import { Cards, Card } from '#components/card';

Turborepo not only speeds up builds, but also the rest of your Continuous Integration pipeline by using [Remote Caching](/docs/core-concepts/remote-caching). Below are a few platform recipes to use Turborepo with your CI providers.

<Cards>
  <Card title="Vercel (Zero configuration)" href="/docs/guides/ci-vendors/vercel" />

  <Card title="GitHub Actions" href="/docs/guides/ci-vendors/github-actions" />

  <Card title="CircleCI" href="/docs/guides/ci-vendors/circleci" />

  <Card title="GitLab CI" href="/docs/guides/ci-vendors/gitlab-ci" />

  <Card title="Travis CI" href="/docs/guides/ci-vendors/travis-ci" />

  <Card title="Buildkite" href="/docs/guides/ci-vendors/buildkite" />
</Cards>

## General Setup

To enable Remote Caching for your CI:

1. Setup the environment variables for Turborepo in your CI to access your Remote Cache.
   | Variable | Description |
   | ----------- | ----------- |
   | `TURBO_TOKEN` | The Bearer token to access the Remote Cache |
   | `TURBO_TEAM` | The account name associated with your repository. When using{' '} <a href="https://vercel.com/docs/monorepos/remote-caching#vercel-remote-cache" rel="noreferrer noopener" target="_blank">Vercel Remote Cache</a>, this is [your team's slug](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fsettings\&title=Get+team+slug). |
2. Clone your repository.
3. Install your dependencies through your package manager.
4. Run your tasks through `turbo`.


- [Travis CI](/guides/ci-vendors/travis-ci.md): How to use Travis CI with Turborepo to optimize your CI workflow

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

The following example shows how to use Turborepo with [Travis CI](https://www.travis-ci.com/).

For a given root `package.json`:

```json title="./package.json"
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
```

And a `turbo.json`:

```json title="./turbo.json"
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
```

Create a file called `.travis.yml` in your repository with the following contents:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```yaml title=".travis.yml"
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
    ```

    > For more information visit the pnpm documentation section on Travis CI integration, view it [here](https://pnpm.io/continuous-integration#travis)
  </Tab>

  <Tab value="yarn">
    Travis CI detects the use of Yarn by the presence of `yarn.lock`. It will automatically ensure it is installed.

    ```yaml title=".travis.yml"
    language: node_js
    node_js:
      - lts/*
    install:
      - yarn
    script:
      - yarn build
    script:
      - yarn test
    ```
  </Tab>

  <Tab value="npm">
    ```yaml title=".travis.yml"
    language: node_js
    node_js:
      - lts/*
    install:
      - npm install
    script:
      - npm run build
    script:
      - npm run test
    ```
  </Tab>

  <Tab value="bun">
    ```yaml title=".travis.yml"
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
    ```
  </Tab>
</Tabs>

## Remote Caching

To use Remote Caching, retrieve the team and token for the Remote Cache for your provider. In this example, we'll use [Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching):

* `TURBO_TOKEN` - The Bearer token to access the Remote Cache
* `TURBO_TEAM` - The slug of the Vercel team to share the artifacts with

To use Vercel Remote Caching, you can get the value of these variables in a few steps:

1. Create a Scoped Access Token to your account in the [Vercel Dashboard](https://vercel.com/account/tokens)

![Vercel Access Tokens](/images/docs/vercel-create-token.png)

Copy the value to a safe place. You'll need it in a moment.

2. Go to your Travis repository settings and scroll down to the *Environment Variables* section. Create a new variable called `TURBO_TOKEN` and enter the value of your Scoped Access Token.

![Travis CI Variables](/images/docs/travis-ci-environment-variables.png)

3. Make a second secret called `TURBO_TEAM` and set it to your team slug - the part after `vercel.com/` in [your Team URL](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fsettings\&title=Find+Team+URL). For example, the slug for `vercel.com/acme` is `acme`.

4. Travis CI automatically loads environment variables stored in project settings into the CI environment. No modifications are necessary for the CI file.


- [Vercel](/guides/ci-vendors/vercel.md): Learn how to use Turborepo on Vercel.

![](/images/docs/turborepo-x-vercel.png)

Vercel's zero-config integration with Turborepo automatically understands your monorepo.

To deploy your Turborepo on Vercel, [create a new project](https://vercel.com/new) and import your code. Your projects will be pre-configured with the correct settings to use the [Vercel Remote Cache](https://vercel.com/docs/monorepos/remote-caching).

For more information about deploying your Turborepo to Vercel, [visit the Vercel documentation](https://vercel.com/docs/concepts/monorepos/turborepo).


- [Framework bindings in libraries](/guides/frameworks/framework-bindings.md): Learn how to create framework bindings in packages.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';

Framework bindings in a [Library Package](/docs/core-concepts/package-types#library-packages) integrate your library's code more deeply with a framework by leveraging APIs from the framework directly in the library.

To do this, use the `peerDependencies` field in `package.json` of the library, which makes the framework APIs available in your library without installing it directly in the package.

<Callout type="good-to-know">
  On this page, we'll be using Next.js for examples, but the concepts below
  apply to any framework or other dependency.
</Callout>

## Example

Add a `peerDependency` to your library for the dependency that you intend to create bindings for.

```json title="./packages/ui/package.json"
{
  "name": "@repo/ui",
  "peerDependencies": {
    "next": "*"
  }
}
```

<Callout type="good-to-know">
  In the example above, the `peerDependency` for `next` accepts any version. You
  may want to specify a range (for example, `">=15"`) according to your needs.
  Additionally, for older package managers, you may need to instruct your
  package manager to install peer dependencies with configuration, or add the
  dependency to `devDependencies` as a workaround.
</Callout>

This will make the dependency available in your library, allowing you to write code like below. Note the `className` prop, which sets a default styling for this component in the monorepo and can be overridden in the `props` object.

```tsx title="./packages/ui/src/link.tsx"
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
```

The version of `next` that will be resolved for the package will come from the consumers of the library. For example, if Next.js 15 is installed in your applications, the TypeScript types and APIs for `next` will also be Next.js 15.

## Splitting framework bindings using entrypoints

Using export paths to split a package into framework-specific entrypoints is the simplest way to add bindings to a library that aims to support multiple frameworks. By splitting entrypoints, bundlers have an easier time understanding the framework you intend to target and you're less likely to see strange bundling errors.

The example below shows a library with two entrypoints, each for a different type of link component. These abstractions likely contain your own styles, APIs, and other adjustments on top of the element they're wrapping.

* `./link`: An `<a>` HTML tag with some default styles from your design system
* `./next-js/link`: A customized version of [the Next.js `Link` component](https://nextjs.org/docs/app/building-your-application/routing/linking-and-navigating#link-component) with props that are preset to your organization's preferences
* `./svelte/link`: A customized version of an [`a` tag for Svelte](https://svelte.dev/docs/kit/link-options) with presets.

```json title="./packages/ui/package.json"
{
  "exports": {
    "./link": "./dist/link.js",
    "./next-js/link": "./dist/next-js/link.js"
  },
  "peerDependencies": {
    "next": "*"
  }
}
```

<Callout type="good-to-know">
  In the example above, the `peerDependency` for `next` accepts any version. You
  may want to specify a range (for example, `">=15"`) according to your needs.
</Callout>

This concept can be applied to any number of frameworks or other dependencies that you'd like to provide bindings for.


- [Frameworks](/guides/frameworks/index.md): Integrate your favorite framework into Turborepo.

import { Cards, Card } from '#components/card';

Turborepo works with **any framework**. Below, you'll find guides for the most common frameworks being used with Turborepo.

<Cards>
  <Card title="Next.js" href="/docs/guides/frameworks/nextjs" />

  <Card title="SvelteKit" href="/docs/guides/frameworks/sveltekit" />

  <Card title="Vite" href="/docs/guides/frameworks/vite" />

  <Card title="Nuxt" href="/docs/guides/frameworks/nuxt" />
</Cards>


- [Next.js](/guides/frameworks/nextjs.md): Learn how to use Next.js in a monorepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';

[Next.js](https://nextjs.org) is the React framework for the web. Used by some of the world's largest companies, Next.js enables you to create high-quality web applications with the power of React components.

## Quickstart

To get started with Next.js in a Turborepo quickly, follow the [quickstart](/docs/getting-started/installation) to create a repository with two Next.js applications:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest
    ```
  </Tab>
</Tabs>

## Adding a Next.js application to an existing repository

Use [`create-next-app`](https://nextjs.org/docs/app/api-reference/create-next-app) to set up a new Next.js application in a package. From the root of your repository, run:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-next-app@latest apps/my-app
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-next-app@latest apps/my-app
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-next-app@latest apps/my-app
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-next-app@latest apps/my-app
    ```
  </Tab>
</Tabs>

## Integrating with your repository

To add [Internal Packages](/docs/core-concepts/internal-packages) to your new application, install them into the app with your package manager:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ```
  </Tab>
</Tabs>

Make sure to run your package manager's install command. You also may need to update `scripts` in `package.json` to fit your use case in your repository.

### Customizing tasks

By default, the new application will use the tasks defined in the root `turbo.json`. If you'd like to configure tasks differently for the new application, use [Package Configurations](/docs/reference/package-configurations).

### Microfrontends

When using Next.js with [Turborepo's microfrontends](/docs/guides/microfrontends), make sure to set the `basePath` property for child applications. This ensures the assets like images and CSS will be routed to the correct application.

```ts title="./apps/my-app/next.config.ts"
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  basePath: '/docs',
};

export default nextConfig;
```


- [Nuxt](/guides/frameworks/nuxt.md): Learn more about using Nuxt in your monorepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';

[Nuxt](https://nuxt.com/) is an open source framework that makes web development intuitive and powerful.

## Quickstart

To get started with Nuxt in a Turborepo quickly, use [the `with-vue-nuxt` example](https://github.com/vercel/turborepo/tree/main/examples/with-vue-nuxt):

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest -e with-vue-nuxt
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest -e with-vue-nuxt
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest -e with-vue-nuxt
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest -e with-vue-nuxt
    ```
  </Tab>
</Tabs>

## Adding a Nuxt application to an existing repository

Use [Nuxi](https://www.npmjs.com/package/nuxi), Nuxt's CLI, to set up a new Nuxt application in a package. From the root of your repository, run:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx nuxi@latest init apps/my-app
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx nuxi@latest init apps/my-app
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx nuxi@latest init apps/my-app
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx nuxi@latest init apps/my-app
    ```
  </Tab>
</Tabs>

## Integrating with your repository

To add [Internal Packages](/docs/core-concepts/internal-packages) to your new application, install them into the app with your package manager:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ```
  </Tab>
</Tabs>

Make sure to run your package manager's install command. You also may need to update `scripts` in `package.json` to fit your use case in your repository.

### Customizing tasks

By default, the new application will use the tasks defined in the root `turbo.json`. If you'd like to configure tasks differently for the new application, use [Package Configurations](/docs/reference/package-configurations).

### Microfrontends

When using Nuxt with [Turborepo's microfrontends](/docs/guides/microfrontends), make sure to set the `base` property for child applications. This ensures the assets like images and CSS will be routed to the correct application.

```ts title="./apps/my-app/vite.config.ts"
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/admin',
});
```


- [SvelteKit](/guides/frameworks/sveltekit.md): Learn more about using SvelteKit in your monorepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';

[SvelteKit](https://kit.svelte.dev/) is a framework for rapidly developing robust, performant web applications using Svelte.

## Quickstart

To get started with SvelteKit in a Turborepo quickly, use [the `with-svelte` example](https://github.com/vercel/turborepo/tree/main/examples/with-svelte):

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest -e with-svelte
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest -e with-svelte
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest -e with-svelte
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest -e with-svelte
    ```
  </Tab>
</Tabs>

## Adding a SvelteKit application to an existing repository

Use [`npm create svelte`](https://kit.svelte.dev/docs/creating-a-project) to set up a new SvelteKit application in a package. From the root of your repository, run:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx sv create
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx sv create
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx sv create
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx sv create
    ```
  </Tab>
</Tabs>

## Integrating with your repository

To add [Internal Packages](/docs/core-concepts/internal-packages) to your new application, install them into the app with your package manager:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ```
  </Tab>
</Tabs>

Make sure to run your package manager's install command. You also may need to update `scripts` in `package.json` to fit your use case in your repository.

### Customizing tasks

By default, the new application will use the tasks defined in the root `turbo.json`. If you'd like to configure tasks differently for the new application, use [Package Configurations](/docs/reference/package-configurations).

### Microfrontends

When using Svelte with [Turborepo's microfrontends](/docs/guides/microfrontends), make sure to set the `base` property for child applications. This ensures the assets like images and CSS will be routed to the correct application.

```ts title="./apps/my-app/vite.config.ts"
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/admin',
});
```


- [Vite](/guides/frameworks/vite.md): Learn more about using Vite in your monorepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';

[Vite](https://vitejs.dev/) is a build tool that aims to provide a faster and leaner development experience for modern web projects.

## Quickstart

To get started with Vite in a Turborepo quickly, use [the `with-vite` example](https://github.com/vercel/turborepo/tree/main/examples/with-vite):

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest -e with-vite
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest -e with-vite
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest -e with-vite
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest -e with-vite
    ```
  </Tab>
</Tabs>

## Adding a Vite application to an existing repository

Use [`npm create vite`](https://vitejs.dev/guide/#scaffolding-your-first-vite-project) to set up a new Vite application in a package. From the root of your repository, run:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm create vite@latest apps/my-app
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn create vite@latest apps/my-app
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm create vite@latest apps/my-app
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bun create vite@latest apps/my-app
    ```
  </Tab>
</Tabs>

## Integrating with your repository

To add [Internal Packages](/docs/core-concepts/internal-packages) to your new application, install them into the app with your package manager:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```diff title="./apps/my-app/package.json"
    {
      "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "*"
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```diff title="./apps/my-app/package.json"
    {
     "name": "my-app",
      "dependencies": {
    +   "@repo/ui": "workspace:*"
      }
    }
    ```
  </Tab>
</Tabs>

Make sure to run your package manager's install command. You also may need to update `scripts` in `package.json` to fit your use case in your repository.

### Customizing tasks

By default, the new application will use the tasks defined in the root `turbo.json`. If you'd like to configure tasks differently for the new application, use [Package Configurations](/docs/reference/package-configurations).

### Microfrontends

When using Vite with [Turborepo's microfrontends](/docs/guides/microfrontends), make sure to set the `base` property for child applications. This ensures the assets like images and CSS will be routed to the correct application.

```ts title="./apps/my-app/vite.config.ts"
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/admin',
});
```


- [Biome](/guides/tools/biome.md): Learn how to use Biome in your Turborepo projects.

import { Callout } from '#components/callout';
import { CreateTurboCallout } from './create-turbo-callout.tsx';

[Biome](https://biomejs.dev/) is a fast formatter for JavaScript, TypeScript, JSX, and JSON that saves CI and developer time.

<CreateTurboCallout />

## Using Biome with Turborepo

Biome is a rare exception to most tools that are used with Turborepo because it is **so extraordinarily fast**. For this reason, we recommend using a [Root Task](/docs/crafting-your-repository/configuring-tasks#registering-root-tasks) rather than creating separate scripts in each of your packages.

<Callout type="info" title="Caching behavior">
  Using Biome at the root of the project will result in cache misses for all
  tasks when you upgrade Biome versions or change configuration. If you prefer
  the tradeoff of higher cache hit ratios in these situations over less
  configuration, you can still use Biome in separate scripts like the other
  recommendations in our guides.
</Callout>

### Initialize Biome

First, [follow the installation documentation to set up Biome](https://biomejs.dev/guides/getting-started/) in your repository. You'll then be able to create a script to use Biome in the root of your repository:

```json title="./package.json"
{
  "scripts": {
    "format-and-lint": "biome check .",
    "format-and-lint:fix": "biome check . --write"
  }
}
```

### Create a root task

In practice, Biome is unlikely to be a bottleneck in the iteration speed of your repository. For this reason, we can have less configuration to manage in our repository by using Biome in a [Root Task](/docs/crafting-your-repository/configuring-tasks#registering-root-tasks).

<Callout type="info">
  If you believe Biome may be faster in your repository split up into tasks in
  packages, you are free to do so. We encourage you to experiment with what's
  best for your use case.
</Callout>

To create a [Root Task](/docs/crafting-your-repository/configuring-tasks#registering-root-tasks), register the scripts to Turborepo:

```json title="./turbo.json"
{
  "tasks": {
    "//#format-and-lint": {},
    "//#format-and-lint:fix": {
      "cache": false
    }
  }
}
```

You'll now be able to run these scripts using `turbo run format-and-lint` and `turbo run format-and-lint:fix`.


- [Docker](/guides/tools/docker.md): Learn how to use Docker in a monorepo.

import { Callout } from '#components/callout';
import { File, Folder, Files } from '#components/files';
import { CreateTurboCallout } from './create-turbo-callout.tsx';

Building a [Docker](https://www.docker.com/) image is a common way to deploy all sorts of applications. However, doing so from a monorepo has several challenges.

<CreateTurboCallout />

## The problem

**In a monorepo, unrelated changes can make Docker do unnecessary work when deploying your app.**

Let's imagine you have a monorepo that looks like this:

<Files>
  <Folder name="apps" defaultOpen>
    <Folder name="api" defaultOpen>
      <File name="server.js" />

      <File name="package.json" />
    </Folder>

    <Folder name="web" defaultOpen>
      <File name="package.json" />
    </Folder>
  </Folder>

  <File name="package.json" />

  <File name="package-lock.json" />
</Files>

You want to deploy `apps/api` using Docker, so you create a Dockerfile:

```docker title="./apps/api/Dockerfile"
FROM node:16

WORKDIR /usr/src/app

# Copy root package.json and lockfile
COPY package.json ./
COPY package-lock.json ./

# Copy the api package.json
COPY apps/api/package.json ./apps/api/package.json

RUN npm install

# Copy app source
COPY . .

EXPOSE 8080

CMD [ "node", "apps/api/server.js" ]
```

This will copy the root `package.json` and the root lockfile to the Docker image. Then, it'll install dependencies, copy the app source and start the app.

You should also create a `.dockerignore` file to prevent node\_modules from being copied in with the app's source.

```txt title=".dockerignore"
node_modules
npm-debug.log
```

### The lockfile changes too often

Docker is pretty smart about how it deploys your apps. Just like Turborepo, it tries to do as [little work as possible](https://bitjudo.com/blog/2014/03/13/building-efficient-dockerfiles-node-dot-js/).

In our Dockerfile's case, it will only run `npm install` if the files it has in its image are *different* from the previous run. If not, it'll restore the `node_modules` directory it had before.

This means that whenever `package.json`, `apps/api/package.json` or `package-lock.json` change, the Docker image will run `npm install`.

This sounds great - until we realize something. The `package-lock.json` is *global* for the monorepo. That means that **if we install a new package inside `apps/web`, we'll cause `apps/api` to redeploy**.

In a large monorepo, this can result in a huge amount of lost time, as any change to a monorepo's lockfile cascades into tens or hundreds of deploys.

## The solution

The solution is to prune the inputs to the Dockerfile to only what is strictly necessary. Turborepo provides a simple solution - `turbo prune`.

```bash title="Terminal"
turbo prune api --docker
```

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

```bash title="Terminal"
docker build -f apps/web/Dockerfile .
```

<Callout type="info">
  This Dockerfile is written for a [Next.js](https://nextjs.org/) app that is
  using the `standalone` [output
  mode](https://nextjs.org/docs/pages/api-reference/next-config-js/output).
</Callout>

```docker title="./apps/web/Dockerfile"
FROM node:18-alpine AS base
RUN apk update
RUN apk add --no-cache libc6-compat
# Set working directory
WORKDIR /app

# ---
FROM base AS prepare
# Replace <your-major-version> with the major version installed in your repository. For example:
# RUN yarn global add turbo@^2
RUN yarn global add turbo@^<your-major-version>
COPY . .
# Add lockfile and package.json's of isolated subworkspace
# Generate a partial monorepo with a pruned lockfile for a target workspace.
# Assuming "web" is the name entered in the project's package.json: { name: "web" }
RUN turbo prune web --docker

# ---
FROM base AS builder
# First install the dependencies (as they change less often)
COPY --from=prepare /app/out/json/ .
RUN yarn install
# Build the project
COPY --from=prepare /app/out/full/ .

# Uncomment and use build args to enable remote caching
# ARG TURBO_TEAM
# ENV TURBO_TEAM=$TURBO_TEAM

# ARG TURBO_TOKEN
# ENV TURBO_TOKEN=$TURBO_TOKEN

RUN yarn turbo build

# ---
FROM base AS runner
# Don't run production as root for security reasons
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./apps/web/.next/static
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/public ./apps/web/public

CMD node apps/web/server.js
```

## Remote Caching

To take advantage of remote caches during Docker builds, you will need to make sure your build container has credentials to access your [Remote Cache](/docs/core-concepts/remote-caching).

There are many ways to take care of secrets in a Docker image. We will use a simple strategy here with multi-stage builds using secrets as build arguments that will get hidden for the final image.

Assuming you are using a Dockerfile similar to the one above, we will bring in some environment variables from build arguments right before `turbo build`:

```docker title="./apps/api/Dockerfile"
ARG TURBO_TEAM
ENV TURBO_TEAM=$TURBO_TEAM

ARG TURBO_TOKEN
ENV TURBO_TOKEN=$TURBO_TOKEN

RUN yarn turbo run build
```

`turbo` will now be able to hit your Remote Cache. To see a Turborepo cache hit for a non-cached Docker build image, run a command like this one from your project root:

```bash title="Terminal"
docker build -f apps/web/Dockerfile . --build-arg TURBO_TEAM=“your-team-name” --build-arg TURBO_TOKEN=“your-token“ --no-cache
```


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
    ```jsonc title="./apps/web/package.json"
    {
      "devDependencies": {
        "@repo/eslint-config": "workspace:*"
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```jsonc title="./apps/web/package.json"
    {
      "devDependencies": {
        "@repo/eslint-config": "*"
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```jsonc title="./apps/web/package.json"
    {
      "devDependencies": {
        "@repo/eslint-config": "*"
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```jsonc title="./apps/web/package.json"
    {
      "devDependencies": {
        "@repo/eslint-config": "workspace:*"
      }
    }
    ```
  </Tab>
</Tabs>

We can then import the configuration like this:

```js title="./apps/web/eslint.config.js"
import { nextJsConfig } from '@repo/eslint-config/next-js';

/** @type {import("eslint").Linter.Config} */
export default nextJsConfig;
```

Additionally, you can add configuration specific to the package like this:

```js title="./apps/web/eslint.config.js"
import { nextJsConfig } from '@repo/eslint-config/next-js';

/** @type {import("eslint").Linter.Config} */
export default [
  ...nextJsConfig,
  // Other configurations
];
```

## ESLint v8 (Legacy)

<Callout type="warn">
  ESLint v8 is end-of-life as of October 5, 2024. We encourage you to upgrade to
  ESLint v9 or later. This documentation is here to help with existing projects
  that have not yet upgraded.
</Callout>

Using legacy configuration from ESLint v8 and lower, we will end up with a file structure like this:

<Files>
  <Folder name="apps" defaultOpen>
    <Folder name="docs" defaultOpen>
      <File name="package.json" />

      <File name=".eslintrc.js" green />
    </Folder>

    <Folder name="web" defaultOpen>
      <File name="package.json" />

      <File name=".eslintrc.js" green />
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
      <File name=".eslintrc.js" green />

      <File name="package.json" />
    </Folder>
  </Folder>
</Files>

There's a package called `@repo/eslint-config`, and two applications, each with their own `.eslintrc.js`.

### The `@repo/eslint-config` package

The `@repo/eslint-config` file contains two files, `next.js`, and `library.js`. These are two different ESLint configurations, which we can use in different packages, depending on our needs.

A configuration for Next.js may look like this:

```js title="./packages/eslint-config/next.js"
/* Custom ESLint configuration for use with Next.js apps. */
module.exports = {
  extends: [
    'eslint-config-turbo',
    'eslint-config-next',
    // ...your other ESLint configurations
  ].map(require.resolve),
  // ...your other configuration
};
```

The `package.json` looks like this:

```json title="./packages/eslint-config/package.json"
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
```

Note that the ESLint dependencies are all listed here. This is useful, since it means we don't need to re-specify the dependencies inside the apps which import `@repo/eslint-config`.

### How to use the `@repo/eslint-config` package

In our `web` app, we first need to add `@repo/eslint-config` as a dependency.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```jsonc title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/eslint-config": "workspace:*"
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```jsonc title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/eslint-config": "*"
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```jsonc title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/eslint-config": "*"
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```jsonc title="./apps/web/package.json"
    {
      "dependencies": {
        "@repo/eslint-config": "workspace:*"
      }
    }
    ```
  </Tab>
</Tabs>

We can then import the config like this:

```js title="./apps/web/.eslintrc.js"
module.exports = {
  root: true,
  extends: ['@repo/eslint-config/next.js'],
};
```

By adding `@repo/eslint-config/next.js` to our `extends` array, we're telling ESLint to look for a package called `@repo/eslint-config`, and reference the file `next.js`.

## Setting up a `lint` task

The `package.json` for each package where you'd like to run ESLint should look like this:

```json title="./packages/*/package.json"
{
  "scripts": {
    "lint": "eslint ."
  }
}
```

With your scripts prepared, you can then create your Turborepo task:

```bash title="./turbo.json"
{
  "tasks": {
    "lint": {}
  }
}
```

You can now run `turbo lint` with [global `turbo`](/docs/getting-started/installation#global-installation) or create a script in your root `package.json`:

```json title="./package.json"
{
  "scripts": {
    "lint": "turbo run lint"
  }
}
```


- [Tools](/guides/tools/index.md): Learn how to use your favorite tools in a monorepo.

import { Cards, Card } from '#components/card';

Turborepo works with **all of your favorite tooling**. Below, you'll find guides for the most common tools being used with Turborepo.

<Cards>
  <Card title="Biome" href="/docs/guides/tools/biome" />

  <Card title="Docker" href="/docs/guides/tools/docker" />

  <Card title="ESLint" href="/docs/guides/tools/eslint" />

  <Card title="Jest" href="/docs/guides/tools/jest" />

  <Card title="Prisma" href="/docs/guides/tools/prisma" />

  <Card title="shadcn/ui" href="/docs/guides/tools/shadcn-ui" />

  <Card title="Storybook" href="/docs/guides/tools/storybook" />

  <Card title="TypeScript" href="/docs/guides/tools/typescript" />

  <Card title="Vitest" href="/docs/guides/tools/vitest" />
</Cards>


- [Jest](/guides/tools/jest.md): Learn how to use Jest in a Turborepo.

import { Callout } from '#components/callout';
import { File, Folder, Files } from '#components/files';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { CreateTurboCallout } from './create-turbo-callout.tsx';

[Jest](https://jestjs.io/) is a common test runner with a vast ecosystem. Integrating with Turborepo will lead to enormous speed-ups.

<CreateTurboCallout />

## Setting up

Let's say we have a monorepo that looks like this:

<Files>
  <Folder name="apps" defaultOpen>
    <Folder name="web" defaultOpen>
      <File name="package.json" />
    </Folder>
  </Folder>

  <Folder name="packages" defaultOpen>
    <Folder name="ui" defaultOpen>
      <File name="package.json" />
    </Folder>
  </Folder>
</Files>

Install `jest` into the packages where you plan on having test suites. For this example, we will have tests in `web` and `@repo/ui`:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm add jest --save-dev --filter=@repo/ui --filter=web
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn workspace web add jest --dev
    yarn workspace @repo/ui add jest --dev
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npm install jest --workspace=web --workspace=@repo/ui --save-dev
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    cd apps/web && bun install jest --dev
    cd packages/ui && bun install jest --dev
    ```
  </Tab>
</Tabs>

Both the `apps/web` and `packages/ui` have their own test suites, so we'll add a `test` script to their `package.json`:

<Tabs items={["web", "@repo/ui"]}>
  <Tab value="web">
    ```json title="./apps/web/package.json"
    {
      "name": "web",
      "scripts": {
        "test": "jest"
      },
      "devDependencies": {
        "jest": "latest"
      }
    }
    ```
  </Tab>

  <Tab value="@repo/ui">
    ```json title="./packages/ui/package.json"
    {
      "name": "@repo/ui",
      "scripts": {
        "test": "jest"
      },
      "devDependencies": {
        "jest": "latest"
      }
    }
    ```
  </Tab>
</Tabs>

Inside the root `turbo.json`, create a `test` task:

```json title="./turbo.json"
{
  "tasks": {
    "test": {}
  }
}
```

Now, `turbo test` can parallelize and cache all of the test suites from each package, only testing code that has changed.

## Running tests in watch mode

When you run your test suite normally, it completes and outputs to `stdout`. This means you can [cache it](/docs/crafting-your-repository/caching) with Turborepo.

But when you run your tests in a watched mode, the process never exits. This makes a watch task more like a [development task](/docs/crafting-your-repository/developing-applications).

Because of this difference, we recommend specifying **two separate Turborepo tasks**: one for running your tests, and one for running them in Jest's watch mode. Inside your each `package.json` file for each workspace:

<Tabs items={["web", "@repo/ui"]}>
  <Tab value="web">
    ```json title="./apps/web/package.json"
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
    ```
  </Tab>

  <Tab value="@repo/ui">
    ```json title="./packages/ui/package.json"
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
    ```
  </Tab>
</Tabs>

Inside the root `turbo.json`:

```json title="./turbo.json"
{
  "tasks": {
    "test": {},
    "test:watch": {
      "cache": false, // [!code highlight]
      "persistent": true // [!code highlight]
    }
  }
}
```

You can now either run this task using [global `turbo`](/docs/getting-started/installation#global-installation) as `turbo test:watch` or from a script in your root `package.json`:

<Tabs items={["Global turbo", "./package.json"]}>
  <Tab value="Global turbo">
    ```bash title="Terminal"
    turbo test
    ```

    ```bash title="Terminal"
    turbo test:watch
    ```
  </Tab>

  <Tab value="./package.json">
    ```json title="./package.json"
    {
      "scripts": {
        "test": "turbo run test",
        "test:watch": "turbo run test:watch"
      }
    }
    ```
  </Tab>
</Tabs>


- [Playwright](/guides/tools/playwright.md): Learn how to use Playwright in a Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

[Playwright](https://playwright.dev/) enables reliable end-to-end testing for modern web apps.

We recommend creating a Playwright package for each test suite that you'd like to run in your monorepo. This may mean suites broken up per-application, per-domain, or some other scheme, according to your needs. If you are unsure, start with creating a Playwright package per-application.

## Handling Playwright's environment variables

Playwright requires several environment variables to run correctly. To ensure that these variables are available within your tasks in [Strict Mode](/docs/crafting-your-repository/using-environment-variables#strict-mode), you'll want to add them to your pass through variables using [`passThroughEnv`](/docs/reference/configuration#passthroughenv) in your end-to-end task or [`globalPassThroughEnv`](/docs/reference/configuration#globalpassthroughenv) globally, depending on your scoping preferences.

<Tabs items={["Only in end-to-end task", "Globally"]}>
  <Tab value="Only in end-to-end task">
    The configuration below using `passThroughEnv` will allow environment variables that start with `PLAYWRIGHT_` into **the `e2e` task** and **will not affect hashing**.

    ```json title="./turbo.json"
    {
      "tasks": {
        "e2e": {
          "passThroughEnv": ["PLAYWRIGHT_*"]
        }
      }
    }
    ```
  </Tab>

  <Tab value="Globally">
    The configuration below using `globalPassThroughEnv` will allow environment variables that start with `PLAYWRIGHT_` into **all tasks** and **will not affect hashing**.

    ```json title="./turbo.json"
    {
      "globalPassThroughEnv": ["PLAYWRIGHT_*"]
    }
    ```
  </Tab>
</Tabs>

Note that pass through variables are used since we don't want to miss cache in situations where these Playwright-internal variables change. For example,`PLAYWRIGHT_BROWSERS_PATH` is used to locate browser binaries used by Playwright, and we don't want to miss cache if this location changes.

## Designing the task graph

We want to ensure the proper caching behavior for our end-to-end suites. Specifically, we want to make sure of cache misses in a few key situations:

* If test suites change, cache gets missed.
* If code tested by the suites changes, cache gets missed.

The first requirement will be met naturally since the hash for the task will change when test code is changed. However, the second requirement means you need to ensure end-to-end tests depend on changes in application source code.

This relationship can be expressed in `turbo.json` and the end-to-end suite's `package.json`.

<Tabs items={["turbo.json", "package.json" ]}>
  <Tab value="turbo.json">
    ```json title="./turbo.json"
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
    ```
  </Tab>

  <Tab value="package.json">
    ```json title="./tooling/playwright-web/package.json"
    {
      "name": "@repo/playwright-web",
      "dependencies": {
        "web": "workspace:*" // [!code highlight]
      }
    }
    ```
  </Tab>
</Tabs>

Later on, when you want to run your end-to-end tests, use [the `--only` flag](/docs/reference/run#--only) to run end-to-end tests without running the application's build first. As an example, your command may look like `turbo run e2e --filter=@repo/playwright-myapp --only`.

## Sharing Playwright utilities

You can also create a common package for shared utilities that you need in your end-to-end test suites. We recommend using `peerDependencies` in this shared package so that you can get access to Playwright used in consumers without having to install Playwright into the shared package itself.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```json title="./packages/playwright-utilities/package.json"
    {
      "name": "@repo/playwright-utilities",
      "peerDependencies": {
        "playwright": "workspace:*"
    }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```json title="./packages/playwright-utilities/package.json"
    {
      "name": "@repo/playwright-utilities",
      "peerDependencies": {
        "playwright": "*"
    }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```json title="./packages/playwright-utilities/package.json"
    {
      "name": "@repo/playwright-utilities",
      "peerDependencies": {
        "playwright": "*"
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```json title="./packages/playwright-utilities/package.json"
    {
      "name": "@repo/playwright-utilities",
      "peerDependencies": {
        "playwright": "workspace:*"
      }
    }
    ```
  </Tab>
</Tabs>


- [Prisma](/guides/tools/prisma.md): Learn how to use Prisma in a Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';
import { Steps, Step } from '#components/steps';
import { CreateTurboCallout } from './create-turbo-callout.tsx';

[Prisma](https://www.prisma.io/) unlocks a new level of developer experience when working with databases thanks to its intuitive data model, automated migrations, type-safety & auto-completion.

[Their official guide](https://www.prisma.io/docs/guides/turborepo) describes how to integrate Prisma into a Turborepo, including:

* Prisma client initialization
* Packaging the client as an [Internal Package](/docs/core-concepts/internal-packages)
* Performing migrations
* Working on your applications locally
* Deploying

## Example

To get started with our community-supported Prisma example, run:

```bash title="Terminal"
npx create-turbo@latest -e with-prisma
```


- [shadcn/ui](/guides/tools/shadcn-ui.md): Learn how to use shadcn/ui in a Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

[shadcn/ui](https://ui.shadcn.com/docs/monorepo) is an open-source set of beautifully designed components made with Tailwind CSS that you can copy and paste into your apps.

To get started with shadcn/ui in a new monorepo, run:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx shadcn@canary init
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    npx shadcn@canary init
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx shadcn@canary init
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx shadcn@canary init
    ```
  </Tab>
</Tabs>

When prompted, select the option for monorepos.

To add a component, run:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx shadcn@canary add [COMPONENT]
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    npx shadcn@canary add [COMPONENT]
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx shadcn@canary add [COMPONENT]
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx shadcn@canary add [COMPONENT]
    ```
  </Tab>
</Tabs>

## More information

To learn more about using shadcn/ui in Turborepo, [visit the docs for shadcn/ui](https://ui.shadcn.com/docs/monorepo).


- [Storybook](/guides/tools/storybook.md): Learn how to use Storybook in a Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';
import { Steps, Step } from '#components/steps';

[Storybook](https://storybook.js.org/) is a popular way to build UI components in an isolated environment. By putting Storybook into your Turborepo, you can easily develop your design system right alongside your applications.

## Quickstart

If you'd rather use a template, this guide is walking through how to build [this Storybook/Turborepo template](https://vercel.com/templates/react/turborepo-design-system) on Vercel.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest -e design-system
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest -e design-system
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest -e design-system
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest -e design-system
    ```
  </Tab>
</Tabs>

## Guide

<Steps>
  <Step>
    ### Create a monorepo

    If you don't have an existing project, use [create-turbo](/docs/getting-started/installation) to create a new monorepo:

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm dlx create-turbo@latest
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn dlx create-turbo@latest
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        npx create-turbo@latest
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        bunx create-turbo@latest
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Create a directory for the app

    You'll need a directory for the Storybook application:

    ```bash title="Terminal"
    mkdir apps/storybook
    cd apps/storybook
    ```
  </Step>

  <Step>
    ### Add the Storybook application

    In the `apps/storybook` directory, initialize a new Storybook application:

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm create storybook@latest
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn create storybook@latest
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        npm create storybook@latest
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        bun create storybook@latest
        ```
      </Tab>
    </Tabs>

    Follow the prompts to create an application. For the rest of this guide, we'll assume React and TypeScript.

    <Callout type="good-to-know">
      After going through Storybook's onboarding, you can [uninstall the onboarding
      addon](https://github.com/storybookjs/addon-onboarding/blob/main/README.md).
    </Callout>
  </Step>

  <Step>
    ### Add your UI kit to Storybook

    Now, install your UI package into Storybook.

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm add @repo/ui --filter=storybook
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn workspace storybook add @repo/ui
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        npm install @repo/ui --workspace=storybook
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        cd apps/storybook && bun install @repo/ui
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Set up a story for your Button component

    Delete the stories and components found in `src/stories` that were created by the Storybook scaffolding tool. You will be making your own.

    As an example, here is a story for the `Button` component from `@repo/ui/button`.

    ```tsx title="./apps/storybook/src/stories/Button.stories.tsx"
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
    ```
  </Step>

  <Step>
    ### Align scripts to your tasks

    Last, integrate the new Storybook application into your Turborepo:

    ```json title="apps/storybook/package.json"
    {
      "scripts": {
        "dev": "storybook dev -p 6006", // [!code highlight]
        "build": "storybook build" // [!code highlight]
      }
    }
    ```

    These scripts will now run with the `turbo dev` and `turbo build` tasks in your `turbo.json`.

    To ensure file outputs are cached when you run `build`, add `storybook-static` to the outputs of your `turbo.json` build task:

    ```diff title="turbo.json"
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
    ```

    <Step>
      ### Add Storybook build outputs to `.gitignore`

      Ensure that the build outputs for Storybook are not committed to source control

      ```diff title=".gitignore"
      + storybook-static
      ```
    </Step>

    <Step>
      ### Verify your configuration

      Run `turbo build` to build the Storybook application alongside the rest of your applications.

      You can also run `turbo build` again to see cache hits for your builds.
    </Step>
  </Step>
</Steps>

## More tips

### Co-locating stories

If you'd prefer to co-locate your stories to their source code (rather than having them in the Storybook application), you'll need some extra configuration.

<Steps>
  <Step>
    #### Re-configure Storybook sources

    In `.storybook/main.ts`, change the `stories` paths in `config` to the directories you'd like to capture. For instance, if you'd like to write stories in the UI package:

    ```diff title="./apps/storybook/.storybook/main.ts"

    const config = {
      stories: [
    -   "../src/**/*.mdx",
    -   "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
    +   "../../../packages/ui/src/**/*.stories.@(js|jsx|mjs|ts|tsx)",
    };
    ```
  </Step>

  <Step>
    #### Move story files to the UI package

    Following along with [the guide above](/docs/guides/tools/storybook#set-up-a-story-for-your-button-component), move the `./apps/storybook/src/stories/Button.stories.tsx` file to `./packages/ui/src/Button.stories.tsx`.

    Update components imports so that they reference the now co-located modules. For instance, in the story's imports:

    ```diff title="./packages/ui/src/Button.stories.tsx"
    - import { Button } from "@repo/ui/button";
    + import { Button } from "./button";
    ```

    <Callout type="good-to-know">
      You may also need to update [absolute
      imports](/docs/guides/tools/typescript#use-nodejs-subpath-imports-instead-of-typescript-compiler-paths)
      according to your changes and usage.
    </Callout>

    You'll also need to install any Storybook packages required for writing stories. For example, moving the story from above would require that you install `@storybook/react` into your `@repo/ui` package.

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm add @storybook/react --filter=@repo/ui --save-dev
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn workspace @repo/ui add @storybook/react --dev
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        npm install @storybook/react --workspace=@repo/ui --save-dev
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        cd packages/ui && bun install @storybook/react --dev
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    #### Configure caching

    Because stories are now in the UI package, changes to those stories can cause cache misses for any builds that depend on your UI package. However, changing a story doesn't mean your production applications should miss cache.

    To prevent this, exclude stories from the inputs to your `build` task in your root `turbo.json`. You'll also need to create a `build:storybook` task, which you'll need in a moment:

    ```json title="./turbo.json"
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
    ```

    Additionally, create a [Package Configuration](/docs/reference/package-configurations) in the `storybook` application so stories are **accounted for in building the Storybook application, specifically**:

    ```json title="./apps/storybook/turbo.json"
    {
      "extends": ["//"],
      "tasks": {
        "build:storybook": {
          "dependsOn": ["^build:storybook"],
          "outputs": ["storybook-static/**"]
        }
      }
    }
    ```

    <Callout type="good-to-know">
      If you are using the [Compiled Package
      pattern](/docs/core-concepts/internal-packages#compiled-packages), you may
      also need to add `^build` to your `dependsOn`.
    </Callout>
  </Step>

  <Step>
    #### Rename the build script

    Last, make sure your script to build Storybook uses the configuration we just wrote by renaming it to the name of the task:

    ```json title="apps/storybook/package.json"
    {
      "scripts": {
        "dev": "storybook dev -p 6006",
        "build:storybook": "storybook build" // [!code highlight]
      }
    }
    ```

    The script that was once `"build"` is now `"build:storybook"` to ensure the stories are included in hashes for caching.
  </Step>

  <Step>
    #### Verify your configuration

    To ensure your setup is correct:

    1. Run `turbo build:storybook build`. You should see cache misses.
    2. Run `turbo build:storybook build` again. You should see all cache hits.
    3. Make a code change **to a story** in your `@repo/ui` package.
    4. Run `turbo build:storybook build` again. You should **only** see a cache miss for the Storybook application. All others should hit cache.
  </Step>
</Steps>

### Adding CSS

If your UI package exports its own CSS, you'll need to add it to the renders in the Storybook app, similar to how you would add it to your applications. [The Storybook documentation](https://storybook.js.org/docs/configure/styling-and-css#css) recommends you add it to the `.storybook/preview.ts` file.


- [Tailwind CSS](/guides/tools/tailwind.md): Learn how to use Tailwind CSS in a Turborepo.

import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from '#components/callout';
import { Steps, Step } from '#components/steps';

[Tailwind CSS](https://tailwindcss.com/) is a CSS framework that allows you to rapidly build modern websites without ever leaving your HTML.

## Quickstart

If you'd rather use a template, this guide is walking through how to build [this Tailwind CSS + Turborepo template](https://github.com/vercel/turborepo/tree/main/examples/with-tailwind).

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest -e with-tailwind
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest -e with-tailwind
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest -e with-tailwind
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest -e with-tailwind
    ```
  </Tab>
</Tabs>

## Guide

<Callout type="info">This guide is for Tailwind CSS v4.</Callout>

<Steps>
  <Step>
    ### Create a monorepo

    If you don't have an existing project, use [create-turbo](/docs/getting-started/installation) to create a new monorepo:

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm dlx create-turbo@latest
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn dlx create-turbo@latest
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        npx create-turbo@latest
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        bunx create-turbo@latest
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Add Tailwind CSS to your application

    [Follow Tailwind CSS's guides](https://tailwindcss.com/docs/installation/using-vite) to set up Tailwind CSS for your frontend framework.

    Once completed, you can start working on bringing your UI package into the applications.
  </Step>

  <Step>
    ### Create a shared Tailwind CSS configuration package

    First, build an [Internal Package](https://turborepo.com/docs/core-concepts/internal-packages) with four files:

    <Tabs items={["package.json", "shared-styles.css", "postcss.config.js (Optional)"]}>
      <Tab value="package.json">
        This `package.json` installs Tailwind CSS so we can create the file shared styles and export for the rest of the repository.

        ```json title="./packages/tailwind-config/package.json"
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
        ```
      </Tab>

      <Tab value="shared-styles.css">
        This `shared-styles.css` file will be shared to the libraries and applications in the repository. The variables shown will be available anywhere that the file is included.

        ```css title="./packages/tailwind-config/shared-styles.css"
        @import 'tailwindcss';

        @theme {
          --blue-1000: #2a8af6;
          --purple-1000: #a853ba;
          --red-1000: #e92a67;
        }
        ```
      </Tab>

      <Tab value="postcss.config.js (Optional)">
        If your frontends need a PostCSS configuration file, you can create one to share.

        ```js title="./packages/tailwind-config/postcss.config.js"
        export const postcssConfig = {
          plugins: {
            '@tailwindcss/postcss': {},
          },
        };
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Create the UI package

    You can now build the components to share to your applications.

    For a full example, [visit the source code for `@repo/ui` package in the Tailwind CSS example](https://github.com/vercel/turborepo/tree/main/examples/with-tailwind/packages/ui). The files required for your Tailwind CSS setup are below.

    <Tabs items={["package.json", "turbo.json", "styles.css"]}>
      <Tab value="package.json">
        The `package.json` installs the dependencies for the package, sets up scripts for development and build environments, and marks the exports for the package.

        ```json title="./packages/ui/package.json"
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
        ```

        <Callout type="good-to-know">
          Above, we've only included the code related to setting up Tailwind. The full
          package.json is
          [here](https://github.com/vercel/turborepo/tree/main/examples/with-tailwind/packages/ui/package.json).
        </Callout>
      </Tab>

      <Tab value="turbo.json">
        Create a `build` and `dev` task that runs the scripts for building of components and style sheets in parallel.

        ```json title="./packages/ui/turbo.json"
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
        ```
      </Tab>

      <Tab value="styles.css">
        This `styles.css` contains component-level styles for the shared UI library.

        ```css title="./packages/ui/src/styles.css"
        /* Component-level styles for the UI package */
        @import 'tailwindcss' prefix(ui);
        ```

        <Callout type="info">
          Tailwind classes used in this package should be prefixed with `ui:` to avoid
          style specificity issues.
        </Callout>
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Use the UI package in an application

    Install the packages you've created into your application.

    <Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
      <Tab value="pnpm">
        ```bash title="Terminal"
        pnpm add @repo/ui @repo/tailwind-config --save-dev --filter=@repo/ui --filter=web
        ```
      </Tab>

      <Tab value="yarn">
        ```bash title="Terminal"
        yarn workspace web add @repo/ui @repo/tailwind-config --dev
        yarn workspace @repo/ui add @repo/ui @repo/tailwind-config --dev
        ```
      </Tab>

      <Tab value="npm">
        ```bash title="Terminal"
        npm install @repo/ui @repo/tailwind-config --workspace=web --workspace=@repo/ui --save-dev
        ```
      </Tab>

      <Tab value="bun">
        ```bash title="Terminal"
        cd apps/web && bun install @repo/ui @repo/tailwind-config --dev
        cd packages/ui && bun install @repo/ui @repo/tailwind-config --dev
        ```
      </Tab>
    </Tabs>

    Then, configure the files in your application so the styles from the UI package are reflected in the application.

    <Tabs items={["globals.css", "layout.tsx", "postcss.config.js (Optional)"]}>
      <Tab value="globals.css">
        ```css title="./apps/web/app/globals.css"
        @import 'tailwindcss';
        @import '@repo/tailwind-config';
        ```
      </Tab>

      <Tab value="layout.tsx">
        ```tsx title="./apps/web/app/layout.tsx"
        import '@repo/ui/styles.css';
        import './globals.css';
        ```
      </Tab>

      <Tab value="postcss.config.js (Optional)">
        ```js title="./apps/web/postcss.config.js"
        import { postcssConfig } from '@repo/tailwind-config/postcss';

        export default postcssConfig;
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>


- [TypeScript](/guides/tools/typescript.md): Learn how to use TypeScript in a monorepo.

import { Callout } from '#components/callout';
import { File, Folder, Files } from '#components/files';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { LinkToDocumentation } from '#components/link-to-documentation';

TypeScript is an excellent tool in monorepos, allowing teams to safely add types to their JavaScript code. While there is some complexity to getting set up, this guide will walk you through the important parts of a TypeScript setup for most use cases.

* [Sharing TypeScript configuration](#sharing-tsconfigjson)
* [Building a TypeScript package](#building-a-typescript-package)
* [Making type checking faster across your workspace](/docs/guides/tools/typescript#linting-your-codebase)

<Callout type="info">
  This guide assumes you are using a recent version of TypeScript and uses some
  features that are only available in those versions. You may need to adjust the
  guidance on this page if you are unable to features from those versions.
</Callout>

## Sharing `tsconfig.json`

You want to build consistency into your TypeScript configurations so that your entire repo can use great defaults and your fellow developers can know what to expect when writing code in the Workspace.

TypeScript's `tsconfig.json` sets the configuration for the TypeScript compiler and features an [`extends` key](https://www.typescriptlang.org/tsconfig#extends) that you'll use to share configuration across your workspace.

This guide will use [`create-turbo`](/docs/reference/create-turbo) as an example.

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```bash title="Terminal"
    pnpm dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="yarn">
    ```bash title="Terminal"
    yarn dlx create-turbo@latest
    ```
  </Tab>

  <Tab value="npm">
    ```bash title="Terminal"
    npx create-turbo@latest
    ```
  </Tab>

  <Tab value="bun">
    ```bash title="Terminal"
    bunx create-turbo@latest
    ```
  </Tab>
</Tabs>

### Use a base `tsconfig` file

Inside `packages/typescript-config`, you have a few `json` files which represent different ways you might want to configure TypeScript in various packages. The `base.json` file is extended by every other `tsconfig.json` in the workspace and looks like this:

```json title="./packages/typescript-config/base.json"
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
```

<LinkToDocumentation href="https://www.typescriptlang.org/tsconfig">
  `tsconfig` options reference
</LinkToDocumentation>

### Creating the rest of the package

The other `tsconfig` files in this package use the `extends` key to start with the base configuration and customize for specific types of projects, like for Next.js (`nextjs.json`) and a React library (`react-library.json`).

Inside `package.json`, name the package so it can be referenced in the rest of the Workspace:

```json title="packages/typescript-config/package.json"
{
  "name": "@repo/typescript-config"
}
```

## Building a TypeScript package

### Using the configuration package

First, install the `@repo/typescript-config` package into your package:

<Tabs groupId="package-manager" items={['pnpm', 'yarn', 'npm', 'bun']} persist>
  <Tab value="pnpm">
    ```json title="./apps/web/package.json"
    {
      "devDependencies": {
         "@repo/typescript-config": "workspace:*",
         "typescript": "latest",
      }
    }
    ```
  </Tab>

  <Tab value="yarn">
    ```json title="./apps/web/package.json"
    {
      "devDependencies": {
         "@repo/typescript-config": "*",
         "typescript": "latest",
      }
    }
    ```
  </Tab>

  <Tab value="npm">
    ```json title="./apps/web/package.json"
    {
      "devDependencies": {
         "@repo/typescript-config": "*",
         "typescript": "latest",
      }
    }
    ```
  </Tab>

  <Tab value="bun">
    ```json title="./apps/web/package.json"
    {
      "devDependencies": {
         "@repo/typescript-config": "workspace:*",
         "typescript": "latest",
      }
    }
    ```
  </Tab>
</Tabs>

Then, extend the `tsconfig.json` for the package from the `@repo/typescript-config` package. In this example, the `web` package is a Next.js application:

```json title="./apps/web/tsconfig.json"
{
  "extends": "@repo/typescript-config/nextjs.json",
  "compilerOptions": {
    "outDir": "dist"
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

### Creating entrypoints to the package

First, make sure your code gets compiled with `tsc` so there will be a `dist` directory. You'll need a `build` script as well as a `dev` script:

```json title="./packages/ui/package.json"
{
  "scripts": {
    "dev": "tsc --watch",
    "build": "tsc"
  }
}
```

Then, set up the entrypoints for your package in `package.json` so that other packages can use the compiled code:

```json title="./packages/ui/package.json"
{
  "exports": {
    "./*": {
      "types": "./src/*.ts",
      "default": "./dist/*.js"
    }
  }
}
```

Setting up `exports` this way has several advantages:

* Using the `types` field allows `tsserver` to use the code in `src` as the source of truth for your code's types. Your editor will always be up-to-date with the latest interfaces from your code.
* You can quickly add new entrypoints to your package without creating [dangerous barrel files](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js#what's-the-problem-with-barrel-files).
* You'll receive auto-importing suggestions for your imports across package boundaries in your editor.

<Callout type="warn">
  If you're publishing the package, you cannot use references to source code in
  `types` since only the compiled code will be published to npm. You'll need to
  generate and reference declaration files and source maps.
</Callout>

## Linting your codebase

To use TypeScript as a linter, you can check the types across your workspace **fast** using Turborepo's caching and parallelization.

First, add a `check-types` script to any package that you want to check the types for:

```json title="./apps/web/package.json"
{
  "scripts": {
    "check-types": "tsc --noEmit"
  }
}
```

Then, create a `check-types` task in `turbo.json`. From the [Configuring tasks guide](/docs/crafting-your-repository/configuring-tasks#dependent-tasks-that-can-be-run-in-parallel), we can make the task run in parallel while respecting source code changes from other packages using a [Transit Node](/docs/core-concepts/package-and-task-graph#transit-nodes):

```json title="./turbo.json"
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
```

Then, run your task using `turbo check-types`.

## Best practices

### Use `tsc` to compile your packages

For [Internal Packages](/docs/core-concepts/internal-packages), we recommend that you use `tsc` to compile your TypeScript libraries whenever possible. While you can use a bundler, it's not necessary and adds extra complexity to your build process. Additionally, bundling a library can mangle the code before it makes it to your applications' bundlers, causing hard to debug issues.

### Enable go-to-definition across package boundaries

"Go-to-definition" is an editor feature for quickly navigating to the original declaration or definition of a symbol (like a variable or function) with a click or hotkey. Once TypeScript is configured correctly, you can navigate across [Internal Packages](/docs/core-concepts/internal-packages) with ease.

#### Just-in-Time Packages

Exports from [Just-in-Time Packages](/docs/core-concepts/internal-packages#just-in-time-packages) will automatically bring you to the original TypeScript source code. Go-to-definition will work as expected.

#### Compiled Packages

Exports from [Compiled Packages](/docs/core-concepts/internal-packages#compiled-packages) require the use of [`declaration`](https://www.typescriptlang.org/tsconfig/#declaration) and [`declarationMap`](https://www.typescriptlang.org/tsconfig/#declarationMap) configurations for go-to-definition to work. After you've enabled these two configurations for the package, compile the package with `tsc`, and open the output directory to find declaration files and source maps.

<Files>
  <Folder defaultOpen name="packages">
    <Folder defaultOpen name="ui">
      <Folder defaultOpen name="dist">
        <File name="button.js" />

        <File name="button.d.ts" green />

        <File name="button.d.ts.map" green />
      </Folder>
    </Folder>
  </Folder>
</Files>

With these two files in place, your editor will now navigate to the original source code.

### Use Node.js subpath imports instead of TypeScript compiler `paths`

It's possible to create absolute imports in your packages using [the TypeScript compiler's `paths` option](https://www.typescriptlang.org/tsconfig#paths), but these paths can cause failed compilation when using [Just-in-Time Packages](https://turborepo.com/docs/core-concepts/internal-packages#just-in-time-packages). [As of TypeScript 5.4](https://devblogs.microsoft.com/typescript/announcing-typescript-5-4/#auto-import-support-for-subpath-imports), you can use [Node.js subpath imports](https://nodejs.org/api/packages.html#imports) instead for a more robust solution.

#### Just-in-Time Packages

In [Just-in-Time packages](https://turborepo.com/docs/core-concepts/internal-packages#just-in-time-packages), `imports` must target the source code in the package, since build outputs like `dist` won't be created.

<Tabs storageKey="ts-imports-jit" items={["package.json", "Source code"]}>
  <Tab value="package.json">
    ```json title="./packages/ui/package.json"
    {
      "imports": {
        "#*": "./src/*"
      }
    }
    ```
  </Tab>

  <Tab value="Source code">
    ```tsx title="./packages/ui/button.tsx"
    import { MY_STRING } from "#utils.ts" // Uses .ts extension // [!code highlight]

    export const Button = () => {
      return (
        <button>{MY_STRING}</button>
      )
    }
    ```
  </Tab>
</Tabs>

#### Compiled Packages

In [Compiled packages](https://turborepo.com/docs/core-concepts/internal-packages#compiled-packages), `imports` target the built outputs for the package.

<Tabs storageKey="ts-imports-compiled" items={["package.json", "Source code"]}>
  <Tab value="package.json">
    ```json title="./packages/ui/package.json"
    {
      "imports": {
        "#*": "./dist/*"
      }
    }
    ```
  </Tab>

  <Tab value="Source code">
    ```tsx title="./packages/ui/button.tsx"
    import { MY_STRING } from '#utils.js'; // Uses .js extension // [!code highlight]

    export const Button = () => {
      return <button>{MY_STRING}</button>;
    };
    ```
  </Tab>
</Tabs>

### You likely don't need a `tsconfig.json` file in the root of your project

As mentioned in the [Structuring your repository guide](/docs/crafting-your-repository/structuring-a-repository#anatomy-of-a-package), you want to treat each package in your tooling as its own unit. This means each package should have its own `tsconfig.json` to use instead of referencing a `tsconfig.json` in the root of your project. Following this practice will make it easier for Turborepo to cache your type checking tasks, simplifying your configuration.

The only case in which you may want to have a `tsconfig.json` in the Workspace root is to set configuration for TypeScript files that are not in packages. For example, if you have a script written with TypeScript that you need to run from the root, you may need a `tsconfig.json` for that file.

However, this practice is also discouraged since any changes in the Workspace root will cause all tasks to miss cache. Instead, move those scripts to a different directory in the repository.

### You likely don't need TypeScript Project References

We don't recommend using TypeScript Project References as they introduce both another point of configuration as well as another caching layer to your workspace. Both of these can cause problems in your repository with little benefit, so we suggest avoiding them when using Turborepo.

## Limitations

### Your editor won't use a package's TypeScript version

`tsserver` is not able to use different TypeScript versions for different packages in your code editor. Instead, it will discover a specific version and use that everywhere.

This can result in differences between the linting errors that show in your editor and when you run `tsc` scripts to check types. If this is an issue for you, consider [keeping the TypeScript dependency on the same version](/docs/crafting-your-repository/managing-dependencies#keeping-dependencies-on-the-same-version).


- [Vitest](/guides/tools/vitest.md): Learn how to use Vitest in a monorepo.

import { Callout } from '#components/callout';
import { File, Folder, Files } from '#components/files';
import { CreateTurboCallout } from './create-turbo-callout.tsx';
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

[Vitest](https://vitest.dev/) is a test runner from the Vite ecosystem. Integrating it with Turborepo will lead to enormous speed-ups.

[The Vitest documentation](https://vitest.dev/guide/workspace) shows how to create a "Vitest Projects" configuration that runs all tests in the monorepo from one root command, enabling behavior like merged coverage reports out-of-the-box. This feature doesn't follow modern best practices for monorepos, since its designed for compatibility with Jest (whose Workspace feature was built before [package manager Workspaces](/docs/crafting-your-repository/structuring-a-repository)).

<Callout type="warning">
  Vitest has deprecated workspaces in favor of projects. When using projects,
  individual project vitest configs can't extend the root config anymore since
  they would inherit the projects configuration. Instead, a separate shared file
  like `vitest.shared.ts` is needed.
</Callout>

Because of this you have two options, each with their own tradeoffs:

* [Leveraging Turborepo for caching](#leveraging-turborepo-for-caching)
* [Using Vitest's Projects feature](#using-vitests-projects-feature)

### Leveraging Turborepo for caching

To improve on cache hit rates and only run tests with changes, you can choose to configure tasks per-package, splitting up the Vitest command into separate, cacheable scripts in each package. This speed comes with the tradeoff that you'll need to create merged coverage reports yourself.

<Callout>
  For a complete example, run `npx create-turbo@latest --example with-vitest` or
  [visit the example's source
  code](https://github.com/vercel/turborepo/tree/main/examples/with-vitest).
</Callout>

#### Setting up

Let's say we have a simple [package manager Workspace](/docs/crafting-your-repository/structuring-a-repository) that looks like this:

<Files>
  <Folder name="apps" defaultOpen>
    <Folder name="web" defaultOpen>
      <File name="package.json" />
    </Folder>
  </Folder>

  <Folder name="packages" defaultOpen>
    <Folder name="ui" defaultOpen>
      <File name="package.json" />
    </Folder>
  </Folder>
</Files>

Both `apps/web` and `packages/ui` have their own test suites, with `vitest` [installed into the packages that use them](/docs/crafting-your-repository/managing-dependencies#install-dependencies-where-theyre-used). Their `package.json` files include a `test` script that runs Vitest:

```json title="./apps/web/package.json"
{
  "scripts": {
    "test": "vitest run"
  },
  "devDependencies": {
    "vitest": "latest"
  }
}
```

Inside the root `turbo.json`, create a `test` task:

```json title="./turbo.json"
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
```

Now, `turbo run test` can parallelize and cache all of the test suites from each package, only testing code that has changed.

#### Running tests in watch mode

When you run your test suite in CI, it logs results and eventually exits upon completion. This means you can [cache it with Turborepo](/docs/crafting-your-repository/caching). But when you run your tests using Vitest's watch mode during development, the process never exits. This makes a watch task more like a [long-running, development task](/docs/crafting-your-repository/developing-applications).

Because of this difference, we recommend specifying **two separate Turborepo tasks**: one for running your tests, and one for running them in watch mode.

<Callout>
  This strategy below creates two tasks, one for local development and one for
  CI. You could choose to make the `test` task for local development and create
  some `test:ci` task instead.
</Callout>

For example, inside the `package.json` file for each workspace:

```json title="./apps/web/package.json"
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest --watch"
  }
}
```

And, inside the root `turbo.json`:

```json title="./turbo.json"
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
```

You can now run your tasks using [global `turbo`](/docs/getting-started/installation#global-installation) as `turbo run test:watch` or from a script in your root `package.json`:

<Tabs items={["Global turbo", "./package.json"]}>
  <Tab value="Global turbo">
    ```bash title="Terminal"
    turbo run test

    turbo run test:watch
    ```
  </Tab>

  <Tab value="./package.json">
    ```json title="./package.json"
    {
      "scripts": {
        "test": "turbo run test",
        "test:watch": "turbo run test:watch"
      }
    }
    ```
  </Tab>
</Tabs>

#### Creating merged coverage reports

[Vitest's Projects feature](#using-vitests-projects-feature) creates an out-of-the-box coverage report that merges all of your packages' tests coverage reports. Following the Turborepo strategy, though, you'll have to merge the coverage reports yourself.

<Callout type="info">
  The [`with-vitest`
  example](https://github.com/vercel/turborepo/tree/main/examples/with-vitest)
  shows a complete example that you may adapt for your needs. You can get
  started with it quickly using `npx create-turbo@latest --example with-vitest`.
</Callout>

To do this, you'll follow a few general steps:

1. Run `turbo run test` to create the coverage reports.
2. Merge the coverage reports with [`nyc merge`](https://github.com/istanbuljs/nyc?tab=readme-ov-file#what-about-nyc-merge).
3. Create a report using `nyc report`.

Turborepo tasks to accomplish will look like:

```json title="./turbo.json"
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
```

With this in place, run `turbo test && turbo report` to create a merged coverage report.

<Callout type="info">
  The [`with-vitest`
  example](https://github.com/vercel/turborepo/tree/main/examples/with-vitest)
  shows a complete example that you may adapt for your needs. You can get
  started with it quickly using `npx create-turbo@latest --example with-vitest`.
</Callout>

### Using Vitest's Projects feature

The Vitest Projects feature doesn't follow the same model as a [package manager Workspace](/docs/crafting-your-repository/structuring-a-repository). Instead, it uses a root script that then reaches out into each package in the repository to handle the tests in that respective package.

In this model, there aren't package boundaries, from a modern JavaScript ecosystem perspective. This means you can't rely on Turborepo's caching, since Turborepo leans on those package boundaries.

Because of this, you'll need to use [Root Tasks](/docs/crafting-your-repository/configuring-tasks#registering-root-tasks) if you want to run the tests using Turborepo. Once you've configured [a Vitest Projects setup](https://vitest.dev/guide/workspace), create the Root Tasks for Turborepo:

```json title="./turbo.json"
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
```

**Notably, the file inputs for a Root Task include all packages by default, so any change in any package will result in a cache miss.** While this does make for a simplified configuration to create merged coverage reports, you'll be missing out on opportunities to cache repeated work.

### Using a hybrid approach

You can combine the benefits of both approaches by implementing a hybrid solution. This approach unifies local development using Vitest's Projects feature while preserving Turborepo's caching in CI. This comes at the tradeoff of slightly more configuration and a mixed task running model in the repository.

First, create a shared configuration package since individual projects can't extend the root config when using projects. Create a new package for your shared Vitest configuration:

```json title="./packages/vitest-config/package.json"
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
```

```json title="./packages/vitest-config/tsconfig.json"
{
  "extends": "@repo/typescript-config/base.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["dist", "node_modules"]
}
```

```ts title="./packages/vitest-config/src/index.ts"
export const sharedConfig = {
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    // Other shared configuration
  },
};
```

Then, create your root Vitest configuration using projects:

```ts title="./vitest.config.ts"
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
```

In this setup, your packages maintain their individual Vitest configurations that import the shared config. First, install the shared config package:

```json title="./packages/ui/package.json"
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
```

Then create the Vitest configuration:

```ts title="./packages/ui/vitest.config.ts"
import { defineConfig } from 'vitest/config';
import { sharedConfig } from '@repo/vitest-config';

export default defineConfig({
  ...sharedConfig,
  test: {
    ...sharedConfig.test,
    // Package-specific overrides if needed
  },
});
```

Make sure to update your `turbo.json` to include the new configuration package in the dependency graph:

```json title="./turbo.json"
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
```

While your root `package.json` includes scripts for running tests globally:

```json title="./package.json"
{
  "scripts": {
    "test:projects": "vitest run",
    "test:projects:watch": "vitest --watch"
  }
}
```

This configuration allows developers to run `pnpm test:projects` or `pnpm test:projects:watch` at the root for a seamless local development experience using Vitest projects, while CI continues to use `turbo run test` to leverage package-level caching. **You'll still need to handle merged coverage reports manually as described in the previous section**.
