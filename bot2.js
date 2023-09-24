require("dotenv").config();

//environment, because I stream (sorry ya'll)
const HOST = "http://127.0.0.1:8000"

// set up tmi.js bot package
const tmi = require("tmi.js");
const fetch = require("node-fetch");
//connect to twitch
const opts = {
  identity: {
    username: "mechachrissie",
    password: `oauth:${process.env.OAUTH_TOKEN}`,
  },
  channels: ["marximusmaximus"],
};

const client = new tmi.Client(opts);

// Register our event handlers (defined below)
client.on("message", onVibesHandler);
client.on("connected", onConnectedHandler);
client.on("message", onMessageHandler);
client.on("message", onVibeRatingHandler);
client.on("message", onSerialBubbler);

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
  const response = await fetch(`${HOST}/chat/`, {
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
  const url = `${HOST}/sentiment/`;
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
    `${user}, your chat is ${
      goodvibes - badvibes
    }% Good Vibes; compound is ${compound}`,
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
  } 
  const commandName = msg.trim();

  const user = context["display-name"];

  const messageLength = msg.split(/\s+/).length;
  const sanitizedMsg = commandName.replace(/`/g, "");
  const messageID = context.id;
  if (commandName.startsWith("!vibes")) {
    const sentence = sanitizedMsg.split("!vibes ")[1];
    console.log(sentence)
    request_chat = JSON.stringify({ message: sentence });
    const response = await fetch(`${HOST}/chat/`, {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: request_chat,
    });
    const data = await response.json();
    const goodvibes = `${Math.round(data.positive * 100, 3)}`;
    const badvibes = `${Math.round(data.negative * 100, 3)}`;
    const compound = `${Math.round(data.compound * 100, 3)}`;
    const allchat = await fetch(`${HOST}/sentiment/`, {
      headers: { "Content-Type": "application/json" },
      method: "Get",
    });
    console.log(allchat);
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
  }
  const commandName = msg.trim();

  const user = context["display-name"];

  const sanitizedMsg = commandName.replace(/`/g, "");
  const messageID = context.id;
  if (commandName.startsWith("!viberating")) {
    const response = await fetch(`${HOST}/totals/`, {
      headers: { "Content-Type": "application/json" },
      method: "Get",
    });
    const data = await response.json();
    let chat_total=0
    for (let row of data){chat_total+=row.vibe_total;}
    let chat_average = chat_total/(data.length || 1)
    let result = [];
    data.reduce(function(res, value) {
      if (!res[value.username]) {
        res[value.username] = { username: value.username, vibe_total: 0 };
        result.push(res[value.username])
      }
      res[value.username].vibe_total += value.vibe_total;
      return res;
    }, {});
    result.sort((a,b)=> b.vibe_total- a.vibe_total)
    console.log(result)
    user_index = result.findIndex(row => row.username === user)
    total_length = result.length
    console.log(`* Executed ${commandName} command`);
    client.reply(
      target,
      `${user}, you are the  #${user_index + 1} ranked user of good vibes out of ${total_length} users. The average vibe in chat is ${chat_average*100}%;`,
      messageID
    );
    // client.say(target,`${user}, your chat is ${goodvibes-badvibes}% Good Vibes `);
  }
}
function onConnectedHandler(addr, port) {
  console.log(`* Connected to ${addr}:${port}`);
}
async function onSerialBubbler(target, context, msg, self) {
  
  if (self || context["display-name"] === "mechachrissie") {
    const commandName = msg.trim();
    // const sanitizedMsg = commandName.replace(/`/g, "");
    if (commandName.startsWith("!irlBubbles")) {
      const response = await fetch("http://127.0.0.1:8000/serial/", {
        headers: { "Content-Type": "application/json" },
        method: "Get",
      });
  }
}}