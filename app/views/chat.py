from flask import Blueprint, session, render_template, request, redirect, jsonify
from datetime import datetime
from app.helpers import login_required, error, get_messages_for_chat, delete_chat_for_user, format_chat_data, send_message_notification
from app.models import db, Chat, User, Follower, Message

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat")
@login_required
def chat():
    user_id = session.get("user_id")
    chats = []

    try:
        # Consulta para obter os chats em que o usuário está envolvido
        chats_results = Chat.query.filter(
            (Chat.user1_id == user_id) & (Chat.user1_deleted == False) |
            (Chat.user2_id == user_id) & (Chat.user2_deleted == False)
        ).all()
        # Armazena os ids de perfis que tenham chat vinculado com o usuário
        # Para garantir que o usuario não vai aparecer nas sugestões
        chat_user_ids = set() 

        if chats_results:        
            # Itera pelas conversas do usuário para a organização das informações e fazer com que elas sejam carregadas corretamente na página
            for chat in chats_results:
                receiver_id = chat.user1_id if chat.user2_id == user_id else chat.user2_id # O usuário que eu quero contatar
                chat_user_ids.add(receiver_id) # Armazena os ids dos perfis que já possuem um chat vinculado com o usuário
                chats.append(format_chat_data(chat, user_id))

        # Pega seguidos do usuário para usar como sugestão e formata em uma lista
        following_ids = [followed.followed_id for followed in Follower.query.filter_by(follower_id=user_id).limit(15).all()]

        sugestions = []
        if following_ids:
            following_ids = [fid for fid in following_ids if fid not in chat_user_ids] # Exclui IDs dos usuários que já possuem um chat com o usuário atual
            result = User.query.filter(User.id.in_(following_ids)).all() # Solicita as informações necessárias dos usuários
            sugestions = result

    except Exception as e:
        # Retorna uma resposta de erro
        return error(f"Erro ao carregar chats: {str(e)}", 500)
    
    return render_template("chat/chat.html", chats=chats, sugestions=sugestions)

@chat_bp.route("/newchat")
@login_required
def newchat():
    user_id = session.get("user_id")
    receiver_id = request.args.get("receiver")

    chat = Chat.query.filter(
        (Chat.user1_id == user_id ) & (Chat.user2_id == receiver_id ) |
        (Chat.user1_id == receiver_id ) & (Chat.user2_id == user_id )
    ).first()

    if chat is not None:
        chat.user1_deleted = False
        chat.user2_deleted = False
    else:
        new_chat = Chat(user1_id=user_id, user2_id=receiver_id)
        db.session.add(new_chat)

    db.session.commit()

    try: 
        chat_id = new_chat.id
    except:
        chat_id = chat.id

    return redirect(f"/chat/{chat_id}")


@chat_bp.route("/chat/<chat_id>")
@login_required
def chat_messages(chat_id):
    chat = Chat.query.filter_by(id=chat_id).first()
    user_id = session.get("user_id")

    if not chat:
        return error("Falha ao carregar conversa", 404)
    if chat.user1_id == user_id:
        receiver = User.query.filter_by(id=chat.user2_id).first()
    else:
        receiver = User.query.filter_by(id=chat.user1_id).first()

    # Usuário que vai receber minhas mensagens
    receiver = {
        "id": receiver.id,
        "socket_id": receiver.socket_id,
        "name": receiver.name,
        "profile_pic": receiver.profile_pic,
    }

    messages_result = get_messages_for_chat(chat_id, user_id)
    messages = []
    new_messages = []

    for message in messages_result:
        responded_message = Message.query.get(message.responded_message_id)
        
        message_data = {
            "timestamp":message.timestamp, 
            "content":message.message, 
            "sender_id":message.sender_id, 
            "message_id":message.id, 
            "responded_message_content": responded_message.message if responded_message else None,
            "responded_message_id": message.responded_message_id,
            "received": False
        }

        if message.sender_id == session.get("user_id"):
            message.received = True

        if message.view:
            # Organiza as mensagens não lidas
            messages.append(message_data)
            continue
        
        if message.sender_id == receiver["id"]:
            # Organiza as mensagens não lidas
            new_messages.append(message_data)
            message.view = True # Atualizar o campo view para True nas mensagens novas
        else: 
            # Mensagens enviadas por mim
            messages.append(message_data)
    db.session.commit()

    chat = {
        "id": chat_id,
        "messages": messages,
        "new_messages": new_messages
    }

    return render_template("chat/message.html", receiver=receiver, chat=chat)


@chat_bp.route("/deletechat", methods=["POST"])
@login_required
def delete_chat():
    chat_id = request.form.get("chat_id")
    user_id = session.get("user_id")
    if chat_id and user_id:
        delete_chat_for_user(chat_id, user_id)
        return redirect("/chat")
    else:
        return error("Algo deu errado", 500)
    

@chat_bp.route("/sendmessage")
@login_required
def send_message():
    chat_id = request.args.get("chat_id")
    receiver_id = request.args.get("receiver_id")
    sender_id = session.get("user_id")
    message_content = request.args.get("message")

    try: 
        responded_message_id = int(request.args.get("responded_message_id")) 
    except: 
        responded_message_id = 0

    new_message = Message(
        chat_id= chat_id,
        sender_id= sender_id,
        receiver_id= receiver_id,
        message= message_content,
        responded_message_id= responded_message_id,
        timestamp= datetime.now()
    )
    chat = Chat.query.get(chat_id)
    # Se algum usuário deletou o chat então ele será mostrado novamente
    if chat.user1_deleted:
        chat.user1_deleted = False

    if chat.user2_deleted:
        chat.user2_deleted = False
        
    db.session.add(new_message)
    db.session.commit()

    result = Message.query.filter_by(id=responded_message_id).first()
    responded_message_content = None
    if result:
        responded_message_content = result.message

    receiver = User.query.filter_by(id=receiver_id).first()
    sender = User.query.filter_by(id=new_message.sender_id).with_entities(User.id, User.name).first()
    # Organiza as informações
    if receiver.socket_id:
        send_message_notification(new_message, receiver, sender, responded_message_content, responded_message_id)

    return jsonify({"content":message_content, "message_id": new_message.id, "responded_message_content": responded_message_content, "responded_message_id": responded_message_id})

@chat_bp.route("/messageviewed")
@login_required
def message_viewed():
    message_id = request.args.get("message_id")
    message = Message.query.filter_by(id=message_id).first()
    message.view = True
    db.session.commit()
    return "message view"