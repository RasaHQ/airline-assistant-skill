"""Action to validate the selected_booking_ref slot."""

import re
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# Booking refs contain both letters AND digits (e.g. ABC123, XA5ZZR)
BOOKING_REF_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*[0-9])[A-Z0-9]{5,8}$", re.IGNORECASE)


class ActionValidateBookingRef(Action):
    """Validate selected_booking_ref and reset if it's garbage."""

    def name(self) -> Text:
        return "action_validate_booking_ref"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        booking_ref = tracker.get_slot("selected_booking_ref")

        if booking_ref and BOOKING_REF_PATTERN.match(booking_ref):
            # Looks like a real booking ref, keep it
            return []

        # Reset garbage values like "flight", "my booking", etc.
        if booking_ref:
            return [SlotSet("selected_booking_ref", None)]

        return []
