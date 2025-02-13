<template>
  <div class="main-bar-view">
    <div class="logo">
      <img :src="logoImage" class="search-icon" @click="$router.push({ name: 'portal' })" />
    </div>
    <div class="search-entry">
      <img :src="SearchIcon" class="search-icon" />
      <input placeholder="输入关键词" ref="keywordRef" @keyup.enter="search" />
    </div>
    <div class="right-view">
      <a href="/admin" target="__black" type="a-link" style="line-height: 40px; width: 80px">后台入口</a>
      <template v-if="userStore.user_token">
        <a-dropdown>
          <a class="ant-dropdown-link" @click="(e) => e.preventDefault()">
            <img :src="AvatarIcon" class="self-img" />
          </a>
          <template #overlay>
            <a-menu>
              <a-menu-item>
                <a @click="goUserCenter('orderView')">我的申请</a>
              </a-menu-item>
              <a-menu-item>
                <a @click="goUserCenter('userInfoEditView')">个人设置</a>
              </a-menu-item>
              <a-menu-item>
                <a @click="quit()">退出</a>
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
      </template>
      <template v-else>
        <button class="login btn hidden-sm" @click="goLogin()">登录</button>
      </template>

      <div class="right-icon" @click="msgVisible = true">
        <img :src="MessageIcon" />
        <span class="msg-point" style=""></span>
      </div>
      <div>
        <a-drawer title="我的消息" placement="right" :closable="true" :maskClosable="true" :visible="msgVisible" @close="onClose">
          <a-spin :spinning="loading" style="min-height: 250px">
            <div class="list-content">
              <div class="notification-view">
                <div class="list">
                  <div class="notification-item flex-view" v-for="item in msgData">
                    <div class="content-box">
                      <div class="header">
                        <span class="title-txt">{{ item.title }}</span>
                        <br />
                        <span class="time">{{ item.create_time }}</span>
                      </div>
                      <div class="content">
                        <p>{{ item.content }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </a-spin>
        </a-drawer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { listApi } from '/@/api/index/notice';
  import { useUserStore } from '/@/store';
  import logoImage from '/@/assets/images/k-logo.png';
  import SearchIcon from '/@/assets/images/search-icon.svg';
  import AvatarIcon from '/@/assets/images/avatar.jpg';
  import MessageIcon from '/@/assets/images/message-icon.svg';
  import { message } from 'ant-design-vue';

  const router = useRouter();
  const route = useRoute();
  const userStore = useUserStore();

  const keywordRef = ref();

  let loading = ref(false);
  let msgVisible = ref(false);
  let msgData = ref([] as any);

  onMounted(() => {
    getMessageList();
  });

  const getMessageList = () => {
    loading.value = true;
    listApi({})
      .then((res) => {
        msgData.value = res.data;
        loading.value = false;
      })
      .catch((err) => {
        console.log(err);
        loading.value = false;
      });
  };
  const search = () => {
    const keyword = keywordRef.value.value;
    if (route.name === 'search') {
      router.push({ name: 'search', query: { keyword: keyword } });
    } else {
      let text = router.resolve({ name: 'search', query: { keyword: keyword } });
      window.open(text.href, '_blank');
    }
  };
  const goLogin = () => {
    router.push({ name: 'login' });
  };

  const goUserCenter = (menuName) => {
    router.push({ name: menuName });
  };
  const quit = () => {
    userStore.logout().then((res) => {
      router.push({ name: 'portal' });
    });
  };
  const onClose = () => {
    msgVisible.value = false;
  };

  const handleJoin = () => {
    let userId = userStore.user_id;
    if (userId) {
      router.push({ name: 'jiajiaoEditView' });
    } else {
      message.warn('请先登录！');
    }
  };
</script>

<style scoped lang="less">
  .main-bar-view {
    position: fixed;
    top: 0;
    left: 0;
    height: 70px; /* 增加高度 */
    width: 100%;
    background: #fff;
    border-bottom: 1px solid #cedce4;
    padding-left: 48px;
    z-index: 16;
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .logo {
    margin-right: 24px;
    img {
      width: 48px; /* 增大Logo图标 */
      height: 48px;
      cursor: pointer;
    }
  }

  .search-entry {
    position: relative;
    width: 400px;
    min-width: 200px;
    height: 40px; /* 增加输入框高度 */
    background: #ecf3fc;
    padding: 0 12px;
    border-radius: 16px;
    font-size: 0;
    cursor: pointer;

    .search-icon {
      width: 24px; /* 增大搜索图标 */
      margin: 8px 10px 0 0;
    }

    input {
      position: absolute;
      top: 6px;
      width: 85%;
      height: 28px;
      border: 0;
      outline: none;
      color: #000;
      background: #ecf3fc;
      font-size: 16px; /* 增大字体 */
    }
  }

  .right-view {
    padding-right: 36px;
    flex: 1;
    display: flex;
    flex-direction: row;
    gap: 24px;
    justify-content: flex-end;

    .username {
      height: 32px;
      line-height: 32px;
      text-align: center;
    }
    button {
      outline: none;
      border: none;
      cursor: pointer;
    }
    img {
      cursor: pointer;
    }

    .right-icon {
      position: relative;
      width: 20px; /* 保持消息图标大小不变 */
      margin: 6px 0 0 6px;
      cursor: pointer;
      display: inline-block;
      font-size: 0;
      span {
        position: absolute;
        right: -16px;
        top: -4px;
        font-size: 14px;
        color: #fff;
        background: #4684e2;
        border-radius: 8px;
        padding: 0 6px;
        height: 18px;
        line-height: 18px;
        font-weight: 600;
        min-width: 22px;
        text-align: center;
      }
      .msg-point {
        position: absolute;
        height: 20px; /* 保持宽度和高度一致 */
        background: #4684e2;
        border-radius: 50%; /* 使其变为圆形 */
    }

    }

    .self-img {
      width: 40px; /* 增大头像图标 */
      height: 40px;
      border-radius: 50%;
      vertical-align: middle;
      cursor: pointer;
    }
    .btn {
      background: #4684e2;
      font-size: 16px;
      color: #fff;
      border-radius: 32px;
      text-align: center;
      width: 80px;
      height: 40px; /* 增大按钮 */
      line-height: 40px;
      vertical-align: middle;
      margin-left: 32px;
    }
  }

  .content-list {
    flex: 1;

    .list-title {
      color: #152844;
      font-weight: 600;
      font-size: 20px;
      height: 48px;
      margin-bottom: 4px;
      border-bottom: 1px solid #cedce4;
    }
  }

  .notification-item {
    padding-top: 16px;

    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      margin-right: 12px;
    }

    .content-box {
      flex: 1;
      border-bottom: 1px dashed #e9e9e9;
      padding: 6px 0 20px;
    }

    .header {
      margin-bottom: 16px;
    }

    .title-txt {
      color: #315c9e;
      font-weight: 600;
      font-size: 16px;
    }

    .time {
      color: #a1adc5;
      font-size: 14px;
    }

    .content {
      margin-top: 6px;
      color: #484848;
      font-size: 14px;
      line-height: 22px;
    }
  }
</style>
