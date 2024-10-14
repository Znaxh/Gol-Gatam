const express = require('express');
const cors = require('cors');
const { MongoClient, ServerApiVersion } = require('mongodb');
const playerRoutes = require('./routes/playerRoutes');
const execRoutes = require('./routes/execModel');

const app = express();

// Middleware
app.use(cors(
  {
    origin: ["https://gol-gatam.vercel.app/"],
    methods: ["POST", "GET"],
    credentials: true
  }
));
app.use(express.json());

const uri = "mongodb+srv://hackasolclient:xAt9qV3IRBGk1eZL@hack-a-sol.pc9l3.mongodb.net/?retryWrites=true&w=majority&appName=hack-a-sol";
let db;

async function connectMongoDB() {
  const client = new MongoClient(uri, {
    serverApi: {
      version: ServerApiVersion.v1,
      strict: true,
      deprecationErrors: true,
    }
  });

  try {
    await client.connect();
    db = client.db('cricket_db');
    console.log("MongoDB connected");
  } catch (err) {
    console.error("Failed to connect to MongoDB", err);
    process.exit(1);
  }
}

// Routes
app.use('/api', (req, res, next) => {
  req.db = db;
  next();
}, playerRoutes);
app.use('/predict', execRoutes);

const PORT = process.env.PORT || 5000;

// Start server after connecting to the database
connectMongoDB().then(() => {
  app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
});

// Graceful shutdown
process.on('SIGINT', async () => {
  await db.client.close();
  console.log('MongoDB connection closed');
  process.exit(0);
});

