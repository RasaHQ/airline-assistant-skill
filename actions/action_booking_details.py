"""Actions to retrieve booking details."""

import asyncio
from datetime import date, timedelta
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


def _mock_bookings() -> Dict[str, List[Dict[str, Any]]]:
    """Generate mock bookings with one flight set to today."""
    today = date.today()
    return {
        "user_123": [
            {
                "booking_ref": "ABC123",
                "origin": "London",
                "destination": "Paris",
                "date": (today + timedelta(days=14)).isoformat(),
                "cabin_class": "Economy",
                "flight_number": "SK201",
            },
            {
                "booking_ref": "XYZ789",
                "origin": "London",
                "destination": "New York",
                "date": today.isoformat(),
                "cabin_class": "Economy",
                "flight_number": "SK450",
            },
        ],
    }


DEFAULT_USER = "user_123"


class ActionGetBookingDetails(Action):
    """Get details for a specific booking."""

    def name(self) -> Text:
        return "action_get_booking_details"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Simulate API latency
        await asyncio.sleep(0.5)

        user_id = tracker.get_slot("user_id") or DEFAULT_USER
        booking_ref = tracker.get_slot("selected_booking_ref")

        bookings = _mock_bookings().get(user_id, [])

        # If no booking selected, use the first one
        if not booking_ref and bookings:
            booking_ref = bookings[0]["booking_ref"]

        # Find the booking
        booking = next((b for b in bookings if b["booking_ref"] == booking_ref), None)

        if booking is None:
            return [SlotSet("api_error", True)]

        return [
            SlotSet("api_error", False),
            SlotSet("selected_booking_ref", booking["booking_ref"]),
            SlotSet("booking_origin", booking["origin"]),
            SlotSet("booking_destination", booking["destination"]),
            SlotSet("booking_date", booking["date"]),
            SlotSet("booking_cabin_class", booking["cabin_class"]),
        ]


class ActionListUserBookings(Action):
    """List all bookings for the current user."""

    def name(self) -> Text:
        return "action_list_user_bookings"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Simulate API latency
        await asyncio.sleep(0.5)

        user_id = tracker.get_slot("user_id") or DEFAULT_USER
        bookings = _mock_bookings().get(user_id, [])

        if not bookings:
            return [SlotSet("api_error", True)]

        # Try to narrow multiple bookings using context from the user's message
        if len(bookings) > 1:
            user_message = tracker.latest_message.get("text", "").lower()
            today = date.today()
            # Match temporal references to booking dates
            date_map = {"today": today, "tomorrow": today + timedelta(days=1)}
            for word, target in date_map.items():
                if word in user_message:
                    matches = [b for b in bookings
                               if b["date"] == target.isoformat()]
                    if len(matches) == 1:
                        bookings = matches
                        break
            # Match destination city names
            if len(bookings) > 1:
                for b in bookings:
                    if b["destination"].lower() in user_message:
                        bookings = [b]
                        break

        # If only one booking (or narrowed to one), auto-select it
        if len(bookings) == 1:
            b = bookings[0]
            dispatcher.utter_message(
                text=f"I found your booking: {b['booking_ref']} — "
                     f"{b['origin']} to {b['destination']} on {b['date']}, "
                     f"travelling in {b['cabin_class']}."
            )
            return [
                SlotSet("api_error", False),
                SlotSet("selected_booking_ref", b["booking_ref"]),
            ]

        # Multiple bookings — list them for the user to choose
        booking_list = []
        for b in bookings:
            booking_list.append(
                f"- {b['booking_ref']} — {b['origin']} to {b['destination']} on {b['date']} ({b['cabin_class']})"
            )

        message = "Here are your upcoming bookings:\n" + "\n".join(booking_list)
        dispatcher.utter_message(text=message)

        return [SlotSet("api_error", False)]
