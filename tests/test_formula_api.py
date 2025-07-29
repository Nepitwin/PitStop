from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd

from pitstop.service.formula_api import FormulaApi
from pitstop.model.race_event import RaceEvent, EventInfo


class DummySchedule(pd.DataFrame):
    @property
    def year(self):
        return 2024

def make_schedule(event_date, round_number=1):
    data = {
        'RoundNumber': [round_number],
        'EventName': ['Test GP'],
        'Location': ['Testland'],
        'Country': ['Testland'],
        'EventDate': [event_date],
        'Session1': ['FP1'],
        'Session1Date': [event_date],
        'Session2': ['FP2'],
        'Session2Date': [event_date],
        'Session3': ['FP3'],
        'Session3Date': [event_date],
        'Session4': ['Q'],
        'Session4Date': [event_date],
        'Session5': ['R'],
        'Session5Date': [event_date],
    }
    return pd.DataFrame(data)

def make_event(date_offset, finished=False):
    date = datetime.now() + timedelta(days=date_offset)
    info = EventInfo(session=1,
        name="Test GP",
        location="Testland",
        date=date,
        sessions=[])

    event = RaceEvent(info)
    event.finished = finished

    return event

def test_get_next_event_returns_next():
    events = [make_event(-2), make_event(0), make_event(5)]
    result = FormulaApi.get_next_event(events)
    assert result is not None
    assert hasattr(result, "date")
    assert result.date.date() == datetime.now().date() + timedelta(days=-2)

def test_get_next_event_returns_next_event_which_is_not_finished():
    events = [make_event(-2, True), make_event(0, True), make_event(5)]
    result = FormulaApi.get_next_event(events)
    assert result is not None
    assert hasattr(result, "date")
    assert result.date.date() == datetime.now().date() + timedelta(days=5)

def test_get_next_event_returns_none_if_all_events_are_finished():
    events = [make_event(-5, True), make_event(-1, True)]
    result = FormulaApi.get_next_event(events)
    assert result is None

def test_get_next_event_same_day_returned():
    events = [make_event(0), make_event(2)]
    result = FormulaApi.get_next_event(events)
    assert result.date.date() == datetime.now().date()

@patch('pitstop.service.formula_api.fastf1.get_session')
def test_get_all_events_from_year(mock_get_session):
    mock_session = MagicMock()
    mock_session.results.empty = True
    mock_get_session.return_value = mock_session

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
    events = FormulaApi.get_all_race_events(schedule)
    assert len(events) == 1
    assert isinstance(events[0], RaceEvent)

@patch('pitstop.service.formula_api.fastf1.get_session')
def test_get_standings(mock_get_session):
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

@patch('pitstop.service.formula_api.fastf1.get_session')
def test_event_in_past_is_finished(mock_get_session):
    mock_session = MagicMock()
    mock_session.results.empty = True
    mock_get_session.return_value = mock_session
    schedule = make_schedule(datetime.now() - timedelta(days=1))
    events = FormulaApi.get_all_race_events(schedule)
    assert events[0].finished is True

@patch('pitstop.service.formula_api.fastf1.get_session')
def test_event_today_finished(mock_get_session):
    mock_session = MagicMock()
    mock_session.results.empty = False
    mock_get_session.return_value = mock_session
    schedule = make_schedule(datetime.now())
    events = FormulaApi.get_all_race_events(schedule)
    assert events[0].finished is True

@patch('pitstop.service.formula_api.fastf1.get_session')
def test_event_today_not_finished(mock_get_session):
    mock_session = MagicMock()
    mock_session.results.empty = True
    mock_get_session.return_value = mock_session
    schedule = make_schedule(datetime.now())
    events = FormulaApi.get_all_race_events(schedule)
    assert events[0].finished is False

@patch('pitstop.service.formula_api.fastf1.get_session')
def test_event_in_future_not_finished(mock_get_session):
    mock_session = MagicMock()
    mock_session.results.empty = True
    mock_get_session.return_value = mock_session
    schedule = make_schedule(datetime.now() + timedelta(days=1))
    events = FormulaApi.get_all_race_events(schedule)
    assert events[0].finished is False

@patch('pitstop.service.formula_api.fastf1.get_session')
def test_sessions_are_created(mock_get_session):
    mock_session = MagicMock()
    mock_session.results.empty = True
    mock_get_session.return_value = mock_session
    schedule = make_schedule(datetime.now())
    events = FormulaApi.get_all_race_events(schedule)
    assert len(events[0].sessions) == 5
