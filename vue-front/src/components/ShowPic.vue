<template>
  <div class="ShowPic">
    <el-main class="mainP" align="center">
      <el-button type="primary" align="center" v-if="loading == true" :loading=true >加载中</el-button>
      <el-button type="primary" align="center" v-if="loading != true" @click="getImgCode">点击查看图片</el-button>
      <div class="block">
       <el-image :src="imgCode" v-loading="loading"></el-image>
      </div>
    </el-main>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ShowPic',
  data () {
    return {
      loading: false,
      imgCode: ''
    }
  },
  created: function () {
    this.loading = true
    this.getImgCode()
    setTimeout(() => {
      this.loading = false
    }, 1000)
  },
  methods: {
    getImgCode () {
      var that = this
      const path = 'http://127.0.0.1:5000/getPic'
      axios.get(path, {
        responseType: 'arraybuffer'
      }).then(function (response) {
        that.loading = true
        setTimeout(() => {
          that.loading = false
        }, 1000)
        that.imgCode =
          'data:image/bmp;base64,' + that.arrayBufferToBase64(response.data)
        that.$message('查询成功')
      }).catch(function (error) {
        that.$message(error)
      })
    },
    arrayBufferToBase64 (buffer) {
      // 第一步，将ArrayBuffer转为二进制字符串
      var binary = ''
      var bytes = new Uint8Array(buffer)
      var len = bytes.byteLength
      for (var i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i])
      }
      // 将二进制字符串转为base64字符串
      return window.btoa(binary)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.mainP {
  position: relative;
  left: 50px;
  top: 10px;
}

</style>
