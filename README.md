LLM returning non‑Python output
Examples:
- markdown
- explanations
- JSON



Repository‑Level Scenarios
Modules that should not be tested
Examples:
- __init__.py
- data files
Your agent must skip them.


Coverage never reaches threshold because:
- module is too complex
- LLM keeps hallucinating
- missing functions are untestable
- modules contanining only print statements and __main__ module
Your agent must detect “unreachable coverage” and stop.


Project Structure Scenarios
	Modules that require configuration
	Modules with side effects on import
	Modules that import optional dependencies
	
Signature mismatch detector failing on complex AST
Examples:
- decorators
- nested functions
- lambdas
- partials
Your signature detector must be hardened.


Human‑Code Scenarios
Real developers write messy code.
Functions with misleading names
Example:
def add(a, b):
    return a - b
Your agent must infer behavior from source, not name.

Pytest Runtime Scenarios	
	infinite loops
	waiting for network
	waiting for input()
	 enforce timeouts
	out of memory
Modules that import large libraries
Coverage slows down dramatically.
Your agent must detect and skip heavy modules.


Tests that require external services
Examples:
- Redis
- Postgres
- AWS
- Kafka
  
Your agent must detect and mock external dependencies.
