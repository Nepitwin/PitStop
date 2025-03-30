from zoneinfo import ZoneInfo

import fastf1

def to_timezone(data, zone_info):
    return data.astimezone(zone_info)

# Enable the cache for performance improvements
fastf1.Cache.enable_cache('../cache')

schedule = fastf1.get_event_schedule(2024, include_testing=False)

zone = ZoneInfo('Europe/Berlin')

# Iterate through all events and print details
for _, event in schedule.iterrows():
    # Original data
    print(f"Round {event['RoundNumber']}: {event['EventName']}")
    print(f"  Location: {event['Location']} - {event['Country']}")
    print(f"  Start Date: {event['EventDate']}")
    print(f"  {event['Session1']}: {event['Session1Date']}")
    print(f"  {event['Session2']}: {event['Session2Date']}")
    print(f"  {event['Session3']}: {event['Session3Date']}")
    print(f"  {event['Session4']}: {event['Session4Date']}")
    print(f"  {event['Session5']}: {event['Session5Date']}")
    print(f"")
    # Adjusted data
    print(f"  {event['Session1']} Berlin: {to_timezone(event['Session1Date'], zone)}")
    print(f"  {event['Session2']} Berlin: {to_timezone(event['Session2Date'], zone)}")
    print(f"  {event['Session3']} Berlin: {to_timezone(event['Session3Date'], zone)}")
    print(f"  {event['Session4']} Berlin: {to_timezone(event['Session4Date'], zone)}")
    print(f"  {event['Session5']} Berlin: {to_timezone(event['Session5Date'], zone)}")

    print("-" * 40)
