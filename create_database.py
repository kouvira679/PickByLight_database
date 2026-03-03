import sqlite3

# Create / connect to database file
conn = sqlite3.connect("pick_by_light.db") # opens connection to the database file
cursor = conn.cursor()  # actually allows the sending of SQL commands 

# ---- TABLE 1: Production Orders ----
cursor.execute("""
CREATE TABLE IF NOT EXISTS Production_Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pcb_required BOOLEAN NOT NULL, 
    pcb_qty INTEGER NOT NULL DEFAULT 1,
    fuse_required INTEGER NOT NULL,
    fuse_qty INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)   
""") # add other required things like fusues, etc

# ---- TABLE 2: Process Data ----
cursor.execute("""
CREATE TABLE IF NOT EXISTS Process_Data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    tag_name TEXT NOT NULL,
    value TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully.")