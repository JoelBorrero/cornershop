def form(action, fields):
    return f'<form action="{action}" method="post">{"<br>".join([input_field(i) for i in fields])}' \
           f'<br><input type="submit" value="Submit"></form>'


def h1(text):
    return f'<h1>{text}</h1>'


def input_field(field):
    return f'<label for="{field["id"]}">{field["label"]}</label><br>' \
           f'<input type="{field["type"]}" id="{field["id"]}" name="{field["id"]}">'


def javascript():
    return """
    <button onclick="logout()">Cerrar sesión</button>
    <script>
        function login() {
            let username = document.getElementById("username").value;
            let password = document.getElementById("password").value;
            fetch("../auth/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: username, password: password }),
            }).then((response) => {
                console.log(response.data);
            });
        }
        function logout() {
            fetch("../auth/logout/", { method: "POST", headers:{"Authorization": "Token 1866490c83984786bcb2e50a6c80a2e3be849dfd","Content-Type": "application/json"    } });
        }

    </script>
    """
