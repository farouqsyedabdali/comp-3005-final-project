-- Health and Fitness Club Management System
-- DML.sql - Sample Data

-- ============================================
-- MEMBERS (5+ members)
-- ============================================

INSERT INTO Member (name, email, date_of_birth, gender, phone, address) VALUES
('John Smith', 'john.smith@email.com', '1990-05-15', 'Male', '613-555-0101', '123 Main St, Ottawa, ON'),
('Sarah Johnson', 'sarah.j@email.com', '1988-08-22', 'Female', '613-555-0102', '456 Oak Ave, Ottawa, ON'),
('Mike Chen', 'mike.chen@email.com', '1992-11-30', 'Male', '613-555-0103', '789 Pine Rd, Ottawa, ON'),
('Emily Davis', 'emily.davis@email.com', '1995-03-10', 'Female', '613-555-0104', '321 Elm St, Ottawa, ON'),
('David Wilson', 'david.w@email.com', '1987-07-18', 'Male', '613-555-0105', '654 Maple Dr, Ottawa, ON'),
('Lisa Anderson', 'lisa.a@email.com', '1993-12-05', 'Female', '613-555-0106', '987 Cedar Ln, Ottawa, ON');

-- ============================================
-- TRAINERS (3+ trainers)
-- ============================================

INSERT INTO Trainer (name, email, specialization, phone) VALUES
('Alex Martinez', 'alex.m@fitness.com', 'Strength Training', '613-555-0201'),
('Jessica Brown', 'jessica.b@fitness.com', 'Yoga & Flexibility', '613-555-0202'),
('Chris Taylor', 'chris.t@fitness.com', 'Cardio & Endurance', '613-555-0203'),
('Morgan Lee', 'morgan.l@fitness.com', 'HIIT & CrossFit', '613-555-0204');

-- ============================================
-- ADMIN (1+ admin)
-- ============================================

INSERT INTO Admin (name, email, phone) VALUES
('Admin User', 'admin@fitness.com', '613-555-0001'),
('Manager Smith', 'manager@fitness.com', '613-555-0002');

-- ============================================
-- ROOMS
-- ============================================

INSERT INTO Room (room_name, capacity, equipment_list, status) VALUES
('Studio A', 30, 'Mats, Weights, Resistance Bands', 'Available'),
('Studio B', 25, 'Treadmills, Bikes, Rowing Machines', 'Available'),
('Training Room 1', 5, 'Bench Press, Dumbbells, Squat Rack', 'Available'),
('Training Room 2', 5, 'Cable Machine, Free Weights', 'Available'),
('Yoga Studio', 20, 'Yoga Mats, Blocks, Straps', 'Available');

-- ============================================
-- EQUIPMENT
-- ============================================

INSERT INTO Equipment (equipment_name, room_id, status, last_maintenance, next_maintenance) VALUES
('Treadmill #1', 2, 'Operational', '2025-10-01', '2026-01-01'),
('Treadmill #2', 2, 'Maintenance', '2025-09-15', '2025-12-15'),
('Bench Press Station', 3, 'Operational', '2025-11-01', '2026-02-01'),
('Cable Machine', 4, 'Out of Order', '2025-08-20', NULL),
('Rowing Machine #1', 2, 'Operational', '2025-10-15', '2026-01-15');

-- ============================================
-- TRAINER AVAILABILITY
-- ============================================

-- Alex Martinez: Monday-Friday, 9 AM - 5 PM
INSERT INTO TrainerAvailability (trainer_id, day_of_week, start_time, end_time) VALUES
(1, 1, '09:00:00', '17:00:00'), -- Monday
(1, 2, '09:00:00', '17:00:00'), -- Tuesday
(1, 3, '09:00:00', '17:00:00'), -- Wednesday
(1, 4, '09:00:00', '17:00:00'), -- Thursday
(1, 5, '09:00:00', '17:00:00'); -- Friday

-- Jessica Brown: Monday, Wednesday, Friday, 10 AM - 6 PM
INSERT INTO TrainerAvailability (trainer_id, day_of_week, start_time, end_time) VALUES
(2, 1, '10:00:00', '18:00:00'), -- Monday
(2, 3, '10:00:00', '18:00:00'), -- Wednesday
(2, 5, '10:00:00', '18:00:00'); -- Friday

-- Chris Taylor: Tuesday-Thursday, 8 AM - 4 PM; Saturday 9 AM - 1 PM
INSERT INTO TrainerAvailability (trainer_id, day_of_week, start_time, end_time) VALUES
(3, 2, '08:00:00', '16:00:00'), -- Tuesday
(3, 3, '08:00:00', '16:00:00'), -- Wednesday
(3, 4, '08:00:00', '16:00:00'), -- Thursday
(3, 6, '09:00:00', '13:00:00'); -- Saturday

-- Morgan Lee: Monday-Friday, 12 PM - 8 PM
INSERT INTO TrainerAvailability (trainer_id, day_of_week, start_time, end_time) VALUES
(4, 1, '12:00:00', '20:00:00'), -- Monday
(4, 2, '12:00:00', '20:00:00'), -- Tuesday
(4, 3, '12:00:00', '20:00:00'), -- Wednesday
(4, 4, '12:00:00', '20:00:00'), -- Thursday
(4, 5, '12:00:00', '20:00:00'); -- Friday

-- ============================================
-- FITNESS GOALS
-- ============================================

INSERT INTO FitnessGoal (member_id, goal_type, target_value, current_value, start_date, target_date, status) VALUES
(1, 'Weight Loss', 75.0, 85.0, '2025-10-01', '2026-03-01', 'Active'),
(1, 'Body Fat Reduction', 15.0, 22.0, '2025-10-01', '2026-04-01', 'Active'),
(2, 'Muscle Gain', 65.0, 60.0, '2025-09-15', '2026-02-15', 'Active'),
(3, 'Endurance', NULL, NULL, '2025-11-01', '2026-05-01', 'Active'),
(4, 'Weight Loss', 60.0, 68.0, '2025-10-20', '2026-04-20', 'Active'),
(5, 'Flexibility', NULL, NULL, '2025-09-01', '2026-03-01', 'Active');

-- ============================================
-- HEALTH METRICS (Historical data)
-- ============================================

-- John Smith's metrics
INSERT INTO HealthMetric (member_id, metric_type, value, recorded_date) VALUES
(1, 'Weight', 88.0, '2025-10-01 08:00:00'),
(1, 'Weight', 86.5, '2025-10-15 08:00:00'),
(1, 'Weight', 85.0, '2025-11-01 08:00:00'),
(1, 'Heart Rate', 72.0, '2025-11-01 08:00:00'),
(1, 'Body Fat', 24.0, '2025-10-01 08:00:00'),
(1, 'Body Fat', 22.5, '2025-11-01 08:00:00'),
(1, 'BMI', 26.5, '2025-11-01 08:00:00');

-- Sarah Johnson's metrics
INSERT INTO HealthMetric (member_id, metric_type, value, recorded_date) VALUES
(2, 'Weight', 60.0, '2025-09-15 09:00:00'),
(2, 'Weight', 61.0, '2025-10-15 09:00:00'),
(2, 'Weight', 61.5, '2025-11-15 09:00:00'),
(2, 'Heart Rate', 68.0, '2025-11-15 09:00:00'),
(2, 'Body Fat', 18.0, '2025-11-15 09:00:00');

-- Mike Chen's metrics
INSERT INTO HealthMetric (member_id, metric_type, value, recorded_date) VALUES
(3, 'Weight', 75.0, '2025-11-01 10:00:00'),
(3, 'Heart Rate', 75.0, '2025-11-01 10:00:00'),
(3, 'BMI', 23.0, '2025-11-01 10:00:00');

-- Emily Davis's metrics
INSERT INTO HealthMetric (member_id, metric_type, value, recorded_date) VALUES
(4, 'Weight', 70.0, '2025-10-20 11:00:00'),
(4, 'Weight', 68.5, '2025-11-20 11:00:00'),
(4, 'Heart Rate', 70.0, '2025-11-20 11:00:00'),
(4, 'Body Fat', 25.0, '2025-10-20 11:00:00'),
(4, 'Body Fat', 23.5, '2025-11-20 11:00:00');

-- David Wilson's metrics
INSERT INTO HealthMetric (member_id, metric_type, value, recorded_date) VALUES
(5, 'Weight', 82.0, '2025-09-01 12:00:00'),
(5, 'Heart Rate', 74.0, '2025-09-01 12:00:00');

-- ============================================
-- GROUP CLASSES
-- ============================================

INSERT INTO GroupClass (class_name, trainer_id, class_date, class_time, duration_minutes, capacity, current_enrollment, room_id, status) VALUES
('Morning Yoga', 2, '2025-12-05', '08:00:00', 60, 20, 5, 5, 'Scheduled'),
('HIIT Bootcamp', 4, '2025-12-05', '18:00:00', 45, 25, 8, 1, 'Scheduled'),
('Cardio Blast', 3, '2025-12-06', '09:00:00', 50, 30, 12, 2, 'Scheduled'),
('Strength Training', 1, '2025-12-06', '14:00:00', 60, 20, 3, 1, 'Scheduled'),
('Evening Yoga', 2, '2025-12-07', '19:00:00', 60, 20, 7, 5, 'Scheduled'),
('CrossFit Challenge', 4, '2025-12-08', '17:00:00', 60, 25, 15, 1, 'Scheduled');

-- ============================================
-- CLASS REGISTRATIONS
-- ============================================

INSERT INTO ClassRegistration (member_id, class_id, registration_date, status) VALUES
(1, 1, '2025-11-20 10:00:00', 'Registered'),
(2, 1, '2025-11-18 14:00:00', 'Registered'),
(3, 2, '2025-11-22 09:00:00', 'Registered'),
(4, 2, '2025-11-21 11:00:00', 'Registered'),
(1, 3, '2025-11-25 08:00:00', 'Registered'),
(2, 3, '2025-11-24 15:00:00', 'Registered'),
(5, 4, '2025-11-23 10:00:00', 'Registered'),
(6, 5, '2025-11-26 12:00:00', 'Registered'),
(1, 5, '2025-11-27 09:00:00', 'Registered'),
(3, 6, '2025-11-28 10:00:00', 'Registered');

-- ============================================
-- PERSONAL TRAINING SESSIONS
-- ============================================

INSERT INTO PersonalTrainingSession (member_id, trainer_id, session_date, session_time, duration_minutes, status, room_id, notes) VALUES
(1, 1, '2025-12-05', '10:00:00', 60, 'Scheduled', 3, 'Focus on weight loss program'),
(2, 1, '2025-12-05', '14:00:00', 60, 'Scheduled', 3, 'Muscle building session'),
(3, 3, '2025-12-06', '10:00:00', 60, 'Scheduled', 4, 'Cardio training'),
(4, 2, '2025-12-07', '11:00:00', 60, 'Scheduled', 5, 'Yoga and flexibility'),
(5, 4, '2025-12-08', '13:00:00', 60, 'Scheduled', 1, 'HIIT workout'),
(1, 1, '2025-12-10', '10:00:00', 60, 'Scheduled', 3, 'Follow-up session');

-- ============================================
-- ROOM BOOKINGS
-- ============================================

INSERT INTO RoomBooking (room_id, booking_date, booking_time, booking_type, reference_id, status) VALUES
(3, '2025-12-05', '10:00:00', 'PT Session', 1, 'Booked'),
(3, '2025-12-05', '14:00:00', 'PT Session', 2, 'Booked'),
(4, '2025-12-06', '10:00:00', 'PT Session', 3, 'Booked'),
(5, '2025-12-05', '08:00:00', 'Group Class', 1, 'Booked'),
(1, '2025-12-05', '18:00:00', 'Group Class', 2, 'Booked'),
(2, '2025-12-06', '09:00:00', 'Group Class', 3, 'Booked'),
(1, '2025-12-06', '14:00:00', 'Group Class', 4, 'Booked'),
(5, '2025-12-07', '19:00:00', 'Group Class', 5, 'Booked'),
(1, '2025-12-08', '17:00:00', 'Group Class', 6, 'Booked'),
(5, '2025-12-07', '11:00:00', 'PT Session', 4, 'Booked'),
(1, '2025-12-08', '13:00:00', 'PT Session', 5, 'Booked'),
(3, '2025-12-10', '10:00:00', 'PT Session', 6, 'Booked');

-- ============================================
-- BILLING
-- ============================================

INSERT INTO Billing (member_id, amount, service_type, due_date, payment_status, payment_method, payment_date) VALUES
(1, 99.99, 'Membership', '2025-12-01', 'Paid', 'Credit Card', '2025-11-28'),
(2, 99.99, 'Membership', '2025-12-01', 'Paid', 'Debit Card', '2025-11-29'),
(3, 99.99, 'Membership', '2025-12-01', 'Pending', NULL, NULL),
(4, 99.99, 'Membership', '2025-12-01', 'Paid', 'Credit Card', '2025-11-30'),
(5, 99.99, 'Membership', '2025-12-01', 'Overdue', NULL, NULL),
(1, 75.00, 'PT Session', '2025-12-05', 'Pending', NULL, NULL),
(2, 75.00, 'PT Session', '2025-12-05', 'Pending', NULL, NULL),
(1, 25.00, 'Group Class', '2025-12-05', 'Paid', 'Credit Card', '2025-11-20'),
(2, 25.00, 'Group Class', '2025-12-05', 'Paid', 'Debit Card', '2025-11-18');

