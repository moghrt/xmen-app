const isLoggedIn = () => {
    return localStorage.getItem('access_token') ? true : false;
};

const protectedRoutes = [
    "Home",
    "Camera",
    "Post.detail",
    "Profile",
    "UserList",
    "ChatIndex",
    "ChatRoom",
]
export { isLoggedIn, protectedRoutes };
