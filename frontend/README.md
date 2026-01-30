# CP-Helper Frontend

The user interface for the Competitive Programming Assistant, built with [Next.js](https://nextjs.org/) and [assistant-ui](https://github.com/Yonom/assistant-ui).

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **UI Components**: assistant-ui, Radix UI, Lucide React
- **Styling**: Tailwind CSS
- **State Management**: React Hooks & assistant-ui runtime
- **Integration**: Custom adapter for FastAPI RAG backend

## Getting Started

1.  **Configure Environment Variables**:
    Create a `.env.local` file (or use `.env`) and set the backend API URL:
    ```bash
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    # or
    pnpm install
    ```

3.  **Run Development Server**:
    ```bash
    npm run dev
    # or
    pnpm dev
    ```

4.  **Access the App**:
    Open [http://localhost:3000](http://localhost:3000) in your browser.

## Key Components

- `app/assistant.tsx`: Main assistant component managing the chat runtime.
- `hooks/adapter.ts`: Custom adapter that connects the frontend to the `api-rag` backend.
- `components/LandingPage.tsx`: The initial entry page for the application.

## Documentation

For the full setup of the CP-Helper system (including backend and RAG engine), please refer to the [Root README](file:///home/sunny/workspace/CP-Helper/README.md).
