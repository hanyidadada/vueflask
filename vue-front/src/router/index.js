import Vue from 'vue'
import Router from 'vue-router'
import ElementUI from 'element-ui'
import HelloWorld from '@/components/HelloWorld'
import Layout from '@/components/Layout'

Vue.use(Router)
Vue.use(ElementUI)
export default new Router({
  routes: [
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/Layout',
      name: 'Layout',
      component: Layout
    }
  ]
})
