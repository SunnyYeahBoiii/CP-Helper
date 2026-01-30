import {
  useLocalRuntime,
  type ChatModelAdapter,
} from "@assistant-ui/react";

const MyCustomAdapter: ChatModelAdapter = {
  // This function is called when the user sends a message
  async *run({ messages, abortSignal }) {
    // 1. Format messages for your API
    const lastMessage = messages[messages.length - 1];
    const payload = {
      question: lastMessage.content[0]?.type === 'text' ? lastMessage.content[0].text : '',
    };

    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000";

    const response = await fetch(`${apiUrl}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      signal: abortSignal,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    // 3. Handle Streaming Response (recommended for chat)
    // If your API returns a simple JSON, just yield it once.
    // If streaming, read the body chunks.
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) return;

    let textSoFar = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      console.log('Received chunk:', chunk);
      const lines = chunk.split('\n').filter(line => line.trim());
      console.log('Parsed lines:', lines);

      for (const line of lines) {
        try {
          const parsed = JSON.parse(line);
          if (parsed.message && parsed.message.content) {
            const content = parsed.message.content;
            textSoFar += content;

            // Yield the update to assistant-ui
            yield {
              content: [
                {
                  type: "text",
                  text: textSoFar, // Send the accumulated text
                },
              ],
            };
          }
        } catch (e) {
          // Ignore invalid JSON lines
          console.error('JSON parse error:', e, 'line:', line);
        }
      }
    }
  },
};

export function useMyCustomRuntime() {
  return useLocalRuntime(MyCustomAdapter);
}
