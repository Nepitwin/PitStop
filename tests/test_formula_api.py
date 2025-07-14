from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd

from pitstop.service.formula_api import FormulaApi
from pitstop.model.race_event import RaceEvent

class DummySchedule(pd.DataFrame):
    @property
    def year(self):
        return 2024

def make_event(date_offset):
    date = datetime.now() + timedelta(days=date_offset)
    return RaceEvent(
        session=1,
        name="Test GP",
        location="Testland",
        date=date,
        sessions=[]
    )

def test_get_next_event_returns_next():
    events = [make_event(-2), make_event(2), make_event(5)]
    result = FormulaApi.get_next_event(events)
    assert result.date > datetime.now()

def test_get_next_event_returns_none():
    events = [make_event(-5), make_event(-1)]
    assert FormulaApi.get_next_event(events) is None

def test_get_all_events_from_year():
    data = {
        'RoundNumber': [1],
        'EventName': ['Test GP'],
        'Location': ['Test City'],
        'Country': ['Testland'],
        'EventDate': [datetime.now()],
        'Session1': ['FP1'],
        'Session1Date': [datetime.now()],
        'Session2': ['FP2'],
        'Session2Date': [datetime.now()],
        'Session3': ['FP3'],
        'Session3Date': [datetime.now()],
        'Session4': ['Q'],
        'Session4Date': [datetime.now()],
        'Session5': ['R'],
        'Session5Date': [datetime.now()],
    }
    schedule = pd.DataFrame(data)
    events = FormulaApi.get_all_events_from_year(schedule)
    assert len(events) == 1
    assert isinstance(events[0], RaceEvent)

@patch('pitstop.service.formula_api.fastf1.get_session')
def test_get_standings(mock_get_session):
    # Mock Session und Ergebnisse
    mock_session = MagicMock()
    mock_session.results = pd.DataFrame([
        {'Points': 25, 'FullName': 'Max Mustermann', 'TeamName': 'Test Team'}
    ])
    mock_get_session.return_value = mock_session

    data = {
        'RoundNumber': [1],
        'Session5Date': [pd.Timestamp.utcnow() - pd.Timedelta(days=1)]
    }
    schedule = DummySchedule(data)
    driver_df, constructor_df = FormulaApi.get_standings(schedule)
    assert not driver_df.empty
    assert not constructor_df.empty
    assert driver_df.iloc[0]['Driver'] == 'Max Mustermann'
    assert constructor_df.iloc[0]['Constructor'] == 'Test Team'

@patch('pitstop.service.formula_api.fastf1.get_event_schedule')
def test_get_event_schedule_returns_schedule(mock_get_event_schedule):
    mock_schedule = MagicMock()
    mock_get_event_schedule.return_value = mock_schedule

    result = FormulaApi.get_event_schedule(2025, include_testing=True)
    mock_get_event_schedule.assert_called_once_with(2025, include_testing=True)
    assert result == mock_schedule

@patch('pitstop.service.formula_api.fastf1.Cache')
def test_set_cache_directory_sets_path(mock_cache):
    FormulaApi.set_cache_directory('C:/test/cache')
    mock_cache.enable_cache.assert_called_once_with('C:/test/cache')
