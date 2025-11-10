from supabase import create_client

url = "https://jvvjdirsdlcnpgdtwlog.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp2dmpkaXJzZGxjbnBnZHR3bG9nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI1NDI2MzksImV4cCI6MjA3ODExODYzOX0.-fkbnWlSdMAXjmYW-3EetOTG1t0wmak5zltwcaNFt14"
supabase = create_client(url, key)

print("✅ Conexión lista a Supabase")
