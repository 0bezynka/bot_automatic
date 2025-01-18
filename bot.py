from config import *
import addons
import time

VERSION = "beta 0.1"

def main():
    while True:
        print("[#] Старт ...")
        # Стена
        print("FLAG_WALL - ", FLAG_WALL)
        if FLAG_WALL:
            print("[ Стена ]")
            addons.create_comment_group(TEXT_WALL)
            print("Тайм-аут:", TIMEOUT)
            time.sleep(TIMEOUT)
            addons.LikeWall()
        
        # Ава
        print("FLAG_AVA -", FLAG_AVA)
        if FLAG_AVA:
            print("[ Ава ]")
            addons.create_comment_group(TEXT_AVA)
            print("Тайм-аут:", TIMEOUT)
            time.sleep(TIMEOUT)
            addons.LikeAva()
        
        print("[#] Сон:", TIME_SLEEP)
        time.sleep(TIME_SLEEP)

if __name__ == "__main__":
    main()