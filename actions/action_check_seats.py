"""Action to check seat availability for a flight."""

import asyncio
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# Mock seat availability data
MOCK_SEAT_DATA = {
    "XYZ789": {  # London to New York
        "seat_available": True,
        "available_seats": ["14A", "14C", "22D", "22F", "31A", "31B"],
        "extra_legroom_available": True,
    },
    "ABC123": {  # London to Paris
        "seat_available": False,
        "available_seats": [],
        "extra_legroom_available": False,
    },
}


class ActionCheckSeatAvailability(Action):
    """Check seat availability for the user's flight."""

    def name(self) -> Text:
        return "action_check_seat_availability"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Simulate API latency
        await asyncio.sleep(0.8)

        booking_ref = tracker.get_slot("selected_booking_ref") or "XYZ789"

        # "Call" the seat API (mocked)
        data = await self._check_seats(booking_ref)

        if data is None:
            return [SlotSet("api_error", True)]

        return [
            SlotSet("api_error", False),
            SlotSet("seat_available", data["seat_available"]),
            SlotSet("available_seats", data["available_seats"]),
        ]

    async def _check_seats(self, booking_ref: str) -> Dict[Text, Any] | None:
        """Check seat availability from the API.

        In production, this would call the real airline API.
        For the demo, we return mock data.
        """
        if booking_ref not in MOCK_SEAT_DATA:
            return MOCK_SEAT_DATA["XA5ZZR"]
        return MOCK_SEAT_DATA[booking_ref]
