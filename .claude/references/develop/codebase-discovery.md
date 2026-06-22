# Codebase Discovery

## Package & Build System Discovery

Scan the project root and common subdirectories for these markers:

| File | Build System | Language/Runtime |
|------|-------------|-----------------|
| `package.json` | npm/yarn/pnpm | JavaScript/TypeScript |
| `tsconfig.json` | TypeScript compiler | TypeScript |
| `requirements.txt` / `pyproject.toml` / `setup.py` | pip/poetry/setuptools | Python |
| `Cargo.toml` | Cargo | Rust |
| `go.mod` | Go modules | Go |
| `pom.xml` | Maven | Java/Kotlin |
| `build.gradle` / `build.gradle.kts` | Gradle | Java/Kotlin |
| `Gemfile` | Bundler | Ruby |
| `*.csproj` / `*.sln` | dotnet/MSBuild | C# |
| `Makefile` | Make | Any |
| `Dockerfile` / `docker-compose.yml` | Docker | Containerized |
| `serverless.yml` / `template.yaml` | Serverless/SAM | Cloud functions |
| `cdk.json` / `cdktf.json` | CDK/CDKTF | Infrastructure |

## Framework Detection Patterns

Identify frameworks by scanning imports and configuration:
- **React**: `import React`, `jsx`/`tsx` files, `react-dom`
- **Next.js**: `next.config.js`, `pages/` or `app/` directory structure
- **Express**: `require('express')`, `app.get/post/use` patterns
- **FastAPI**: `from fastapi import`, `@app.get` decorators
- **Django**: `settings.py` with `INSTALLED_APPS`, `urls.py`, `models.py`
- **Spring Boot**: `@SpringBootApplication`, `application.properties/yml`
- **Rails**: `config/routes.rb`, `app/controllers/`, `ActiveRecord`

## Source File Classification

Classify every source file into one of these categories:
- **Model/Entity**: Data structures, database models, DTOs, schemas
- **Controller/Handler**: Request routing, input parsing, response formatting
- **Service/UseCase**: Business logic, orchestration, domain operations
- **Repository/DAO**: Data access, queries, persistence abstraction
- **Utility/Helper**: Cross-cutting functions, formatters, validators
- **Configuration**: App config, environment setup, dependency injection
- **Middleware**: Request/response pipeline (auth, logging, error handling)
- **Test**: Unit tests, integration tests, fixtures, factories
- **Migration**: Database schema changes, data migrations
- **Static/Asset**: Templates, stylesheets, images, static content

## Dependencies

Record the dependencies a component relies on — internal (other modules in this repo) and external (third-party packages). Note any circular references you happen to spot. Do not build a full file-by-file dependency graph; the living docs do not hold one (changing a public surface is verified by find-references at the time, which stays accurate where a hand-maintained edge list rots).

## API Endpoint Inventory

For each discovered endpoint, record:
- HTTP method and path (or GraphQL operation name)
- Request parameters (path, query, body, headers)
- Response shape and status codes
- Authentication/authorization requirements

## Technical Debt Indicators

Flag these patterns during code scan:
- TODO/FIXME/HACK comments
- Suppressed linter warnings (`// eslint-disable`, `# noqa`, `@SuppressWarnings`)
- Hard-coded credentials, URLs, or magic numbers
- God classes/files (>500 lines with multiple responsibilities)
- Missing error handling on I/O operations
- Duplicated logic, dead code (unused imports, unreachable branches, commented-out blocks)
- Missing tests on critical paths
- Outdated dependencies (major version behind)
