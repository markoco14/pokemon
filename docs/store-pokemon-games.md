# Move pokemon games from in-memory dict to database

Who's That Pokemon games are currently stored in application memory.

Every time the server crashes or restarts, the games are wiped.

While that is OK, I'd like to preserve games with a database and use sql to interact with game state

I'm going to make general game and game_guess tables.

I'll handle the game theming at the endpoint level.