"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
additional_activities = {
    # Sports (2)
    "Soccer Team": {
        "description": "Competitive soccer team training and matches against other schools",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "riley@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap swimming, technique drills, and friendly meets",
        "schedule": "Mondays and Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 20,
        "participants": ["jordan@mergington.edu", "casey@mergington.edu"]
    },

    # Artistic (2)
    "Drama Club": {
        "description": "Acting workshops, script rehearsals, and seasonal productions",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["lana@mergington.edu", "nate@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Painting, drawing, and mixed media projects for all skill levels",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isla@mergington.edu", "leo@mergington.edu"]
    },

    # Intellectual (2)
    "Science Olympiad": {
        "description": "Hands-on science challenges and competition preparation",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["maya@mergington.edu", "owen@mergington.edu"]
    },
    "Debate Team": {
        "description": "Public speaking, argumentation practice, and interschool debates",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["zara@mergington.edu", "liam@mergington.edu"]
    }
}

@app.on_event("startup")
def _merge_additional_activities():
    try:
        activities.update(additional_activities)
    except NameError:
        # activities not defined yet (should be defined later in the module),
        # but if startup runs before that for any reason, skip merging.
        pass
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Optional: check max participants
    if len(activity["participants"]) >= activity.get("max_participants", float("inf")):
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
