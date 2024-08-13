const routes = [

  {
    path: '/login',
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/PageLogin.vue') },
    ]
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/', name: 'Home', component: () => import('src/pages/PageHome.vue') },
      { path: '/camera', name: 'Camera', component: () => import('src/pages/PageCamera.vue') },
      { path: '/post/:id', name: 'Post.detail', component: () => import('src/pages/PagePostDetail.vue') },
      { path: '/profile/:id', name: 'Profile', component: () => import('src/pages/PageProfile.vue') },
      { path: '/chat/:id', name: 'ChatRoom', component: () => import('src/pages/chat/PageChat.vue') },
      { path: '/chat', name: 'ChatIndex', component: () => import('src/pages/chat/PageIndexChat.vue') },
      { path: '/user-list', name: 'UserList', component: () => import('src/pages/PageUserList.vue') },
    ]
  },
  /*{
    path: '/post/:id',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'post.detail', component: () => import('src/pages/PagePostDetail.vue') },
    ]
  },*/

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
