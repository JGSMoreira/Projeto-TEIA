import dotenv
import os

dotenv.load_dotenv()

print(os.getenv('OPEN_SUBTITLES_API_KEY'))