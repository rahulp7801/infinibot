require('dotenv').config()
const mongoose = require('mongoose')

const express = require('express')
const cors = require('cors')
const session = require('express-session')
const Store = require('connect-mongo')
const app = express()

const PORT = process.env.PORT || 3002

require('./strategies/discord')
const passport = require('passport')

mongoose.connect(`mongodb+srv://${process.env.MONGO_USER}:${process.env.MONGO_PASS}@infinibot.f381p.mongodb.net/DASHBOARD` , {
    useNewUrlParser: true,
    useUnifiedTopology: true
})

app.use(express.json())
app.use(express.urlencoded({extended: false}))

app.use(cors({
    origin: ['http://localhost:3000'],
    credentials: true
}))

app.use(session({
    secret: process.env.SESSION_SECRET,
    cookie: {
        maxAge: 60000 * 60 * 24
    },
    resave: false,
    saveUninitialized: false,
    store: Store.create({mongoUrl: `mongodb+srv://${process.env.MONGO_USER}:${process.env.MONGO_PASS}@infinibot.f381p.mongodb.net/DASHBOARD`})
}))
app.use(passport.initialize())
app.use(passport.session())

const routes = require('./routes')
app.use('/api', routes)


app.listen(PORT, () => console.log(`Listening on Port ${PORT}`))