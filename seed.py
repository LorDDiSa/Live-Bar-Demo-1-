import sqlite3, os
DB = os.getenv("DB_PATH", "db.sqlite3")
con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS venues (
  id TEXT PRIMARY KEY, name TEXT, address TEXT,
  lat REAL, lon REAL, capacity INTEGER, rating REAL,
  photo TEXT, seed_occupancy REAL
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  venue_id TEXT, source TEXT, value REAL, created_at REAL
)""")
venues = [
    ("neon","Neon Club","Кунаева 75",43.2430,76.9398,300,4.8,"/static/neon.jpg",0.77),
    ("bar777","Bar 777","Абылай Хана 43",43.2389,76.9450,120,4.5,"/static/bar.jpg",0.75),
    ("oldtown","OldTown Pub","Достык 102",43.2435,76.9390,100,4.6,"/static/pub.jpg",0.65),
    ("coffeelab","CoffeeLab","Панфилова 40",43.2410,76.9275,60,4.4,"/static/cafe.jpg",0.42),
    ("quiet","Quiet Tea","Жибек Жолы 63",43.2422,76.9322,50,4.2,"/static/tea.jpg",0.30),
    ("sky","Sky Lounge","Esentai Mall",43.2377,76.9345,150,4.7,"/static/lounge.jpg",0.53),
    ("vega","Vega Karaoke","Толе би 55",43.2418,76.9495,200,4.1,"/static/karaoke.jpg",0.60)
]
cur.executemany("INSERT OR IGNORE INTO venues VALUES (?,?,?,?,?,?,?,?,?)", venues)
con.commit(); con.close()
print("Seed OK")