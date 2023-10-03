

export default function HomePage() {
    return <>
    <form action="/action_page.php">
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
    </>
}