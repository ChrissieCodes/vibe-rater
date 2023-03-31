const Fs = require("fs");
const http = require("http");
const { parse } = require("csv-parse");

const wordLookup = {
  positive: [],
  negative: [],
};

const parser = parse(
  {
    delimiter: ",",
  },
  (err, data) => {
    if (err) {
      throw err;
    }

    // Do yo thang grrrl!

    const headerRow = data.shift();

    data.forEach((row) => {
      const [id, negative, positive] = row;

      wordLookup.positive.push(positive);
      wordLookup.negative.push(negative);
    });
  }
);
Fs.createReadStream("./connotation.csv").pipe(parser);
console.log(wordLookup);
