import Vue from 'vue'
import Router from 'vue-router'
import ElementUI from 'element-ui'
import HelloWorld from '@/components/HelloWorld'
import Layout from '@/components/Layout'
import ShowPic from '@/components/ShowPic'

Vue.use(Router)
Vue.use(ElementUI)
export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      meta: {index: 1},
      component: HelloWorld
    },
    {
      path: '/Layout',
      name: 'Layout',
      meta: {index: 2},
      component: Layout
    },
    {
      path: '/ShowPic',
      name: 'ShowPic',
      meta: {index: 3},
      component: ShowPic
    }
  ]
})
