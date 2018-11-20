const jsonServer = require('json-server')
const server = jsonServer.create()
const router = jsonServer.router('db.json')
const rewriter = jsonServer.rewriter({
    "/image/1/img.jpg": "/img0.jpg",
    "/next": "/image/1",
    "/target/1/thumb.jpg": "/target01.jpg"
});
const middlewares = jsonServer.defaults()

server.use(rewriter)
server.use(middlewares)
server.use(jsonServer.bodyParser)
server.use((req, res, next) => {
    if (req.method === "POST" && req.path === '/image/1/targets') {
        router.db.write().then((db) => {
            db.image[0].targets.push(req.body);
            res.status(201).jsonp(req.body);
        });
    }
    else {
        next();
    }
})
server.use(router)
server.listen(5000, () => {
    console.log('Server is running on port 5000')
})