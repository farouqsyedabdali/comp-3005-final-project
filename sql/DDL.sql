-- Health and Fitness Club Management System
-- DDL.sql - Database Schema Definition

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS ClassRegistration CASCADE;
DROP TABLE IF EXISTS PersonalTrainingSession CASCADE;
DROP TABLE IF EXISTS GroupClass CASCADE;
DROP TABLE IF EXISTS TrainerAvailability CASCADE;
DROP TABLE IF EXISTS HealthMetric CASCADE;
DROP TABLE IF EXISTS FitnessGoal CASCADE;
DROP TABLE IF EXISTS RoomBooking CASCADE;
DROP TABLE IF EXISTS Equipment CASCADE;
DROP TABLE IF EXISTS Billing CASCADE;
DROP TABLE IF EXISTS Member CASCADE;
DROP TABLE IF EXISTS Trainer CASCADE;
DROP TABLE IF EXISTS Admin CASCADE;
DROP TABLE IF EXISTS Room CASCADE;

-- Drop views, triggers, and functions
DROP VIEW IF EXISTS member_dashboard_view CASCADE;
DROP TRIGGER IF EXISTS update_class_capacity_trigger ON ClassRegistration;
DROP FUNCTION IF EXISTS update_class_capacity() CASCADE;

-- ============================================
-- CORE ENTITIES
-- ============================================

-- Member Entity
CREATE TABLE Member (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20),
    phone VARCHAR(20),
    address TEXT,
    registration_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT valid_email CHECK (email LIKE '%@%.%'),
    CONSTRAINT valid_dob CHECK (date_of_birth <= CURRENT_DATE)
);

-- Trainer Entity
CREATE TABLE Trainer (
    trainer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(20),
    hire_date DATE DEFAULT CURRENT_DATE
);

-- Admin Entity
CREATE TABLE Admin (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'Administrator'
);

-- Room Entity
CREATE TABLE Room (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(50) UNIQUE NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    equipment_list TEXT,
    status VARCHAR(20) DEFAULT 'Available' CHECK (status IN ('Available', 'Maintenance', 'Occupied'))
);

-- ============================================
-- RELATIONSHIP ENTITIES
-- ============================================

-- Personal Training Session (Member-Trainer relationship)
CREATE TABLE PersonalTrainingSession (
    session_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES Member(member_id) ON DELETE CASCADE,
    trainer_id INTEGER NOT NULL REFERENCES Trainer(trainer_id) ON DELETE CASCADE,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    duration_minutes INTEGER DEFAULT 60 CHECK (duration_minutes > 0),
    status VARCHAR(20) DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'Completed', 'Cancelled')),
    room_id INTEGER REFERENCES Room(room_id),
    notes TEXT,
    CONSTRAINT no_overlap_trainer UNIQUE (trainer_id, session_date, session_time),
    CONSTRAINT valid_session_date CHECK (session_date >= CURRENT_DATE)
);

-- Group Class (Trainer-Class relationship)
CREATE TABLE GroupClass (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    trainer_id INTEGER NOT NULL REFERENCES Trainer(trainer_id) ON DELETE CASCADE,
    class_date DATE NOT NULL,
    class_time TIME NOT NULL,
    duration_minutes INTEGER DEFAULT 60 CHECK (duration_minutes > 0),
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    current_enrollment INTEGER DEFAULT 0 CHECK (current_enrollment >= 0),
    room_id INTEGER REFERENCES Room(room_id),
    status VARCHAR(20) DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'Completed', 'Cancelled')),
    CONSTRAINT valid_class_date CHECK (class_date >= CURRENT_DATE),
    CONSTRAINT enrollment_check CHECK (current_enrollment <= capacity)
);

-- Class Registration (Member-GroupClass many-to-many relationship)
CREATE TABLE ClassRegistration (
    registration_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES Member(member_id) ON DELETE CASCADE,
    class_id INTEGER NOT NULL REFERENCES GroupClass(class_id) ON DELETE CASCADE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Registered' CHECK (status IN ('Registered', 'Cancelled', 'Completed')),
    CONSTRAINT unique_registration UNIQUE (member_id, class_id)
);

-- ============================================
-- SUPPORTING ENTITIES
-- ============================================

-- Health Metric (Member attribute - historical)
CREATE TABLE HealthMetric (
    metric_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES Member(member_id) ON DELETE CASCADE,
    metric_type VARCHAR(50) NOT NULL CHECK (metric_type IN ('Weight', 'Height', 'Heart Rate', 'Body Fat', 'Blood Pressure', 'BMI')),
    value DECIMAL(10, 2) NOT NULL CHECK (value > 0),
    recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- Fitness Goal (Member attribute)
CREATE TABLE FitnessGoal (
    goal_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES Member(member_id) ON DELETE CASCADE,
    goal_type VARCHAR(50) NOT NULL CHECK (goal_type IN ('Weight Loss', 'Weight Gain', 'Body Fat Reduction', 'Muscle Gain', 'Endurance', 'Flexibility')),
    target_value DECIMAL(10, 2),
    current_value DECIMAL(10, 2),
    start_date DATE DEFAULT CURRENT_DATE,
    target_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Completed', 'Cancelled')),
    CONSTRAINT valid_target_date CHECK (target_date > start_date)
);

-- Trainer Availability
CREATE TABLE TrainerAvailability (
    availability_id SERIAL PRIMARY KEY,
    trainer_id INTEGER NOT NULL REFERENCES Trainer(trainer_id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Sunday, 6=Saturday
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CONSTRAINT valid_time_range CHECK (end_time > start_time),
    CONSTRAINT no_overlap_availability UNIQUE (trainer_id, day_of_week, start_time, end_time)
);

-- Room Booking
CREATE TABLE RoomBooking (
    booking_id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES Room(room_id) ON DELETE CASCADE,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    booking_type VARCHAR(20) NOT NULL CHECK (booking_type IN ('PT Session', 'Group Class')),
    reference_id INTEGER NOT NULL, -- References session_id or class_id
    status VARCHAR(20) DEFAULT 'Booked' CHECK (status IN ('Booked', 'Completed', 'Cancelled')),
    CONSTRAINT no_double_booking UNIQUE (room_id, booking_date, booking_time),
    CONSTRAINT valid_booking_date CHECK (booking_date >= CURRENT_DATE)
);

-- Equipment
CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    room_id INTEGER REFERENCES Room(room_id),
    status VARCHAR(20) DEFAULT 'Operational' CHECK (status IN ('Operational', 'Maintenance', 'Out of Order')),
    last_maintenance DATE,
    next_maintenance DATE,
    maintenance_notes TEXT
);

-- Billing
CREATE TABLE Billing (
    bill_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES Member(member_id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    service_type VARCHAR(50) NOT NULL CHECK (service_type IN ('Membership', 'PT Session', 'Group Class', 'Equipment Rental')),
    due_date DATE NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'Pending' CHECK (payment_status IN ('Pending', 'Paid', 'Overdue', 'Cancelled')),
    payment_method VARCHAR(50),
    payment_date DATE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INDEXES
-- ============================================

-- Index on member email for fast lookups (required)
CREATE INDEX idx_member_email ON Member(email);

-- Additional useful indexes
CREATE INDEX idx_session_date ON PersonalTrainingSession(session_date);
CREATE INDEX idx_class_date ON GroupClass(class_date);
CREATE INDEX idx_health_metric_member_date ON HealthMetric(member_id, recorded_date DESC);
CREATE INDEX idx_trainer_availability ON TrainerAvailability(trainer_id, day_of_week);

-- ============================================
-- VIEWS
-- ============================================

-- Member Dashboard View (required)
CREATE VIEW member_dashboard_view AS
SELECT 
    m.member_id,
    m.name,
    m.email,
    -- Latest health metrics
    (SELECT value FROM HealthMetric hm1 
     WHERE hm1.member_id = m.member_id 
     AND hm1.metric_type = 'Weight' 
     ORDER BY recorded_date DESC LIMIT 1) AS latest_weight,
    (SELECT value FROM HealthMetric hm2 
     WHERE hm2.member_id = m.member_id 
     AND hm2.metric_type = 'Heart Rate' 
     ORDER BY recorded_date DESC LIMIT 1) AS latest_heart_rate,
    (SELECT value FROM HealthMetric hm3 
     WHERE hm3.member_id = m.member_id 
     AND hm3.metric_type = 'Body Fat' 
     ORDER BY recorded_date DESC LIMIT 1) AS latest_body_fat,
    -- Active goals count
    (SELECT COUNT(*) FROM FitnessGoal fg 
     WHERE fg.member_id = m.member_id 
     AND fg.status = 'Active') AS active_goals_count,
    -- Past classes count
    (SELECT COUNT(*) FROM ClassRegistration cr
     JOIN GroupClass gc ON cr.class_id = gc.class_id
     WHERE cr.member_id = m.member_id 
     AND gc.class_date < CURRENT_DATE
     AND cr.status = 'Completed') AS past_classes_count,
    -- Upcoming sessions count
    (SELECT COUNT(*) FROM PersonalTrainingSession pts
     WHERE pts.member_id = m.member_id
     AND pts.session_date >= CURRENT_DATE
     AND pts.status = 'Scheduled') AS upcoming_sessions_count
FROM Member m;

-- ============================================
-- TRIGGERS
-- ============================================

-- Function to update class capacity when registration changes (required)
CREATE OR REPLACE FUNCTION update_class_capacity()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Increment enrollment when someone registers
        UPDATE GroupClass 
        SET current_enrollment = current_enrollment + 1
        WHERE class_id = NEW.class_id
        AND current_enrollment < capacity;
        
        -- Check if capacity exceeded
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Class is at full capacity';
        END IF;
        
    ELSIF TG_OP = 'DELETE' THEN
        -- Decrement enrollment when someone cancels
        UPDATE GroupClass 
        SET current_enrollment = current_enrollment - 1
        WHERE class_id = OLD.class_id
        AND current_enrollment > 0;
        
    ELSIF TG_OP = 'UPDATE' THEN
        -- Handle status changes
        IF OLD.status = 'Registered' AND NEW.status = 'Cancelled' THEN
            UPDATE GroupClass 
            SET current_enrollment = current_enrollment - 1
            WHERE class_id = NEW.class_id
            AND current_enrollment > 0;
        ELSIF OLD.status = 'Cancelled' AND NEW.status = 'Registered' THEN
            UPDATE GroupClass 
            SET current_enrollment = current_enrollment + 1
            WHERE class_id = NEW.class_id
            AND current_enrollment < capacity;
            
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Class is at full capacity';
            END IF;
        END IF;
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Trigger on ClassRegistration table
CREATE TRIGGER update_class_capacity_trigger
    AFTER INSERT OR UPDATE OR DELETE ON ClassRegistration
    FOR EACH ROW
    EXECUTE FUNCTION update_class_capacity();
