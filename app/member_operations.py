from database import execute_query, execute_update, execute_transaction
from datetime import datetime
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

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

def register_member(name, email, date_of_birth, gender=None, phone=None, address=None):
    if not validate_email(email):
        print("Error: Invalid email format")
        return None
    
    if not validate_date(date_of_birth):
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return None
    
    check_query = "SELECT member_id FROM Member WHERE email = %s"
    existing = execute_query(check_query, (email,))
    
    if existing:
        print(f"Error: Email {email} is already registered")
        return None
    
    insert_query = """
        INSERT INTO Member (name, email, date_of_birth, gender, phone, address)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING member_id
    """
    
    try:
        result = execute_query(insert_query, (name, email, date_of_birth, gender, phone, address), fetch=True)
        if result:
            member_id = result[0]['member_id']
            print(f"\n✓ Registration successful! Member ID: {member_id}")
            return member_id
    except Exception as e:
        print(f"Error during registration: {e}")
        return None

def update_profile(member_id, name=None, phone=None, address=None):
    updates = []
    params = []
    
    if name:
        updates.append("name = %s")
        params.append(name)
    if phone:
        updates.append("phone = %s")
        params.append(phone)
    if address:
        updates.append("address = %s")
        params.append(address)
    
    if not updates:
        print("No updates provided")
        return False
    
    params.append(member_id)
    update_query = f"UPDATE Member SET {', '.join(updates)} WHERE member_id = %s"
    
    try:
        rows = execute_update(update_query, tuple(params))
        if rows > 0:
            print("\n✓ Profile updated successfully")
            return True
        else:
            print("Error: Member not found")
            return False
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False

def add_fitness_goal(member_id, goal_type, target_value, target_date, current_value=None):
    if not validate_date(target_date):
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return False
    
    insert_query = """
        INSERT INTO FitnessGoal (member_id, goal_type, target_value, current_value, target_date)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING goal_id
    """
    
    try:
        result = execute_query(insert_query, (member_id, goal_type, target_value, current_value, target_date), fetch=True)
        if result:
            print(f"\n✓ Fitness goal added successfully! Goal ID: {result[0]['goal_id']}")
            return True
    except Exception as e:
        print(f"Error adding fitness goal: {e}")
        return False

def log_health_metric(member_id, metric_type, value, notes=None):
    insert_query = """
        INSERT INTO HealthMetric (member_id, metric_type, value, notes)
        VALUES (%s, %s, %s, %s)
        RETURNING metric_id
    """
    
    try:
        result = execute_query(insert_query, (member_id, metric_type, value, notes), fetch=True)
        if result:
            print(f"\n✓ Health metric logged successfully! Metric ID: {result[0]['metric_id']}")
            return True
    except Exception as e:
        print(f"Error logging health metric: {e}")
        return False

def view_dashboard(member_id):
    dashboard_query = "SELECT * FROM member_dashboard_view WHERE member_id = %s"
    
    try:
        dashboard = execute_query(dashboard_query, (member_id,))
        if not dashboard:
            print("Error: Member not found")
            return
        
        data = dashboard[0]
        
        print("\n" + "="*60)
        print(f"DASHBOARD - {data['name']}")
        print("="*60)
        
        print("\n📊 Latest Health Metrics:")
        if data['latest_weight']:
            print(f"   Weight: {data['latest_weight']} kg")
        if data['latest_heart_rate']:
            print(f"   Heart Rate: {data['latest_heart_rate']} bpm")
        if data['latest_body_fat']:
            print(f"   Body Fat: {data['latest_body_fat']}%")
        
        print(f"\n🎯 Active Goals: {data['active_goals_count']}")
        goals_query = """
            SELECT goal_type, target_value, current_value, target_date
            FROM FitnessGoal
            WHERE member_id = %s AND status = 'Active'
            ORDER BY target_date
        """
        goals = execute_query(goals_query, (member_id,))
        for goal in goals:
            print(f"   • {goal['goal_type']}: {goal['current_value'] or 'N/A'} → {goal['target_value']} (by {goal['target_date']})")
        
        print(f"\n📅 Past Classes Attended: {data['past_classes_count']}")
        
        print(f"\n⏰ Upcoming PT Sessions: {data['upcoming_sessions_count']}")
        sessions_query = """
            SELECT pts.session_date, pts.session_time, t.name as trainer_name
            FROM PersonalTrainingSession pts
            JOIN Trainer t ON pts.trainer_id = t.trainer_id
            WHERE pts.member_id = %s
            AND pts.session_date >= CURRENT_DATE
            AND pts.status = 'Scheduled'
            ORDER BY pts.session_date, pts.session_time
            LIMIT 5
        """
        sessions = execute_query(sessions_query, (member_id,))
        for session in sessions:
            print(f"   • {session['session_date']} at {session['session_time']} with {session['trainer_name']}")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"Error loading dashboard: {e}")

def check_trainer_availability(trainer_id, session_date, session_time, duration_minutes=60):
    day_query = "SELECT EXTRACT(DOW FROM %s::date)::int as day_of_week"
    day_result = execute_query(day_query, (session_date,))
    if not day_result:
        return False
    
    day_of_week = day_result[0]['day_of_week']
    
    avail_query = """
        SELECT * FROM TrainerAvailability
        WHERE trainer_id = %s
        AND day_of_week = %s
        AND start_time <= %s::time
        AND end_time >= (%s::time + INTERVAL '%s minutes')
    """
    availability = execute_query(avail_query, (trainer_id, day_of_week, session_time, session_time, duration_minutes))
    
    if not availability:
        return False
    
    conflict_query = """
        SELECT session_id FROM PersonalTrainingSession
        WHERE trainer_id = %s
        AND session_date = %s
        AND session_time = %s
        AND status = 'Scheduled'
    """
    conflicts = execute_query(conflict_query, (trainer_id, session_date, session_time))
    
    return len(conflicts) == 0

def check_room_availability(room_id, session_date, session_time):
    conflict_query = """
        SELECT booking_id FROM RoomBooking
        WHERE room_id = %s
        AND booking_date = %s
        AND booking_time = %s
        AND status = 'Booked'
    """
    conflicts = execute_query(conflict_query, (room_id, session_date, session_time))
    return len(conflicts) == 0

def schedule_pt_session(member_id, trainer_id, session_date, session_time, duration_minutes=60, room_id=None):
    if not validate_date(session_date):
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return None
    
    if not validate_time(session_time):
        print("Error: Invalid time format. Use HH:MM")
        return None
    
    if not check_trainer_availability(trainer_id, session_date, session_time, duration_minutes):
        print("Error: Trainer is not available at this time")
        return None
    
    if room_id and not check_room_availability(room_id, session_date, session_time):
        print("Error: Room is not available at this time")
        return None
    
    insert_query = """
        INSERT INTO PersonalTrainingSession 
        (member_id, trainer_id, session_date, session_time, duration_minutes, room_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING session_id
    """
    
    try:
        result = execute_query(insert_query, (member_id, trainer_id, session_date, session_time, duration_minutes, room_id), fetch=True)
        if result:
            session_id = result[0]['session_id']
            
            if room_id:
                booking_query = """
                    INSERT INTO RoomBooking 
                    (room_id, booking_date, booking_time, booking_type, reference_id)
                    VALUES (%s, %s, %s, 'PT Session', %s)
                """
                execute_update(booking_query, (room_id, session_date, session_time, session_id))
            
            print(f"\n✓ PT session scheduled successfully! Session ID: {session_id}")
            return session_id
    except Exception as e:
        print(f"Error scheduling session: {e}")
        return None

def reschedule_pt_session(session_id, new_date, new_time):
    if not validate_date(new_date):
        print("Error: Invalid date format. Use YYYY-MM-DD")
        return False
    
    if not validate_time(new_time):
        print("Error: Invalid time format. Use HH:MM")
        return False
    
    get_query = "SELECT trainer_id, room_id FROM PersonalTrainingSession WHERE session_id = %s"
    session = execute_query(get_query, (session_id,))
    
    if not session:
        print("Error: Session not found")
        return False
    
    trainer_id = session[0]['trainer_id']
    room_id = session[0]['room_id']
    
    if not check_trainer_availability(trainer_id, new_date, new_time):
        print("Error: Trainer is not available at this time")
        return False
    
    if room_id and not check_room_availability(room_id, new_date, new_time):
        print("Error: Room is not available at this time")
        return False
    
    update_query = """
        UPDATE PersonalTrainingSession
        SET session_date = %s, session_time = %s
        WHERE session_id = %s
    """
    
    try:
        execute_update(update_query, (new_date, new_time, session_id))
        
        if room_id:
            booking_update = """
                UPDATE RoomBooking
                SET booking_date = %s, booking_time = %s
                WHERE reference_id = %s AND booking_type = 'PT Session'
            """
            execute_update(booking_update, (new_date, new_time, session_id))
        
        print("\n✓ Session rescheduled successfully")
        return True
    except Exception as e:
        print(f"Error rescheduling session: {e}")
        return False
