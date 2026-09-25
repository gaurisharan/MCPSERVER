import logging
import os
from pathlib import Path
from urllib.parse import quote

import httpx
from dotenv import load_dotenv
from google import genai
from mcp.server import MCPServer


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mini-mcp")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.1-flash-lite",
)

USER_AGENT = "MiniMCPResearchAssistant/1.0"


# ---------------------------------------------------------
# MCP SERVER
# ---------------------------------------------------------

mcp = MCPServer(
    "Research Assistant",
    instructions=(
        "A research assistant providing weather information, "
        "Wikipedia summaries, and Gemini-powered answers."
    ),
)


# ---------------------------------------------------------
# Weather descriptions
# ---------------------------------------------------------

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


# ---------------------------------------------------------
# TOOL 1: Open-Meteo
# ---------------------------------------------------------

@mcp.tool()
async def get_weather(
    latitude: float,
    longitude: float,
) -> dict:
    """Get current weather using the free Open-Meteo API."""

    if not -90 <= latitude <= 90:
        return {"error": "Latitude must be between -90 and 90."}

    if not -180 <= longitude <= 180:
        return {"error": "Longitude must be between -180 and 180."}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "apparent_temperature,"
                        "precipitation,"
                        "wind_speed_10m,"
                        "weather_code"
                    ),
                    "timezone": "auto",
                },
            )

            response.raise_for_status()

        data = response.json()
        current = data.get("current", {})

        current["weather_description"] = WEATHER_CODES.get(
            current.get("weather_code"),
            "Unknown",
        )

        return {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "timezone": data.get("timezone"),
            "current": current,
            "units": data.get("current_units"),
        }

    except httpx.HTTPError as exc:
        log.exception("Open-Meteo request failed")
        return {"error": f"Weather request failed: {exc}"}


# ---------------------------------------------------------
# TOOL 2: Wikipedia
# ---------------------------------------------------------

@mcp.tool()
async def wikipedia_summary(topic: str) -> dict:
    """Get an English Wikipedia summary for a topic."""

    topic = topic.strip()

    if not topic:
        return {"error": "Please provide a topic."}

    title = quote(
        topic.replace(" ", "_"),
        safe="",
    )

    url = (
        "https://en.wikipedia.org/api/rest_v1/"
        f"page/summary/{title}"
    )

    try:
        async with httpx.AsyncClient(
            timeout=10,
            follow_redirects=True,
        ) as client:

            response = await client.get(
                url,
                headers={"User-Agent": USER_AGENT},
            )

        if response.status_code == 404:
            return {
                "error": f"No Wikipedia page found for '{topic}'."
            }

        response.raise_for_status()

        data = response.json()

        return {
            "title": data.get("title"),
            "description": data.get("description"),
            "summary": data.get("extract"),
            "url": (
                data.get("content_urls", {})
                .get("desktop", {})
                .get("page")
            ),
        }

    except httpx.HTTPError as exc:
        log.exception("Wikipedia request failed")
        return {"error": f"Wikipedia request failed: {exc}"}


# ---------------------------------------------------------
# TOOL 3: Gemini
# ---------------------------------------------------------

@mcp.tool()
async def ask_llm(
    question: str,
    context: str = "",
) -> str:
    """
    Ask Gemini a question.

    context can contain information retrieved from
    Wikipedia or another tool.
    """

    question = question.strip()

    if not question:
        return "Please provide a question."

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "GEMINI_API_KEY is missing. "
            "Add it to the .env file."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a concise research assistant.

Question:
{question}

Additional context:
{context if context else "(none)"}

Answer accurately.
Do not invent facts.
If the supplied context is insufficient, say so.
"""

    try:
        response = await client.aio.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        return response.text or "Gemini returned an empty response."

    except Exception as exc:
        log.exception("Gemini request failed")
        return f"Gemini request failed: {exc}"


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

if __name__ == "__main__":
    log.info("Starting Mini MCP Research Assistant")
    mcp.run(transport="stdio")