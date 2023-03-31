const tmi = require("tmi.js");

const client = new tmi.Client({ channels: ["mechachrissie"] });

client.connect()

client.on('message', (channel, tags, message, self) => {
    // "Alca: Hello, Chat!"
    console.log(`${tags['display-name']}: ${message}`);
});

