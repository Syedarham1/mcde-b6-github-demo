from datetime import datetime

class BookingScheduler:
    def __init__(self):
        self.bookings = {}

    def add_booking(self, room, start: datetime, end: datetime, booking_id):
        if end <= start:
            raise ValueError("End time must be after start time.")
        if booking_id in [b['id'] for room_list in self.bookings.values() for b in room_list]:
            raise ValueError("Duplicate booking ID.")

        if room not in self.bookings:
            self.bookings[room] = []

        conflicts = []
        for b in self.bookings[room]:
            if not (end <= b['start'] or start >= b['end']):
                conflicts.append(b)

        if conflicts:
            return False, conflicts

        self.bookings[room].append({'id': booking_id, 'start': start, 'end': end})
      
        self.bookings[room].sort(key=lambda x: x['start'])
        return True, []