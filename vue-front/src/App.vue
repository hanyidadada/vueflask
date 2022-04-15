<template>
  <div id="app" style="width: 100%;margin-top:0px;">
    <el-table :show-header="false" :data="tableData" >
      <el-table-column align="left">
        <el-image :src="require('./assets/csu18.png')"/>
      </el-table-column>
      <el-table-column align="center">
        <el-image :src="require('./assets/header.png')"/>
      </el-table-column>
    </el-table>
    <el-divider><i class="el-icon-mobile-phone"></i></el-divider>
      <el-container>
          <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
            <el-menu router mode="horizontal" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" :default-openeds="['1']">
              <el-submenu>
                <template slot="title"><i class="el-icon-s-tools"></i>功能</template>
                  <el-menu-item index="Layout">重构功能</el-menu-item>
                  <el-menu-item index="HelloWorld">图片测试</el-menu-item>
              </el-submenu>
            </el-menu>
          </el-aside>
        <router-view/>
      </el-container>
  </div>
</template>

<script>
import 'element-ui/lib/theme-chalk/index.css'

export default {
  name: 'App',
  data () {
    return {
      tableData: [{}]
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
  color: #2c3e50;
  margin-top: 60px;
}
</style>
