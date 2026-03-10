
# Turborepo documentation

Generated at: Wed, 17 Dec 2025 20:47:48 GMT

## Turborepo

> Turborepo is a build system optimized for JavaScript and TypeScript, written in Rust.

## Docs

- [Core concepts](/core-concepts/index.md): Learn about the core concepts behind Turborepo.
- [Internal Packages](/core-concepts/internal-packages.md): Learn how to build Internal Packages in your monorepo.
- [Package and Task Graphs](/core-concepts/package-and-task-graph.md): Turborepo builds a Task Graph based on your configuration and repository structure.
- [Package types](/core-concepts/package-types.md): Learn about the different types of packages in a workspace.
- [Remote Caching](/core-concepts/remote-caching.md): Share cache artifacts across machines for even faster builds.
- [Caching](/crafting-your-repository/caching.md): Learn about caching in Turborepo.
- [Configuring tasks](/crafting-your-repository/configuring-tasks.md): Learn how to describe the workflows in your repository to get them done as fast as possible.
- [Constructing CI](/crafting-your-repository/constructing-ci.md): Learn how Turborepo can help you efficiently complete all the necessary tasks and accelerate your development workflow.
- [Creating an Internal Package](/crafting-your-repository/creating-an-internal-package.md): Learn how to create an Internal Package for your monorepo.
- [Developing applications](/crafting-your-repository/developing-applications.md): Learn how to develop applications in your repository.
- [Crafting your repository](/crafting-your-repository/index.md): Design and build your Turborepo.
- [Managing dependencies](/crafting-your-repository/managing-dependencies.md): Learn how to manage dependencies in your monorepo's workspace.
- [Running tasks](/crafting-your-repository/running-tasks.md): Learn how to run tasks in your repository through the `turbo` CLI.
- [Structuring a repository](/crafting-your-repository/structuring-a-repository.md): Start by creating a repository using the conventions of the ecosystem.
- [Understanding your repository](/crafting-your-repository/understanding-your-repository.md): Learn how to understand your repository structure using Turborepo.
- [Upgrading](/crafting-your-repository/upgrading.md): Learn how to upgrade `turbo` to get the latest improvements to your repository.
- [Using environment variables](/crafting-your-repository/using-environment-variables.md): Learn how to handle environments for your applications.
- [Add to an existing repository](/getting-started/add-to-existing-repository.md): Using Turborepo with your existing repository
- [Editor integration](/getting-started/editor-integration.md): Making the most of Turborepo
- [Start with an example](/getting-started/examples.md): Start with an example Turborepo.
- [Getting started](/getting-started/index.md): Get started with Turborepo.
- [Installation](/getting-started/installation.md): Learn how to get started with Turborepo.
- [Buildkite](/guides/ci-vendors/buildkite.md): Learn how to use Buildkite with Turborepo.
- [CircleCI](/guides/ci-vendors/circleci.md): Learn how to use CircleCI with Turborepo.
- [GitHub Actions](/guides/ci-vendors/github-actions.md): Learn how to use GitHub Actions with Turborepo.
- [GitLab CI](/guides/ci-vendors/gitlab-ci.md): Learn how to use GitLab CI with Turborepo.
- [Continuous Integration](/guides/ci-vendors/index.md): Recipes for using Turborepo with Vercel, GitHub Actions, and other continuous integration providers.
- [Travis CI](/guides/ci-vendors/travis-ci.md): How to use Travis CI with Turborepo to optimize your CI workflow
- [Vercel](/guides/ci-vendors/vercel.md): Learn how to use Turborepo on Vercel.
- [Framework bindings in libraries](/guides/frameworks/framework-bindings.md): Learn how to create framework bindings in packages.
- [Frameworks](/guides/frameworks/index.md): Integrate your favorite framework into Turborepo.
- [Next.js](/guides/frameworks/nextjs.md): Learn how to use Next.js in a monorepo.
- [Nuxt](/guides/frameworks/nuxt.md): Learn more about using Nuxt in your monorepo.
- [SvelteKit](/guides/frameworks/sveltekit.md): Learn more about using SvelteKit in your monorepo.
- [Vite](/guides/frameworks/vite.md): Learn more about using Vite in your monorepo.
- [Generating code](/guides/generating-code.md): Learn how to generate code using Turborepo.
- [Handling platforms](/guides/handling-platforms.md): Learn how to handle caching around operating systems, architectures, and other arbitrary conditions for Turborepo tasks.
- [Guides](/guides/index.md): Learn how to use your favorite tooling in a Turborepo.
- [Microfrontends](/guides/microfrontends.md): Learn how to use Turborepo's built-in microfrontends proxy for local development.
- [Migrating from Nx](/guides/migrating-from-nx.md): Learn how to migrate to Turborepo from Nx.
- [Multi-language support](/guides/multi-language.md): Learn how to use multiple languages with Turborepo.
- [Publishing libraries](/guides/publishing-libraries.md): Learn how to publish libraries to the npm registry from a monorepo.
- [Single-package workspaces](/guides/single-package-workspaces.md): Learn how to use Turborepo in a single-package workspace.
- [Skipping tasks](/guides/skipping-tasks.md): Never do the same work twice.
- [Biome](/guides/tools/biome.md): Learn how to use Biome in your Turborepo projects.
- [Docker](/guides/tools/docker.md): Learn how to use Docker in a monorepo.
- [ESLint](/guides/tools/eslint.md): Learn how to use ESLint in a monorepo.
- [Tools](/guides/tools/index.md): Learn how to use your favorite tools in a monorepo.
- [Jest](/guides/tools/jest.md): Learn how to use Jest in a Turborepo.
- [Playwright](/guides/tools/playwright.md): Learn how to use Playwright in a Turborepo.
- [Prisma](/guides/tools/prisma.md): Learn how to use Prisma in a Turborepo.
- [shadcn/ui](/guides/tools/shadcn-ui.md): Learn how to use shadcn/ui in a Turborepo.
- [Storybook](/guides/tools/storybook.md): Learn how to use Storybook in a Turborepo.
- [Tailwind CSS](/guides/tools/tailwind.md): Learn how to use Tailwind CSS in a Turborepo.
- [TypeScript](/guides/tools/typescript.md): Learn how to use TypeScript in a monorepo.
- [Vitest](/guides/tools/vitest.md): Learn how to use Vitest in a monorepo.
- [Introduction](/index.md): Welcome to the Turborepo documentation!
- [Invalid environment variable prefix](/messages/invalid-env-prefix.md): Learn more about errors with invalid environment variable prefixes in Turborepo.
- [Missing root task in turbo.json](/messages/missing-root-task-in-turbo-json.md): Learn more about errors for missing root tasks in turbo.json in Turborepo.
- [Package task in single-package workspace error](/messages/package-task-in-single-package-workspace.md): Learn more about errors with package tasks in single-package workspaces.
- [Recursive `turbo` invocations](/messages/recursive-turbo-invocations.md): Learn more about errors with recursive scripts and tasks in Turborepo.
- [Unnecessary package task syntax error](/messages/unnecessary-package-task-syntax.md): Learn more about errors with unnecessary package task syntax in Turborepo.
- [bin](/reference/bin.md): API reference for the `turbo bin` command
- [boundaries](/reference/boundaries.md): API reference for the `turbo boundaries` command
- [Configuring turbo.json](/reference/configuration.md): Learn how to configure Turborepo through `turbo.json`.
- [create-turbo](/reference/create-turbo.md): Quickly set up a new Turborepo repository from scratch.
- [devtools](/reference/devtools.md): API reference for the `turbo devtools` command
- [eslint-config-turbo](/reference/eslint-config-turbo.md): Learn more about eslint-config-turbo.
- [eslint-plugin-turbo](/reference/eslint-plugin-turbo.md): Learn more about eslint-plugin-turbo.
- [generate](/reference/generate.md): API reference for the `turbo generate` command
- [File glob specification](/reference/globs.md): Learn about the file glob specification used by `turbo`.
- [Turborepo API reference](/reference/index.md): Learn about Turborepo's APIs using the reference.
- [info](/reference/info.md): API reference for the `turbo info` command
- [link](/reference/link.md): API reference for the `turbo link` command
- [login](/reference/login.md): API reference for the `turbo login` command
- [logout](/reference/logout.md): API reference for the `turbo logout` command
- [ls](/reference/ls.md): API reference for the `turbo ls` command
- [Options overview](/reference/options-overview.md): Flags, configurations, and System Environment Variables for Turborepo
- [Package Configurations](/reference/package-configurations.md): Learn how to use Package Configurations to bring greater task flexibility to your monorepo's package.
- [prune](/reference/prune.md): API reference for the `turbo prune` command
- [query](/reference/query.md): API reference for the `turbo query` command
- [run](/reference/run.md): API reference for the `turbo run` command
- [scan](/reference/scan.md): API reference for the `turbo scan` command
- [System environment variables](/reference/system-environment-variables.md): Learn about system variables used by Turborepo.
- [telemetry](/reference/telemetry.md): API reference for the `turbo telemetry` command
- [@turbo/codemod](/reference/turbo-codemod.md): Learn more about how Turborepo uses codemods to make version migrations easy.
- [@turbo/gen](/reference/turbo-gen.md): Quickly generate new code in your Turborepo.
- [turbo-ignore](/reference/turbo-ignore.md): Learn how to use turbo-ignore to skip tasks in CI.
- [unlink](/reference/unlink.md): API reference for the `turbo unlink` command
- [watch](/reference/watch.md): API reference for the `watch` command
- [Support policy](/support-policy.md): Learn about Turborepo's Support policy.