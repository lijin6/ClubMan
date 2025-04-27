<template>
  <div class="activity-admin">
    <!-- 搜索和操作栏 -->
    <div class="toolbar">
      <a-space>
        <a-button type="primary" @click="showCreateModal">新建活动</a-button>
        <a-select
          v-model:value="filterStatus"
          style="width: 120px"
          placeholder="筛选状态"
          allowClear
          @change="fetchActivities"
        >
          <a-select-option value="draft">草稿</a-select-option>
          <a-select-option value="published">已发布</a-select-option>
          <a-select-option value="archived">已归档</a-select-option>
        </a-select>
      </a-space>
    </div>

    <!-- 活动表格 -->
    <a-table
      :columns="columns"
      :data-source="activities"
      :loading="loading"
      :pagination="pagination"
      rowKey="id"
      @change="handleTableChange"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'status'">
          <a-tag :color="getStatusColor(record.status)">
            {{ statusMap[record.status] }}
          </a-tag>
        </template>
        
        <template v-if="column.key === 'action'">
          <a-space>
            <a @click="showEditModal(record)">编辑</a>
            <a-dropdown>
              <a class="ant-dropdown-link" @click.prevent>
                更多 <down-outlined />
              </a>
              <template #overlay>
                <a-menu>
                  <a-menu-item 
                    v-if="record.status !== 'published'" 
                    @click="updateStatus(record.id, 'published')"
                  >
                    发布
                  </a-menu-item>
                  <a-menu-item 
                    v-if="record.status !== 'archived'" 
                    @click="updateStatus(record.id, 'archived')"
                  >
                    归档
                  </a-menu-item>
                  <a-menu-item 
                    v-if="record.status !== 'draft'" 
                    @click="updateStatus(record.id, 'draft')"
                  >
                    设为草稿
                  </a-menu-item>
                  <a-menu-item>
                    <a-popconfirm
                      title="确定删除此活动?"
                      @confirm="() => handleDelete(record.id)"
                    >
                      <span style="color: red">删除</span>
                    </a-popconfirm>
                  </a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 活动编辑/创建模态框 -->
    <a-modal
      v-model:visible="modal.visible"
      :title="modal.title"
      :confirm-loading="modal.confirmLoading"
      @ok="handleSubmit"
      @cancel="handleCancel"
      width="800px"
    >
      <a-form 
        ref="formRef"
        :model="formState"
        :rules="rules"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 20 }"
      >
        <a-form-item label="活动名称" name="title">
          <a-input v-model:value="formState.title" placeholder="请输入活动名称" />
        </a-form-item>
        <a-form-item label="活动内容" name="content">
          <a-textarea 
            v-model:value="formState.content" 
            placeholder="请输入活动内容"
            :rows="6"
          />
        </a-form-item>
        <a-form-item label="活动状态" name="status">
          <a-select v-model:value="formState.status" placeholder="请选择活动状态">
            <a-select-option value="draft">草稿</a-select-option>
            <a-select-option value="published">已发布</a-select-option>
            <a-select-option value="archived">已归档</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="开始时间" name="start_time">
          <a-date-picker
            v-model:value="formState.start_time"
            show-time
            format="YYYY-MM-DD HH:mm"
            style="width: 100%"
            placeholder="请选择开始时间"
          />
        </a-form-item>
        <a-form-item label="结束时间" name="end_time">
          <a-date-picker
            v-model:value="formState.end_time"
            show-time
            format="YYYY-MM-DD HH:mm"
            style="width: 100%"
            placeholder="请选择结束时间"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { DownOutlined } from '@ant-design/icons-vue'
import axios from 'axios'
import dayjs from 'dayjs'

// 表格列配置
const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '活动名称', dataIndex: 'title', key: 'title' },
  { title: '开始时间', dataIndex: 'start_time', key: 'start_time', width: 180 },
  { title: '结束时间', dataIndex: 'end_time', key: 'end_time', width: 180 },
  { title: '状态', dataIndex: 'status', key: 'status', width: 100 },
  { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 180 },
  { title: '操作', key: 'action', width: 180 }
]

// 状态映射
const statusMap = {
  draft: '草稿',
  published: '已发布',
  archived: '已归档'
}

// 数据状态
const activities = ref([])
const loading = ref(false)
const filterStatus = ref('')
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  pageSizeOptions: ['10', '20', '50']
})

// 模态框状态
const modal = reactive({
  visible: false,
  title: '新建活动',
  isEdit: false,
  confirmLoading: false,
  currentId: null
})

// 表单状态
const formRef = ref()
const formState = reactive({
  title: '',
  content: '',
  status: 'draft',
  start_time: null,
  end_time: null
})

// 表单验证规则
const rules = {
  title: [{ required: true, message: '请输入活动名称', trigger: 'blur' }],
  content: [{ required: true, message: '请输入活动内容', trigger: 'blur' }],
  status: [{ required: true, message: '请选择活动状态', trigger: 'change' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' },
    {
      validator: (_, value) => {
        if (!value || !formState.start_time) return Promise.resolve()
        if (value.isBefore(formState.start_time)) {
          return Promise.reject('结束时间必须晚于开始时间')
        }
        return Promise.resolve()
      },
      trigger: 'change'
    }
  ]
}

// 获取状态标签颜色
const getStatusColor = (status) => {
  const colors = {
    draft: 'orange',
    published: 'green',
    archived: 'gray'
  }
  return colors[status] || 'default'
}

// 获取活动列表
const fetchActivities = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.current,
      page_size: pagination.pageSize
    }
    
    if (filterStatus.value) {
      params.status = filterStatus.value
    }
    
    const response = await axios.get('http://127.0.0.1:8000/myapp/admin/activities/', { params })
    
    if (response.data?.code === 0) {
      activities.value = response.data.data || []
      pagination.total = response.data.total || 0
    } else {
      message.warning(response.data?.msg || '获取数据失败')
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    message.error(error.response?.data?.msg || '获取数据失败')
  } finally {
    loading.value = false
  }
}

// 表格分页/排序变化
const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchActivities()
}

// 更新活动状态
const updateStatus = async (id, status) => {
  try {
    loading.value = true
    const response = await axios.patch(
      `http://127.0.0.1:8000/myapp/admin/activities/${id}/status/`,
      { status }
    )
    
    if (response.data?.code === 0) {
      message.success('状态更新成功')
      await fetchActivities()
    } else {
      message.warning(response.data?.msg || '状态更新失败')
    }
  } catch (error) {
    console.error('更新状态失败:', error)
    message.error(error.response?.data?.msg || '状态更新失败')
  } finally {
    loading.value = false
  }
}

// 重置模态框状态
const resetModal = () => {
  formRef.value?.resetFields()
  Object.assign(formState, {
    title: '',
    content: '',
    status: 'draft',
    start_time: null,
    end_time: null
  })
  modal.visible = false
  modal.confirmLoading = false
  modal.isEdit = false
  modal.currentId = null
}

// 显示创建模态框
const showCreateModal = () => {
  resetModal()
  modal.visible = true
  modal.title = '新建活动'
}

// 显示编辑模态框
const showEditModal = (record) => {
  resetModal()
  modal.visible = true
  modal.title = '编辑活动'
  modal.isEdit = true
  modal.currentId = record.id
  
  // 填充表单数据
  Object.assign(formState, {
    title: record.title,
    content: record.content,
    status: record.status,
    start_time: record.start_time ? dayjs(record.start_time) : null,
    end_time: record.end_time ? dayjs(record.end_time) : null
  })
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    modal.confirmLoading = true
    
    const payload = {
      title: formState.title,
      content: formState.content,
      status: formState.status,
      start_time: formState.start_time?.format('YYYY-MM-DD HH:mm'),
      end_time: formState.end_time?.format('YYYY-MM-DD HH:mm')
    }

    let response
    if (modal.isEdit) {
      response = await axios.put(
        `http://127.0.0.1:8000/myapp/admin/activities/${modal.currentId}/`,
        payload
      )
    } else {
      response = await axios.post(
        'http://127.0.0.1:8000/myapp/admin/activities/',
        payload
      )
    }

    if (response.data?.code === 0) {
      message.success(response.data?.msg || '操作成功')
      resetModal()
      await fetchActivities()
    } else {
      message.warning(response.data?.msg || '操作失败')
    }
  } catch (error) {
    console.error('提交表单错误:', error)
    message.error(error.response?.data?.msg || '操作失败')
  } finally {
    modal.confirmLoading = false
  }
}

// 删除活动
const handleDelete = async (id) => {
  try {
    loading.value = true
    const response = await axios.delete(
      `http://127.0.0.1:8000/myapp/admin/activities/${id}/`
    )
    
    if (response.data?.code === 0) {
      message.success(response.data?.msg || '删除成功')
      await fetchActivities()
    } else {
      message.warning(response.data?.msg || '删除失败')
    }
  } catch (error) {
    console.error('删除活动失败:', error)
    message.error(error.response?.data?.msg || '删除失败')
  } finally {
    loading.value = false
  }
}

// 取消模态框
const handleCancel = () => {
  resetModal()
}

// 初始化加载数据
onMounted(() => {
  fetchActivities()
})
</script>

<style scoped>
.activity-admin {
  padding: 20px;
  background: #fff;
}

.toolbar {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>