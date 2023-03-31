require("dotenv").config();
// set up tmi.js bot package
const tmi = require("tmi.js");
const fetch = require("node-fetch");
//connect to twitch
const opts = {
  identity: {
    username: "mechachrissie",
    password: `oauth:${process.env.OAUTH_TOKEN}`,
  },
  channels: ["chrissiecodes"],
};

const client = new tmi.Client(opts);

// Register our event handlers (defined below)
client.on("message", onVibesHandler);
client.on("connected", onConnectedHandler);
client.on("message", onMessageHandler);

// Connect to Twitch:
client.connect();
//TODO:fix vibes they utilize !vibes in the chat message with the calculation
async function onMessageHandler(target, context, msg, self) {
  if (self || context["display-name"] === "StreamElements") {
    return;
  }
  const commandName = msg.trim();
  const user = context["display-name"];
  const messageLength = msg.split(/\s+/).length;
  const sanitizedMsg = commandName.replace(/`/g, "");
  const messageID = context.id;
  const sentence = sanitizedMsg;
  request_chat = JSON.stringify({ message: sentence });
  const response = await fetch("http://127.0.0.1:8000/chat/", {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: request_chat,
  });
  const data = await response.json();
  if (data.positive + data.negative === 0) {
    return;
  }
  post_chat = JSON.stringify({
    username: user,
    positive: data.positive,
    neutral: data.neutral,
    negative: data.negative,
    number_of_chats: 1,
  });
  const url = `http://127.0.0.1:8000/sentiment/`;
  const put = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: post_chat,
  });

  const goodvibes = `${Math.round(data.positive * 100, 3)}`;
  const badvibes = `${Math.round(data.negative * 100, 3)}`;
  const compound = `${Math.round(data.compound * 100, 3)}`;
  console.log(
    target,
    `${user}, your chat is ${goodvibes - badvibes}% Good Vibes; compound is ${compound}`,
    messageID
  );
}

/**
 * This function is for !vibes
 * @param {*} target
 * @param {*} context
 * @param {*} msg
 * @param {*} self
 * @returns
 */
async function onVibesHandler(target, context, msg, self) {
  if (self || context["display-name"] === "StreamElements") {
    return;
  } // Ignore messages from the bot

  // Remove whitespace from chat message
  const commandName = msg.trim();

  const user = context["display-name"];

  const messageLength = msg.split(/\s+/).length;
  const sanitizedMsg = commandName.replace(/`/g, "");
  const messageID = context.id;
  if (commandName.startsWith("!vibes")) {
    const sentence = sanitizedMsg.split("!vibes ")[1];
    request_chat = JSON.stringify({ message: sentence });
    const response = await fetch("http://127.0.0.1:8000/chat/", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: request_chat,
    });
    const data = await response.json();
    const goodvibes = `${Math.round(data.positive * 100, 3)}`;
    const badvibes = `${Math.round(data.negative * 100, 3)}`;
    const compound = `${Math.round(data.compound * 100, 3)}`;
    const allchat = await fetch("http://127.0.0.1:8000/sentiment/{user}", {
      headers: { "Content-Type": "application/json" },
      method: "Get",
    });
    console.log(allchat)
    console.log(`* Executed ${commandName} command`);
    client.reply(
      target,
      `${user}, your chat is ${goodvibes - badvibes}% Good Vibes;`,
      messageID
    );
    // client.say(target,`${user}, your chat is ${goodvibes-badvibes}% Good Vibes `);
  }
}

async function onVibeRatingHandler(target, context, msg, self) {
  if (self || context["display-name"] === "StreamElements") {
    return;
  } // Ignore messages from the bot

  // Remove whitespace from chat message
  const commandName = msg.trim();

  const user = context["display-name"];

  const sanitizedMsg = commandName.replace(/`/g, "");
  if (commandName.startsWith("!viberating")) {
    const response = await fetch("http://127.0.0.1:8000/totals/{user}", {
      headers: { "Content-Type": "application/json" },
      method: "Get",
    });
    const data = await response.json();
    const rank = data.rank;
    const count = data.user_count
    client.reply(
      target,
      `${user}, you are ranked ${rank} out of ${count} users;`,
    );
    const allchat = await fetch("http://127.0.0.1:8000/sentiment/{user}", {
      headers: { "Content-Type": "application/json" },
      method: "Get",
    });
    console.log(allchat)
    console.log(`* Executed ${commandName} command`);
    client.reply(
      target,
      `${user}, you are ranked ${rank} out of ${count} users;`,
    );
    // client.say(target,`${user}, your chat is ${goodvibes-badvibes}% Good Vibes `);
  }
}
function onConnectedHandler(addr, port) {
  console.log(`* Connected to ${addr}:${port}`);
}
