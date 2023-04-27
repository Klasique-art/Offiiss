from django.shortcuts import render

# Create your views here.

def chat_room(request, room_name):
    return render(request, 'chat/chat.html', {
        'room_name': room_name
    })


# def room_create(request):
#     if request.method == 'POST':
#         form = RoomCreateForm(request.POST)
#         if form.is_valid():
#             room_name = form.cleaned_data['room_name']
#             # Create new room and redirect to the chat room.
#             ...
#     else:
#         form = RoomCreateForm()
#     return render(request, 'chat/room_create.html', {'form': form})