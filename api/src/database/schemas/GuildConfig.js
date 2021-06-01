const mongoose = require('mongoose')

const GuildConfigSchema = new mongoose.Schema(
    {

        // _id: {
        //     type: String,
        //     required: true
        // },
        name: {
            type: String,
            required: true
        },
        prefix: {
            type: String,
            required: true
        },
        welcomemsg: {
            type: String,
            required: true
        },
        welcomechannel: {
            type: Number,
            required: true
        },
        priv_welcomemsg: {
            type: String,
            required: true
        },
        leavemsg: {
            type: String,
            required: true
        },
        captchaon: {
            type: String,
            required: true
        },
        muterole: {
            type: String,
            required: true
        },
        spamdetect: {
            type: String,
            required: true
        },
        logging: {
            type: String,
            required: true
        },
        logchannel: {
            type: String,
            required: true
        },
        levelups: {
            type: String,
            required: true
        },
        ghostpingon: {
            type: String,
            required: true
        },
        ghostcount: {
            type: String,
            required: true
        },
        blacklistenab: {
            type: String,
            required: true
        },
        mcip: {
            type: String,
            required: true
        },
        starchannel: {
            type: String,
            required: true
        },
        welcomenick: {
            type: String,
            required: true
        },
        welcomerole: {
            type: String,
            required: true
        }
    }
)

module.exports = mongoose.model('GuildConfig', GuildConfigSchema)

