import React from 'react'
import { MenuComponent } from '../../components/MenuWrapper'

import { getGuilds, getUserDetails } from '../../utils/api'
import './index.css'

export function MenuPage(props) {

    const [user, setUser] = React.useState(null)
    const [loading, setLoading] = React.useState(true)
    const [guilds, setGuilds] = React.useState([])

    React.useEffect(() => {
        getUserDetails().then(({ data }) => {
            console.log(data)
            setUser(data)
            setLoading(false)
            return getGuilds()
        }).then(({ data }) => {
            console.log(data)
            setGuilds(data)
        }).catch((err) => {
            console.error(err)
            setLoading(false)
            window.location = 'http://localhost:3001/api/auth/discord'
        })
    }, [])

    return !loading && (
        <div class="menuPage">
            <h1>Choose a Server</h1>
            <MenuComponent guilds={guilds}/>
        </div>

    )
}