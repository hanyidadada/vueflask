<template>
  <div class="LayOut">
    <el-main>
        <el-form :inline="true" class="demo-form-inline">
            <el-form-item label="核号">
                <el-select v-model="corenum" placeholder="请选择核号">
                    <el-option label="1" value="1"></el-option>
                    <el-option label="2" value="2"></el-option>
                    <el-option label="3" value="3"></el-option>
                    <el-option label="4" value="4"></el-option>
                    <el-option label="5" value="5"></el-option>
                    <el-option label="6" value="6"></el-option>
                    <el-option label="7" value="7"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="写入地址">
                <el-input
                    placeholder="请输入写入地址"
                    suffix-icon="el-icon-date"
                    v-model="WriteAddr"
                    maxlength="8"
                    show-word-limit>
                </el-input>
            </el-form-item>
            <el-form-item label="入口地址">
                <el-input
                    placeholder="请输入入口地址"
                    suffix-icon="el-icon-date"
                    v-model="EntryAddr"
                    maxlength="8"
                    show-word-limit>
                </el-input>
            </el-form-item>
            <el-upload
            class="upload-demo"
            ref="upload"
            :before-remove="beforeRemove"
            :limit="1"
            :file-list="fileList"
            :on-change="changeFile"
            :on-remove="removeFile"
            :on-exceed="handleExceed"
            :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">开始重构</el-button>
            <div slot="tip" class="el-upload__tip">只能上传bin文件</div>
            </el-upload>
        </el-form>
        <!-- <el-button type="primary" @click="sendArgs">主要按钮</el-button> -->
        <!-- <el-form :inline="true" class="status-form" > -->
            <el-table
              :data="tableData"
              style="width: 100%"
              :row-class-name="tableRowClassName">
              <el-table-column
                prop="num"
                label="核号"
                width="180">
              </el-table-column>
              <el-table-column
                prop="state"
                label="状态"
                width="180">
              </el-table-column>
              <el-table-column
                prop="binname"
                label="执行镜像">
              </el-table-column>
            </el-table>
        <!-- </el-form> -->
    </el-main>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'LayOut',
  data () {
    return {
      corenum: '',
      WriteAddr: '',
      EntryAddr: '',
      fileList: [],
      tableData: [{
        num: '0',
        state: 'running',
        binname: 'Control Core'
      },
      {
        num: '1',
        state: 'stopped',
        binname: ''
      },
      {
        num: '2',
        state: 'stopped',
        binname: ''
      },
      {
        num: '3',
        state: 'stopped',
        binname: ''
      },
      {
        num: '4',
        state: 'stopped',
        binname: ''
      },
      {
        num: '5',
        state: 'stopped',
        binname: ''
      },
      {
        num: '6',
        state: 'stopped',
        binname: ''
      },
      {
        num: '7',
        state: 'stopped',
        binname: ''
      }]
    }
  },
  methods: {
    sendArgs: function () {
      var that = this
      const path = 'http://127.0.0.1:5000/sendArgs'
      axios.get(path, {params: {corenum: that.corenum, EntryAddr: that.EntryAddr, WriteAddr: that.WriteAddr}}).then(response => {
        let msg = response.data.msg
        this.$message('Success' + response.status + ',' + msg)
      }).catch(function (error) {
        this.$message(error)
      })
    },
    changeFile (file, fileList) {
      this.fileList = fileList
    },
    removeFile (file, fileList) {
      this.fileList = fileList // 再一次赋值
    },
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    beforeRemove (file) {
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    submitUpload (file) {
      var formdata = new FormData()
      this.fileList.forEach((val, index) => {
        formdata.append('file', val.raw)
      })
      formdata.append('corenum', this.corenum)
      formdata.append('WriteAddr', this.WriteAddr)
      formdata.append('EntryAddr', this.EntryAddr)
      let config = {
        headers: {'Content-Type': 'multipart/form-data'}
      }
      axios.post('http://127.0.0.1:5000/upload', formdata, config).then(response => {
        this.$message(response.data.msg)
        var index = parseInt(this.corenum)
        this.tableData[index].state = 'running'
        this.tableData[index].binname = formdata.get('file').name
      }).catch(error => {
        if (error.response.status === 400) {
          this.$message.error('参数错误！请检查参数！')
        }
        if (error.response.status === 500) {
          this.$message.error('镜像文件格式错误！请上传bin文件！')
        }
      })
    },
    tableRowClassName ({row, rowIndex}) {
      if (row.state === 'stopped') {
        return 'warning-row'
      } else if (row.state === 'running') {
        return 'success-row'
      }
      return ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-table>>>.warning-row {
  background: rgb(22, 133, 217)
}

.el-table>>>.success-row {
  background: #0ce1da
}
</style>
