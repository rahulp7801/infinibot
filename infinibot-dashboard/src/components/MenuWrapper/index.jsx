import { React } from 'react'
import addServer from '../../assets/addServer.svg'

export function MenuComponent({
    history,
    guilds
}) {
    function addServerRedirect() {
        window.location.href = "https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands"
    }
    function dashboardRedirect(guildID) {
        window.location = 'server/' + guildID + '/config'
    }
    return (
        <div class="serverList">
            {guilds.map((guild) => (
                <div class="picture" onClick={() => dashboardRedirect(guild.id)}>
                    <img id='profil' src={`https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.png`} alt={guild.name}/>
                    <h5>Go To Dashboard</h5>
                </div>
            ))}
            <div class="picture addServer" onClick={addServerRedirect}>
                <img id='profil' class="addServerImage" src={addServer} alt="Add Server"/>
            </div>
        </div>
    )
}