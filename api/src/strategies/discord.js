const passport = require('passport')
const DiscordStrategy = require('passport-discord')
const User = require('../database/schemas/user')

passport.serializeUser((user, done) => {
    done(null, user.discordId)
})

passport.deserializeUser(async (discordId, done) => {
    try {
        const user = await User.findOne({discordId})
        return user ? done(null, user) : done(null, null)
    } catch (err) {
        console.error(err)
        return done(err, null)
    }
})

passport.use(new DiscordStrategy({
    clientID: process.env.DASHBOARD_CLIENT_ID,
    clientSecret: process.env.DASHBOARD_CLIENT_SECRET,
    callbackURL: process.env.DASHBOARD_CALLBACK_URL,
    scope: ['identify', 'guilds']
}, async (accessToken, refreshToken, profile, done) => {
    const {id, username, discriminator, avatar, guilds} = profile
    console.log(id, username, discriminator, avatar)
    try {
        const findUser = await User.findOneAndUpdate({discordId: id}, {
            discordTag: `${username}#${discriminator}`,
            avatar,
            guilds
        }, {new: true, useFindAndModify: true})
        if (findUser) {
            console.log(`User ${username}#${discriminator} (${id}) was found and his data was updated!`)
            return done(null, findUser)
        } else {
            const newUser = User.create({
                discordId: id,
                discordTag: `${username}#${discriminator}`,
                avatar,
                guilds
            })
            return done(null, newUser)
        }
    } catch (err) {
        console.error(err)
        return done(err, null)
    }
}))