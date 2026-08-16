import type { Plugin } from "@opencode-ai/plugin"

// Session context plugin — gives agents a tool to compact the current session
// and preserves critical state across compaction.
//
// Why: every request re-sends the full conversation as prompt-cache reads. A
// team-lead session that accumulates sub-agent results drifts to 100K+ tokens
// and pays that on every step. Compacting between delegation waves resets the
// cache floor to ~system-prompt size.
//
// Tools:
//   - session_compact — compact the current session (resets prompt-cache context)
//   - session_summarize — summarize the current session (same API family)
//
// Hooks:
//   - experimental.session.compacting — injects state (todo, issue, next step)
//     into the compaction prompt so it survives the context collapse.

export const SessionContext: Plugin = async ({ client }) => {
  async function runCommand(sessionID: string, command: string): Promise<string> {
    if (!sessionID) return "No sessionID available — command skipped."
    const res = await client.session.command({
      path: { id: sessionID },
      body: { command, arguments: "" },
    })
    return `Session command "${command}" executed.`
  }

  return {
    tool: {
      session_compact: {
        description:
          "Compact the current session: collapse the conversation into a summary to reset prompt-cache context. Use between sub-agent delegation waves, never mid-task.",
        args: {},
        async execute(_args, context) {
          return runCommand(context.sessionID, "session.compact")
        },
      },
      session_summarize: {
        description:
          "Summarize the current session without compacting it. The summary is stored on the session and can be read to regain context.",
        args: {},
        async execute(_args, context) {
          if (!context.sessionID) return "No sessionID available — summarize skipped."
          const res = await client.session.summarize({
            path: { id: context.sessionID },
          })
          return `Session summarized (${res.data}).`
        },
      },
    },

    "experimental.session.compacting": async (input, output) => {
      output.context.push(`## Persistent state — do not lose across compaction
Keep the following so work can continue after compaction:
- The active GitHub issue / task being worked on
- Files currently being modified or planned
- The next step to take
- Any blockers or pending decisions
If this session does not have such state, state that explicitly.`)
    },
  }
}
