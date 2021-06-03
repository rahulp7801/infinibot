const fetch = require('node-fetch')

async function getBotGuilds() {
    const response = await fetch('http://discord.com/api/v6/users/@me/guilds', {
        method: "GET",
        headers: {
            Authorization: `Bot ${process.env.BOT_TOKEN}`
        }
    })
    return response.json()
}

async function getGuildInfo(guildID) {
    const response = await fetch('http://discord.com/api/v6/guilds/' + guildID, {
        method: "GET",
        headers: {
            Authorization: `Bot ${process.env.BOT_TOKEN}`
        }
    })
    return response.json()
}

async function getGuildChannels(guildID) {
    const response = await fetch('http://discord.com/api/v6/guilds/' + guildID + '/channels', {
        method: "GET",
        headers: {
            Authorization: `Bot ${process.env.BOT_TOKEN}`
        }
    })
    return response.json()
}

async function getGuildBans(guildID) {
    const response = await fetch('http://discord.com/api/v6/guilds/' + guildID + '/bans', {
        method: "GET",
        headers: {
            Authorization: `Bot ${process.env.BOT_TOKEN}`
        }
    })
    return response.json()
}

async function getUserInfo(uID) {
    const response = await fetch('http://discord.com/api/v6/users/' + uID, {
        method: "GET",
        headers: {
            Authorization: `Bot ${process.env.BOT_TOKEN}`
        }
    })
    return response.json()
}


module.exports =  {getBotGuilds, getGuildInfo, getGuildChannels, getGuildBans, getUserInfo}