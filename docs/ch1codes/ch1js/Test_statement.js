// Test_statement.js
const { statement } = require('./statement.js');
const plays = require('./plays.json');
const invoices = require('./invoices.json') 


context = statement(invoices, plays);

console.log(context);