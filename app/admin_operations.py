from database import execute_query, execute_update
from datetime import datetime, date

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time(time_str):
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def check_room_double_booking(room_id, booking_date, booking_time, exclude_booking_id=None):
    conflict_query = """
        SELECT booking_id FROM RoomBooking
        WHERE room_id = %s
        AND booking_date = %s
        AND booking_time = %s
        AND status = 'Booked'
    """
    params = (room_id, booking_date, booking_time)
    
    if exclude_booking_id:
        conflict_query += " AND booking_id != %s"
        params = params + (exclude_booking_id,)
    
    conflicts = execute_query(conflict_query, params)
    return len(conflicts) > 0

def book_room_for_session(room_id, session_id, booking_date, booking_time):
    if not validate_date(booking_date):
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return None
    
    if not validate_time(booking_time):
        print("Error: Invalid time format. Use HH:MM")
        return None
    
    session_query = "SELECT member_id, trainer_id FROM PersonalTrainingSession WHERE session_id = %s"
    session = execute_query(session_query, (session_id,))
    
    if not session:
        print("Error: PT Session not found")
        return None
    
    if check_room_double_booking(room_id, booking_date, booking_time):
        print("Error: Room is already booked at this time")
        return None
    
    room_query = "SELECT status, capacity FROM Room WHERE room_id = %s"
    room = execute_query(room_query, (room_id,))
    
    if not room:
        print("Error: Room not found")
        return None
    
    if room[0]['status'] != 'Available':
        print(f"Error: Room is currently {room[0]['status']}")
        return None
    
    insert_query = """
        INSERT INTO RoomBooking 
        (room_id, booking_date, booking_time, booking_type, reference_id, status)
        VALUES (%s, %s, %s, 'PT Session', %s, 'Booked')
        RETURNING booking_id
    """
    
    try:
        result = execute_query(insert_query, (room_id, booking_date, booking_time, session_id), fetch=True)
        if result:
            booking_id = result[0]['booking_id']
            
            update_query = "UPDATE PersonalTrainingSession SET room_id = %s WHERE session_id = %s"
            execute_update(update_query, (room_id, session_id))
            
            print(f"\n✓ Room booked successfully! Booking ID: {booking_id}")
            return booking_id
    except Exception as e:
        print(f"Error booking room: {e}")
        return None

def book_room_for_class(room_id, class_id, booking_date, booking_time):
    if not validate_date(booking_date):
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return None
    
    if not validate_time(booking_time):
        print("Error: Invalid time format. Use HH:MM")
        return None
    
    class_query = "SELECT capacity, current_enrollment FROM GroupClass WHERE class_id = %s"
    cls = execute_query(class_query, (class_id,))
    
    if not cls:
        print("Error: Group Class not found")
        return None
    
    room_query = "SELECT capacity FROM Room WHERE room_id = %s"
    room = execute_query(room_query, (room_id,))
    
    if not room:
        print("Error: Room not found")
        return None
    
    if room[0]['capacity'] < cls[0]['capacity']:
        print(f"Error: Room capacity ({room[0]['capacity']}) is less than class capacity ({cls[0]['capacity']})")
        return None
    
    if check_room_double_booking(room_id, booking_date, booking_time):
        print("Error: Room is already booked at this time")
        return None
    
    room_status_query = "SELECT status FROM Room WHERE room_id = %s"
    room_status = execute_query(room_status_query, (room_id,))
    
    if room_status[0]['status'] != 'Available':
        print(f"Error: Room is currently {room_status[0]['status']}")
        return None
    
    insert_query = """
        INSERT INTO RoomBooking 
        (room_id, booking_date, booking_time, booking_type, reference_id, status)
        VALUES (%s, %s, %s, 'Group Class', %s, 'Booked')
        RETURNING booking_id
    """
    
    try:
        result = execute_query(insert_query, (room_id, booking_date, booking_time, class_id), fetch=True)
        if result:
            booking_id = result[0]['booking_id']
            
            update_query = "UPDATE GroupClass SET room_id = %s WHERE class_id = %s"
            execute_update(update_query, (room_id, class_id))
            
            print(f"\n✓ Room booked successfully! Booking ID: {booking_id}")
            return booking_id
    except Exception as e:
        print(f"Error booking room: {e}")
        return None

def view_room_bookings(room_id=None, booking_date=None):
    query = """
        SELECT rb.booking_id, r.room_name, rb.booking_date, rb.booking_time,
               rb.booking_type, rb.reference_id, rb.status
        FROM RoomBooking rb
        JOIN Room r ON rb.room_id = r.room_id
        WHERE 1=1
    """
    params = []
    
    if room_id:
        query += " AND rb.room_id = %s"
        params.append(room_id)
    
    if booking_date:
        query += " AND rb.booking_date = %s"
        params.append(booking_date)
    
    query += " ORDER BY rb.booking_date, rb.booking_time"
    
    try:
        bookings = execute_query(query, tuple(params) if params else None)
        
        if not bookings:
            print("\nNo bookings found")
            return
        
        print("\n📅 Room Bookings:")
        print("=" * 80)
        for booking in bookings:
            print(f"\nBooking ID: {booking['booking_id']}")
            print(f"  Room: {booking['room_name']}")
            print(f"  Date: {booking['booking_date']}")
            print(f"  Time: {booking['booking_time']}")
            print(f"  Type: {booking['booking_type']}")
            print(f"  Reference ID: {booking['reference_id']}")
            print(f"  Status: {booking['status']}")
        print()
    except Exception as e:
        print(f"Error viewing bookings: {e}")

def view_available_rooms(booking_date, booking_time, min_capacity=None):
    query = """
        SELECT r.room_id, r.room_name, r.capacity, r.status
        FROM Room r
        WHERE r.status = 'Available'
        AND r.room_id NOT IN (
            SELECT room_id FROM RoomBooking
            WHERE booking_date = %s
            AND booking_time = %s
            AND status = 'Booked'
        )
    """
    params = [booking_date, booking_time]
    
    if min_capacity:
        query += " AND r.capacity >= %s"
        params.append(min_capacity)
    
    query += " ORDER BY r.capacity"
    
    try:
        rooms = execute_query(query, tuple(params))
        
        if not rooms:
            print(f"\nNo available rooms on {booking_date} at {booking_time}")
            return
        
        print(f"\n🏢 Available Rooms on {booking_date} at {booking_time}:")
        print("-" * 60)
        for room in rooms:
            print(f"  Room ID: {room['room_id']} - {room['room_name']} (Capacity: {room['capacity']})")
        print()
    except Exception as e:
        print(f"Error viewing available rooms: {e}")

def log_equipment_issue(equipment_id, issue_description, status='Maintenance'):
    if status not in ['Maintenance', 'Out of Order']:
        print("Error: Status must be 'Maintenance' or 'Out of Order'")
        return False
    
    check_query = "SELECT equipment_name FROM Equipment WHERE equipment_id = %s"
    equipment = execute_query(check_query, (equipment_id,))
    
    if not equipment:
        print("Error: Equipment not found")
        return False
    
    update_query = """
        UPDATE Equipment
        SET status = %s,
            maintenance_notes = COALESCE(maintenance_notes || E'\n', '') || %s || ' (Logged: ' || CURRENT_TIMESTAMP::text || ')'
        WHERE equipment_id = %s
        RETURNING equipment_id
    """
    
    try:
        result = execute_query(update_query, (status, issue_description, equipment_id), fetch=True)
        if result:
            print(f"\n✓ Equipment issue logged successfully!")
            print(f"   Equipment: {equipment[0]['equipment_name']}")
            print(f"   Status: {status}")
            return True
    except Exception as e:
        print(f"Error logging equipment issue: {e}")
        return False

def update_equipment_maintenance(equipment_id, maintenance_date=None, next_maintenance_date=None, status='Operational'):
    if status not in ['Operational', 'Maintenance', 'Out of Order']:
        print("Error: Invalid status")
        return False
    
    updates = []
    params = []
    
    if maintenance_date:
        if not validate_date(maintenance_date):
            print("Error: Invalid date format. Use YYYY-MM-DD")
            return False
        updates.append("last_maintenance = %s")
        params.append(maintenance_date)
    
    if next_maintenance_date:
        if not validate_date(next_maintenance_date):
            print("Error: Invalid date format. Use YYYY-MM-DD")
            return False
        updates.append("next_maintenance = %s")
        params.append(next_maintenance_date)
    
    updates.append("status = %s")
    params.append(status)
    params.append(equipment_id)
    
    update_query = f"UPDATE Equipment SET {', '.join(updates)} WHERE equipment_id = %s"
    
    try:
        rows = execute_update(update_query, tuple(params))
        if rows > 0:
            print("\n✓ Equipment maintenance record updated successfully")
            return True
        else:
            print("Error: Equipment not found")
            return False
    except Exception as e:
        print(f"Error updating maintenance record: {e}")
        return False

def view_equipment_status(room_id=None, status_filter=None):
    query = """
        SELECT e.equipment_id, e.equipment_name, r.room_name, 
               e.status, e.last_maintenance, e.next_maintenance, e.maintenance_notes
        FROM Equipment e
        LEFT JOIN Room r ON e.room_id = r.room_id
        WHERE 1=1
    """
    params = []
    
    if room_id:
        query += " AND e.room_id = %s"
        params.append(room_id)
    
    if status_filter:
        query += " AND e.status = %s"
        params.append(status_filter)
    
    query += " ORDER BY e.status, e.equipment_name"
    
    try:
        equipment = execute_query(query, tuple(params) if params else None)
        
        if not equipment:
            print("\nNo equipment found")
            return
        
        print("\n🔧 Equipment Status:")
        print("=" * 80)
        
        for eq in equipment:
            print(f"\nEquipment ID: {eq['equipment_id']}")
            print(f"  Name: {eq['equipment_name']}")
            print(f"  Room: {eq['room_name'] or 'Unassigned'}")
            print(f"  Status: {eq['status']}")
            if eq['last_maintenance']:
                print(f"  Last Maintenance: {eq['last_maintenance']}")
            if eq['next_maintenance']:
                print(f"  Next Maintenance: {eq['next_maintenance']}")
            if eq['maintenance_notes']:
                print(f"  Notes: {eq['maintenance_notes'][:100]}...")
        print()
    except Exception as e:
        print(f"Error viewing equipment: {e}")

def view_equipment_needing_maintenance():
    query = """
        SELECT e.equipment_id, e.equipment_name, r.room_name, 
               e.status, e.last_maintenance, e.next_maintenance
        FROM Equipment e
        LEFT JOIN Room r ON e.room_id = r.room_id
        WHERE e.status IN ('Maintenance', 'Out of Order')
           OR (e.next_maintenance IS NOT NULL AND e.next_maintenance <= CURRENT_DATE + INTERVAL '30 days')
        ORDER BY 
            CASE e.status 
                WHEN 'Out of Order' THEN 1
                WHEN 'Maintenance' THEN 2
                ELSE 3
            END,
            e.next_maintenance
    """
    
    try:
        equipment = execute_query(query)
        
        if not equipment:
            print("\n✓ All equipment is operational")
            return
        
        print("\n⚠️ Equipment Needing Attention:")
        print("=" * 80)
        
        for eq in equipment:
            print(f"\nEquipment ID: {eq['equipment_id']} - {eq['equipment_name']}")
            print(f"  Room: {eq['room_name'] or 'Unassigned'}")
            print(f"  Status: {eq['status']}")
            if eq['next_maintenance']:
                days_until = (eq['next_maintenance'] - date.today()).days
                if days_until < 0:
                    print(f"  ⚠️ Next Maintenance: {eq['next_maintenance']} (OVERDUE by {abs(days_until)} days)")
                elif days_until <= 30:
                    print(f"  ⚠️ Next Maintenance: {eq['next_maintenance']} (in {days_until} days)")
        print()
    except Exception as e:
        print(f"Error viewing equipment needing maintenance: {e}")
