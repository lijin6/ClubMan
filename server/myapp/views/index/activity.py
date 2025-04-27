from django.http import JsonResponse
from django.views.decorators.http import require_GET
from datetime import datetime
from ..db_utils import db_cursor

@require_GET
def activity_list(request):
    """前端活动展示接口（返回所有已发布的活动）"""
    try:
        with db_cursor() as cursor:
            # 查询所有已发布的活动，按创建时间降序排列
            cursor.execute("""
            SELECT 
                id, 
                title, 
                content, 
                status,
                start_time, 
                end_time,
                created_at
            FROM activities 
            WHERE status = 'published'
            ORDER BY created_at DESC
            """)
            
            current_time = datetime.now()
            activities = []
            for row in cursor.fetchall():
                end_time = row['end_time']
                days_left = (end_time - current_time).days if end_time else None
                
                activities.append({
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'status': row['status'],
                    'start_time': row['start_time'].strftime('%Y-%m-%d %H:%M') if row['start_time'] else None,
                    'end_time': row['end_time'].strftime('%Y-%m-%d %H:%M') if row['end_time'] else None,
                    'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M') if row['created_at'] else None,
                    'days_left': days_left,
                    'is_active': bool(end_time and end_time > current_time) if end_time else None
                })
            
            return JsonResponse({
                'code': 200,
                'message': 'success',
                'data': {
                    'activities': activities,
                    'current_time': current_time.strftime('%Y-%m-%d %H:%M'),
                    'total': len(activities)
                }
            })
            
    except Exception as e:
        # 记录错误日志
        import logging
        logging.error(f"活动列表获取失败: {str(e)}", exc_info=True)
        
        return JsonResponse({
            'code': 500,
            'message': '服务器内部错误',
            'detail': str(e)
        }, status=500)