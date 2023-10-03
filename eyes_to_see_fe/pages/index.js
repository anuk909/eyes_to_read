
export default function HomePage() {
    return <div style={{textAlign: "center"}}>
    <h1>Eyes To See</h1>
    <br />
    <br />
    <form>
    <label htmlFor="username">Username: </label>
    <input type="text" id="username" name="username" />
    <br />
    <br />
    <label htmlFor="password">Password: </label>
    <input type="text" id="password" name="password" />
    <br />
    <br />
    <input type="submit" defaultValue="Submit" />
    </form>
    </div>
}