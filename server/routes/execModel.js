const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');

router.post('/',async (req,res)=>{
    const body = await req.body
    const player = body.player
    const opp_team= body.oppteam
    
    rs = await executePythonone('/home/modiji/Balls/hack-a-sol/server/execModel.py',player,opp_team)

    sr = await executePythonTwo('/home/modiji/Balls/hack-a-sol/server/execStrike.py',player,opp_team)

    res.json({
        run_scored : rs,
        strike_rate : sr
    })


});

module.exports = router;


const executePythonone = async (script, arg2, arg3) => {
  try{
        const py = spawn("python", [script, arg2, arg3]);

          const result = await new Promise((resolve, reject) => {
            let output = '';

            py.stdout.on('data', (data) => {
              output += data.toString();
            });

            py.stderr.on("data", (data) => {
              console.error(`[python] Error occurred: ${data}`);
              reject(`Error occurred in ${script}`);
            });

            py.on("exit", (code) => {
              if (code === 0) {
                resolve(output);
              } else {
                reject(`Child process exited with code ${code}`);
              }
            });
          });

          return result;

    }catch(err){
        return 'Not In Database'
    }
}


const executePythonTwo = async (script, arg2, arg3) => {
  try{
        const py = spawn("python", [script, arg2, arg3]);

          const result = await new Promise((resolve, reject) => {
            let output = '';

            py.stdout.on('data', (data) => {
              output += data.toString();
            });

            py.stderr.on("data", (data) => {
              console.error(`[python] Error occurred: ${data}`);
              reject(`Error occurred in ${script}`);
            });

            py.on("exit", (code) => {
              if (code === 0) {
                resolve(output);
              } else {
                reject(`Child process exited with code ${code}`);
              }
            });
          });

          return result;

    }catch(err){
        return 'Not in Database'
    }
}
