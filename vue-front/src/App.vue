<template>
  <div id="app" style="width: 100%;margin-top:0px;">
    <el-table :show-header="false" :data="tableData" :row-class-name="tableClass">
      <el-table-column align="left">
        <el-image :src="require('./assets/uestc.png')"/>
      </el-table-column>
      <el-table-column align="center">
        <el-image :src="require('./assets/header.png')"/>
      </el-table-column>
    </el-table>
    <el-divider><i class="el-icon-mobile-phone"></i></el-divider>
      <el-container>
          <el-aside background-color="#333399" width="200px">
            <el-menu router mode="horizontal" background-color="#333399" text-color="#fff" active-text-color="#f6941d" :default-openeds="['1']">
              <el-submenu>
                <template slot="title"><i class="el-icon-s-tools"></i>功能</template>
                  <el-menu-item index="Layout">重构功能</el-menu-item>
                  <el-menu-item index="ShowPic">图片测试</el-menu-item>
              </el-submenu>
            </el-menu>
          </el-aside>
        <transition :name="transitionName">
          <router-view></router-view>
        </transition>
      </el-container>
  </div>
</template>

<script>
import 'element-ui/lib/theme-chalk/index.css'

export default {
  name: 'App',
  data () {
    return {
      tableData: [{}],
      transitionName: ''
    }
  },
  watch: {// 使用watch 监听$router的变化
    $route (to, from) {
      // 如果to索引大于from索引,判断为前进状态,反之则为后退状态
      if (to.meta.index > from.meta.index) {
        // 设置动画名称
        this.transitionName = 'slide-left'
      } else {
        this.transitionName = 'slide-right'
      }
    }
  },
  methods: {
    tableClass () {
      return 'success-row'
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #398fe6;
  margin-top: 60px;
}
.slide-right-enter-active,
.slide-right-leave-active,
.slide-left-enter-active,
.slide-left-leave-active {
  will-change: transform;
  transition: all 200ms;
  position: relative;
}
.slide-right-enter {
  opacity: 0;
  transform: translate3d(0, 100%, 0);
}
.slide-right-leave-active {
  opacity: 0;
  transform: translate3d(0, -100%, 0);
}
.slide-left-enter {
  opacity: 0;
  transform: translate3d(0, -100%, 0);
}
.slide-left-leave-active {
  opacity: 0;
  transform: translate3d(0, 100%, 0);
}
.el-table .success-row {
  background: #333399;
}
</style>
