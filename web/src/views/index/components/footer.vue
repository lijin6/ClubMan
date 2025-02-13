<template>
  <div class="footer-view">
    <div class="foot-link-box flex-view">
      <a class="foot-link" href="https://www.decathlon.com" target="_blank">体育用品购买</a>
      <div class="link-split"></div>
      <a href="/admin" class="foot-link" target="/admin">管理员入口</a>
      <div class="link-split"></div>
      <a class="foot-link" href="https://www.apple.com.cn/shop/buy-mac/macbook-pro" target="_blank">计算机资源</a>
      <div class="link-split"></div>
      <a class="foot-link" href="https://www.store.steampowered.com" target="_blank">游戏相关</a>
    </div>
    <div class="footer-infos">
      <span>
        <a style="color: rgb(174, 174, 174)" href="https://www.your-campus-club.com" target="_blank">校园社团管理系统</a>
      </span>
      <span>&nbsp;&nbsp;</span>
    </div>
    <div class="address">
      <p>地址: 北京市海淀区XX路XX号</p>
    </div>
  </div>
</template>

<script>
  import { Modal } from 'ant-design-vue';

  export default {
    name: 'Footer',
    data() {
      return {};
    },
    methods: {
      handleSource() {
        Modal.info({
          title: '欢迎体验',
          content: '使用过程中遇到问题，可以咨询作者：lengqin1024（微信）',
          onOk() {},
        });
      },
    },
  };
</script>

<style scoped lang="less">
  .flex-view {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
  }

  .footer-view {
    max-width: 1108px;
    margin: 0 auto;
    padding: 24px 0 20px 54px;
    background-color: rgba(211, 211, 211, 0.3); /* 浅灰透明背景 */
    border-radius: 8px; /* 可选，增加圆角 */
    
    .foot-link-box {
      display: -webkit-box;
      display: -ms-flexbox;
      display: flex;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      overflow: hidden;
      margin: 24px auto 16px;
      -webkit-box-pack: center;
      -ms-flex-pack: center;
      justify-content: center;
      .foot-link {
        margin: 0 16px;
        color: #2a4f88;
      }
      a {
        background-color: transparent;
        text-decoration: none;
        color: var(--mid-blue);
      }
    }

    .footer-infos {
      height: 16px;
      line-height: 16px;
      font-size: 12px;
      padding-left: 63px;
      color: #aeaeae;
      margin-top: 16px;
      text-align: center; 
    }
    
    .address {
      text-align: center;
      height: 16px;
      line-height: 16px;
      font-size: 12px;
      color: #aeaeae;
      margin-top: 8px;
    }
  }
</style>
