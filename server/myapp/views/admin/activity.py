from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes
from myapp.handler import APIResponse
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.permission.permission import isDemoAdminUser
from ..db_utils import db_cursor
import json


@api_view(['GET', 'POST'])
# @authentication_classes([AdminTokenAuthtication])
def admin_activity_list(request):
    """活动管理列表接口"""
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        if request.method == 'GET':
            with db_cursor() as cursor:
                cursor.execute("""
                SELECT id, title, status, start_time, end_time, created_at
                FROM activities
                ORDER BY created_at DESC
                """)
                
                activities = []
                for row in cursor.fetchall():
                    activities.append({
                        'id': row['id'],
                        'title': row['title'],
                        'status': row['status'],
                        'start_time': row['start_time'].strftime('%Y-%m-%d %H:%M'),
                        'end_time': row['end_time'].strftime('%Y-%m-%d %H:%M'),
                        'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M')
                    })
                
                return APIResponse(code=0, msg='查询成功', data=activities)
                
        elif request.method == 'POST':
            data = request.data
            required_fields = ['title', 'content', 'start_time', 'end_time']
            if not all(field in data for field in required_fields):
                return APIResponse(code=1, msg='缺少必填字段')
            
            with db_cursor() as cursor:
                cursor.execute("""
                INSERT INTO activities (title, content, status, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s)
                """, (
                    data['title'],
                    data['content'],
                    data.get('status', 'draft'),
                    datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M'),
                    datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M')
                ))
                activity_id = cursor.lastrowid
                
                return APIResponse(
                    code=0, 
                    msg='创建成功', 
                    data={'id': activity_id}
                )
                
    except Exception as e:
        return APIResponse(code=1, msg=str(e))

@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([AdminTokenAuthtication])
def admin_activity_detail(request, activity_id):
    """单个活动管理接口"""
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        if request.method == 'GET':
            with db_cursor() as cursor:
                cursor.execute("""
                SELECT id, title, content, status, start_time, end_time
                FROM activities
                WHERE id = %s
                """, (activity_id,))
                
                row = cursor.fetchone()
                if not row:
                    return APIResponse(code=1, msg='活动不存在')
                    
                return APIResponse(code=0, msg='查询成功', data={
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'status': row['status'],
                    'start_time': row['start_time'].strftime('%Y-%m-%d %H:%M'),
                    'end_time': row['end_time'].strftime('%Y-%m-%d %H:%M')
                })
                
        elif request.method == 'PUT':
            data = request.data
            updates = []
            params = []
            
            if 'title' in data:
                updates.append("title = %s")
                params.append(data['title'])
            if 'content' in data:
                updates.append("content = %s")
                params.append(data['content'])
            if 'status' in data:
                updates.append("status = %s")
                params.append(data['status'])
            if 'start_time' in data:
                try:
                    updates.append("start_time = %s")
                    params.append(datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M'))
                except ValueError:
                    return APIResponse(code=1, msg='开始时间格式错误(应为YYYY-MM-DD HH:MM)')
            if 'end_time' in data:
                try:
                    updates.append("end_time = %s")
                    params.append(datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M'))
                except ValueError:
                    return APIResponse(code=1, msg='结束时间格式错误(应为YYYY-MM-DD HH:MM)')
            
            if not updates:
                return APIResponse(code=1, msg='没有可更新的字段')
            
            sql = f"UPDATE activities SET {', '.join(updates)} WHERE id = %s"
            params.append(activity_id)
            
            with db_cursor() as cursor:
                cursor.execute(sql, params)
                if cursor.rowcount == 0:
                    return APIResponse(code=1, msg='活动不存在')
                
                return APIResponse(code=0, msg='更新成功')
                
        elif request.method == 'DELETE':
            with db_cursor() as cursor:
                cursor.execute("""
                UPDATE activities SET status = 'archived' WHERE id = %s
                """, (activity_id,))
                
                if cursor.rowcount == 0:
                    return APIResponse(code=1, msg='活动不存在')
                
                return APIResponse(code=0, msg='活动已归档')
                
    except Exception as e:
        return APIResponse(code=1, msg=str(e))
    
@api_view(['PATCH'])
def update_activity_status(request, activity_id):
    """更新活动状态接口"""
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        data = request.data
        if 'status' not in data:
            return APIResponse(code=1, msg='缺少status字段')
        
        status = data['status']
        valid_statuses = ['draft', 'published', 'archived']
        
        if status not in valid_statuses:
            return APIResponse(code=1, msg=f'无效的状态值，必须是: {", ".join(valid_statuses)}')

        with db_cursor() as cursor:
            # 先检查活动是否存在
            cursor.execute("SELECT id FROM activities WHERE id = %s", (activity_id,))
            if not cursor.fetchone():
                return APIResponse(code=1, msg='活动不存在')
            
            # 更新状态
            cursor.execute(
                "UPDATE activities SET status = %s WHERE id = %s",
                (status, activity_id)
            )
            
            return APIResponse(code=0, msg='状态更新成功')
            
    except Exception as e:
        return APIResponse(code=1, msg=str(e))
    
    
