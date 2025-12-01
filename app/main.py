import sys
from database import execute_query, get_connection
import member_operations as member_ops
import trainer_operations as trainer_ops
import admin_operations as admin_ops

def print_header():
    print("\n" + "="*70)
    print("  HEALTH AND FITNESS CLUB MANAGEMENT SYSTEM")
    print("="*70)

def print_separator():
    print("-" * 70)

def get_user_input(prompt, validator=None):
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty. Please try again.")
            continue
        if validator:
            try:
                if validator(value):
                    return value
                else:
                    print("Invalid input. Please try again.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            return value

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer")

def list_members():
    query = "SELECT member_id, name, email FROM Member ORDER BY name"
    members = execute_query(query)
    if members:
        print("\nMembers:")
        for m in members:
            print(f"  ID: {m['member_id']} - {m['name']} ({m['email']})")
    else:
        print("No members found")
    return members

def list_trainers():
    query = "SELECT trainer_id, name, specialization FROM Trainer ORDER BY name"
    trainers = execute_query(query)
    if trainers:
        print("\nTrainers:")
        for t in trainers:
            print(f"  ID: {t['trainer_id']} - {t['name']} ({t['specialization']})")
    else:
        print("No trainers found")
    return trainers

def list_rooms():
    query = "SELECT room_id, room_name, capacity, status FROM Room ORDER BY room_name"
    rooms = execute_query(query)
    if rooms:
        print("\nRooms:")
        for r in rooms:
            print(f"  ID: {r['room_id']} - {r['room_name']} (Capacity: {r['capacity']}, Status: {r['status']})")
    else:
        print("No rooms found")
    return rooms

def list_equipment():
    query = "SELECT equipment_id, equipment_name, status FROM Equipment ORDER BY equipment_name"
    equipment = execute_query(query)
    if equipment:
        print("\nEquipment:")
        for e in equipment:
            print(f"  ID: {e['equipment_id']} - {e['equipment_name']} (Status: {e['status']})")
    else:
        print("No equipment found")
    return equipment

def member_menu():
    while True:
        print_header()
        print("\nMEMBER MENU")
        print_separator()
        print("1. Register New Member")
        print("2. Update Profile")
        print("3. Add Fitness Goal")
        print("4. Log Health Metric")
        print("5. View Dashboard")
        print("6. Schedule PT Session")
        print("7. Reschedule PT Session")
        print("8. Back to Main Menu")
        print_separator()
        
        choice = get_int_input("Select an option (1-8): ", 1, 8)
        
        if choice == 1:
            print("\n--- REGISTER NEW MEMBER ---")
            name = get_user_input("Name: ")
            email = get_user_input("Email: ")
            dob = get_user_input("Date of Birth (YYYY-MM-DD): ")
            gender = input("Gender (optional, press Enter to skip): ").strip() or None
            phone = input("Phone (optional, press Enter to skip): ").strip() or None
            address = input("Address (optional, press Enter to skip): ").strip() or None
            member_ops.register_member(name, email, dob, gender, phone, address)
            input("\nPress Enter to continue...")
        
        elif choice == 2:
            print("\n--- UPDATE PROFILE ---")
            members = list_members()
            if members:
                member_id = get_int_input("\nEnter Member ID: ")
                name = input("New Name (optional, press Enter to skip): ").strip() or None
                phone = input("New Phone (optional, press Enter to skip): ").strip() or None
                address = input("New Address (optional, press Enter to skip): ").strip() or None
                member_ops.update_profile(member_id, name, phone, address)
            input("\nPress Enter to continue...")
        
        elif choice == 3:
            print("\n--- ADD FITNESS GOAL ---")
            members = list_members()
            if members:
                member_id = get_int_input("\nEnter Member ID: ")
                print("\nGoal Types: Weight Loss, Weight Gain, Body Fat Reduction, Muscle Gain, Endurance, Flexibility")
                goal_type = get_user_input("Goal Type: ")
                try:
                    target_value = float(input("Target Value: ").strip())
                except ValueError:
                    print("Invalid target value")
                    input("\nPress Enter to continue...")
                    continue
                target_date = get_user_input("Target Date (YYYY-MM-DD): ")
                current_input = input("Current Value (optional, press Enter to skip): ").strip()
                current_value = float(current_input) if current_input else None
                member_ops.add_fitness_goal(member_id, goal_type, target_value, target_date, current_value)
            input("\nPress Enter to continue...")
        
        elif choice == 4:
            print("\n--- LOG HEALTH METRIC ---")
            members = list_members()
            if members:
                member_id = get_int_input("\nEnter Member ID: ")
                print("\nMetric Types: Weight, Height, Heart Rate, Body Fat, Blood Pressure, BMI")
                metric_type = get_user_input("Metric Type: ")
                try:
                    value = float(input("Value: ").strip())
                except ValueError:
                    print("Invalid value")
                    input("\nPress Enter to continue...")
                    continue
                notes = input("Notes (optional, press Enter to skip): ").strip() or None
                member_ops.log_health_metric(member_id, metric_type, value, notes)
            input("\nPress Enter to continue...")
        
        elif choice == 5:
            print("\n--- MEMBER DASHBOARD ---")
            members = list_members()
            if members:
                member_id = get_int_input("\nEnter Member ID: ")
                member_ops.view_dashboard(member_id)
            input("\nPress Enter to continue...")
        
        elif choice == 6:
            print("\n--- SCHEDULE PT SESSION ---")
            members = list_members()
            trainers = list_trainers()
            if members and trainers:
                member_id = get_int_input("\nEnter Member ID: ")
                trainer_id = get_int_input("Enter Trainer ID: ")
                session_date = get_user_input("Session Date (YYYY-MM-DD): ")
                session_time = get_user_input("Session Time (HH:MM): ")
                duration = get_int_input("Duration in minutes (default 60, press Enter for default): ", 1) or 60
                room_input = input("Room ID (optional, press Enter to skip): ").strip()
                room_id = int(room_input) if room_input else None
                member_ops.schedule_pt_session(member_id, trainer_id, session_date, session_time, duration, room_id)
            input("\nPress Enter to continue...")
        
        elif choice == 7:
            print("\n--- RESCHEDULE PT SESSION ---")
            query = """
                SELECT pts.session_id, pts.session_date, pts.session_time, m.name as member_name
                FROM PersonalTrainingSession pts
                JOIN Member m ON pts.member_id = m.member_id
                WHERE pts.status = 'Scheduled'
                ORDER BY pts.session_date
            """
            sessions = execute_query(query)
            if sessions:
                print("\nUpcoming Sessions:")
                for s in sessions:
                    print(f"  Session ID: {s['session_id']} - {s['member_name']} on {s['session_date']} at {s['session_time']}")
                session_id = get_int_input("\nEnter Session ID: ")
                new_date = get_user_input("New Date (YYYY-MM-DD): ")
                new_time = get_user_input("New Time (HH:MM): ")
                member_ops.reschedule_pt_session(session_id, new_date, new_time)
            else:
                print("No scheduled sessions found")
            input("\nPress Enter to continue...")
        
        elif choice == 8:
            break

def trainer_menu():
    while True:
        print_header()
        print("\nTRAINER MENU")
        print_separator()
        print("1. Set Availability")
        print("2. View Availability")
        print("3. View Schedule")
        print("4. Lookup Member")
        print("5. Back to Main Menu")
        print_separator()
        
        choice = get_int_input("Select an option (1-5): ", 1, 5)
        
        if choice == 1:
            print("\n--- SET AVAILABILITY ---")
            trainers = list_trainers()
            if trainers:
                trainer_id = get_int_input("\nEnter Trainer ID: ")
                print("\nDay of Week: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday")
                day_of_week = get_int_input("Day of Week (0-6): ", 0, 6)
                start_time = get_user_input("Start Time (HH:MM): ")
                end_time = get_user_input("End Time (HH:MM): ")
                trainer_ops.add_availability(trainer_id, day_of_week, start_time, end_time)
            input("\nPress Enter to continue...")
        
        elif choice == 2:
            print("\n--- VIEW AVAILABILITY ---")
            trainers = list_trainers()
            if trainers:
                trainer_id = get_int_input("\nEnter Trainer ID: ")
                trainer_ops.view_availability(trainer_id)
            input("\nPress Enter to continue...")
        
        elif choice == 3:
            print("\n--- VIEW SCHEDULE ---")
            trainers = list_trainers()
            if trainers:
                trainer_id = get_int_input("\nEnter Trainer ID: ")
                trainer_ops.view_trainer_schedule(trainer_id)
            input("\nPress Enter to continue...")
        
        elif choice == 4:
            print("\n--- LOOKUP MEMBER ---")
            name_search = get_user_input("Enter member name (or partial name): ")
            trainer_ops.lookup_member_by_name(name_search)
            input("\nPress Enter to continue...")
        
        elif choice == 5:
            break

def admin_menu():
    while True:
        print_header()
        print("\nADMIN MENU")
        print_separator()
        print("1. Book Room for PT Session")
        print("2. Book Room for Group Class")
        print("3. View Room Bookings")
        print("4. View Available Rooms")
        print("5. Log Equipment Issue")
        print("6. Update Equipment Maintenance")
        print("7. View Equipment Status")
        print("8. View Equipment Needing Maintenance")
        print("9. Back to Main Menu")
        print_separator()
        
        choice = get_int_input("Select an option (1-9): ", 1, 9)
        
        if choice == 1:
            print("\n--- BOOK ROOM FOR PT SESSION ---")
            rooms = list_rooms()
            query = """
                SELECT pts.session_id, pts.session_date, pts.session_time, m.name as member_name
                FROM PersonalTrainingSession pts
                JOIN Member m ON pts.member_id = m.member_id
                WHERE pts.status = 'Scheduled'
                ORDER BY pts.session_date
            """
            sessions = execute_query(query)
            if rooms and sessions:
                print("\nScheduled PT Sessions:")
                for s in sessions:
                    print(f"  Session ID: {s['session_id']} - {s['member_name']} on {s['session_date']} at {s['session_time']}")
                room_id = get_int_input("\nEnter Room ID: ")
                session_id = get_int_input("Enter Session ID: ")
                session = next((s for s in sessions if s['session_id'] == session_id), None)
                if session:
                    admin_ops.book_room_for_session(room_id, session_id, str(session['session_date']), str(session['session_time']))
                else:
                    print("Session not found")
            input("\nPress Enter to continue...")
        
        elif choice == 2:
            print("\n--- BOOK ROOM FOR GROUP CLASS ---")
            rooms = list_rooms()
            query = """
                SELECT class_id, class_name, class_date, class_time, capacity
                FROM GroupClass
                WHERE status = 'Scheduled'
                ORDER BY class_date
            """
            classes = execute_query(query)
            if rooms and classes:
                print("\nScheduled Group Classes:")
                for c in classes:
                    print(f"  Class ID: {c['class_id']} - {c['class_name']} on {c['class_date']} at {c['class_time']} (Capacity: {c['capacity']})")
                room_id = get_int_input("\nEnter Room ID: ")
                class_id = get_int_input("Enter Class ID: ")
                cls = next((c for c in classes if c['class_id'] == class_id), None)
                if cls:
                    admin_ops.book_room_for_class(room_id, class_id, str(cls['class_date']), str(cls['class_time']))
                else:
                    print("Class not found")
            input("\nPress Enter to continue...")
        
        elif choice == 3:
            print("\n--- VIEW ROOM BOOKINGS ---")
            room_input = input("Room ID (optional, press Enter for all): ").strip()
            room_id = int(room_input) if room_input else None
            date_input = input("Date (YYYY-MM-DD, optional, press Enter for all): ").strip()
            booking_date = date_input if date_input else None
            admin_ops.view_room_bookings(room_id, booking_date)
            input("\nPress Enter to continue...")
        
        elif choice == 4:
            print("\n--- VIEW AVAILABLE ROOMS ---")
            booking_date = get_user_input("Date (YYYY-MM-DD): ")
            booking_time = get_user_input("Time (HH:MM): ")
            capacity_input = input("Minimum Capacity (optional, press Enter to skip): ").strip()
            min_capacity = int(capacity_input) if capacity_input else None
            admin_ops.view_available_rooms(booking_date, booking_time, min_capacity)
            input("\nPress Enter to continue...")
        
        elif choice == 5:
            print("\n--- LOG EQUIPMENT ISSUE ---")
            equipment = list_equipment()
            if equipment:
                equipment_id = get_int_input("\nEnter Equipment ID: ")
                issue = get_user_input("Issue Description: ")
                print("\nStatus Options: Maintenance, Out of Order")
                status = get_user_input("Status: ")
                admin_ops.log_equipment_issue(equipment_id, issue, status)
            input("\nPress Enter to continue...")
        
        elif choice == 6:
            print("\n--- UPDATE EQUIPMENT MAINTENANCE ---")
            equipment = list_equipment()
            if equipment:
                equipment_id = get_int_input("\nEnter Equipment ID: ")
                maint_date = input("Maintenance Date (YYYY-MM-DD, optional): ").strip() or None
                next_maint = input("Next Maintenance Date (YYYY-MM-DD, optional): ").strip() or None
                print("\nStatus Options: Operational, Maintenance, Out of Order")
                status = input("Status (default: Operational): ").strip() or 'Operational'
                admin_ops.update_equipment_maintenance(equipment_id, maint_date, next_maint, status)
            input("\nPress Enter to continue...")
        
        elif choice == 7:
            print("\n--- VIEW EQUIPMENT STATUS ---")
            room_input = input("Room ID (optional, press Enter for all): ").strip()
            room_id = int(room_input) if room_input else None
            status_input = input("Status filter (optional, press Enter for all): ").strip() or None
            admin_ops.view_equipment_status(room_id, status_input)
            input("\nPress Enter to continue...")
        
        elif choice == 8:
            admin_ops.view_equipment_needing_maintenance()
            input("\nPress Enter to continue...")
        
        elif choice == 9:
            break

def main():
    try:
        conn = get_connection()
        conn.close()
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running")
        print("2. Database 'fitness_club' exists")
        print("3. Password is set correctly in app/database.py")
        sys.exit(1)
    
    while True:
        print_header()
        print("\nMAIN MENU")
        print_separator()
        print("1. Member Operations")
        print("2. Trainer Operations")
        print("3. Admin Operations")
        print("4. Exit")
        print_separator()
        
        choice = get_int_input("Select a role (1-4): ", 1, 4)
        
        if choice == 1:
            member_menu()
        elif choice == 2:
            trainer_menu()
        elif choice == 3:
            admin_menu()
        elif choice == 4:
            print("\nThank you for using the Health and Fitness Club Management System!")
            break

if __name__ == "__main__":
    main()
