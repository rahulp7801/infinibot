import axios from 'axios'

export function getUserDetails() {
    return axios.get('http://localhost:3001/api/auth', {withCredentials: true})
}

export function getGuilds() {
    return axios.get('http://localhost:3001/api/discord/guilds', {withCredentials: true})
}

export function postNewPrefix(guildID, prefix) {
    return axios.put(`http://localhost:3001/api/discord/guilds/${guildID}/prefix`, {prefix: prefix}, {withCredentials: true})
}

export function getGuildInfo(guildID) {
    return axios.get(`http://localhost:3001/api/discord/guilds/${guildID}/info`, {withCredentials: true})
}
export function getGuildConfig(guildID) {
    return axios.get(`http://localhost:3001/api/discord/guilds/${guildID}/config`, {withCredentials: true})
}