"""
Synthetic data only. No real patient information.

Task: write `placeable_beds(beds, request)` — given the request, return the beds
you could place this patient in, best first.

A bed is a dict with:
  bed_id            e.g. "B-201"
  unit              "Med-Surg" | "Telemetry" | "ICU" | "General" | "Step-down" | "Isolation"
  service_line      e.g. "Cardiology"
  status            "open" | "occupied" | "pending_discharge" | "dirty"
  acuity_level      1 (general) .. 4 (ICU)
  isolation_capable True/False
  last_updated      ISO timestamp string

Use minutes_old(bed["last_updated"]) if you need the age of the data — you do NOT
need to parse timestamps yourself.
"""
from datetime import datetime

NOW = datetime.fromisoformat("2026-08-31T09:00:00")

def minutes_old(ts):
    """Minutes since a bed's data was last updated."""
    return (NOW - datetime.fromisoformat(ts)).total_seconds() / 60


BEDS = [
    {"bed_id": "B-201", "unit": "Med-Surg",  "service_line": "Cardiology",         "status": "open",              "acuity_level": 2, "isolation_capable": False, "last_updated": "2026-08-31T08:52:00"},
    {"bed_id": "B-202", "unit": "Med-Surg",  "service_line": "Cardiology",         "status": "occupied",          "acuity_level": 2, "isolation_capable": False, "last_updated": "2026-08-31T08:40:00"},
    {"bed_id": "B-203", "unit": "Med-Surg",  "service_line": "Cardiology",         "status": "open",              "acuity_level": 2, "isolation_capable": True,  "last_updated": "2026-08-31T08:15:00"},
    {"bed_id": "B-210", "unit": "Med-Surg",  "service_line": "Pulmonology",        "status": "pending_discharge", "acuity_level": 2, "isolation_capable": False, "last_updated": "2026-08-31T08:58:00"},
    {"bed_id": "B-305", "unit": "Telemetry", "service_line": "Cardiology",         "status": "open",              "acuity_level": 3, "isolation_capable": False, "last_updated": "2026-08-31T08:57:00"},
    {"bed_id": "B-306", "unit": "Telemetry", "service_line": "Cardiology",         "status": "open",              "acuity_level": 3, "isolation_capable": True,  "last_updated": "2026-08-31T07:30:00"},
    {"bed_id": "B-307", "unit": "Telemetry", "service_line": "Neurology",          "status": "dirty",             "acuity_level": 3, "isolation_capable": False, "last_updated": "2026-08-31T08:50:00"},
    {"bed_id": "B-410", "unit": "ICU",       "service_line": "Cardiology",         "status": "open",              "acuity_level": 4, "isolation_capable": True,  "last_updated": "2026-08-31T08:55:00"},
    {"bed_id": "B-411", "unit": "ICU",       "service_line": "Pulmonology",        "status": "occupied",          "acuity_level": 4, "isolation_capable": True,  "last_updated": "2026-08-31T08:20:00"},
    {"bed_id": "B-412", "unit": "ICU",       "service_line": "Cardiology",         "status": "open",              "acuity_level": 4, "isolation_capable": False, "last_updated": "2026-08-31T06:45:00"},
    {"bed_id": "B-120", "unit": "General",   "service_line": "General",            "status": "open",              "acuity_level": 1, "isolation_capable": False, "last_updated": "2026-08-31T08:59:00"},
    {"bed_id": "B-121", "unit": "General",   "service_line": "General",            "status": "open",              "acuity_level": 1, "isolation_capable": True,  "last_updated": "2026-08-31T08:30:00"},
    {"bed_id": "B-720", "unit": "Isolation", "service_line": "Cardiology",         "status": "open",              "acuity_level": 2, "isolation_capable": True,  "last_updated": "2026-08-31T08:56:00"},
    {"bed_id": "B-721", "unit": "Isolation", "service_line": "Infectious Disease", "status": "open",              "acuity_level": 2, "isolation_capable": True,  "last_updated": "2026-08-31T07:10:00"},
    {"bed_id": "B-508", "unit": "Step-down", "service_line": "Cardiology",         "status": "open",              "acuity_level": 2, "isolation_capable": False, "last_updated": "2026-08-31T08:10:00"},
]

# Primary incoming transfer request.
REQUEST = {
    "acuity_needed": 2,
    "isolation_required": True,
    "preferred_service_line": "Cardiology",
}


def placeable_beds(beds, request):
   # Filter - clinical, operation rules 

   valid_beds = [
      bed for bed in beds
      if bed["status"] == "open"
      and bed["acuity_level"] == request.get("acuity_needed")
      and (not request.get("isolation_required") or bed["isolation_capable"])
   ]


    # Rank - what would best fit the operational needs/preferences

   pref_service = request.get("preferred_service_line")

   # Sort keys: (is_not_preferred_service, data_age_in_minutes)

   valid_beds.sort(key=lambda b: (
      b["service_line"] != pref_service, minutes_old(b["last_updated"])
   ))

   return valid_beds


if __name__ == "__main__":
    for bed in placeable_beds(BEDS, REQUEST) or []:
        print(bed["bed_id"], bed["unit"], bed["service_line"])

