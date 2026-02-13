"""Action to check upgrade availability for a flight."""

import asyncio
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# Mock upgrade availability data
MOCK_UPGRADE_DATA = {
    "XYZ789": {  # London to New York
        "upgrade_available": True,
        "upgrade_cabin": "Premium Economy",
        "upgrade_price": "$349",
        "current_cabin": "Economy",
    },
    "ABC123": {  # London to Paris
        "upgrade_available": False,
        "upgrade_cabin": None,
        "upgrade_price": None,
        "current_cabin": "Economy",
    },
}


class ActionCheckUpgradeAvailability(Action):
    """Check if upgrades are available for the user's flight."""

    def name(self) -> Text:
        return "action_check_upgrade_availability"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Simulate API latency
        await asyncio.sleep(1.0)

        booking_ref = tracker.get_slot("selected_booking_ref") or "XYZ789"

        # "Call" the upgrade API (mocked)
        data = await self._check_upgrades(booking_ref)

        if data is None:
            return [SlotSet("api_error", True)]

        return [
            SlotSet("api_error", False),
            SlotSet("upgrade_available", data["upgrade_available"]),
            SlotSet("upgrade_cabin", data["upgrade_cabin"]),
            SlotSet("upgrade_price", data["upgrade_price"]),
            SlotSet("booking_cabin_class", data["current_cabin"]),
        ]

    async def _check_upgrades(self, booking_ref: str) -> Dict[Text, Any] | None:
        """Check upgrade availability from the API.

        In production, this would call the real airline API.
        For the demo, we return mock data.
        """
        if booking_ref not in MOCK_UPGRADE_DATA:
            # Default to showing upgrade available for demo purposes
            return MOCK_UPGRADE_DATA["XYZ789"]
        return MOCK_UPGRADE_DATA[booking_ref]
