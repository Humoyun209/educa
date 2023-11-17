from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseForbidden


@login_required
def course_chat_room(request: HttpRequest, course_id: int):
    try:
        course = request.user.courses_joined.get(id=course_id)
    except:
        return HttpResponseForbidden()
    return render(request, 'chat/room.html', {'course': course})