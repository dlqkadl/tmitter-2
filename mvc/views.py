from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from tmitter.settings import *
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseServerError
from tmitter.mvc.models import Note, User, Category, Area

# Create your views here.

# ##################
# common functions #
####################


# do login
def __do_login(request, _username, _password):
    _state = __check_login(_username, _password)
    if _state['success']:
        # save login info to session
        request.session['islogin'] = True
        request.session['userid'] = _state['userid']
        request.session['username'] = _username
        request.session['realname'] = _state['realname']

    return _state


# get session user id
def __user_id(request):
    return request.session.get('userid', '')


# get session username
def __user_name(request):
    return request.session.get('username', '')


# return user login state
def __is_login(request):
    return request.session.get('islogin', False)


def signup(request):
    # check is login
    _islogin = __is_login(request)

    if _islogin:
        return HttpResponseRedirect('/')    # 如果已经登录，重定向到根目录

    _userinfo = {                           # 用户数据结构
        'username': '',
        'password': '',
        'confirm': '',
        'realname': '',
        'email': '',
    }

    try:
        _userinfo = {
            'username': request.POST['username'],
            'password': request.POST['password'],
            'confirm': request.POST['confirm'],
            'realname': request.POST['realname'],
            'email': request.POST['email'],
        }
        _is_post = True
    except KeyError:
        _is_post = False

    if _is_post:                                # 如果是post消息，执行注册逻辑
        _state = __do_signup(request, _userinfo)
    else:
        _state = {
            'success': False,
            'message': _('Signup'),
        }

    if _state['success']:
        return __result_message(request, _('Signup succeed'), _('Your account was registered successfully.'))

    _result = {                                 # 显示注册信息
        'success': _state['success'],
        'message': _state['message'],
        'form': {
            'username': _userinfo['username'],
            'realname': _userinfo['realname'],
            'email': _userinfo['email'],
        }
    }

    _template = loader.get_template('signup.html')      # 渲染注册页面
    _context = {                                        # 配置模板参数
        'page_title': _('Signup'),
        'state': _result,
    }
    _output = _template.render(_context)
    return HttpResponse(_output)


# pst signup data
def __do_signup(request, _userinfo):
    _state = {
        'success': True,
        'message': '',
    }

    # check username exist
    if _userinfo['username'] == '':
        _state['success'] = False
        _state['message'] = _('"Username" have not been inputed.')
        return _state

    if _userinfo['password'] == '':
        _state['success'] = False
        _state['message'] = _('"Password" have not been inputed.')
        return _state

    if _userinfo['realname'] == '':
        _state['success'] = False
        _state['message'] = _('"Realname" have not been inputed.')
        return _state

    if _userinfo['email'] == '':
        _state['success'] = False
        _state['message'] = _('"Email" have not been inputed.')
        return _state

    # check username whether had existed
    if __check_username_exist(_userinfo['username']):
        _state['success'] = False
        _state['message'] = _('"Username" have existed')
        return _state

    # check password & confirm password 检查两次密码输入是否匹配
    if _userinfo['password'] != _userinfo['confirm']:
        _state['success'] = False
        _state['message'] = _('"Confirm Passwords" have not matched.')
        return _state

    _user = User(
        username=_userinfo['username'],
        realname=_userinfo['realname'],
        password=_userinfo['password'],
        email=_userinfo['email'],
        area=Area.objects.get(id=1)
    )

    _user.user_save()
    return _state


# 调度登录操作的视图函数
def signin(request):
    # get user login status
    _islogin = __is_login(request)

    if _islogin:
        return HttpResponseRedirect('/')

    _username = ''
    _password = ''
    try:                        # 获取输入用户名和密码
        # get post params
        _username = request.POST['username']
        _password = request.POST['password']
        _is_post = True
    except KeyError:
        _is_post = False

    # check username and password
    if _is_post:
        _state = __do_login(request, _username, _password)

        if _state['success']:
            return __return_message(request, _('Login succeed'), _('You have login now.'))

    else:
        _state = {
            'success': False,
            'message': _('Please login first'),
        }

    # body content
    # 显示登录页面
    _template = loader.get_template('signin.html')
    _context = {
        'page_tile': _('Signin'),
        'state': _state,
    }
    _output = _template.render(_context)
    return HttpResponse(_output)