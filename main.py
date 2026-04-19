import sys
sys.path.append("src")

import asyncio
import json

from support_agent.clients.llm import LLMClient
from support_agent.data.loader import load_all_tickets
from support_agent.pipelines.ticket_processor import TicketProcessor


async def main() -> None:
    llm = LLMClient()
    processor = TicketProcessor(llm)

    tickets = load_all_tickets()

    print(f"Loaded {len(tickets)} tickets.\n")

    # Show first 10 in demo
    for i, ticket in enumerate(tickets[:10], start=1):
        print("\n" + "=" * 100)
        print(f"TICKET #{i}")
        print("=" * 100)
        print("DATASET LABEL:", ticket.get("intent"))
        print("RAW INPUT:", ticket["user_message"])

        result = await processor.process_ticket(ticket["user_message"])

        print("\nFINAL STRUCTURED RESULT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())