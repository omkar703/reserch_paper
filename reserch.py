from fastapi import FastAPI, Query
from arxiv import Client, Search, SortCriterion, SortOrder

app = FastAPI()

# Initialize arXiv client
arxiv_client = Client()

# --------------------------
# Search arXiv
# --------------------------
@app.get("/search/arxiv")
async def search_arxiv(query: str = Query(..., min_length=2), max_results: int = 10):
    search = Search(
        query=query,
        max_results=max_results,
        sort_by=SortCriterion.SubmittedDate,
        sort_order=SortOrder.Descending
    )
    results = list(arxiv_client.results(search))
    return {
        "source": "arXiv",
        "results": [{"title": r.title, "id": r.entry_id} for r in results]
    }

# --------------------------
# Feed of 50 arXiv papers (general trending feed)
# --------------------------
@app.get("/feed/arxiv")
async def arxiv_feed():
    query = "artificial intelligence"  # default topic for feed
    search = Search(
        query=query,
        max_results=50,
        sort_by=SortCriterion.SubmittedDate,
        sort_order=SortOrder.Descending
    )
    results = list(arxiv_client.results(search))
    return {
        "source": "arXiv",
        "feed_count": len(results),
        "feed": [{"title": r.title, "id": r.entry_id} for r in results]
    }

# --------------------------
# Suggest endpoint (simple keyword-based suggestion)
# --------------------------
@app.get("/suggest/arxiv")
async def suggest_arxiv(query: str = Query(..., min_length=2)):
    # Basic hardcoded suggestions — ideally you’d use NLP or store history/keywords
    base = query.lower()
    suggestions = [
        f"{base} in healthcare",
        f"{base} with deep learning",
        f"{base} survey",
        f"{base} applications",
        f"recent {base} trends"
    ]
    return {"query": query, "suggestions": suggestions}
