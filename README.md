# Four In A Row (Python)
**Project Overview - Server-Client Game Architecture**

This project focuses on implementing a server-client architecture for a game. The architecture comprises two sides: the client, which interacts with and plays the game, and the server, which manages the game's operation. The server enables multiple clients to play simultaneously, updates game progress, and offers different difficulty levels. Communication between the server and clients utilizes the reliable TCP protocol.

**Server:**
The server code handles client connections and implements game logic. It includes functions for setting up the server, checking available positions in the game, and managing different game scenarios, including victory conditions and blocking opponents.

**Client:**
The client code operates alongside the server and communicates with it to play the game. It collects user preferences, interacts with the server, displays game updates, and sends column choices to the server for validation.

This project showcases the implementation of a simple game using a server-client architecture, demonstrating communication, decision-making, and user interaction aspects.
