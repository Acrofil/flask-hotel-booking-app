from booking_engine import app
from meinheld import server


if __name__ == "__main__":
    server.listen(("0.0.0.0", 8000))
    server.run(app)
    