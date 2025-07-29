from datetime import datetime
from typing import List, Optional
from collections import defaultdict

import fastf1
import pandas as pd
from fastf1.events import EventSchedule

from pitstop.model.race_event import RaceEvent, EventInfo
from pitstop.model.race_session import RaceSession


class FormulaApi:

    @staticmethod
    def set_cache_directory(cache_dir: str) -> None:
        fastf1.Cache.enable_cache(cache_dir)

    @staticmethod
    def get_event_schedule(year: int, include_testing: bool = False) -> EventSchedule:
        return fastf1.get_event_schedule(year, include_testing=include_testing)

    @staticmethod
    def get_next_event(events: List[RaceEvent]) -> Optional[RaceEvent]:
        return next((event for event in events if event.finished is False), None)

    @staticmethod
    def get_all_race_events(schedule: EventSchedule) -> list[RaceEvent]:

        events = []

        for _, event in schedule.iterrows():
            session_one = RaceSession(event['Session1'], event['Session1Date'])
            session_two = RaceSession(event['Session2'], event['Session2Date'])
            session_three = RaceSession(event['Session3'], event['Session3Date'])
            session_four = RaceSession(event['Session4'], event['Session4Date'])
            session_five = RaceSession(event['Session5'], event['Session5Date'])

            sessions = [session_one, session_two, session_three, session_four, session_five]

            event_info = EventInfo(event['RoundNumber'],
                event['EventName'],
                f"{event['Location']} - {event['Country']}",
                event['EventDate'],
                sessions)

            race_event = RaceEvent(event_info)

            date = event['EventDate'].date()
            current_data = datetime.now().date()

            # Event is in future
            if date < current_data:
                race_event.finished = True

            # Verify if event has finished
            if date == current_data:
                session = fastf1.get_session(2025, event['RoundNumber'], 'R')
                session.load(laps=False, telemetry=False, weather=False, messages=False)
                if not session.results.empty:
                    race_event.finished = True

            events.append(race_event)

        return events

    @staticmethod
    def get_standings(schedule: EventSchedule) -> tuple[pd.DataFrame, pd.DataFrame]:

        year = schedule.year

        driver_pts = defaultdict(float)
        constructor_pts = defaultdict(float)

        now = pd.Timestamp.utcnow()

        for _, event in schedule.iterrows():
            round_num = event['RoundNumber']
            race_date = event['Session5Date']

            if race_date > now:
                break  # Skip upcoming races

            # --- Race Session ---
            FormulaApi._add_standing_results_from_round(year, round_num, "R", driver_pts, constructor_pts)
            # --- Sprint Session ---
            FormulaApi._add_standing_results_from_round(year, round_num, "S", driver_pts, constructor_pts)

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

    @staticmethod
    def _add_standing_results_from_round(year: int,
                                         round_number: int,
                                         identifier: str,
                                         driver_pts: dict,
                                         constructor_pts: dict) -> None:
        try:
            session = fastf1.get_session(year, round_number, identifier)
            session.load(laps=False, telemetry=False, weather=False, messages=False)
            results = session.results

            for _, row in results.iterrows():
                points = row['Points']
                name = row['FullName']
                team = row['TeamName']
                driver_pts[name] += points
                constructor_pts[team] += points
        except ValueError:
            pass  # No sprint for this round
