
const SignIn = () => {
  return (
    <form action="login.php" method="POST">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required> </input>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required> </input>
        </div>
        <button type="submit">Log In</button>
    </form>
  );
};

export default SignIn;