import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from app.agent.tool_service import InvestigationService, get_session

with get_session() as db:
    svc = InvestigationService(db)
    print("Entities:")
    print(svc.search_entities("Juhu"))
