from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_optional
from app.models.user import User
from app.models.topic import DSATopic
from app.models.pattern import DSAPattern
from app.utils.cache import analytics_cache

router = APIRouter()


@router.get("")
def get_knowledge_graph(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """
    Returns nodes and edges formatted for React Flow.
    Topics are positioned as hubs, patterns radiate out or form directed DAG.
    Cached for high throughput.
    """
    cache_key = "knowledge_graph_full"
    cached = analytics_cache.get(cache_key)
    if cached:
        return cached
    topics = db.query(DSATopic).order_by(DSATopic.sort_order).all()
    patterns = db.query(DSAPattern).all()

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    # Position topics in a layered grid
    grid_cols = 4
    x_gap = 280
    y_gap = 180

    topic_coords = {}
    for idx, t in enumerate(topics):
        col = idx % grid_cols
        row = idx // grid_cols
        x = col * x_gap + 50
        y = row * y_gap + 50
        topic_coords[str(t.id)] = (x, y)

        nodes.append({
            "id": f"topic-{t.id}",
            "type": "topicNode",
            "position": {"x": x, "y": y},
            "data": {
                "label": t.name,
                "slug": t.slug,
                "nodeType": "topic",
                "patternCount": len(t.patterns),
                "masteryLevel": "insufficient_evidence",
                "masteryScore": 0,
            },
        })

    # Pattern nodes positioned near their parent topics
    for p in patterns:
        parent_coord = topic_coords.get(str(p.topic_id), (100, 100))
        # slight offset for visual layout
        p_x = parent_coord[0] + 40
        p_y = parent_coord[1] + 80

        nodes.append({
            "id": f"pattern-{p.id}",
            "type": "patternNode",
            "position": {"x": p_x, "y": p_y},
            "data": {
                "label": p.name,
                "slug": p.slug,
                "nodeType": "pattern",
                "difficulty": p.difficulty_level,
                "topicId": str(p.topic_id),
            },
        })

        # Topic -> Pattern edge
        edges.append({
            "id": f"edge-topic-{p.topic_id}-to-pattern-{p.id}",
            "source": f"topic-{p.topic_id}",
            "target": f"pattern-{p.id}",
            "animated": False,
            "style": {"stroke": "#4f46e5", "strokeWidth": 1.5, "opacity": 0.4},
        })

        # Pattern prerequisite edges
        for prereq in p.prerequisites:
            edges.append({
                "id": f"edge-prereq-{prereq.id}-to-{p.id}",
                "source": f"pattern-{prereq.id}",
                "target": f"pattern-{p.id}",
                "animated": True,
                "style": {"stroke": "#f59e0b", "strokeWidth": 2, "strokeDasharray": "4 2"},
                "label": "requires",
            })

    result = {
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "total_topics": len(topics),
            "total_patterns": len(patterns),
            "total_edges": len(edges),
        },
    }
    analytics_cache.set(cache_key, result, ttl=60)
    return result
