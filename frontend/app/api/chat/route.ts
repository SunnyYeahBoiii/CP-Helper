export async function POST(req: Request) {
  const body = await req.json();

  // Proxy to Python RAG backend
  const ragApiUrl = process.env.RAG_API_URL ?? "http://localhost:8000";

  const response = await fetch(`${ragApiUrl}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    return new Response(`RAG API Error: ${response.statusText}`, {
      status: response.status,
    });
  }

  // Stream the response back to the client
  return new Response(response.body, {
    headers: {
      "Content-Type": "text/plain",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
    },
  });
}
