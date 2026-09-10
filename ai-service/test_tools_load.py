from app.agent.tools import get_all_tools
tools = get_all_tools()
for t in tools:
    print(t.name)
print(f"\nTotal: {len(tools)} tools loaded")
