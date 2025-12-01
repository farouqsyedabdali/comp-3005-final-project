# Health and Fitness Club Management System

A database-driven CLI application for managing a health and fitness club, supporting members, trainers, and administrative staff.

## Project Structure

```
/project-root
  /sql
    DDL.sql          # Database schema definition
    DML.sql          # Sample data
  /app
    database.py          # Database connection handling
    member_operations.py  # Member functions (4 operations)
    trainer_operations.py # Trainer functions (2 operations)
    admin_operations.py   # Admin functions (2 operations)
    main.py              # CLI menu system
  /docs
    ERD.pdf         # ER diagram (to be created)
  README.md         # This file
```

## Prerequisites

- Python 3.7 or higher
- PostgreSQL 12 or higher
- psycopg2 library

## Setup Instructions

### 1. Install PostgreSQL

Ensure PostgreSQL is installed and running on your system.

### 2. Create Database

```sql
CREATE DATABASE fitness_club;
```

### 3. Set Database Password

Edit `app/database.py` and set your PostgreSQL password:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'fitness_club',
    'user': 'postgres',
    'password': 'YOUR_PASSWORD_HERE'  # Fill this in
}
```

### 4. Install Python Dependencies

```bash
pip install psycopg2-binary
```

### 5. Initialize Database Schema

Run the DDL script to create all tables, views, triggers, and indexes:

```bash
psql -U postgres -d fitness_club -f sql/DDL.sql
```

### 6. Load Sample Data

Run the DML script to populate the database with sample data:

```bash
psql -U postgres -d fitness_club -f sql/DML.sql
```

### 7. Run the Application

```bash
python app/main.py
```

## Features

### Member Operations (4 functions)
1. **User Registration** - Register new members with validation
2. **Profile Management** - Update profile, add fitness goals, log health metrics
3. **Dashboard** - View latest health metrics, active goals, class count, upcoming sessions
4. **PT Session Scheduling** - Book and reschedule personal training sessions

### Trainer Operations (2 functions)
1. **Set Availability** - Define weekly availability slots (prevents overlaps)
2. **Schedule View** - View assigned PT sessions and group classes

### Admin Operations (2 functions)
1. **Room Booking** - Assign rooms for sessions/classes (prevents double-booking)
2. **Equipment Maintenance** - Log issues, track status, update maintenance records

## Database Features

- **6 Entities**: Member, Trainer, Admin, PersonalTrainingSession, GroupClass, HealthMetric, Room
- **5 Relationships**: Member-Session, Trainer-Session, Member-Class, Member-Metric, Trainer-Class
- **1 View**: `member_dashboard_view` - Aggregates member dashboard data
- **1 Trigger**: `update_class_capacity_trigger` - Auto-updates class enrollment
- **1 Index**: `idx_member_email` - Fast member email lookups

## Usage

1. Start the application: `python app/main.py`
2. Select a role (Member, Trainer, or Admin)
3. Choose an operation from the menu
4. Follow the prompts to complete the operation

## Demo Video

https://youtu.be/wZkT4DSSowQ

## Notes

- All dates should be in `YYYY-MM-DD` format
- All times should be in `HH:MM` format (24-hour)
- The system validates inputs and prevents invalid operations (e.g., double-booking, capacity exceeded)
- Health metrics are stored historically and do not overwrite previous entries

## Group Information

- **Group Size**: Solo (1 student)
- **Entities**: 6
- **Relationships**: 5
- **Operations**: 8 total (4 member, 2 trainer, 2 admin)

