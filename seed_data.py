# Seed data for School Attendance System
# Creates sample data: 1 admin, 1 principal, 5 teachers, 8 classes, 160 students

from database import init_db, execute_query, execute_insert
from auth import hash_password


def seed_database():
    """Seed the database with sample data."""

    # Check if data already exists
    existing_users = execute_query("SELECT COUNT(*) as count FROM users")
    if existing_users[0]['count'] > 0:
        print("Database already seeded. Skipping...")
        return

    print("Seeding database with sample data...")

    # Create users
    admin_id = create_user("admin", "school123", "admin", "Admin User", "منتظم")
    principal_id = create_user("principal", "school123", "principal", "Principal", "پرنسپل")

    # Create 5 teachers
    teacher_ids = []
    for i in range(1, 6):
        teacher_id = create_user(
            f"teacher{i}",
            "school123",
            "teacher",
            f"Teacher {i}",
            f"استاد {i}"
        )
        teacher_ids.append(teacher_id)

    print(f"Created {len(teacher_ids) + 2} users (1 admin, 1 principal, 5 teachers)")

    # Create 8 classes
    classes = [
        ("6-A", "چھٹی الف"),
        ("6-B", "چھٹی ب"),
        ("7-A", "ساتویں الف"),
        ("7-B", "ساتویں ب"),
        ("8-A", "آٹھویں الف"),
        ("8-B", "آٹھویں ب"),
        ("9-A", "نویں الف"),
        ("10-A", "دسویں الف"),
    ]

    class_ids = []
    for i, (class_name, class_name_ur) in enumerate(classes):
        # Assign teacher to class (first 5 classes get teachers)
        teacher_id = teacher_ids[i] if i < len(teacher_ids) else None
        class_id = execute_insert(
            "INSERT INTO classes (name, name_ur, teacher_id) VALUES (?, ?, ?)",
            (class_name, class_name_ur, teacher_id)
        )
        class_ids.append(class_id)

    print(f"Created {len(class_ids)} classes")

    # Create 20 students per class (160 total)
    student_count = 0
    for class_id, (class_name, _) in zip(class_ids, classes):
        for roll_no in range(1, 21):
            student_name = f"Student {class_name}-{roll_no:02d}"
            student_name_ur = f"طالب علم {class_name}-{roll_no:02d}"
            parent_phone = f"0300-{1000000 + student_count:07d}"

            execute_insert(
                "INSERT INTO students (name_en, name_ur, roll_no, class_id, parent_phone) VALUES (?, ?, ?, ?, ?)",
                (student_name, student_name_ur, f"{roll_no:02d}", class_id, parent_phone)
            )
            student_count += 1

    print(f"Created {student_count} students (20 per class)")
    print("\nSample credentials:")
    print("  Admin:     username='admin',     password='school123'")
    print("  Principal: username='principal', password='school123'")
    print("  Teachers:  username='teacher1-5', password='school123'")
    print("\nDatabase seeding complete!")


def create_user(username, password, role, name_en, name_ur=None):
    """Create a user with hashed password."""
    hashed = hash_password(password)
    return execute_insert(
        "INSERT INTO users (username, password, role, name_en, name_ur) VALUES (?, ?, ?, ?, ?)",
        (username, hashed, role, name_en, name_ur)
    )


if __name__ == "__main__":
    # Initialize database schema
    init_db()

    # Seed with sample data
    seed_database()
