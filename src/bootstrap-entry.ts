import { realpathSync } from 'fs'
import { ensureBootstrapMacro } from './bootstrapMacro'

// Support overriding cwd via CLAUDE_CODE_OVERRIDE_CWD environment variable.
// This must run before any module reads process.cwd() (e.g., bootstrap/state.ts,
// TrustDialog via getFsImplementation().cwd()).
if (process.env.CLAUDE_CODE_OVERRIDE_CWD) {
  const targetDir = process.env.CLAUDE_CODE_OVERRIDE_CWD
  try {
    const resolved = realpathSync(targetDir)
    process.chdir(resolved)
  } catch {
    process.chdir(targetDir)
  }
}

ensureBootstrapMacro()

await import('./entrypoints/cli.tsx')
