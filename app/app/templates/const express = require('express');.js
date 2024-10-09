const express = require('express');
const Web3 = require('web3');
const mysql = require('mysql2');

// Connect to Ganache
const web3 = new Web3('http://127.0.0.1:7545');

// Connect to MySQL
const db = mysql.createConnection({
    host: '127.0.0.1',
    port: 5000,
    user: 'root',
    password: 'root8',
    database: 'organ_donation'
});

db.connect(err => {
    if (err) {
        console.error('MySQL connection failed:', err.stack);
        return;
    }
    console.log('Connected to MySQL on port 5000');
});

// Initialize Express
const app = express();

// Example route to interact with smart contract
app.get('/storeData', async (req, res) => {
    try {
        const accounts = await web3.eth.getAccounts();
        const contract = new web3.eth.Contract(abi, contractAddress);

        // Call a method from the smart contract
        const result = await contract.methods.someFunction().call({ from: accounts[0] });

        // Insert data into MySQL
        const query = 'INSERT INTO your_table (data) VALUES (?)';
        db.query(query, [result], (err, results) => {
            if (err) {
                console.error(err);
                res.status(500).send('Error storing data');
            } else {
                res.send('Data stored successfully');
            }
        });
    } catch (error) {
        console.error(error);
        res.status(500).send('Error interacting with the contract');
    }
});

// Start the server
app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
