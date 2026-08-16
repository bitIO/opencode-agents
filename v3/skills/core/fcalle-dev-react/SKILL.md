---
name: fcalle-dev-react
description: React patterns — functional components, hooks rules, state management, RSC, accessibility, forms, CSS conventions. Use when writing or reviewing React/Next.js components, hooks, TSX files, or UI logic.
---

## React

- **Functional components + hooks**; class components only when interfacing with legacy code.
- **Server components / RSC** when the framework supports it (Next.js 13+); fetch on the server when you can.
- **One component per file** for non-trivial components; co-locate styles and tests.
- **Props are read-only** — never mutate; derive state instead.
- **`useState` for local UI state, `useReducer` for complex transitions, context for cross-cutting concerns, a real store (Zustand/Redux Toolkit/Jotai) for app state.**
- **No prop drilling beyond 2–3 levels** — lift to context or store.
- **Stable keys** — never use array index as a key for dynamic lists.
- **Memoization is opt-in, not default** — `useMemo`/`useCallback` only when profiling shows a need.
- **Effects are escape hatches** — prefer event handlers and derived state. If you reach for `useEffect`, ask "is this really a side effect of rendering?"
- **Suspense + Error Boundaries** at route level, minimum.
- **Accessibility is non-negotiable** — semantic HTML, ARIA only when semantics fall short, keyboard navigable, color contrast checked.
- **Forms** — controlled inputs for validation-heavy forms, uncontrolled for simple ones; consider `react-hook-form` for complex cases.
- **CSS** — design system first; CSS Modules / Tailwind / vanilla-extract over global styles. No inline styles except for dynamic values.
