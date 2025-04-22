import fastf1
import pandas as pd
from datetime import datetime
from typing import List, Optional
from collections import defaultdict
from django.conf import settings
from pitstop.model.RaceEvent import RaceEvent
from pitstop.model.RaceSession import RaceSession


class FormulaApi:

    def __init__(self):
        # Enable the cache for performance improvements
        fastf1.Cache.enable_cache(settings.BASE_DIR)

    @staticmethod
    def get_next_event(events: List[RaceEvent]) -> Optional[RaceEvent]:
        current_date = datetime.now()

        future_events = [event for event in events if event.date > current_date]

        if future_events:
            return sorted(future_events, key=lambda e: e.date)[0]

        return None

    @staticmethod
    def get_all_events_from_year(year: int) -> list[RaceEvent]:

        events = []

        schedule = fastf1.get_event_schedule(year, include_testing=False)

        for _, event in schedule.iterrows():
            session_one = RaceSession(event['Session1'], event['Session1Date'])
            session_two = RaceSession(event['Session2'], event['Session2Date'])
            session_three = RaceSession(event['Session3'], event['Session3Date'])
            session_four = RaceSession(event['Session4'], event['Session4Date'])
            session_five = RaceSession(event['Session5'], event['Session5Date'])
            sessions = [session_one, session_two, session_three, session_four, session_five]
            race_event = RaceEvent(event['RoundNumber'], event['EventName'], f"{event['Location']} - {event['Country']}", event['EventDate'], sessions)
            events.append(race_event)

        return events

    @staticmethod
    def get_standings(year: int) -> tuple[pd.DataFrame, pd.DataFrame]:

        # TODO -> Method is actually very slow, try to optimize it
        # TODO -> Cache usage should be used to speed up the process to persist actually standing and update if new racing data is available

        driver_pts = defaultdict(float)
        constructor_pts = defaultdict(float)

        schedule = fastf1.get_event_schedule(year)
        now = pd.Timestamp.utcnow()

        for _, event in schedule.iterrows():
            round_num = event['RoundNumber']
            race_date = event['Session5Date']

            if race_date > now:
                continue  # Skip upcoming races

            # --- Race Session ---
            try:
                race = fastf1.get_session(year, round_num, 'R')
                race.load()
                results = race.results

                for _, row in results.iterrows():
                    points = row['Points']
                    name = row['FullName']
                    team = row['TeamName']
                    driver_pts[name] += points
                    constructor_pts[team] += points
            except Exception:
                pass  # No racing data

            # --- Sprint Session ---
            try:
                sprint = fastf1.get_session(2025, round_num, 'S')
                sprint.load()
                results = sprint.results

                for _, row in results.iterrows():
                    points = row['Points']
                    name = row['FullName']
                    team = row['TeamName']
                    driver_pts[name] += points
                    constructor_pts[team] += points
            except Exception:
                pass  # No sprint for this round

        # Create standings tables
        driver_df = pd.DataFrame([
            {'Driver': name, 'Points': pts}
            for name, pts in driver_pts.items()
        ]).sort_values(by='Points', ascending=False).reset_index(drop=True)

        constructor_df = pd.DataFrame([
            {'Constructor': name, 'Points': pts}
            for name, pts in constructor_pts.items()
        ]).sort_values(by='Points', ascending=False).reset_index(drop=True)

        driver_df.index += 1
        constructor_df.index += 1
        driver_df.insert(0, 'Position', driver_df.index)
        constructor_df.insert(0, 'Position', constructor_df.index)

        return driver_df, constructor_df