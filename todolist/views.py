from django.shortcuts import render, redirect
from .models import Todo


# Create your views here.


def home(request):
    # 判断
    # 如果用户发送的是POST请求
    if request.method == "POST":
        # 判断用户输入是否为空字符串'' # 利用前端去判断也可以 或许更好 JavaScript? 前后端都去判断，仅前端判断不安全
        if request.POST['待办事项'] == '':
            content = {'清单': Todo.objects.all(), '提示': '请输入内容后再提交'}
            return render(request, 'home.html', content)

        else:
            new_row = Todo(event=request.POST['待办事项'], finished=False)
            new_row.save()
            content = {'清单': Todo.objects.all(), '信息': '添加成功'}
            return render(request, 'home.html', content)
            # request.POST 返回 QueryDic, 是 django 自带的对象

    # 如果用户发送的是GET请求
    elif request.method == "GET":
        content = {'清单': Todo.objects.all()}
        return render(request, 'home.html', content)


def about(request):
    return render(request, 'about.html')


def edit(request, event_id):
    if request.method == "POST":
        if request.POST['已修改事项'] == '':
            return render(request, 'edit.html', {'提示': '请输入内容后提交'})
        else:
            modified_row = Todo.objects.get(id=event_id)
            modified_row.event = request.POST['已修改事项']
            modified_row.save()
            return redirect("todolist:主页")

    else:
        content = {'待修改事项': Todo.objects.get(id=event_id).event}
        return render(request, 'edit.html', content)


def delete(request, event_id):
    Todo.objects.get(id=event_id).delete()
    return redirect("todolist:主页")


def cross(request, event_id):
    modified_row = Todo.objects.get(id=event_id)
    if request.POST['完成状态'] == '已完成':
        modified_row.finished = True
    else:
        modified_row.finished = False
    modified_row.save()
    return redirect('todolist:主页')
