<template>
  <footer class="footer-view">
    <div class="footer-content">
      <div class="foot-link-box">
        <a class="foot-link" href="https://www.decathlon.com" target="_blank">体育用品购买</a>
        <span class="link-divider">|</span>
        <a class="foot-link" href="/admin" target="_blank">管理员入口</a>
        <span class="link-divider">|</span>
        <a class="foot-link" href="https://www.apple.com.cn/shop/buy-mac/macbook-pro" target="_blank">计算机资源</a>
        <span class="link-divider">|</span>
        <a class="foot-link" href="https://www.store.steampowered.com" target="_blank">游戏相关</a>
      </div>
      <div class="footer-info">
        <a class="footer-brand" href="https://www.your-campus-club.com" target="_blank">
          校园社团管理系统
        </a>
        <div class="footer-address">
          <p>地址: 贵阳市xxx</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// 使用Vue 3的setup语法
</script>

<style scoped lang="less">
.footer-view {
  width: 100%;
  background: rgba(0, 0, 0, 1); /* 纯黑色透明背景 */
  color: #fff;
  padding: 2rem 0;
  margin-top: auto; /* 确保页脚在页面底部 */
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.foot-link-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.foot-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
  
  &:hover {
    color: #fff;
    text-decoration: underline;
  }
}

.link-divider {
  color: rgba(255, 255, 255, 0.3);
  user-select: none;
}

.footer-info {
  text-align: center;
  margin-top: 1rem;
}

.footer-brand {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
  text-decoration: none;
  
  &:hover {
    color: #fff;
  }
}

.footer-address {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .footer-content {
    padding: 0 1rem;
  }
  
  .foot-link-box {
    gap: 0.5rem;
  }
  
  .foot-link, .link-divider {
    font-size: 0.8rem;
  }
}
</style>