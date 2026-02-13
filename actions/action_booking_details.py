"""Actions to retrieve booking details."""

import asyncio
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# Mock booking data
MOCK_BOOKINGS = {
    "user_123": [
        {
            "booking_ref": "ABC123",
            "origin": "London",
            "destination": "Paris",
            "date": "2025-11-18",
            "cabin_class": "Economy",
            "flight_number": "SK201",
        },
        {
            "booking_ref": "XYZ789",
            "origin": "London",
            "destination": "New York",
            "date": "2026-02-09",
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

        bookings = MOCK_BOOKINGS.get(user_id, [])

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
        bookings = MOCK_BOOKINGS.get(user_id, [])

        if not bookings:
            dispatcher.utter_message(text="I couldn't find any bookings for your account.")
            return [SlotSet("api_error", True)]

        # Format booking list
        booking_list = []
        for b in bookings:
            booking_list.append(
                f"• {b['booking_ref']} — {b['origin']} to {b['destination']} on {b['date']}"
            )

        message = "Here are your upcoming bookings:\n" + "\n".join(booking_list)
        dispatcher.utter_message(text=message)

        return [SlotSet("api_error", False)]
