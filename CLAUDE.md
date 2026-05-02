# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **restored Claude Code source tree** reconstructed from source maps. Version: `999.0.0-restored`. Some modules contain restoration-time fallbacks and shim behavior — prefer minimal, auditable changes and document any workaround.

## Commands

```bash
bun install          # Install dependencies and local shim packages
bun run dev          # Start the restored CLI entrypoint interactively
bun run start        # Alias for dev
bun run version      # Verify CLI boots and prints version
bun run dev:restore-check   # Run through dev-entry.ts for restoration checks
```

- **Runtime**: Bun 1.3.5+ required, Node.js 24+ required
- **No lint or test scripts** are configured in package.json
- There is no consolidated automated test suite — validate changes by running `bun run dev` and exercising the affected flow manually

## Architecture

### Entry Points

- `src/bootstrap-entry.ts` — Main entry point. Supports `CLAUDE_CODE_OVERRIDE_CWD` env var, then imports `src/entrypoints/cli.tsx`
- `src/entrypoints/` — Contains CLI, MCP, agent SDK, and sandbox entry points

### Core Structure

| Directory | Purpose |
|-----------|---------|
| `src/commands/` | ~80 CLI slash commands (e.g., `/help`, `/model`, `/mcp`). Each command is a self-contained module with `index.ts` entry |
| `src/tools/` | Tool implementations (BashTool, FileReadTool, AgentTool, etc.). Each tool is a directory with its implementation |
| `src/services/` | Background services: analytics, API, MCP, LSP, settings sync, memory, etc. |
| `src/components/` | React/Ink UI components for the TUI |
| `src/bridge/` | Remote control bridge (mobile/web client communication via REPL bridge, SSE, WebSocket) |
| `src/cli/` | CLI infrastructure: transports (SSE, WebSocket, Hybrid), structured I/O, remote I/O |
| `src/skills/` | Bundled skill definitions (`claude-api` for various languages, `verify`) |
| `src/shims/` | Local package shims for Chrome MCP, Computer Use, color-diff-napi, modifiers-napi, url-handler-napi |
| `src/vendor/` | Restored/compatibility code |
| `src/tasks/` | Task management: DreamTask, LocalAgentTask, RemoteAgentTask, etc. |
| `src/state/` | Application state management |
| `src/types/` | TypeScript type definitions |

### Command System

Commands are defined in `src/commands/` and registered in `src/commands.ts`. Types:
- **`prompt`** — Expands to text sent to the model (skills, slash commands)
- **`local`** — Local text output commands
- **`local-jsx`** — Ink UI rendering commands (blocked in remote/bridge mode)

Feature flags (`bun:bundle`) gate optional commands like BRIDGE_MODE, VOICE_MODE, ULTRAPLAN, etc.

### Module Path Alias

`tsconfig.json` maps `src/*` → `./src/*` for imports.

## Coding Conventions

- TypeScript-first with ESM imports and `react-jsx`
- No semicolons in most files, single quotes preferred
- camelCase for variables/functions, PascalCase for React components and manager classes
- kebab-case for command directories (e.g., `src/commands/install-slack-app/`)
- Some files have `ANT-ONLY import markers` — do not reorder imports in those files
- Prefer small, focused modules over broad utility dumps

## Important Notes

- This is **not pristine upstream source** — many files are reconstructed
- Modules with restoration fallbacks may behave differently from the original
- When changing code, prefer minimal diffs that are easy to audit
- Document any workaround added due to restored/shimmed module behavior
