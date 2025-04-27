from django.db import models

class Activity(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档')
    ]
    
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='published')
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'activities'
        
    @classmethod
    def init_table(cls):
        with db_cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                content TEXT NOT NULL,
                status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_status (status),
                INDEX idx_time (start_time, end_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)