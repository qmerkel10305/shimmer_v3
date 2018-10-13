const jsonServer = require('json-server')
const server = jsonServer.create()
const router = jsonServer.router('db.json')
const rewriter = jsonServer.rewriter({
    "/image/1/img.jpg": "/img0.jpg",
    "/next": "/image/1"
});
const middlewares = jsonServer.defaults()

server.use(rewriter)
server.use(middlewares)
server.use(router)
server.listen(5000, () => {
    console.log('Server is running on port 5000')
})