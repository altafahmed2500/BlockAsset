from django.db import connection

# Disable foreign key checks
with connection.cursor() as cursor:
    cursor.execute("PRAGMA foreign_keys = OFF;")
    cursor.execute("DELETE FROM auth_user WHERE is_superuser = 0;")
    cursor.execute("PRAGMA foreign_keys = ON;")  # Re-enable foreign key checks
