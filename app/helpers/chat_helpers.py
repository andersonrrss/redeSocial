from app.models import db, Chat, Message, User

def get_messages_for_chat(chat_id, user_id):
    chat = Chat.query.get(chat_id)
    if chat.user1_id == user_id:
        # Retorna apenas as mensagens que não foram deletadas pelo usuário 1
        return Message.query.filter(
        (Message.chat_id == chat_id) & (Message.user1_deleted == False)
        ).all()
    elif chat.user2_id == user_id:
        # Retorna apenas as mensagens que não foram deletadas pelo usuário 2
        return Message.query.filter(
        (Message.chat_id == chat_id) & (Message.user2_deleted == False)
        ).all()
    
def delete_chat_for_user(chat_id, user_id):
    chat = Chat.query.get(chat_id) #id do chat
    messages = Message.query.filter_by(chat_id=chat_id).all() # mensagens do chat
    # Deleta o chat para o usuário que quis deletá-lo
    if chat.user1_id == user_id:
        chat.user1_deleted = True
        # Deleta todas as mensagens do chat para o usuário 1
        for message in messages:
            message.user1_deleted = True
    elif chat.user2_id == user_id:
        chat.user2_deleted = True
        # Deleta todas as mensagens do chat para o usuário 2
        for message in messages:
            message.user2_deleted = True

    if chat.user1_deleted and chat.user2_deleted:
        # Se ambos os usuários excluíram o chat, exclua o chat e suas mensagens
        Message.query.filter_by(chat_id=chat_id).delete()
        Chat.query.filter_by(id=chat_id).delete()
        db.session.delete(chat)
    db.session.commit()


def format_chat_data(chat, receiver_id):
    receiver = User.query.get(receiver_id)
    # Organiza as informações
    return {
        "id": chat.id,
        "receiver": {
            "name": receiver.name,
            "profile_pic": receiver.profile_pic
        },
    }

def send_message_notification(message, receiver, sender, responded_message_content, responded_message_id):
    from app import socketio

    message_data = {
            "message_id": message.id,
            "content": message.message,
            "chat_id": message.chat_id,
            "sender_id": sender.id,
            "sender_name": sender.name,
            "timestamp": message.timestamp.isoformat(),
            "responded_message_content": responded_message_content,
            "responded_message_id": responded_message_id
        }
       
    # Emite a notificação
    socketio.emit("new-message", message_data, room=receiver.socket_id)