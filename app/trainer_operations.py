"""
Trainer Operations Module
Implements 2 trainer functions:
1. Set Availability
2. Schedule View
"""
from database import execute_query, execute_update
from datetime import datetime

def validate_time(time_str):
    """Validate time format HH:MM"""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def day_name(day_num):
    """Convert day number to name"""
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return days[day_num] if 0 <= day_num <= 6 else 'Invalid'

# ============================================
# OPERATION 1: SET AVAILABILITY
# ============================================

def check_availability_overlap(trainer_id, day_of_week, start_time, end_time, exclude_id=None):
    """
    Check if availability slot overlaps with existing slots.
    
    Returns:
        True if overlap exists, False otherwise
    """
    overlap_query = """
        SELECT availability_id FROM TrainerAvailability
        WHERE trainer_id = %s
        AND day_of_week = %s
        AND (
            (start_time <= %s::time AND end_time > %s::time) OR
            (start_time < %s::time AND end_time >= %s::time) OR
            (start_time >= %s::time AND end_time <= %s::time)
        )
    """
    params = (trainer_id, day_of_week, start_time, start_time, end_time, end_time, start_time, end_time)
    
    if exclude_id:
        overlap_query += " AND availability_id != %s"
        params = params + (exclude_id,)
    
    overlaps = execute_query(overlap_query, params)
    return len(overlaps) > 0

def add_availability(trainer_id, day_of_week, start_time, end_time):
    """
    Add availability slot for a trainer.
    
    Args:
        trainer_id: Trainer ID
        day_of_week: Day of week (0=Sunday, 6=Saturday)
        start_time: Start time in HH:MM format
        end_time: End time in HH:MM format
    
    Returns:
        availability_id if successful, None otherwise
    """
    if not validate_time(start_time):
        print("Error: Invalid start time format. Use HH:MM")
        return None
    
    if not validate_time(end_time):
        print("Error: Invalid end time format. Use HH:MM")
        return None
    
    if day_of_week < 0 or day_of_week > 6:
        print("Error: Day of week must be 0-6 (0=Sunday, 6=Saturday)")
        return None
    
    # Check if end_time > start_time
    start_dt = datetime.strptime(start_time, '%H:%M')
    end_dt = datetime.strptime(end_time, '%H:%M')
    if end_dt <= start_dt:
        print("Error: End time must be after start time")
        return None
    
    # Check for overlaps
    if check_availability_overlap(trainer_id, day_of_week, start_time, end_time):
        print(f"Error: Availability overlaps with existing slot on {day_name(day_of_week)}")
        return None
    
    # Insert availability
    insert_query = """
        INSERT INTO TrainerAvailability (trainer_id, day_of_week, start_time, end_time)
        VALUES (%s, %s, %s, %s)
        RETURNING availability_id
    """
    
    try:
        result = execute_query(insert_query, (trainer_id, day_of_week, start_time, end_time), fetch=True)
        if result:
            avail_id = result[0]['availability_id']
            print(f"\n✓ Availability added successfully! Availability ID: {avail_id}")
            print(f"   {day_name(day_of_week)}: {start_time} - {end_time}")
            return avail_id
    except Exception as e:
        print(f"Error adding availability: {e}")
        return None

def update_availability(availability_id, start_time=None, end_time=None):
    """
    Update an existing availability slot.
    
    Args:
        availability_id: Availability ID to update
        start_time: New start time (optional)
        end_time: New end time (optional)
    """
    # Get current availability
    get_query = "SELECT trainer_id, day_of_week, start_time, end_time FROM TrainerAvailability WHERE availability_id = %s"
    current = execute_query(get_query, (availability_id,))
    
    if not current:
        print("Error: Availability slot not found")
        return False
    
    trainer_id = current[0]['trainer_id']
    day_of_week = current[0]['day_of_week']
    old_start = current[0]['start_time'].strftime('%H:%M')
    old_end = current[0]['end_time'].strftime('%H:%M')
    
    new_start = start_time if start_time else old_start
    new_end = end_time if end_time else old_end
    
    if start_time and not validate_time(start_time):
        print("Error: Invalid start time format. Use HH:MM")
        return False
    
    if end_time and not validate_time(end_time):
        print("Error: Invalid end time format. Use HH:MM")
        return False
    
    # Check for overlaps (excluding current slot)
    if check_availability_overlap(trainer_id, day_of_week, new_start, new_end, exclude_id=availability_id):
        print(f"Error: Updated availability overlaps with another slot")
        return False
    
    # Update
    updates = []
    params = []
    
    if start_time:
        updates.append("start_time = %s")
        params.append(start_time)
    if end_time:
        updates.append("end_time = %s")
        params.append(end_time)
    
    if not updates:
        print("No updates provided")
        return False
    
    params.append(availability_id)
    update_query = f"UPDATE TrainerAvailability SET {', '.join(updates)} WHERE availability_id = %s"
    
    try:
        execute_update(update_query, tuple(params))
        print("\n✓ Availability updated successfully")
        return True
    except Exception as e:
        print(f"Error updating availability: {e}")
        return False

def view_availability(trainer_id):
    """
    View all availability slots for a trainer.
    
    Args:
        trainer_id: Trainer ID
    """
    query = """
        SELECT availability_id, day_of_week, start_time, end_time
        FROM TrainerAvailability
        WHERE trainer_id = %s
        ORDER BY day_of_week, start_time
    """
    
    try:
        slots = execute_query(query, (trainer_id,))
        if not slots:
            print("\nNo availability slots set")
            return
        
        print(f"\n📅 Availability Schedule for Trainer ID {trainer_id}:")
        print("-" * 50)
        current_day = -1
        for slot in slots:
            day = slot['day_of_week']
            if day != current_day:
                print(f"\n{day_name(day)}:")
                current_day = day
            start = slot['start_time'].strftime('%H:%M')
            end = slot['end_time'].strftime('%H:%M')
            print(f"   {start} - {end} (ID: {slot['availability_id']})")
        print()
    except Exception as e:
        print(f"Error viewing availability: {e}")

# ============================================
# OPERATION 2: SCHEDULE VIEW
# ============================================

def view_trainer_schedule(trainer_id):
    """
    View trainer's upcoming PT sessions and assigned classes.
    
    Args:
        trainer_id: Trainer ID
    """
    print(f"\n📋 Schedule for Trainer ID {trainer_id}")
    print("=" * 70)
    
    # Get trainer name
    trainer_query = "SELECT name FROM Trainer WHERE trainer_id = %s"
    trainer = execute_query(trainer_query, (trainer_id,))
    if trainer:
        print(f"Trainer: {trainer[0]['name']}\n")
    
    # Get PT Sessions
    sessions_query = """
        SELECT pts.session_id, pts.session_date, pts.session_time, 
               pts.duration_minutes, m.name as member_name, r.room_name
        FROM PersonalTrainingSession pts
        JOIN Member m ON pts.member_id = m.member_id
        LEFT JOIN Room r ON pts.room_id = r.room_id
        WHERE pts.trainer_id = %s
        AND pts.session_date >= CURRENT_DATE
        AND pts.status = 'Scheduled'
        ORDER BY pts.session_date, pts.session_time
    """
    
    try:
        sessions = execute_query(sessions_query, (trainer_id,))
        
        print("🏋️ Personal Training Sessions:")
        print("-" * 70)
        if sessions:
            for session in sessions:
                date = session['session_date']
                time = session['session_time'].strftime('%H:%M')
                duration = session['duration_minutes']
                member = session['member_name']
                room = session['room_name'] or 'TBD'
                print(f"  • {date} at {time} ({duration} min) - {member} - Room: {room}")
        else:
            print("  No upcoming PT sessions")
        
        print()
        
        # Get Group Classes
        classes_query = """
            SELECT gc.class_id, gc.class_name, gc.class_date, gc.class_time,
                   gc.duration_minutes, gc.current_enrollment, gc.capacity, r.room_name
            FROM GroupClass gc
            LEFT JOIN Room r ON gc.room_id = r.room_id
            WHERE gc.trainer_id = %s
            AND gc.class_date >= CURRENT_DATE
            AND gc.status = 'Scheduled'
            ORDER BY gc.class_date, gc.class_time
        """
        
        classes = execute_query(classes_query, (trainer_id,))
        
        print("👥 Group Classes:")
        print("-" * 70)
        if classes:
            for cls in classes:
                date = cls['class_date']
                time = cls['class_time'].strftime('%H:%M')
                duration = cls['duration_minutes']
                enrollment = cls['current_enrollment']
                capacity = cls['capacity']
                room = cls['room_name'] or 'TBD'
                print(f"  • {cls['class_name']} - {date} at {time} ({duration} min)")
                print(f"    Enrollment: {enrollment}/{capacity} - Room: {room}")
        else:
            print("  No upcoming group classes")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"Error viewing schedule: {e}")

def lookup_member_by_name(name_search):
    """
    Lookup member by name (case-insensitive search).
    Shows current goal and last metric.
    
    Args:
        name_search: Name or partial name to search
    """
    search_query = """
        SELECT m.member_id, m.name, m.email
        FROM Member m
        WHERE LOWER(m.name) LIKE LOWER(%s)
        ORDER BY m.name
        LIMIT 10
    """
    
    try:
        members = execute_query(search_query, (f'%{name_search}%',))
        
        if not members:
            print(f"\nNo members found matching '{name_search}'")
            return
        
        print(f"\n🔍 Members matching '{name_search}':")
        print("-" * 70)
        
        for member in members:
            member_id = member['member_id']
            print(f"\n{member['name']} (ID: {member_id}, Email: {member['email']})")
            
            # Get active goals
            goals_query = """
                SELECT goal_type, target_value, current_value, target_date
                FROM FitnessGoal
                WHERE member_id = %s AND status = 'Active'
                ORDER BY target_date
                LIMIT 3
            """
            goals = execute_query(goals_query, (member_id,))
            
            if goals:
                print("  Current Goals:")
                for goal in goals:
                    current = goal['current_value'] or 'N/A'
                    target = goal['target_value']
                    print(f"    • {goal['goal_type']}: {current} → {target} (by {goal['target_date']})")
            
            # Get latest metric
            metric_query = """
                SELECT metric_type, value, recorded_date
                FROM HealthMetric
                WHERE member_id = %s
                ORDER BY recorded_date DESC
                LIMIT 1
            """
            metric = execute_query(metric_query, (member_id,))
            
            if metric:
                m = metric[0]
                date = m['recorded_date'].strftime('%Y-%m-%d')
                print(f"  Latest Metric: {m['metric_type']} = {m['value']} (recorded {date})")
            
            print()
        
    except Exception as e:
        print(f"Error looking up member: {e}")

