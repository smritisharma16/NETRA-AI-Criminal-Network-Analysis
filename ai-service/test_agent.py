import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from app.agent.workflow import run_investigation
print(run_investigation("C-001", "Who is Juhu?", "REQ-TEST"))
