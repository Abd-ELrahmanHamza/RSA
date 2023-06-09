<div align="center">
<img height="300" src="./images/banner.jpg">
<h1/>
</div>

<div align="center">
    <h1 align='center'>⚡️<i>RSA</i>⚡️</h1>
    <p> A widely used for secure data transmission.</p>
</div>

<h2 style="display:inline">📝 Table of Contents</h2>

- 📑 About
- ⛏️ Built With
- 🏁 Getting started
- ✍️ Contributors
- 🔒 License

## 📑 About

- A chat app that implements RSA encryption for secure communication
- The application follows a client-server architecture, where multiple clients connect to a single server. Each client has two separate threads one for sending messages and another for receiving messages. On the server-side, A dedicated thread for each connected client to handle their messages.
- We have implemented an attack algorithm to evaluate how the strength of the algorithm is affected by the key size. The objective is to test the effectiveness of the encryption technique under different key sizes and assess its level of security.


![effect of key size on algorithm strength](./images/graph.png)
## ⛏️ Built With

- Python
- Sympy
- socket
- Threading

## 🏁 Getting started

### Run the server

```bash
$ python server.py
```

### Run first client

```bash
$ python client.py
```

### Run second client

```bash
$ python client.py
```

## ✍️ Contributors

<table>
  <tr>

<td align="center">
<a href="https://github.com/Abd-ELrahmanHamza" target="_black">
<img src="https://avatars.githubusercontent.com/u/68310502?v=4" width="150px;" alt="Abdelrahman Hamza"/><br /><sub><b>Abdelrahman Hamza</b></sub></a><br />
</td>

</tr>
 </table>

## 🔒 License <a name = "license"></a>

> This software is licensed under MIT License, See [License](https://github.com/CMP24-SWE-TEAM3/Front-End/blob/main/LICENSE) .
