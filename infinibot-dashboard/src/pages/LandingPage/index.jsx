
export function LandingPage(props) {
    const login = () => window.location.href = '/dashboard/menu'
    return (
        <div>
            <h1>Landing Page</h1>
        <button onClick={() => login()}>Dashboard</button>
        </div>
    )
}