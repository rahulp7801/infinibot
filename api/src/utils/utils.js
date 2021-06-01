function getMutualGuilds(userGuilds, botGuilds) {
    return userGuilds.filter((guild) => botGuilds.find((botGuild) => (botGuild.id === guild.id) && ((guild.permissions & 0x20) === 0x20)))
}

function checkUserGuildPerms(discordUserGuilds, guildID) {
    const guild = discordUserGuilds.find(x => x.id === guildID);
if ((guild.permissions & 0x20) === 0x20) {
    return true
} else return false
}

module.exports = {getMutualGuilds, checkUserGuildPerms}