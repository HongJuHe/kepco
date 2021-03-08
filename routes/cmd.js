const express = require('express');
const {spawn, exec} = require('child_process');
const path = require('path');
const { Z_DEFAULT_COMPRESSION } = require('zlib');
const router = express.Router();
const basePath = path.join(__dirname, '../', 'pyroscripts')

var req_info = {
    python : "",
    result : undefined,
    script : "",
    index : "",
    
}

var _exec;

router.post('/', function(req,res, next) {

  req_info.index = req.body.index
  req_info.script = "script" + req_info.index + ".py";

  let args = []

  args.push(req_info.index)

  _exec = [path.join(basePath, req_info.script)].concat(args)
  console.log("_exec")
  console.log(_exec)

  

  // spawn new child process to call the python script
  req_info.python = spawn('python', _exec);

  console.log("execute");
  res.status(200).json({
    script : _exec.join(' '),
    result : req_info.result
  });

  // collect data from script
  req_info.python.stdout.on('data', function (data) {

    console.log('Pipe result from python script ... ' + _exec.join(' '));
    req_info.result = data.toString();
    console.log("RESULT: "+req_info.result);
    return;
  });
})

router.get('/', function(req, res, next){

  res.status(200).json({
      script : _exec.join(' '),
      result : req_info.result
  });

  req_info = {
    python : "",
    result : undefined,
    script : "",
    index : ""
  };
  
});

module.exports = router;