import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os

token = os.environ.get('TOKEN')
group_id = os.environ.get('GROUP_ID')
my_name = os.environ.get('NAME')

vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id)


def send_message(peer_id, random_id, msg):
    vk.method('messages.send', {
        'peer_id': peer_id,
        'random_id': random_id,
        'message': msg
    })


def remove_user(peer_id, user_id):
    vk.method('messages.removeChatUser', {
        'chat_id': peer_id - 2000000000,
        'user_id': user_id
    })


def get_user_name_by_id(user_id):
    response = vk.method('users.get', {
        'user_ids': user_id
    })[0]
    return response['first_name'] + ' ' + response['last_name']


commands = ['votekick','respect', 'clearvotekick', 'help', 'kick', 'addkickpermission', 'removekickpermission']
votekick_list = dict()
votekick_list_ofVOTES = dict()
respect_list = dict()
who_can_kick = [my_name]
max_num = 3


def addkickpermission(message):
    text = message['text']
    text = text[1:len(text)]
    from_id = message['from_id']
    peer_id = message['peer_id']
    random_id = message['random_id']
    if get_user_name_by_id(from_id) == my_name:
        parts = text.split(' ')
        user_id = ''.join(parts[1:len(parts)])
        if user_id[0] == '[' and user_id[-1] == ']':
            user_id = user_id.split('|')[0]
            user_id = user_id[3:len(user_id)]
            who_can_kick.append(get_user_name_by_id(int(user_id)))
            send_message(peer_id, random_id, str(who_can_kick[-1])+' - дано разрешение на /kick')
        else:
            send_message(peer_id, random_id, 'Неверный ввод пользователя')
    else:
        send_message(peer_id, random_id, 'У вас нет прав')


def removekickpermission(message):
    text = message['text']
    text = text[1:len(text)]
    from_id = message['from_id']
    peer_id = message['peer_id']
    random_id = message['random_id']
    if get_user_name_by_id(from_id) == my_name:
        parts = text.split(' ')
        user_id = ''.join(parts[1:len(parts)])
        if user_id[0] == '[' and user_id[-1] == ']':
            user_id = user_id.split('|')[0]
            user_id = user_id[3:len(user_id)]
            name = get_user_name_by_id(int(user_id))
            if name in who_can_kick:
                who_can_kick.remove(name)
            send_message(peer_id, random_id, name+' - забрано разрешение на /kick')
        else:
            send_message(peer_id, random_id, 'Неверный ввод пользователя')
    else:
        send_message(peer_id, random_id, 'У вас нет прав')


def kick(message):
    text = message['text']
    text = text[1:len(text)]
    from_id = message['from_id']
    peer_id = message['peer_id']
    random_id = message['random_id']
    if get_user_name_by_id(from_id) in who_can_kick:
        parts = text.split(' ')

        user_id = ''.join(parts[1:len(parts)])
        if user_id[0] == '[' and user_id[-1] == ']':
            user_id = user_id.split('|')[0]
            user_id = user_id[3:len(user_id)]
            remove_user(peer_id, int(user_id))
        else:
            send_message(peer_id, random_id, 'Неверный ввод пользователя')
    else:
        send_message(peer_id, random_id, 'У вас нет прав')


def help(message):
    text = message['text']
    text = text[1:len(text)]
    from_id = message['from_id']
    peer_id = message['peer_id']
    random_id = message['random_id']
    send_message(peer_id, random_id, 'Команды:\n' + '\n'.join(map(lambda x: '\t/' + x, commands)))


def clearvotekick(message):
    text = message['text']
    text = text[1:len(text)]
    from_id = message['from_id']
    peer_id = message['peer_id']
    random_id = message['random_id']

    if get_user_name_by_id(from_id) == my_name:
        votekick_list_ofVOTES.clear()
        votekick_list.clear()
        send_message(peer_id, random_id, "Список голосования очищен")
    else:
        send_message(peer_id, random_id, "У вас нет прав")


def votekick(message):
    text = message['text']
    text = text[1:len(text)]
    from_id = message['from_id']
    peer_id = message['peer_id']
    random_id = message['random_id']
    parts = text.split(' ')

    user_id = ''.join(parts[1:len(parts)])
    if user_id[0] == '[' and user_id[-1] == ']':
        user_id = user_id.split('|')[0]
        user_id = user_id[3:len(user_id)]
    else:
        user_id = ''

    if user_id == '':
        send_message(peer_id, random_id, 'Неверный ввод пользователя')
    else:
        need_send = True
        user_id = int(user_id)
        name = get_user_name_by_id(user_id)

        if name == my_name:
            send_message(peer_id, random_id, 'Создателя не трогай! Вот твое наказание')
            user_id = from_id
            name = get_user_name_by_id(user_id)

        if user_id in votekick_list.keys():
            if from_id not in votekick_list_ofVOTES[user_id]:
                votekick_list_ofVOTES[user_id].append(from_id)
                votekick_list[user_id] += 1
            else:
                need_send = False
        else:
            votekick_list[user_id] = 1
            votekick_list_ofVOTES[user_id] = [from_id]

        if user_id == from_id:
            send_message(peer_id, random_id, 'Ты дурак?'
                         )
        if need_send:
            send_message(peer_id,
                         random_id,
                         name + ' ' + str(votekick_list[user_id]) + '/' + str(max_num) + ' на исключение')
        if votekick_list[user_id] == max_num:
            remove_user(peer_id, user_id)
            votekick_list.pop(user_id)


def respect(message):
    text = message['text']
    text = text[1:len(text)]
    from_id = message['from_id']
    peer_id = message['peer_id']
    random_id = message['random_id']
    parts = text.split(' ')

    user_id = ''.join(parts[1:len(parts)])
    if user_id[0] == '[' and user_id[-1] == ']':
        user_id = user_id.split('|')[0]
        user_id = user_id[3:len(user_id)]
    else:
        user_id = ''

    if user_id == '':
        send_message(peer_id, random_id, 'Неверный ввод пользователя')
    else:
        user_id = int(user_id)
        name = get_user_name_by_id(user_id)

        if user_id == from_id:
            send_message(peer_id, random_id, 'Нарцисс чертов! А ну пошел вон')
            votekick(message)
        else:
            if user_id in respect_list.keys():
                respect_list[user_id] += 1
            else:
                respect_list[user_id] = 1

            send_message(peer_id,
                         random_id,
                         name + ' ' + str(respect_list[user_id]) + ' уважуха_score')


def command_parser(message):
    text = message['text']
    text = text[1:len(text)]
    peer_id = message['peer_id']
    random_id = message['random_id']
    command = text.split(' ')[0]
    if command in commands:
        if command == 'votekick':
            votekick(message)
        elif command == 'clearvotekick':
            clearvotekick(message)
        elif command == 'help':
            help(message)
        elif command == 'respect':
            respect(message)
        elif command == 'addkickpermission':
            addkickpermission(message)
        elif command == 'kick':
            kick(message)
        elif command == 'removekickpermission':
            removekickpermission(message)
    else:
        send_message(peer_id, random_id, 'Неверная команда')


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            try:
                if '/' == event.obj['message']['text'][0]:
                    command_parser(event.obj['message'])
            except IndexError:
                print('INDEX ERROR')


if __name__ == '__main__':
    main()
