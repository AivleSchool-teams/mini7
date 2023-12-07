from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from .models import Board
#from users.decorators import login_message_required, admin_required
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
#from .forms import BoardWriteForm
#from users.models import User
import mimetypes
from mimetypes import guess_type
import os
import re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from urllib.parse import quote
import urllib
from django.conf import settings

# 공지사항 게시판 권한
# level 2,3 = READ
# level 1 관리자 = CREATE, READ + 본인 글 UPDATE, DELETE
# level 0 개발자 = CREATE, READ, UPDATE, DELETE


# # 공지사항 리스트 뷰
# class BoardListView(ListView):
#     model = Board
#     paginate_by = 15
#     template_name = 'board/board_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
#     context_object_name = 'board_list'        #DEFAULT : <app_label>_list

#     def get_queryset(self):
#         search_keyword = self.request.GET.get('q', '')
#         search_type = self.request.GET.get('type', '')
#         board_list = Board.objects.order_by('-id') 
        
#         if search_keyword :
#             if len(search_keyword) > 1 :
#                 if search_type == 'all':
#                     search_board_list = board_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
#                 elif search_type == 'title_content':
#                     search_board_list = board_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
#                 elif search_type == 'title':
#                     search_board_list = board_list.filter(title__icontains=search_keyword)    
#                 elif search_type == 'content':
#                     search_board_list = board_list.filter(content__icontains=search_keyword)    
#                 elif search_type == 'writer':
#                     search_board_list = board_list.filter(writer__user_id__icontains=search_keyword)

#                 # if not search_board_list :
#                 #     messages.error(self.request, '일치하는 검색 결과가 없습니다.')
#                 return search_board_list
#             else:
#                 messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
#         return board_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = context['paginator']
#         page_numbers_range = 5
#         max_index = len(paginator.page_range)

#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1

#         start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >= max_index:
#             end_index = max_index

#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range

#         search_keyword = self.request.GET.get('q', '')
#         search_type = self.request.GET.get('type', '')
#         board_fixed = Board.objects.filter(top_fixed=True).order_by('-registered_date')

#         if len(search_keyword) > 1 :
#             context['q'] = search_keyword
#         context['type'] = search_type
#         context['board_fixed'] = board_fixed

#         return context


# # 공지사항 게시글 보기
# @login_message_required
# def board_detail_view(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     # board = Board.objects.filter(id=pk)
#     session_cookie = request.session['user_id']
#     cookie_name = F'board_hits:{session_cookie}'

#     if request.user == board.writer:
#         board_auth = True
#     else:
#         board_auth = False

#     context = {
#         'board': board,
#         'board_auth': board_auth,
#     }
#     response = render(request, 'board/board_detail.html', context)

#     # 조회수 GET증가 방지 쿠키처리
#     if request.COOKIES.get(cookie_name) is not None:
#         cookies = request.COOKIES.get(cookie_name)
#         cookies_list = cookies.split('|')
#         if str(pk) not in cookies_list:
#             response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
#             # board.update(hits=F('hits') + 1)
#             board.hits += 1
#             board.save()
#             return response
#     else:
#         response.set_cookie(cookie_name, pk, expires=None)
#         # board.update(hits=F('hits') + 1)
#         board.hits += 1
#         board.save()
#         return response
#     return render(request, 'board/board_detail.html', context)


# # 공지사항 글쓰기
# @login_message_required
# @admin_required
# def board_write_view(request):
#     if request.method == "POST":
#         form = BoardWriteForm(request.POST, request.FILES)
#         user = request.session['user_id']
#         user_id = User.objects.get(user_id = user)
#         # upload_files = request.FILES.getlist('files')

#         if form.is_valid():
#             board = form.save(commit = False)
#             board.writer = user_id
#             # 첨부파일명 save
#             if request.FILES:
#                 if 'upload_files' in request.FILES.keys():
#                     board.filename = request.FILES['upload_files'].name
#                 # extension = board.filename.split(".")[1].lower()
#                 # board.extension = '.' + extension
#             board.save()
#             return redirect('board:board_list')
#     else:
#         form = BoardWriteForm()
#     return render(request, "board/board_write.html", {'form': form})


# # 공지사항 게시글 수정
# @login_message_required
# def board_edit_view(request, pk):
#     board = Board.objects.get(id=pk)

#     if request.method == "POST":
#         if(board.writer == request.user or request.user.level == '0'):

#             file_change_check = request.POST.get('fileChange', False)
#             file_check = request.POST.get('upload_files-clear', False)
            
#             if file_check or file_change_check:
#                 os.remove(os.path.join(settings.MEDIA_ROOT, board.upload_files.path))

#             form = BoardWriteForm(request.POST, request.FILES, instance=board)
#             if form.is_valid():
#                 # test-------------------------------#
#                 board = form.save(commit = False)
#                 if request.FILES:
#                     if 'upload_files' in request.FILES.keys():
#                         board.filename = request.FILES['upload_files'].name
#                 board.save()
#                 #------------------------------------#
#                 # form.save()
#                 messages.success(request, "수정되었습니다.")
#                 return redirect('/board/'+str(pk))
#     else:
#         board = Board.objects.get(id=pk)
#         if board.writer == request.user or request.user.level == '0':
#             form = BoardWriteForm(instance=board)
#             # test---------------------------------------------------------#
#             context = {
#                 'form': form,
#                 'edit': '수정하기',
#             }
#             if board.filename and board.upload_files:
#                 context['filename'] = board.filename
#                 context['file_url'] = board.upload_files.url
#             #--------------------------------------------------------------#
#             # return render(request, "board/board_write.html", {'form': form, 'edit': '수정하기'})
#             return render(request, "board/board_write.html", context)
#         else:
#             messages.error(request, "본인 게시글이 아닙니다.")
#             return redirect('/board/'+str(pk))


# # 공지사항 게시글 삭제
# @login_message_required
# def board_delete_view(request, pk):
#     board = Board.objects.get(id=pk)
#     if board.writer == request.user or request.user.level == '0':
#         board.delete()
#         messages.success(request, "삭제되었습니다.")
#         return redirect('/board/')
#     else:
#         messages.error(request, "본인 게시글이 아닙니다.")
#         return redirect('/board/'+str(pk))


# # 공지사항 게시글 첨부파일 다운로드 한글명 인코딩
# @login_message_required
# def board_download_view(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     url = board.upload_files.url[1:]
#     print(type(url))
#     print(url)
#     file_url = urllib.parse.unquote(url)
    
#     if os.path.exists(file_url):
#         with open(file_url, 'rb') as fh:
#             # quote_file_url = urllib.parse.quote(file_url.encode('utf-8'))
#             quote_file_url = urllib.parse.quote(board.filename.encode('utf-8'))
#             response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
#             # response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url[29:]
#             response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
#             return response
#         raise Http404
    
def detail(request):
    return render(request, 'board_detail.html')

def list(request):
    return render(request, 'board_list.html')

def board(request):
    return render(request, 'board.html')