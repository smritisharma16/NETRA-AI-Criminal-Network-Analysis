import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from app.agent.tool_service import InvestigationService, get_session

with get_session() as db:
    svc = InvestigationService(db)
    print("Graph:")
    print(svc.explore_graph("C-001", "E-66989689", 5))
