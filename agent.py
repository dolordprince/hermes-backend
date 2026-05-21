import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Groq free tier — OpenAI-compatible, fastest inference available
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

MODEL = os.environ.get("MODEL", "llama-3.3-70b-versatile")

SYSTEM = {
    "role": "system",
    "content": (
        "You are DavTeam Agent — built by David (DavTeam). "
        "Expert in ARM64/Termux CLI, FastAPI, Bun/TypeScript, "
        "Android builds, Cloudflare tunnels, SaaS architecture. "
        "Be direct. Prefer working code over explanation."
    )
}

async def chat(history: list[dict], user_input: str) -> str:
    history.append({"role": "user", "content": user_input})

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[SYSTEM, *history],
        temperature=0.7,
        max_tokens=2048,
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply
