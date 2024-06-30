#This content goes to the front end. The key is the user view, the value is the back to search on API
search_types = {
"Open Folios": "OpenFolio", "Checked Out": "CheckedOut",
"In House": "InHouse", "No Show": "NoShow",
"Cancellation": "Cancellation"
}


if __name__ == '__main__':
    #This is just to check
    allowed_list = [
        "AdvanceCheckedIn",
        "Any", "Arrival", "Arrived", "AutoFolioSettlement", "Cancellation",
        "CheckedOut", "Complimentary", "DayUse", "Departure", "GuestMessages", "InHouse",
        "MassCancellation", "MobileCheckout", "NoShow", "OpenBalance", "OpenFolio", "Operator",
        "PlayerSnapshot", "PostStayPendingBalance", "PostToRoom", 
        "PreRegistered", "Queued", "RegisteredAndInHouse", "ResvBlockTraces", "Routing",
        "ScheduledCheckOut", "Turndown", "WaitList", "WalkIn"
    ]