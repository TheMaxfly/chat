

# # def chat(request):
# #     messages = Message.objects.all().order_by('timestamp')
# #     return render(request, 'chat/chat.html', {'messages': messages})

# # def send_message(request):
# #     if request.method == 'POST':
# #         sender = request.POST.get('sender')
# #         receiver = request.POST.get('receiver')
# #         content = request.POST.get('content')
# #         message = Message.objects.create(sender=sender, receiver=receiver, content=content)
# #         return JsonResponse({'status': 'success', 'message_id': message.id})
# #     return JsonResponse({'status': 'error'})

# from django.shortcuts import render, get_object_or_404, redirect
# from django.utils import timezone
# from django.contrib.auth.decorators import login_required
# from .models import TemporaryConversation, Message
# from .forms import MessageForm
# from django.contrib.auth.models import User
# from django.utils.crypto import get_random_string
# import uuid


# @login_required
# def index(request):
#     return redirect('chat:advisor_list')



# @login_required
# def index(request):
#     # Rediriger vers une page spécifique, comme la liste des conseillers ou une page d'accueil
#     return redirect('chat:start_conversation', advisor_id=1)  # Remplacez 1 par l'ID d'un conseiller valide

# @login_required
# def chat_window(request):
#     return render(request, 'chat/chat_window.html')







# @login_required
# def start_conversation(request, advisor_id):
#     advisor = get_object_or_404(User, id=advisor_id, is_superuser=False, profile__is_advisor=True)
    
#     # Vérifiez si une conversation existe déjà entre le client et le conseiller
#     conversation = TemporaryConversation.objects.filter(
#         client=request.user,
#         advisor=advisor,
#         expires_at__gt=timezone.now()
#     ).first()
    
#     if not conversation:
#         # Créez une nouvelle conversation si aucune n'existe
#         conversation_name = f"conversation_{uuid.uuid4()}"
#         conversation = TemporaryConversation.objects.create(
#             name=conversation_name,
#             client=request.user,
#             advisor=advisor,
#             expires_at=timezone.now() + timezone.timedelta(hours=1)  # Conversation expire après 1 heure
#         )
    
#     return redirect('chat:conversation_detail', conversation_id=conversation.id)

# @login_required
# def conversation_detail(request, conversation_id):
#     conversation = get_object_or_404(TemporaryConversation, id=conversation_id)
#     if request.user != conversation.client and request.user != conversation.advisor:
#         return redirect('chat:advisor_list')  # Rediriger si l'utilisateur n'est pas autorisé

#     messages = conversation.messages.order_by('timestamp')
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.conversation = conversation
#             message.save()
#             return redirect(request.path)
#     else:
#         form = MessageForm()

#     return render(request, 'chat/conversation_detail.html', {
#         'conversation': conversation,
#         'messages': messages,
#         'form': form,
#         'room_name': conversation.name,  # Assurez-vous de passer le nom de la salle au template
#     })
# @login_required
# def advisor_list(request):
#     advisors = User.objects.filter(is_superuser=False, profile__is_advisor=True)
#     return render(request, 'chat/advisor_list.html', {'advisors': advisors})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import TemporaryConversation, Message
from .forms import MessageForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
import uuid

@login_required
def index(request):
    if request.user.profile.is_advisor:
        return redirect('chat:advisor_conversations')
    return redirect('chat:advisor_list')

@login_required
def chat_window(request):
    return render(request, 'chat/chat_window.html')

@login_required
def start_conversation(request, advisor_id):
    advisor = get_object_or_404(User, id=advisor_id, is_superuser=False, profile__is_advisor=True)
    
    # Vérifiez si une conversation existe déjà entre le client et le conseiller
    conversation = TemporaryConversation.objects.filter(
        client=request.user,
        advisor=advisor,
        expires_at__gt=timezone.now()
    ).first()
    
    if not conversation:
        # Créez une nouvelle conversation si aucune n'existe
        conversation_name = f"conversation_{uuid.uuid4()}"
        conversation = TemporaryConversation.objects.create(
            name=conversation_name,
            client=request.user,
            advisor=advisor,
            expires_at=timezone.now() + timezone.timedelta(hours=1)  # Conversation expire après 1 heure
        )
    
    return redirect('chat:conversation_detail', conversation_id=conversation.id)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(TemporaryConversation, id=conversation_id)
    if request.user != conversation.client and request.user != conversation.advisor:
        return redirect('chat:advisor_list')  # Rediriger si l'utilisateur n'est pas autorisé

    messages = conversation.messages.order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect(request.path)
    else:
        form = MessageForm()

    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'room_name': conversation.name,  # Assurez-vous de passer le nom de la salle au template
    })

@login_required
def advisor_list(request):
    advisors = User.objects.filter(is_superuser=False, profile__is_advisor=True)
    return render(request, 'chat/advisor_list.html', {'advisors': advisors})

@login_required
def advisor_conversations(request):
    conversations = TemporaryConversation.objects.filter(advisor=request.user, expires_at__gt=timezone.now())
    return render(request, 'chat/advisor_conversations.html', {'conversations': conversations})


