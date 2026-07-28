---
name: bikeshed
description: Run two independent subagents through a structured debate on the same prompt — independent answers, cross-critique, revision, then a synthesized unified response. Use when explicitly invoked as /bikeshed with a prompt, or when the user asks for a two-agent debate/adversarial comparison on a plan, design, or other complex piece of work. Best for plans and complex open-ended work, not simple factual questions.
---

# Bikeshed: two-agent structured debate

Take the user's prompt (everything after `/bikeshed`), run it through two independent subagents in a debate protocol, and synthesize their final answers into one unified response. If no prompt was given, ask the user what question or plan to bikeshed before starting.

The value comes from independence followed by controlled exchange. Do not let either agent see the other's work before Round 1 is complete, and do not editorialize when relaying material between them — pass responses and critiques verbatim.

## Protocol

Call the two agents **Agent A** and **Agent B**. Both are `general-purpose` subagents spawned with the Agent tool. Run each round's two calls in parallel (same message, two tool uses). Spawn Round 1 synchronously (`run_in_background: false`). Keep continuity with SendMessage using each agent's ID/name; never respawn a fresh agent mid-protocol, because the whole point is that each agent accumulates the full debate in its own context.

**Timing reality**: SendMessage resumes a completed agent *in the background* — the tool returns immediately and the agent's reply arrives later as a task notification. So Rounds 2 and 3 are: send both messages, end your turn with a brief status, and wait for BOTH notifications before starting the next round. Never fabricate or predict a pending agent's output, and never proceed with only one side's result.

**Critique routing** (easy to cross up): in Round 3, Agent A receives *Agent B's critique of A's response*, and Agent B receives *Agent A's critique of B's response* — each agent gets the critique written ABOUT its own work, not its own critique echoed back.

By the end, each agent's context contains, in order:

1. The original prompt
2. Its own original response
3. The other agent's original response
4. Its own critique of the other agent's response
5. The other agent's critique of its own response

### Round 1 — independent responses

Spawn Agent A and Agent B in parallel with the same prompt:

> You are one of two agents independently working on the same task. Respond to the following prompt as thoroughly and well as you can. You will later see another agent's response and be asked to critique it, so make your reasoning explicit. If the task requires reading the codebase or other research, do that research now.
>
> PROMPT:
> {the user's prompt, verbatim, plus any relevant conversation context the agents need to do the task — e.g. what the repo is, and "this is a planning task, do NOT modify files" when applicable}

Both agents may read the repo, search, etc. as needed for the task.

Optional divergence: both agents are the same model given the same prompt, so their Round 1 responses tend to overlap heavily. When the task is wide-open (a plan, a design), you may append one sentence assigning each a complementary emphasis (e.g. "lean conservative/minimal" vs. "lean ambitious/thorough") to widen the explored space. Keep the core prompt identical; skip this when the user's prompt already implies a specific angle.

### Round 2 — cross-critique

Send each agent the other's Round 1 response via SendMessage:

> Here is the other agent's response to the same prompt:
>
> {other agent's Round 1 response, verbatim}
>
> Critique it. First VERIFY its factual claims against the source (the codebase, docs, data) where feasible — a critique grounded in checked facts is worth far more than one argued from your own draft. Then identify concrete weaknesses, errors, risks, and omissions, and note anything it does better than your own response. Be specific and adversarial but fair — the goal is to improve the final answer, not to win.

### Round 3 — receive critique and produce the final response

Send each agent the critique the *other* agent wrote about *its* response:

> Here is the other agent's critique of YOUR original response:
>
> {other agent's Round 2 critique, verbatim}
>
> You now have the full exchange in context: the prompt, both original responses, your critique of theirs, and their critique of yours. Produce your final, complete response to the original prompt. Incorporate whatever the exchange showed to be right — steal the other agent's good ideas, concede valid criticisms, and defend the choices that survived scrutiny. Your final message IS the deliverable: make it a standalone, complete response to the prompt, not a diff against your earlier draft.

### Synthesis

You (the orchestrator) now hold both final responses. Write one unified response to the user:

- Merge the two into a single coherent answer — the best structure, ideas, and details from each, not a side-by-side comparison.
- Where the agents converged after debate, present that consensus with confidence; convergence after adversarial exchange is a meaningful signal.
- Where they still disagree, do not paper over it: state the disagreement, both positions briefly, and give your own recommendation with reasoning.
- Briefly note (a sentence or two, not a play-by-play) anything notable from the debate — e.g. a serious error one agent caught in the other, or a point that flipped after critique.

The unified response is the deliverable. Do not dump both agents' full final answers on the user unless they ask.

## Notes

- This protocol is expensive (6 subagent turns; a real run on a planning prompt cost ~430k subagent tokens and ~10 minutes wall clock). Don't use it for tasks with a single verifiable answer; suggest a direct approach instead if the prompt is trivial.
- Heavy convergence between the two final responses is normal and is itself a signal — report it as such in the synthesis rather than manufacturing disagreement.
- If the task involves modifying files, keep BOTH agents read-only/plan-only during the debate — the deliverable is the synthesized plan or response. Apply changes only afterward, and only if the user asked for implementation.
- If one agent dies or a SendMessage fails, retry once; if it still fails, tell the user which round broke and salvage what you have (e.g. synthesize from the surviving material) rather than silently restarting from scratch.
