# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Activity
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_superuser

def update_activity_status(request, activity_id, status):
    try:
        activity = Activity.objects.get(id=activity_id)
        activity.status = status
        activity.save()
        return JsonResponse({'message': f'活动状态已更新为 {status}'}, status=200)
    except Activity.DoesNotExist:
        return JsonResponse({'message': '活动不存在'}, status=404)
    except Exception:
        return JsonResponse({'message': '更新活动状态时发生错误'}, status=500)

@csrf_exempt
@login_required
def create_activity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description')
            if not isinstance(name, str) or not isinstance(description, str):
                return JsonResponse({'message': '活动名称和描述必须为字符串类型'}, status=400)
            if name and description:
                activity = Activity.objects.create(
                    user=request.user,
                    name=name,
                    description=description
                )
                return JsonResponse({'message': '活动发起成功', 'activity_id': activity.id}, status=201)
            else:
                return JsonResponse({'message': '活动名称和描述不能为空'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': '无效的 JSON 数据，请检查请求体格式'}, status=400)
        except Exception as e:
            logger.error(f"创建活动时发生错误: {str(e)}", exc_info=True)
            return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
@user_passes_test(is_admin)
def approve_activity(request, activity_id):
    if request.method == 'POST':
        return update_activity_status(request, activity_id, 'approved')

@csrf_exempt
@user_passes_test(is_admin)
def reject_activity(request, activity_id):
    if request.method == 'POST':
        return update_activity_status(request, activity_id, 'rejected')
