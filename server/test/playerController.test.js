
// server/test/playerController.test.js
const request = require('supertest');
const express = require('express');
const { getPlayer } = require('../controllers/playerController');
const { expect } = require('chai');

const app = express();
app.use(express.json());
app.get('/api/players', getPlayer); // Use relative path for the route

describe('GET /api/players', () => {
    it('should return players with default limit and offset', async () => {
        const response = await request(app).get('/api/players?limit=5&offset=0'); // Use relative path
        expect(response.status).eq(200);
        expect(response.body).instanceOf(Array);
        expect(response.body.length).eq(5);
    });

    it('should return players with specific limit and offset', async () => {
        const response = await request(app).get('/api/players?limit=2&offset=2'); // Use relative path
        expect(response.status).eq(200);
        expect(response.body).instanceOf(Array);
        expect(response.body.length).eq(2);
    });

    it('should handle invalid queries gracefully', async () => {
        const response = await request(app).get('/api/players?limit=invalid&offset=invalid'); // Use relative path
        expect(response.status).eq(200); // Adjust based on how you handle errors
        expect(response.body).instanceOf(Array);
    });
});

