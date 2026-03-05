# WedConnect Frontend

React (Vite) frontend for WedConnect. Built with TypeScript, Tailwind CSS, shadcn/ui, and Axios.

## Setup

```bash
npm install
```

Copy environment variables and point to your backend:

```bash
cp .env.example .env.local
```

Edit `.env.local` and set `VITE_API_BASE_URL` to your backend API base URL (e.g. `http://localhost:8000` for local Django). Do not commit `.env` or `.env.local`.

## Development

```bash
npm run dev
```

Runs the app at `http://localhost:5173` (or the next available port).

## Build

```bash
npm run build
```

Output is in `dist/`.

## Environment

| Variable | Description |
|----------|-------------|
| `VITE_API_BASE_URL` | Backend API base URL with no trailing slash (e.g. `http://localhost:8000`). Used by the Axios client in `src/api/client.ts`. |

## Project structure

- `src/api/` – Axios client and API functions (auth, vendors)
- `src/components/ui/` – shadcn/ui components; add more with `npx shadcn@latest add <component>`
- `src/components/layout/` – Layout components
- `src/pages/` – Route-level pages
- `src/hooks/` – Custom hooks (e.g. `useApi`)
- `src/types/` – Shared TypeScript types
- `src/lib/utils.ts` – Utilities (e.g. `cn` for class names)
