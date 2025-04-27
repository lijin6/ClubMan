<template>
    <div class="activity-page">
      <!-- 头部组件 -->
      <Header />
      
      <div class="activity-container">
        <a-page-header
          title="活动公告"
          @back="() => router.push('/portal')"
        />
        
        <div class="activity-list">
          <a-spin :spinning="loading">
            <div class="activity-cards">
              <div 
                v-for="activity in activities" 
                :key="activity.id" 
                class="activity-card"
                :class="{ 'expired': !activity.is_active }"
              >
                <div class="activity-header">
                  <h3>{{ activity.title }}</h3>
                  <div class="activity-status">
                    <a-tag :color="getActivityTagColor(activity)">
                      {{ getActivityStatusText(activity) }}
                    </a-tag>
                  </div>
                </div>
                
                <pre class="activity-content">{{ activity.content }}</pre>
                
                <div class="activity-meta">
                  <div class="time-info">
                    <span><calendar-outlined /> {{ activity.start_time }}</span>
                    <span>至</span>
                    <span><clock-circle-outlined /> {{ activity.end_time }}</span>
                  </div>
                  <div class="publish-time">
                    <span><schedule-outlined /> 发布于 {{ activity.created_at }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <a-empty 
              v-if="!loading && activities.length === 0" 
              description="暂无活动"
            />
          </a-spin>
        </div>
      </div>
      
      <!-- 底部组件 -->
      <Footer />
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { message } from 'ant-design-vue'
  import { 
    CalendarOutlined, 
    ClockCircleOutlined,
    ScheduleOutlined
  } from '@ant-design/icons-vue'
  import Header from '/@/views/index/components/header.vue'
  import Footer from '/@/views/index/components/footer.vue'
  
  const router = useRouter()
  const activities = ref<any[]>([])
  const loading = ref(false)
  
  // 获取所有已发布活动
  const fetchActivities = async () => {
    try {
      loading.value = true
      const response = await fetch('http://127.0.0.1:8000/myapp/index/activities')
      const data = await response.json()
      
      if (data.code === 200) {
        activities.value = data.data.activities.map((activity: any) => ({
          ...activity,
          // 添加额外的展示字段
          status_display: getActivityStatusText(activity),
          tag_color: getActivityTagColor(activity)
        }))
      } else {
        message.error(data.message || '获取活动列表失败')
      }
    } catch (error) {
      message.error('网络请求失败')
      console.error('获取活动列表失败:', error)
    } finally {
      loading.value = false
    }
  }
  
  // 获取活动状态文本
  const getActivityStatusText = (activity: any) => {
    if (!activity.is_active) return '已结束'
    if (activity.days_left === 0) return '最后一天'
    if (activity.days_left !== undefined && activity.days_left > 0) {
      return `剩余${activity.days_left}天`
    }
    return '进行中'
  }
  
  // 获取活动标签颜色
  const getActivityTagColor = (activity: any) => {
    if (!activity.is_active) return 'gray'
    if (activity.days_left === 0) return 'red'
    if (activity.days_left !== undefined && activity.days_left > 0) {
      if (activity.days_left < 3) return 'red'
      if (activity.days_left < 7) return 'orange'
      return 'green'
    }
    return 'blue'
  }
  
  // 查看活动详情
  const viewDetail = (activity: any) => {
    router.push({
      name: 'activity-detail',
      query: { id: activity.id }
    })
  }
  
  onMounted(() => {
    fetchActivities()
  })
  </script>
  
  <style scoped lang="less">
  .activity-page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f5f5f5;
  }
  
  .activity-container {
    flex: 1;
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    padding: 20px;
  }
  
  .activity-list {
    margin-top: 20px;
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .activity-cards {
    display: grid;
    gap: 16px;
  }
  
  .activity-card {
    padding: 16px;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    transition: all 0.3s;
    background: #fff;
    
    &.expired {
      opacity: 0.8;
      background-color: #fafafa;
    }
    
    &:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      transform: translateY(-2px);
    }
  }
  
  .activity-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    
    h3 {
      margin: 0;
      color: #333;
      font-size: 16px;
      font-weight: 500;
    }
  }
  
  .activity-content {
    white-space: pre-wrap;
    margin-bottom: 12px;
    line-height: 1.6;
    color: #666;
    font-family: inherit;
    padding: 12px;
    background: #f9f9f9;
    border-radius: 4px;
    max-height: 200px;
    overflow: auto;
  }
  
  .activity-meta {
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 12px;
    color: #999;
    
    .time-info {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .publish-time {
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }
  
  :deep(.ant-empty) {
    margin: 40px 0;
  }
  
  :deep(.ant-tag) {
    margin-right: 0;
  }
  </style>