const router = require('express').Router()
const { getBotGuilds, getGuildInfo, getGuildChannels, getGuildBans, getUserInfo } = require('../utils/api')
const User = require('../database/schemas/user')
const { getMutualGuilds, checkUserGuildPerms, removeArrayItem } = require('../utils/utils')
const GuildConfig = require('../database/schemas/GuildConfig')

var MongoClient = require('mongodb').MongoClient;

router.get('/guilds', async (req, res) => {
    const guilds = await getBotGuilds()

    const user = await User.findOne({ discordId: req.user.discordId })
    if (user) {
        const userGuilds = user.get('guilds')
        const mutualGuilds = getMutualGuilds(userGuilds, guilds)
        res.send(mutualGuilds)
    } else res.status(401).send({ msg: "Unauthorized" })
})



router.put('/guilds/:guildId/prefix', async (req, res) => {
    const { prefix } = req.body
    const { guildId } = req.params

    if (!prefix) return res.status(400).send({ "msg": "Prefix Required" })

    if (!req.user || !checkUserGuildPerms(req.user.guilds, guildId)) return res.status(401).send({ "msg": "User Does not have Sufficent Permissions" })

    const guilds = await getBotGuilds()
    var done = false
    await guilds.forEach((guild) => {
        if (guild.id == guildId) {
            done = true
            const url = `mongodb+srv://${process.env.MONGO_USER}:${process.env.MONGO_PASS}@infinibot.f381p.mongodb.net/`;
            MongoClient.connect(url, async (err, guildDBO) => {
                if (err) {
                    console.error(err)
                    res.status(500).send({ msg: "We could not connect to your Server Config, try again later. If this persists, contact us" })
                    return err
                } else {
                    const guildDB = guildDBO.db(`GUILD${guildId}`)
                    const config = guildDB.collection("config")
                    const guildConfig = await guildDB.collection("config").findOne({})
                    const name = guildConfig.name
                    const update = await config.updateOne({ name: name }, { $set: { prefix: prefix } })
                    guildDBO.close()
                    return update ? res.status(200).send({ msg: "Update Accepted!" }) : res.status(500).send({ msg: "We could not update your Server Config, try again later. If this persists, contact us" })
                }
            })
            return true
        }
    })

    if (!done) {
        return res.status(400).send({ msg: "InfiniBot is Not In the Provided Server" })
    }
})

router.get('/guilds/:guildId/config', async (req, res) => {
    const { guildId } = req.params;

    if (!req.user || !checkUserGuildPerms(req.user.guilds, guildId)) return res.status(401).send({ "msg": "User Does not have Sufficent Permissions" })

    const guilds = await getBotGuilds()
    var done = false
    await guilds.forEach(async (guild) => {
        if (guild.id == guildId) {
            done = true
            const url = `mongodb+srv://${process.env.MONGO_USER}:${process.env.MONGO_PASS}@infinibot.f381p.mongodb.net/`;
            MongoClient.connect(url, async (err, guildDBO) => {
                if (err) {
                    console.error(err)
                    res.status(500).send({ msg: "We could not connect to your Server Config, try again later. If this persists, contact us" })
                    return err
                } else {
                    const guildDB = guildDBO.db(`GUILD${guildId}`)
                    const config = guildDB.collection("config")
                    const guildConfig = await guildDB.collection("config").findOne({})
                    const name = guildConfig.name
                    const data = await config.findOne({ name: name })
                    guildDBO.close()
                    console.log(data)
                    return data ? res.status(200).send(data) : res.status(404).send({ msg: "We could not find your Server Config, try again later. If this persists, contact us" })
                }
            })
            return true
        }
    })

    if (!done) {
        return res.status(400).send({ msg: "InfiniBot is Not In the Provided Server" })
    }
})

router.get('/guilds/:guildId/info', async (req, res) => {
    const { guildId } = req.params

    if (!req.user || !checkUserGuildPerms(req.user.guilds, guildId)) return res.status(401).send({ "msg": "User Does not have Sufficent Permissions" })

    const info = await getGuildInfo(guildId)
    const channels = await getGuildChannels(guildId)

    const result = {
        info: info,
        channels: channels
    }

    return info && channels ? res.status(200).send(result) : res.status(404).send({ msg: "Info Not Found" })
})

router.get('/guilds/:guildId/modinfo', async (req, res) => {
    const { guildId } = req.params;

    if (!req.user || !checkUserGuildPerms(req.user.guilds, guildId)) return res.status(401).send({ "msg": "User Does not have Sufficent Permissions" })

    const guilds = await getBotGuilds()
    var done = false
    await guilds.forEach(async (guild) => {
        if (guild.id == guildId) {
            done = true
            const url = `mongodb+srv://${process.env.MONGO_USER}:${process.env.MONGO_PASS}@infinibot.f381p.mongodb.net/`;
            MongoClient.connect(url, async (err, guildDBO) => {
                if (err) {
                    console.error(err)
                    res.status(500).send({ msg: "We could not connect to your Server Config, try again later. If this persists, contact us" })
                    return err
                } else {
                    const guildDB = guildDBO.db(`GUILD${guildId}`)
                    const guildWarns = await guildDB.collection("warns").find().toArray()
                    const bans = await getGuildBans(guildId)
                    guildWarns.splice(0, 1)
                    const data = {
                        warns: guildWarns,
                        bans: bans,
                        logs: [{action: "BAN", moderator: 13234332334}]
                    }
                    guildDBO.close()
                    return data ? res.status(200).send(data) : res.status(404).send({ msg: "We could not find your Server Config, try again later. If this persists, contact us" })
                }
            })
            return true
        }
    })

    if (!done) {
        return res.status(400).send({ msg: "InfiniBot is Not In the Provided Server" })
    }
})

router.get('/user/:uID/info', async (req, res) => {
    const {uID} = req.params

    if (!uID) return res.status(400).send({msg: "User ID is Required"})

    const data = await getUserInfo(uID)
    return data ? res.status(200).send(data) : res.status(404).send({ msg: "We could not find your Server Config, try again later. If this persists, contact us" })
})

module.exports = router