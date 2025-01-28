import vk_api
import config
import logging
import time

# Панель для работы с базой
import panel_db

# Логи
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a", encoding="UTF-8",
                    format="%(asctime)s %(levelname)s %(message)s")

# Подгружаем токен
vk=vk_api.VkApi(token=config.TOKEN)

# Стена
def LikeWall():
    # Поиск по нашей стр последнего поста
    WallGet = vk.method("wall.get",{'count':1})
    LastPost = int(WallGet['items'][0]['id'])

    file_name = f"{LastPost}_wall"
    
    # Создание БД
    panel_db.create(file_name)
    # Установка онлайна
    vk.method("account.setOnline")
    
    # Список из БАЗЫ
    check_list = []
    # Запрос в базу
    logging.info("Запрос в базу")
    search_all = panel_db.search_all(file_name)
    for i in search_all:
        check_list.append(i[0])

    # Сколько лайкнуло на моей записи
    LikesGetList = vk.method("likes.getList",{'type':'post','item_id':LastPost})
    get_list = list(LikesGetList['items'])

    # Перебор
    for ids in get_list:
        if not ids in check_list:
            # Информация о пользователе
            UsersGet = vk.method("users.get",{'user_ids':ids})
            # Проверка открыт ли профиль
            if UsersGet[0]['is_closed']:
                 logging.error(f"Профиль закрыт - {ids}")
                 panel_db.add_user(file_name, ids)
            else:
                # Если профиль открыт то ...
                try:
                    logging.info("Начинаю искать запись")
                    WallGet = vk.method("wall.get",{'owner_id':ids,'count':1})
                    
                    # Проверка на наличие записей на стене
                    if WallGet['count'] > 0:
                        # Проверяет, находится ли объект в списке 'Мне нравится' у меня.
                        LikesGetList = vk.method("likes.isLiked",{'type':'post','owner_id':ids,'item_id':int(WallGet['items'][0]['id'])})
                        # Если нету то ...
                        if LikesGetList['liked'] == 0:
                            LikesAdd = vk.method("likes.add",{'owner_id':ids,'type':'post','item_id':int(WallGet['items'][0]['id'])})
                            logging.info(f"[+] Запись лайкнул - {ids}")
                            panel_db.add_user(file_name, ids)
                        else:
                            logging.info(f"[+] Запись была отмечена - {ids}")
                            panel_db.add_user(file_name, ids)
                    else:
                        logging.info(f"Записей на стене нету - {ids}")
                        panel_db.add_user(file_name, ids)
                    
                except Exception as error:
                    logging.error(error, f"ОШИБКА - {ids}")
                    panel_db.add_user(file_name, ids)

# Ава
def LikeAva():
    # Получение инф об фото которое на аве
    Get_Info_Ava = vk.method('photos.get', {'album_id': 'profile', 'rev': 1, 'extended': 1, 'count': 1})
    # Список людей которые лайкнули
    Like_List = vk.method("likes.getList",{"type":"photo","owner_id":Get_Info_Ava['items'][0]['owner_id'],"item_id":Get_Info_Ava['items'][0]['id']})
    LastPhoto = Get_Info_Ava['items'][0]['id']

    file_name = f"{LastPhoto}_photo"

    # Создание БД
    panel_db.create(file_name)
    # Установка онлайна
    vk.method("account.setOnline")

    # Список из БАЗЫ
    check_list = []
    # Запрос в базу
    search_all = panel_db.search_all(file_name)
    for i in search_all:
        check_list.append(i[0])
    
    check_photo = Like_List['items']
    # перебираем айди
    for ids in check_photo:
        # если нету в базе то ...
        if not ids in check_list:
            try:
                # Информация о пользователе
                Info_User= vk.method("users.get",{"user_ids":ids})
                
                # Если открыт
                if Info_User[0]['can_access_closed'] == True:
                    # Последнее фото
                    Photo_Get= vk.method("photos.get",{"owner_id":Info_User[0]['id'],"album_id":"profile","rev":"1"})
                    ids_photo = (Photo_Get['items'][0]['id'])
                    
                    # Проверяет, находится ли объект в списке 'Мне нравится' у меня.
                    Likes_is_Liked= vk.method("likes.isLiked",{"user_id":755728119,"type":"photo","owner_id":ids,"item_id":ids_photo})
                    # Если нету то ...
                    if Likes_is_Liked['liked'] == 0:
                        Likes_Add= vk.method("likes.add",{"type":"photo","owner_id":ids,"item_id":ids_photo})
                        logging.info(f"[##] Понравилось фото - {Info_User[0]['first_name']} {Info_User[0]['last_name']}")
                        panel_db.add_user(file_name, ids)
                        time.sleep(5)
                    else:
                        logging.info(f"[##] Фото уже было отмечено - {Info_User[0]['first_name']} {Info_User[0]['last_name']}")
                        panel_db.add_user(file_name, ids)
                else:
                    logging.info(f"Страница закрыта - {Info_User[0]['first_name']} {Info_User[0]['last_name']}")
                    panel_db.add_user(file_name, ids)
            
            except Exception as error:
                logging.error(error, f"ОШИБКА - {ids}")
                panel_db.add_user(file_name, ids)

# Создание записи на стене в группе для ЛАЙКОВ
def create_comment_group(text):
    print("[#] Рассылка в группы")
    
    for ids_group in config.GROUP_IDS_LIKE:
        WallPost = vk.method("wall.post",{'owner_id':ids_group,'message':text})
        logging.info(f"[+] Оставил запись в группе: {ids_group}")
        time.sleep(5)
    
    print("[#] Рассылку закончил")