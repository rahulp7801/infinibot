// DISCORD RPC
const rpc = require("discord-rpc");
const client = new rpc.Client({ transport: 'ipc' });
const config = {
    "ClientID": "852431558241026058",
    "LargeImage": "test",
    "LargeImageText": "Guest Picks",
    "SmallImage": "djflame_logo",
    "SmallImageText": "DJFlame",
    "Button1": "Join Party",
    "Url1": "https://djflame.tech",
    "State": "17:00",
    "Details": "Playing Never Gonna Give You Up"
}

client.login({ clientId: "852431558241026058" }).catch(console.error);

client.on('ready', () => {
    console.log('Your presence works now check your discord profile :D')
    client.request('SET_ACTIVITY', {
        pid: process.pid,
        activity: {
            details: config.Details,
            state: config.State,
            assets: {
                large_image: config.LargeImage,
                large_text: config.LargeImageText,
                small_image: config.SmallImage,
                small_text: config.SmallImageText,
            },
            buttons: [
                {
                    label: config.Button1, url: config.Url1
                }
            ]
        }
    })
})