const express = require('express');
const {spawn} = require('child_process');
const path = require('path');
const { Z_DEFAULT_COMPRESSION } = require('zlib');
const router = express.Router();
const basePath = path.join(__dirname, '../', 'pyroscripts')
//let pred_PV, smp, P2P, RT_Pnet

router.post('/', function(req,res, next) {
  let index = req.body.index
  let script = "script"+index+".py";
  let args = []
  args.push(index)
  /*if(index=="KPU_10")
  {
    args.push(pred_PV);
  }
  else if(index=="KPU_11")
  {
    args.push(smp);
  }
  else if(index=="KPU_12")
  {
    args.push(P2P);
  }
  else if(index=="POSTECH_8")
  {
    args.push(RT_Pnet)
  }*/
  //args.push(eval(req.body.arguments))
  //args.push(req.body.arguments.split(' '))
  let exec = [path.join(basePath, script)].concat(args)
  console.log(exec)
  let result;
  // spawn new child process to call the python script
  let python = spawn('python', exec);

  // collect data from script
  python.stdout.on('data', function (data) {
    console.log('Pipe result from python script ... ' + exec.join(' '));
    result = data.toString();
    console.log("RESULT: "+result)
    /*if(index=="POSTECH_6")
    {
      pred_PV = result;
    }
    else if(index="KPU_10")
    {
      smp = result;
    }
    else if(index="KPU_11")
    {
      P2P = result;
    }
    else if(index="KPU_12")
    {
      RT_Pnet = result;
    }*/
  });

  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);

    // send data to client
    res.status(200).json({
      script: exec.join(' '),
      result: result,
    });
  });
})

module.exports = router;